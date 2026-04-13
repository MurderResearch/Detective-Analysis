#!/bin/bash
# 推理解剖室 — 一鍵建置並推送
# 用法：在 Terminal 執行 bash ~/Library/CloudStorage/Dropbox/Working/MurderResearch/publish.sh

cd "$(dirname "$0")"

echo "🔨 建置網站..."
python3 build.py

echo ""
echo "📤 推送到 GitHub..."
git add -A
git commit -m "$(date '+%Y-%m-%d') 更新分析"
git push

echo ""
echo "✅ 完成！網站將在 1-2 分鐘內更新。"
