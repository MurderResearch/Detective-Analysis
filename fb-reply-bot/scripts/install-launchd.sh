#!/usr/bin/env bash
#
# install-launchd.sh — 把 fb-reply-bot 安裝成 macOS launchd agent，每 1 小時跑一次。
#
# 用法：
#   bash scripts/install-launchd.sh
#
# 會做：
#   1. 偵測 node 絕對路徑（優先用環境的 which node，找不到則列出常見位置讓你選）
#   2. 確認 .env 存在
#   3. mkdir -p logs
#   4. 用 sed 把模板 plist 裡的 __NODE_BIN__ / __PROJECT_DIR__ / __NODE_DIR__ 替換掉
#   5. 複製到 ~/Library/LaunchAgents/ 並 launchctl bootstrap
#
# 參考：
#   launchctl list | grep fbreplybot
#   tail -f logs/bot.log logs/bot.err.log
#   bash scripts/uninstall-launchd.sh

set -euo pipefail

LABEL="com.user.fbreplybot"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$PROJECT_DIR/scripts/com.user.fbreplybot.plist"
AGENTS_DIR="$HOME/Library/LaunchAgents"
TARGET="$AGENTS_DIR/$LABEL.plist"
UID_="$(id -u)"

msg()  { printf "\033[1;34m==>\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m⚠\033[0m  %s\n" "$*"; }
err()  { printf "\033[1;31m✗\033[0m  %s\n" "$*" >&2; }

# ---- 1. 找 node ----
find_node() {
  if command -v node >/dev/null 2>&1; then
    command -v node
    return
  fi
  for cand in \
    /opt/homebrew/bin/node \
    /usr/local/bin/node \
    "$HOME/.nvm/versions/node/"*/bin/node \
    "$HOME/.volta/bin/node" \
    "$HOME/.asdf/shims/node"; do
    if [ -x "$cand" ]; then
      echo "$cand"
      return
    fi
  done
  return 1
}

NODE_BIN="${NODE_BIN:-$(find_node || true)}"
if [ -z "${NODE_BIN:-}" ] || [ ! -x "$NODE_BIN" ]; then
  err "找不到 node。請先安裝 Node.js 18+，或用 NODE_BIN=/path/to/node bash $0"
  exit 1
fi
NODE_VER="$("$NODE_BIN" --version 2>/dev/null || echo unknown)"
NODE_DIR="$(dirname "$NODE_BIN")"
msg "使用 node: $NODE_BIN ($NODE_VER)"

# ---- 2. 檢查 .env ----
if [ ! -f "$PROJECT_DIR/.env" ]; then
  warn ".env 不存在。還沒填 token 的話 bot 跑起來會報錯。"
  warn "可以先 cp .env.example .env 再編輯，或現在就繼續（之後再補）。"
  read -r -p "繼續安裝？[y/N] " ans
  [[ "$ans" =~ ^[Yy]$ ]] || { err "取消"; exit 1; }
fi

# ---- 3. logs ----
mkdir -p "$PROJECT_DIR/logs"
msg "log 目錄：$PROJECT_DIR/logs"

# ---- 4. 產生 plist ----
if [ ! -f "$TEMPLATE" ]; then
  err "找不到模板 $TEMPLATE"
  exit 1
fi

mkdir -p "$AGENTS_DIR"

# 用 | 當分隔符避免路徑裡的 / 衝突
sed -e "s|__NODE_BIN__|$NODE_BIN|g" \
    -e "s|__NODE_DIR__|$NODE_DIR|g" \
    -e "s|__PROJECT_DIR__|$PROJECT_DIR|g" \
    "$TEMPLATE" > "$TARGET"

msg "寫入 $TARGET"

# 檢查 plist 合法性
if ! plutil -lint "$TARGET" >/dev/null; then
  err "plist 格式錯誤，取消"
  rm -f "$TARGET"
  exit 1
fi

# ---- 5. launchctl ----
# 如果已經載入過，先卸載再載入
if launchctl print "gui/$UID_/$LABEL" >/dev/null 2>&1; then
  msg "已存在同名 agent，先 bootout..."
  launchctl bootout "gui/$UID_/$LABEL" || true
fi

msg "bootstrap launchd agent..."
launchctl bootstrap "gui/$UID_" "$TARGET"
launchctl enable "gui/$UID_/$LABEL"

msg "安裝完成 ✅"
cat <<EOF

— 下一步 —
  立即觸發一次（測試）：   launchctl kickstart -k gui/$UID_/$LABEL
  看 log：                tail -f $PROJECT_DIR/logs/bot.log $PROJECT_DIR/logs/bot.err.log
  檢查狀態：              launchctl print gui/$UID_/$LABEL | head -40
  卸載：                  bash scripts/uninstall-launchd.sh

排程已經啟用，launchd 每 3600 秒會自動跑一次 \`node src/index.js\`。
EOF
