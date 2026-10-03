"""Check CVAT exports against the public Day 5 task contract, without answers.

This checks files, classes, image names and mask representation. It cannot
determine whether an annotation is correct or award points.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MAX_MEMBER_BYTES = 100 * 1024 * 1024
MAX_ARCHIVE_BYTES = 300 * 1024 * 1024


def task_registry(root: Path = ROOT) -> dict:
    return json.loads((root / "data" / "manifest.json").read_text(encoding="utf-8"))["tasks"]


def expected_for(name: str, info: dict, root: Path = ROOT) -> tuple[set[str], set[str]]:
    base = root / "data" / info["path"]
    images = {p.name for p in (base / "images").glob("*.jpg")}
    classes = set(json.loads((base / "classes.json").read_text(encoding="utf-8"))["classes"])
    return images, classes


def _members(path: Path) -> dict[str, bytes]:
    if not path.is_file():
        raise ValueError("không tìm thấy ZIP")
    try:
        with zipfile.ZipFile(path) as archive:
            infos = [item for item in archive.infolist() if not item.is_dir()]
            if sum(item.file_size for item in infos) > MAX_ARCHIVE_BYTES:
                raise ValueError("ZIP giải nén vượt 300 MB")
            result = {}
            for item in infos:
                pure = PurePosixPath(item.filename)
                if pure.is_absolute() or ".." in pure.parts or "\\" in item.filename:
                    raise ValueError(f"đường dẫn không an toàn trong ZIP: {item.filename}")
                if item.file_size > MAX_MEMBER_BYTES:
                    raise ValueError(f"file quá lớn trong ZIP: {item.filename}")
                if item.filename in result:
                    raise ValueError(f"file trùng trong ZIP: {item.filename}")
                result[item.filename] = archive.read(item)
            return result
    except (OSError, zipfile.BadZipFile) as exc:
        raise ValueError(f"không đọc được ZIP: {exc}") from exc


def _semantic(members: dict[str, bytes], images: set[str], classes: set[str]) -> tuple[dict, list[str], list[str]]:
    errors, warnings = [], []
    mask_files = [key for key in members if "SegmentationClass/" in key and key.lower().endswith(".png")]
    names = [Path(key).stem + ".jpg" for key in mask_files]
    if not mask_files:
        errors.append("không có PNG trong SegmentationClass/; kiểm format Segmentation mask 1.1")
    for key in mask_files:
        if not members[key].startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append(f"file không có chữ ký PNG: {key}")
    missing, extra = images - set(names), set(names) - images
    if missing:
        errors.append("thiếu mask ảnh: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("mask không thuộc task: " + ", ".join(sorted(extra)))
    if len(names) != len(set(names)):
        errors.append("nhiều mask cùng tên ảnh")
    labelmaps = [key for key in members if Path(key).name == "labelmap.txt"]
    labels = set()
    if len(labelmaps) != 1:
        errors.append("cần đúng một labelmap.txt")
    else:
        for line in members[labelmaps[0]].decode("utf-8", "replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and ":" in line:
                labels.add(line.split(":", 1)[0])
        unknown = labels - classes - {"background", "void", "unlabeled"}
        if unknown:
            errors.append("label ngoài classes.json: " + ", ".join(sorted(unknown)))
        absent = classes - labels
        if absent:
            warnings.append("class không xuất hiện trong labelmap (kiểm task): " + ", ".join(sorted(absent)))
    return {"mask_images": sorted(set(names)), "labelmap_classes": sorted(labels)}, errors, warnings


def _segmentation_kind(seg: object) -> str | None:
    if isinstance(seg, list) and seg:
        if all(isinstance(poly, list) and len(poly) >= 6 and len(poly) % 2 == 0
               and all(isinstance(x, (int, float)) for x in poly) for poly in seg):
            return "polygon"
    if isinstance(seg, dict) and isinstance(seg.get("size"), list) and len(seg["size"]) == 2:
        if isinstance(seg.get("counts"), (str, list)):
            return "RLE"
    return None


def _coco(members: dict[str, bytes], images: set[str], classes: set[str], panoptic: bool) -> tuple[dict, list[str], list[str]]:
    errors, warnings = [], []
    candidates = [key for key in members if key.lower().endswith(".json") and "annotation" in key.lower()]
    if len(candidates) != 1:
        return {}, ["cần đúng một COCO JSON trong annotations/"], warnings
    try:
        data = json.loads(members[candidates[0]])
    except (ValueError, UnicodeDecodeError) as exc:
        return {}, [f"COCO JSON không đọc được: {exc}"], warnings
    if not isinstance(data, dict) or any(not isinstance(data.get(key), list) for key in ("images", "categories", "annotations")):
        return {}, ["COCO JSON phải có ba list images, categories, annotations"], warnings
    image_ids = {}
    names = []
    for item in data["images"]:
        if not isinstance(item, dict) or "id" not in item or "file_name" not in item:
            errors.append("image record thiếu id/file_name")
            continue
        name = Path(str(item["file_name"])).name
        if not isinstance(item["id"], (str, int)):
            errors.append("image id phải là chuỗi hoặc số")
            continue
        if item["id"] in image_ids:
            errors.append(f"image id trùng: {item['id']}")
        image_ids[item["id"]] = name
        names.append(name)
    if len(names) != len(set(names)):
        errors.append("image file_name trùng")
    if images - set(names):
        errors.append("thiếu ảnh: " + ", ".join(sorted(images - set(names))))
    if set(names) - images:
        errors.append("ảnh không thuộc task: " + ", ".join(sorted(set(names) - images)))
    cat_ids = {}
    for item in data["categories"]:
        if not isinstance(item, dict) or "id" not in item or "name" not in item:
            errors.append("category record thiếu id/name")
            continue
        if not isinstance(item["id"], (str, int)):
            errors.append("category id phải là chuỗi hoặc số")
            continue
        if item["id"] in cat_ids:
            errors.append(f"category id trùng: {item['id']}")
        cat_ids[item["id"]] = item["name"]
    unknown = set(cat_ids.values()) - classes
    if unknown:
        errors.append("category ngoài classes.json: " + ", ".join(sorted(unknown)))
    counts, kinds, seen_ids = Counter(), Counter(), set()
    for item in data["annotations"]:
        if not isinstance(item, dict):
            errors.append("annotation không phải object")
            continue
        ann_id = item.get("id")
        if not isinstance(ann_id, (str, int)):
            errors.append("annotation id phải là chuỗi hoặc số")
            continue
        if ann_id in seen_ids:
            errors.append(f"annotation id trùng: {item.get('id')}")
        seen_ids.add(ann_id)
        image_id, category_id = item.get("image_id"), item.get("category_id")
        if not isinstance(image_id, (str, int)) or not isinstance(category_id, (str, int)):
            errors.append(f"annotation {ann_id} có image/category id không hợp lệ")
            continue
        image, cls = image_ids.get(image_id), cat_ids.get(category_id)
        if image is None or cls is None:
            errors.append(f"annotation {item.get('id')} trỏ đến image/category không tồn tại")
            continue
        kind = _segmentation_kind(item.get("segmentation"))
        if kind is None:
            errors.append(f"annotation {item.get('id')} thiếu polygon/RLE hợp lệ")
        else:
            kinds[kind] += 1
        counts[f"{image} / {cls}"] += 1
    if not data["annotations"]:
        warnings.append("COCO không có annotation nào")
    if panoptic:
        stuff = {"road", "sidewalk", "building", "vegetation", "sky"}
        missing_stuff = stuff - set(count.split(" / ", 1)[1] for count in counts)
        if missing_stuff:
            warnings.append("chưa thấy stuff class: " + ", ".join(sorted(missing_stuff)))
        warnings.append("COCO 1.0 chỉ xác nhận các mask; hãy kiểm trực quan chồng lấn và phủ vùng panoptic trong CVAT")
    return {"images": sorted(set(names)), "annotation_count": len(data["annotations"]),
            "segmentation_kinds": dict(kinds), "counts_by_image_class": dict(sorted(counts.items()))}, errors, warnings


def inspect_task(name: str, path: Path, root: Path = ROOT) -> dict:
    info = task_registry(root)[name]
    images, classes = expected_for(name, info, root)
    result = {"task": name, "type": info["type"], "file": str(path), "errors": [], "warnings": [], "details": {}}
    if not path.exists():
        result["warnings"].append("chưa có ZIP; ghi trong REPORT.md nếu chưa kịp")
        return result
    try:
        members = _members(path)
        if info["type"] == "semantic":
            details, errors, warnings = _semantic(members, images, classes)
        else:
            details, errors, warnings = _coco(members, images, classes, info["type"] == "panoptic")
        result.update(details=details, errors=errors, warnings=warnings)
    except ValueError as exc:
        result["errors"].append(str(exc))
    return result


def inspect_all(directory: Path, root: Path = ROOT) -> dict:
    tasks = task_registry(root)
    results = [inspect_task(name, directory / f"{name}.zip", root) for name in tasks]
    unknown = sorted(path.name for path in directory.glob("*.zip") if path.stem not in tasks) if directory.is_dir() else []
    return {"tasks": results, "unknown_zips": unknown,
            "error_count": sum(len(row["errors"]) for row in results),
            "missing_count": sum(not Path(row["file"]).exists() for row in results)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=ROOT / "submissions", help="thư mục chứa ZIP theo mã task")
    parser.add_argument("--task", choices=task_registry(), help="kiểm một task")
    parser.add_argument("--json", type=Path, help="ghi kết quả QC dạng JSON")
    args = parser.parse_args()
    report = ({"tasks": [inspect_task(args.task, args.dir / f"{args.task}.zip")]} if args.task
              else inspect_all(args.dir))
    for row in report["tasks"]:
        label = "LỖI" if row["errors"] else ("THIẾU" if not Path(row["file"]).exists() else "OK")
        print(f"[{label}] {row['task']}: {Path(row['file']).name}")
        for item in row["errors"]:
            print("  ! " + item)
        for item in row["warnings"]:
            print("  ? " + item)
        if row["details"].get("annotation_count") is not None:
            print("  annotations:", row["details"]["annotation_count"], row["details"]["segmentation_kinds"])
    if report.get("unknown_zips"):
        print("ZIP tên không thuộc task:", ", ".join(report["unknown_zips"]))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(any(row["errors"] for row in report["tasks"]))


if __name__ == "__main__":
    sys.exit(main())
