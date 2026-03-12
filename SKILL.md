---
name: extract-images-to-webp
description: Extract image files from a source folder tree into a flat output folder and save them as WebP without resizing. Use when the user wants to pull images out of nested folders, batch-convert PNG/JPG/TIFF/BMP/GIF files to WebP, preserve visual dimensions, keep stable filenames, or avoid overwriting duplicate names by adding numeric suffixes.
---

# Extract Images To WebP

## Overview

Use this skill to recursively collect images from a directory tree and write a flattened WebP batch to a new folder. Keep the source files untouched, preserve pixel dimensions, and resolve filename collisions deterministically.

## Workflow

1. Confirm the source folder and choose an output folder. Default to creating a sibling folder instead of overwriting the source.
2. Run [`scripts/extract_images_to_webp.py`](/Users/Huang/.codex/skills/extract-images-to-webp/scripts/extract_images_to_webp.py) with the source and output paths.
3. Review the summary for file count, duplicate handling, and total size before reporting back.

## Defaults

- Convert to WebP with `quality=95`, `method=6`, `alpha_quality=100`, and `exact=True`.
- Preserve original pixel dimensions. Do not resize unless the user explicitly asks.
- Keep the source tree unchanged. Write only to the output folder.
- Flatten the output into a single directory.
- If two files would produce the same output name, keep the first as-is and append `_2`, `_3`, and so on to later files.

## Command

```bash
python3 /Users/Huang/.codex/skills/extract-images-to-webp/scripts/extract_images_to_webp.py \
  --source "/path/to/source" \
  --output "/path/to/output"
```

## Notes

- Pillow with WebP support is required. Check with:
```bash
python3 - <<'PY'
from PIL import features
print(features.check("webp"))
PY
```
- Supported inputs: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.gif`, `.tif`, `.tiff`.
- For GIF or multi-frame inputs, this script writes the first frame only. If the user needs animation preserved, do not use this skill as-is.
