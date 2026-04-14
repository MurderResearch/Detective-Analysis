# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

推理解剖室 (Detective Analysis) — a Chinese-language project that systematically analyzes 88 classic detective fiction works across 5 authors (Poe, Doyle, Leblanc, Chesterton, Christie). Each analysis evaluates when a careful reader can logically deduce the truth from author-provided clues, scored via 推理難度 (Deducibility, 1-5 stars) and 迷霧等級 (Fog Rating, 1-5 stars).

## Build & Deploy

```bash
# Build: generate HTML from markdown analysis files
python3 build.py

# One-command build + git push
bash publish.sh
```

**Python dependency:** `pip install markdown`

CI/CD runs via GitHub Actions on push to main: builds with Python 3.12, deploys `docs/` to GitHub Pages.

## Architecture

**Content pipeline:** Markdown → Python build → Static HTML + Facebook summaries

- **Source content:** `{author}/*_analysis.md` files (one per work analyzed) plus `{author}/AUTHOR.md` for author intros
- **Author directories:** `poe/`, `doyle/`, `leblanc/`, `chesterton/`, `christie/`
- **Build script:** `build.py` — parses markdown metadata via regex, generates article HTML pages, homepage cards, and FB post summaries
- **Site template:** `website/index.html` — base homepage template that `build.py` injects article cards into
- **Output directory:** `docs/` — all generated output (articles HTML, index.html, fb-summaries JSON/TXT, published.json)

**Daily publishing logic:** `build.py` publishes one article per day (Taiwan timezone UTC+8). It checks `docs/published.json` to see if today's article was already published; if not, it picks the next unpublished article in alphabetical order.

## Key build.py Functions

- `parse_analysis_md()` — extracts title, author, year, detective, ratings, synopsis from markdown
- `generate_article_html()` — creates full article page with dark theme
- `generate_article_card_html()` — creates homepage grid card
- `generate_fb_summary()` — creates Facebook post template (JSON + TXT)
- `update_index_html()` — injects cards into `website/index.html` → `docs/index.html`
- `build()` — main orchestration

## Content Format

Analysis files follow a strict structure defined in `ANALYSIS_FRAMEWORK.md`: 基本資訊 (metadata), 推理難度總評 (ratings), 真相拆解 (truth analysis with 關鍵線索/輔助線索/假線索 tables), 推理路徑重建 (reasoning path reconstruction), 補充說明 (remarks).

## Important Notes

- All content is in Traditional Chinese (繁體中文)
- `.gitignore` excludes `.txt` source files — only `.md` analysis files are tracked
- `docs/` is the deploy target (GitHub Pages serves from this directory)
- Project schedule and author ordering are in `PROJECT.md`
