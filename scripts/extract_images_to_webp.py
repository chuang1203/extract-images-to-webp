#!/usr/bin/env python3

import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageFile


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
}

ImageFile.LOAD_TRUNCATED_IMAGES = True


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Recursively extract image files from a source directory, flatten them, "
            "and save them as WebP in an output directory."
        )
    )
    parser.add_argument("--source", required=True, help="Source directory to scan recursively.")
    parser.add_argument("--output", required=True, help="Output directory for flattened WebP files.")
    parser.add_argument("--quality", type=int, default=95, help="WebP quality for lossy encoding.")
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, min(8, (os.cpu_count() or 1))),
        help="Number of worker processes used for encoding.",
    )
    return parser.parse_args()


def iter_images(source_dir: Path):
    for path in sorted(source_dir.rglob("*")):
        if path.name.startswith("._"):
            continue
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def unique_output_path(output_dir: Path, stem: str) -> Path:
    candidate = output_dir / f"{stem}.webp"
    if not candidate.exists():
        return candidate

    index = 2
    while True:
        candidate = output_dir / f"{stem}_{index}.webp"
        if not candidate.exists():
            return candidate
        index += 1


def normalize_image(image: Image.Image) -> Image.Image:
    image.load()

    if getattr(image, "is_animated", False):
        image.seek(0)

    if image.mode in ("P", "PA"):
        return image.convert("RGBA")
    if image.mode == "CMYK":
        return image.convert("RGB")
    if image.mode in ("RGB", "RGBA", "L", "LA"):
        return image

    return image.convert("RGBA" if "A" in image.getbands() else "RGB")


def convert_one(job):
    source_path, destination_path, quality = job
    source_path = Path(source_path)
    destination_path = Path(destination_path)

    source_bytes = source_path.stat().st_size
    with Image.open(source_path) as image:
        prepared = normalize_image(image)
        prepared.save(
            destination_path,
            format="WEBP",
            quality=quality,
            alpha_quality=100,
            exact=True,
            method=6,
        )

    output_bytes = destination_path.stat().st_size
    return source_bytes, output_bytes


def main():
    args = parse_args()
    source_dir = Path(args.source).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    jobs = []
    duplicates = 0

    for source_path in iter_images(source_dir):
        destination_path = unique_output_path(output_dir, source_path.stem)
        if destination_path.stem != source_path.stem:
            duplicates += 1
        jobs.append((str(source_path), str(destination_path), args.quality))

    source_bytes = 0
    output_bytes = 0
    with ProcessPoolExecutor(max_workers=max(1, args.workers)) as executor:
        for job_source_bytes, job_output_bytes in executor.map(convert_one, jobs):
            source_bytes += job_source_bytes
            output_bytes += job_output_bytes

    converted = len(jobs)

    print(f"converted={converted}")
    print(f"duplicates_renamed={duplicates}")
    print(f"source_bytes={source_bytes}")
    print(f"output_bytes={output_bytes}")
    if source_bytes:
        print(f"ratio={output_bytes / source_bytes:.4f}")


if __name__ == "__main__":
    main()
