#!/usr/bin/env bash
# 每日自動分析 + 發布腳本（v2 — 分階段、有 timeout、可斷點續跑）
# crontab: 6 5 * * * /Users/letranger/Code/MurderResearch/scripts/daily-publish.sh
set -euo pipefail

# cron 不會自動 source shell config，手動載入 PATH 等設定
[ -f "$HOME/.zshenv" ] && source "$HOME/.zshenv"
# 移除 API key，改走 claude.ai 訂閱認證（避免 API credit 計費）
unset ANTHROPIC_API_KEY

REPO_DIR="$HOME/Code/MurderResearch"
LOG_DIR="$HOME/.murder-research/logs"
LOG_FILE="$LOG_DIR/daily-$(TZ=Asia/Taipei date '+%Y-%m-%d').log"
CLAUDE="/opt/homebrew/bin/claude"
PHASE1_TIMEOUT=5400   # 分析稿最多 90 分鐘（秒）
PHASE2_TIMEOUT=5400   # 翻譯最多 90 分鐘（秒）
LANGS="en zh-CN ja ko de es fr"

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

log() { echo "[$(TZ=Asia/Taipei date '+%Y-%m-%d %H:%M:%S')] $*"; }

# macOS 沒有 timeout 指令，用 bash 原生實作
run_with_timeout() {
    local secs=$1; shift
    "$@" &
    local cmd_pid=$!
    ( sleep "$secs" && kill -TERM "$cmd_pid" 2>/dev/null && log "TIMEOUT: 超過 ${secs}s，已終止 PID $cmd_pid" ) &
    local watcher_pid=$!
    wait "$cmd_pid" 2>/dev/null
    local exit_code=$?
    kill "$watcher_pid" 2>/dev/null 2>&1; wait "$watcher_pid" 2>/dev/null 2>&1
    # 消除 bash 的 "Terminated" 訊息
    jobs >/dev/null 2>&1
    return $exit_code
}

log "=== 開始每日發布 ==="
cd "$REPO_DIR"

# ── 0. Pull latest ──
git pull --rebase origin main

# ── 1. 今天已發布？ ──
TODAY=$(TZ=Asia/Taipei date '+%Y-%m-%d')
POSTED_DATE=$(python3 -c "import json; print(json.load(open('docs/fb-summaries/fb-posted.json'))['date'])" 2>/dev/null || echo "")
if [ "$POSTED_DATE" = "$TODAY" ]; then
    log "今天 ($TODAY) 已發布，跳過"
    exit 0
fi

