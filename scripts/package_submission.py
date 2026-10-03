"""Create one auditable Day 5 hand-in ZIP from REPORT.md and CVAT exports."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from inspect_submissions import ROOT, inspect_all, task_registry


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package(directory: Path, report_path: Path, output: Path, learner_id: str) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", learner_id):
        raise ValueError("mã học viên chỉ gồm chữ, số, _ hoặc -, dài 1–40 ký tự")
    if not report_path.is_file():
        raise ValueError(f"chưa có {report_path}; sao chép reports/REPORT_TEMPLATE.md thành REPORT.md và điền")
    if output.resolve() == report_path.resolve() or output.resolve().parent == directory.resolve():
        raise ValueError("đặt gói cuối ngoài thư mục ZIP export để không tự đóng gói chính nó")
    qc = inspect_all(directory)
    bad = [row["task"] for row in qc["tasks"] if row["errors"]]
    if bad:
        raise ValueError("export có lỗi hợp đồng: " + ", ".join(bad) + "; chạy scripts/inspect_submissions.py")
    files = [("REPORT.md", report_path)]
    for name in task_registry():
        path = directory / f"{name}.zip"
        if path.is_file():
            files.append((f"exports/{name}.zip", path))
    if len(files) == 1:
        raise ValueError("chưa có ZIP export nào")
    manifest = {"learner_id": learner_id, "tasks_present": [p.stem for _, p in files[1:]],
                "tasks_missing": [name for name in task_registry() if not (directory / f"{name}.zip").is_file()],
                "files": {arcname: _sha256(path) for arcname, path in files}}
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for arcname, path in files:
            archive.write(path, arcname)
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--learner-id", required=True)
    parser.add_argument("--dir", type=Path, default=ROOT / "submissions")
    parser.add_argument("--report", type=Path, default=ROOT / "REPORT.md")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    output = args.out or ROOT / f"day5-{args.learner_id}.zip"
    try:
        result = package(args.dir, args.report, output, args.learner_id)
    except ValueError as exc:
        print("Không thể đóng gói:", exc, file=sys.stderr)
        return 1
    print("Đã tạo", output)
    print("Task có export:", ", ".join(result["tasks_present"]))
    if result["tasks_missing"]:
        print("Task chưa có export (cần giải thích trong REPORT.md):", ", ".join(result["tasks_missing"]))
    print("Đây là kiểm cấu trúc, không phải điểm hay xác nhận mask đúng.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
