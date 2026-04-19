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
- Source novel `.txt` files ARE tracked in the repo (committed 2026-04-19 to support remote scheduled runs)
- `docs/` is the deploy target (GitHub Pages serves from this directory)
- Project schedule and author ordering are in `PROJECT.md`
- Working directory is `~/Code/MurderResearch` (moved off Dropbox 2026-04-19 due to loose-object corruption)

---

## 每日自動化架構（2026-04-19 起）

每天清晨 05:06（Taipei）全自動發布，流程完全在雲端跑，本機不需要開著。

**執行順序：**

1. **05:06 Taipei** — Claude Code RemoteTrigger `trig_01Q39kqQ8n7oJ5JEigK73ZR6` 觸發遠端 agent（Sonnet 4.6）
2. Agent clone repo → 判斷下一本書 → 寫 `_analysis.md` + 7 語翻譯 → `python3 build.py` → `git push`
3. Push 觸發兩條 GitHub Actions：
   - `.github/workflows/deploy.yml` → 部署 `docs/` 到 GitHub Pages
   - `.github/workflows/post-to-fb.yml` → 讀 repo secrets 發 FB + 發 Telegram「✅ 已發布」到「謀殺研究室」群組
4. **07:00 Taipei** — `.github/workflows/daily-check.yml` 守衛檢查 fb-posted.json 的 date 是否 = 今日；若否，發 Telegram「⚠️ 今日尚未發布」

**排程管理頁：** https://claude.ai/code/scheduled/trig_01Q39kqQ8n7oJ5JEigK73ZR6

### 給 Claude（如果你是被觸發的那隻 agent）

你跑在 Anthropic CCR 雲端，網路 allowlist **只允許 GitHub / 套件下載等有限 endpoint**。**不要** curl Telegram / Slack / 任何第三方 API——會被擋。所有外部通知由 GitHub Actions 接手，你只需專心做內容、git push。

**主流程步驟：**

1. 讀 `CLAUDE.md`、`ANALYSIS_FRAMEWORK.md`、`PROJECT.md`
2. 讀 `docs/published.json` 看已發布 slug；讀 `docs/fb-summaries/fb-posted.json`。若 date = 今日（Taipei），**直接結束 session**，不用通知
3. 對照 `PROJECT.md` 找下一本要分析但還沒寫 `_analysis.md` 的書
   - 例：若最後一筆是 D7 Vol1，今天就是 D8 `Works_of_Poe_Vol2`
4. 讀原始 `.txt`（已 commit 進 repo，檔案在各作者資料夾下；大檔案用 `Read` 的 offset/limit 分段）
5. 依 `ANALYSIS_FRAMEWORK.md` 寫 `{作者}/{書名}_analysis.md`（檔名與 .txt 一致後綴 `_analysis`）
6. 產 7 語翻譯到 `{作者}/translations/{slug}.{lang}.md`（`en, zh-CN, ja, ko, de, es, fr`），**完整忠實翻譯、不摘要**。metadata 標籤用該語系對應詞（見 `build.py` 的 `META_LABELS`）。可並行啟動 Agent 加速
7. `python3 build.py` 生成 HTML + FB 摘要
8. `git add -A` → `git commit -m "$(date '+%Y-%m-%d') 每日更新"` → `git push`
9. FB 與成功 Telegram 通知由 GH Actions 接手，你不用也不能直接發

**品質底線：** 分析稿必含「基本資訊 / 推理難度總評 / 故事大綱 / 真相拆解（含關鍵線索、輔助線索、假線索三表）/ 推理路徑重建 / 補充說明」六大段。文風深度參考 `poe/The_Cask_of_Amontillado_analysis.md`。

**套件缺失：** `pip3 install markdown`（雲端不用 `--break-system-packages`）。

### FB 發文機制（自動化用）

- 憑證走 GitHub Repo Secrets：`FB_PAGE_ACCESS_TOKEN`、`FB_PAGE_ID`、`FB_GRAPH_VERSION`
- GH Actions workflow：`.github/workflows/post-to-fb.yml`，`push` 到 `docs/fb-summaries/latest.json` 時觸發
- 發文工具：`scripts/post-to-fb.py`（純 Python stdlib，讀 env var 或 `fb-reply-bot/.env`）
- 冪等：`fb-posted.json` 已有今日紀錄則 skip
- 手動測試：`python3 scripts/post-to-fb.py --dry-run`

### Telegram 通知機制

- 憑證走 GitHub Repo Secrets：`TELEGRAM_BOT_TOKEN`（@MurderResearchBot）、`TELEGRAM_CHAT_ID`（`-5160768597` = 謀殺研究室群組）
- 成功通知在 `post-to-fb.yml` 的 `Notify Telegram (success)` step
- 失敗通知：`post-to-fb.yml` 的 `Notify Telegram (failure)` step + `daily-check.yml` 守衛（07:00 Taipei）
- 重要：**agent 本身無法發 Telegram**（CCR 網路 allowlist），所有通知必經 GH Actions

### 給人類使用者（Letranger）

若想手動補發：
```bash
cd ~/Code/MurderResearch
bash publish.sh
```

`publish.sh` 會 build + push；push 後 GH Actions 會自動發 FB + Telegram。如果本機沒有 `fb-reply-bot/.env`（新機器），手動發也沒關係——git push 進來 GH Actions 照樣會用 repo secrets 發。

### 常見失敗與除錯

- **Agent 雲端失敗（整個 session crashed）** → 07:00 Taipei 守衛發 ⚠️ 告警
- **Agent 跑了但 git push 失敗** → 同上，守衛抓得到
- **GH Actions FB 發文失敗（token 過期等）** → `post-to-fb.yml` failure branch 發 ❌ + run 連結
- **FB token 過期** → `python3 scripts/post-to-fb.py` 會拋 HTTP 190；需 rotate token 後更新 repo secret `FB_PAGE_ACCESS_TOKEN`
- **build 缺 markdown 套件（本機）** → `pip3 install markdown --break-system-packages`
- **今天已發過** → `post-to-fb.py` 自動 skip，無通知，正常
