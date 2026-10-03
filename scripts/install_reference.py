"""Install the officially released Day 5 tier reference ZIP for local scoring.

The archive must contain only the expected groundtruth files beneath data/tiers/.
This script never downloads an archive and refuses to overwrite existing answers.
"""

from __future__ import annotations

import argparse
import json
import shutil
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 100 * 1024 * 1024
MAX_TOTAL_BYTES = 300 * 1024 * 1024


def expected_files(root: Path = ROOT) -> set[str]:
    tiers = root / "data" / "tiers"
    easy = {f"data/tiers/easy_semantic/groundtruth/{p.stem}.png"
            for p in (tiers / "easy_semantic" / "images").glob("*.jpg")}
    hard = {f"data/tiers/hard_panoptic/groundtruth/png/{p.stem}.png"
            for p in (tiers / "hard_panoptic" / "images").glob("*.jpg")}
    if len(easy) != 3 or len(hard) != 2:
        raise ValueError("Task images are incomplete; cannot validate the reference package")
    return easy | hard | {
        "data/tiers/medium_instance/groundtruth/instances.json",
        "data/tiers/hard_panoptic/groundtruth/panoptic.json",
    }


def install(archive_path: Path, root: Path = ROOT) -> list[Path]:
    expected = expected_files(root)
    with zipfile.ZipFile(archive_path) as archive:
        members = [info for info in archive.infolist() if not info.is_dir()]
        names = [info.filename for info in members]
        if len(names) != len(set(names)) or set(names) != expected:
            raise ValueError("Reference ZIP must contain exactly the seven expected groundtruth files; "
                             f"missing={sorted(expected - set(names))}, extra={sorted(set(names) - expected)}")
        if sum(info.file_size for info in members) > MAX_TOTAL_BYTES:
            raise ValueError("Reference ZIP expands beyond 300 MB")
        for info in members:
            path = PurePosixPath(info.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in info.filename
                    or info.file_size > MAX_FILE_BYTES
                    or stat.S_ISLNK(info.external_attr >> 16)):
                raise ValueError(f"Unsafe reference member: {info.filename}")
            target = root.joinpath(*path.parts)
            if target.exists():
                raise ValueError(f"Refusing to overwrite an existing reference: {target}")
            if info.filename.endswith(".png") and not archive.read(info)[:8] == b"\x89PNG\r\n\x1a\n":
                raise ValueError(f"Invalid PNG reference: {info.filename}")
            if info.filename.endswith(".json"):
                json.loads(archive.read(info))
        installed = []
        for info in members:
            target = root.joinpath(*PurePosixPath(info.filename).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, target.open("xb") as destination:
                shutil.copyfileobj(source, destination)
            installed.append(target)
    return installed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    files = install(args.archive)
    print(f"Installed {len(files)} official reference files locally (gitignored).")
