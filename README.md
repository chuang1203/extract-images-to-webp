# extract-images-to-webp

Codex skill for recursively extracting images from a folder tree, flattening them, and converting them to WebP without resizing.

## Install

Use Codex's GitHub installer against the repo root:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo chuang1203/extract-images-to-webp \
  --path . \
  --name extract-images-to-webp
```

Restart Codex after installation.

## Repository layout

- `SKILL.md`: trigger description and workflow
- `agents/openai.yaml`: UI metadata
- `scripts/extract_images_to_webp.py`: converter script
