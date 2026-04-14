#!/usr/bin/env bash
#
# uninstall-launchd.sh — 把 fb-reply-bot 從 launchd 移除。

set -euo pipefail

LABEL="com.user.fbreplybot"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
UID_="$(id -u)"

msg()  { printf "\033[1;34m==>\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m⚠\033[0m  %s\n" "$*"; }

if launchctl print "gui/$UID_/$LABEL" >/dev/null 2>&1; then
  msg "bootout gui/$UID_/$LABEL ..."
  launchctl bootout "gui/$UID_/$LABEL" || true
else
  warn "agent 沒有在執行"
fi

if [ -f "$TARGET" ]; then
  rm -v "$TARGET"
else
  warn "$TARGET 不存在"
fi

msg "卸載完成 ✅（logs/ 和 .fb-reply-bot-state.json 沒動，要清請自行刪）"
