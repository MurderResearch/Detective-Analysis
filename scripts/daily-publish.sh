#!/usr/bin/env bash
# 每日自動分析 + 發布腳本
# crontab: 6 5 * * * /Users/letranger/Code/MurderResearch/scripts/daily-publish.sh
set -euo pipefail

# cron 不會自動 source shell config，手動載入 API key
[ -f "$HOME/.zshenv" ] && source "$HOME/.zshenv"

REPO_DIR="$HOME/Code/MurderResearch"
LOG_DIR="$HOME/.murder-research/logs"
LOG_FILE="$LOG_DIR/daily-$(date '+%Y-%m-%d').log"
CLAUDE="/opt/homebrew/bin/claude"

mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== $(date '+%Y-%m-%d %H:%M:%S') 開始每日發布 ==="

cd "$REPO_DIR"

# 1. 拉最新
git pull --rebase origin main

# 2. 檢查今天是否已發布
TODAY=$(TZ=Asia/Taipei date '+%Y-%m-%d')
POSTED_DATE=$(python3 -c "import json; print(json.load(open('docs/fb-summaries/fb-posted.json'))['date'])" 2>/dev/null || echo "")
if [ "$POSTED_DATE" = "$TODAY" ]; then
    echo "今天 ($TODAY) 已發布，跳過"
    exit 0
fi

# 3. 用 claude CLI 執行分析 + 翻譯 + build + push
$CLAUDE -p "你是推理解剖室的每日分析 agent。請依 CLAUDE.md 的「每日自動化 SOP」主流程步驟 1-8 完整執行。

重點提醒：
- 先讀 CLAUDE.md、ANALYSIS_FRAMEWORK.md、PROJECT.md
- 讀 docs/published.json 和 docs/fb-summaries/fb-posted.json 判斷下一本
- 讀原始 .txt 檔（大檔用 offset/limit 分段讀）
- 寫 _analysis.md + 7 語翻譯
- 執行 python3 build.py
- git add -A && git commit && git push
- 品質底線：分析稿必含六大段（基本資訊/推理難度總評/故事大綱/真相拆解/推理路徑重建/補充說明）
- 翻譯必須完整忠實，不得摘要

如果 fb-posted.json 的 date 已是今日（台灣時間），直接結束。" \
    --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Agent" \
    --model sonnet \
    --max-turns 80 \
    --verbose 2>&1

EXIT_CODE=$?
echo "=== $(date '+%Y-%m-%d %H:%M:%S') 結束 (exit=$EXIT_CODE) ==="
