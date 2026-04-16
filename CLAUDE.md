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

---

## 每日自動化 SOP（Cowork 排程任務會觸發此流程）

這個 repo 由 Cowork 排程任務 `daily-murder-analysis` 每天清晨 05:06（Taiwan time）觸發一個 Claude session 來執行。那個 session 的 Claude（= 你，如果你正在讀這段）請**完整依序執行以下步驟**：

### Step 1：判斷今天該分析哪本書

1. 讀 `docs/published.json` 看哪些 slug 已經發布。
2. 讀 `docs/fb-summaries/fb-posted.json` 看 `date` 欄位 — 若 **等於今日（Taiwan time）**，代表今天所有事都做完了，**直接結束 session**，不要重複做。
3. 對照 `PROJECT.md` 的排程表，找出**下一本該分析但還沒寫 `_analysis.md` 的書**。
   - 例：若 published.json 最後一筆是 Cask of Amontillado（D2），今天就要分析 D3 `The_Fall_of_the_House_of_Usher`。
   - 原始文本 .txt 檔在各作者資料夾底下（例：`poe/The_Fall_of_the_House_of_Usher.txt`），**這些檔案 gitignored 但本機存在**。

### Step 2：撰寫分析稿

1. 讀 `ANALYSIS_FRAMEWORK.md` 了解格式規範。
2. 讀原始 .txt 檔（使用 Read tool；大檔案用 offset/limit 分段）。
3. 依框架寫出 `{作者}/{書名}_analysis.md`，**檔名必須與 .txt 原始檔一致、後加 `_analysis`**（例：`The_Fall_of_the_House_of_Usher_analysis.md`）。
4. 品質底線：必須包含「基本資訊 / 推理難度總評 / 故事大綱 / 真相拆解（含關鍵線索、輔助線索、假線索三表）/ 推理路徑重建 / 補充說明」六大段。可參考 `poe/The_Cask_of_Amontillado_analysis.md` 作為文風與深度範本。

### Step 2.5：翻譯分析稿為其他語系

分析稿寫完後，必須為該篇產生 7 個語系的翻譯檔，放入 `{作者}/translations/` 目錄：

1. 翻譯檔命名規則：`{slug}.{lang}.md`（slug 是 kebab-case，例：`the-fall-of-the-house-of-usher.en.md`）
2. 需要產生的語系：`en`、`zh-CN`、`ja`、`ko`、`de`、`es`、`fr`
3. 每個翻譯檔必須是**完整、忠實**的翻譯——不可摘要或省略任何段落、表格、線索
4. metadata 標籤必須使用該語系的對應詞（見 `build.py` 的 `META_LABELS` 字典），以便 build 時正確解析
5. ⭐ 星等保持原樣不翻譯
6. 可參考 `poe/translations/the-cask-of-amontillado.en.md` 作為英文翻譯範本
7. `zh-CN` 版本需將繁體中文全部轉為簡體中文

**提示：** 可同時啟動多個 Agent 並行翻譯以加速。

### Step 3：建置 + Push + 發 FB（一條龍）

```bash
bash publish.sh
```

這個腳本會：
1. 清 git lock（若有）
2. 跑 `python3 build.py` 生成 HTML、首頁卡片、FB 摘要（寫入 `docs/fb-summaries/latest.{json,txt}`）
3. `git add -A` → commit → push（觸發 GitHub Actions 部署到 GitHub Pages）
4. 呼叫 `python3 scripts/post-to-fb.py` 發文到粉專
5. 若 `fb-posted.json` 有更新，再 commit & push 一次

### Step 4：驗證

- `docs/published.json` 是否多了今日這筆
- `docs/fb-summaries/fb-posted.json` 的 `date` 是否為今日
- 若兩者皆有，**session 任務完成**

### FB 發文機制（給你想了解細節用）

- Credentials 在 `fb-reply-bot/.env`（gitignored）：`FB_PAGE_ACCESS_TOKEN`、`FB_PAGE_ID`、`FB_GRAPH_VERSION`
- 發文工具：`scripts/post-to-fb.py`（純 Python、僅用 stdlib）
- 冪等：`fb-posted.json` 若今日已有紀錄，自動跳過，不會重複發
- 手動測試：`python3 scripts/post-to-fb.py --dry-run`
- 強制重發（罕用）：`python3 scripts/post-to-fb.py --force`

### 常見失敗處理

- **Git lock 卡住** → `publish.sh` 已經會自動清 `.git/index.lock` 等，不需手動處理
- **FB token 過期** → `post-to-fb.py` 會拋出 HTTP 190；需請使用者跑 `bash fb-reply-bot/scripts/refresh-token.sh` 更新 token
- **build 失敗缺 markdown 套件** → `pip3 install markdown --break-system-packages`
- **今天已發過** → `post-to-fb.py` 自動 skip，非錯誤

### 給人類使用者（Letranger）

若你在非排程時段想手動補發，流程：
```bash
cd ~/Library/CloudStorage/Dropbox/Working/MurderResearch
bash publish.sh
```
全流程自動。
