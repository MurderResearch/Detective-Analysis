#!/bin/bash
# 推理解剖室 — 一鍵建置並推送
# 用法：在 Terminal 執行 bash ~/Library/CloudStorage/Dropbox/Working/MurderResearch/publish.sh

set -euo pipefail

cd "$(dirname "$0")"

# 清掉可能殘留的 git lock 檔（前次當掉造成）
rm -f .git/HEAD.lock .git/index.lock .git/refs/remotes/origin/main.lock 2>/dev/null || true

echo "🔨 建置網站..."
if ! python3 build.py; then
  echo ""
  echo "❌ 建置失敗。常見原因：缺少 markdown 套件。"
  echo "   請執行：pip3 install markdown --break-system-packages"
  exit 1
fi

echo ""
echo "📤 推送到 GitHub..."
git add -A

# 若沒有任何變更，跳過 commit（避免 commit 失敗讓整個腳本中止）
if git diff --cached --quiet; then
  echo "ℹ️  沒有變更需要 commit，略過。"
else
  git commit -m "$(date '+%Y-%m-%d') 更新分析"
fi

git push

echo ""
echo "📱 發文到 FB 粉專..."
# 若今日已發文過，script 會自行跳過；失敗不中斷整體流程（僅警告）
if ! python3 scripts/post-to-fb.py; then
  echo "⚠️  FB 發文失敗，請檢查 token 或手動執行 python3 scripts/post-to-fb.py"
fi

# 若 FB 發文後更新了 fb-posted.json，再提交一次
if ! git diff --quiet docs/fb-summaries/fb-posted.json 2>/dev/null; then
  git add docs/fb-summaries/fb-posted.json
  git commit -m "$(date '+%Y-%m-%d') FB 發文紀錄" || true
  git push || true
fi

echo ""
echo "✅ 完成！網站將在 1-2 分鐘內更新。"