# ── 2. 判斷下一本書 ──
# 讀 PROJECT.md 的排程表，對比已有 _analysis.md 檔案，找出下一本
NEXT_INFO=$(python3 -c "
import re, os

AUTHOR_DIRS = ['poe', 'doyle', 'leblanc', 'chesterton', 'christie']

def find_txt(filename):
    \"\"\"在各作者目錄搜尋 txt 檔，回傳 (author, filename)\"\"\"
    for d in AUTHOR_DIRS:
        if os.path.exists(os.path.join(d, filename)):
            return d
    return None

# 從 PROJECT.md 讀排程，追蹤當前 phase 作者
schedule = []
current_author = None
with open('PROJECT.md') as f:
    for line in f:
        # 偵測 phase header 來確定作者
        for d in AUTHOR_DIRS:
            if f'{d}/AUTHOR.md' in line:
                current_author = d
        m = re.match(r'\|\s*D(\d+)\s*\|\s*\x60([^\x60]+\.txt)\x60\s*\|', line)
        if m:
            day = int(m.group(1))
            txt = m.group(2).strip()
            if '/' in txt:
                author, filename = txt.split('/', 1)
            else:
                filename = txt
                # 先試實際檔案位置，再 fallback 到 phase header
                found = find_txt(filename)
                author = found if found else (current_author or 'poe')
            base = filename.replace('.txt', '')
            analysis = f'{author}/{base}_analysis.md'
            schedule.append((day, author, base, analysis))

# 找第一個沒有 analysis 檔案的
for day, author, base, analysis_path in schedule:
    if not os.path.exists(analysis_path):
        print(f'{day}|{author}|{base}|{analysis_path}')
        break
" 2>&1)

if [ -z "$NEXT_INFO" ]; then
    log "所有書目都已有分析稿，無需發布"
    exit 0
fi

DAY_NUM=$(echo "$NEXT_INFO" | cut -d'|' -f1)
AUTHOR=$(echo "$NEXT_INFO" | cut -d'|' -f2)
BASE_NAME=$(echo "$NEXT_INFO" | cut -d'|' -f3)
ANALYSIS_PATH=$(echo "$NEXT_INFO" | cut -d'|' -f4)
TXT_PATH="${AUTHOR}/${BASE_NAME}.txt"
SLUG=$(echo "$BASE_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g')

log "D${DAY_NUM}: ${AUTHOR}/${BASE_NAME} (slug: ${SLUG})"
log "TXT: ${TXT_PATH} → Analysis: ${ANALYSIS_PATH}"

# 確認 txt 檔存在
if [ ! -f "$TXT_PATH" ]; then
    log "ERROR: 找不到原始檔案 ${TXT_PATH}"
    exit 1
fi

# ── Phase 1: 寫分析稿 ──
if [ -f "$ANALYSIS_PATH" ]; then
    log "Phase 1 跳過：分析稿已存在"
else
    log "Phase 1: 寫分析稿..."
    run_with_timeout "$PHASE1_TIMEOUT" $CLAUDE -p "你是推理解剖室的分析 agent。

任務：為 ${TXT_PATH} 寫分析稿，存為 ${ANALYSIS_PATH}。

步驟：
1. 讀 ANALYSIS_FRAMEWORK.md 了解格式要求
2. 讀 poe/The_Cask_of_Amontillado_analysis.md 作為文風參考
3. 讀原始 ${TXT_PATH}（大檔用 offset/limit 分段讀，每次最多 2000 行）
4. 寫 ${ANALYSIS_PATH}，必含六大段：基本資訊 / 推理難度總評 / 故事大綱 / 真相拆解（含關鍵線索、輔助線索、假線索三表）/ 推理路徑重建 / 補充說明
5. 如果是選集（Vol/Works），挑 3-4 篇推理相關篇目分析

品質底線：深度分析，不能只是摘要。文風參考上述範例稿。
完成後不需要做其他事（不需翻譯、不需 build、不需 push）。" \
        --allowedTools "Bash,Read,Write,Edit,Glob,Grep" \
        --model sonnet \
        --max-turns 30 \
        --verbose 2>&1 || {
        log "ERROR: Phase 1 失敗 (exit=$?)"
        exit 1
    }

    if [ ! -f "$ANALYSIS_PATH" ]; then
        log "ERROR: Phase 1 完成但分析稿不存在"
        exit 1
    fi
    log "Phase 1 完成：$(wc -l < "$ANALYSIS_PATH") 行"
fi

# ── Phase 2: 寫 7 語翻譯 ──
TRANS_DIR="${AUTHOR}/translations"
mkdir -p "$TRANS_DIR"

# 檢查哪些翻譯還缺
MISSING_LANGS=""
for lang in $LANGS; do
    if [ ! -f "${TRANS_DIR}/${SLUG}.${lang}.md" ]; then
        MISSING_LANGS="${MISSING_LANGS} ${lang}"
    fi
done
MISSING_LANGS=$(echo "$MISSING_LANGS" | xargs)  # trim

if [ -z "$MISSING_LANGS" ]; then
    log "Phase 2 跳過：7 語翻譯皆已存在"
else
    log "Phase 2: 翻譯缺少的語系: ${MISSING_LANGS}"
    run_with_timeout "$PHASE2_TIMEOUT" $CLAUDE -p "你是推理解剖室的翻譯 agent。

任務：將 ${ANALYSIS_PATH} 翻譯成以下語系：${MISSING_LANGS}
輸出路徑：${TRANS_DIR}/${SLUG}.{lang}.md

步驟：
1. 讀 ${ANALYSIS_PATH}（原文，繁體中文）
2. 讀 build.py 找到 META_LABELS dict，了解各語系的 metadata 標籤詞
3. 為每個缺少的語系寫完整翻譯檔
4. 可用 Agent tool 並行翻譯以加速

重要規則：
- 完整忠實翻譯，不得摘要或省略
- metadata 標籤用該語系對應詞（參考 build.py 的 META_LABELS）
- 檔名格式：${SLUG}.{lang}.md（lang = en, zh-CN, ja, ko, de, es, fr）
- 完成後不需要做其他事（不需 build、不需 push）" \
        --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Agent" \
        --model sonnet \
        --max-turns 50 \
        --verbose 2>&1 || {
        log "WARNING: Phase 2 翻譯未全部完成 (exit=$?)"
    }

    # 報告翻譯結果
    STILL_MISSING=""
    for lang in $LANGS; do
        if [ ! -f "${TRANS_DIR}/${SLUG}.${lang}.md" ]; then
            STILL_MISSING="${STILL_MISSING} ${lang}"
        fi
    done
    if [ -n "$STILL_MISSING" ]; then
        log "WARNING: 仍缺翻譯:${STILL_MISSING}（繼續 build，缺的語系會 fallback 到繁中）"
    else
        log "Phase 2 完成：7 語翻譯全數就緒"
    fi
fi

# ── Phase 3: Build ──
log "Phase 3: python3 build.py..."
pip3 install markdown --break-system-packages -q 2>/dev/null || true
python3 build.py
log "Phase 3 完成"

# ── Phase 4: Git push ──
log "Phase 4: git add + commit + push..."
git add -A
if git diff --cached --quiet; then
    log "WARNING: 沒有變更需要 commit"
    exit 0
fi
git commit -m "$(TZ=Asia/Taipei date '+%Y-%m-%d') 每日更新"
git push
log "Phase 4 完成：push 成功"

log "=== 每日發布完成，GH Actions 接手部署與 FB 發文 ==="
