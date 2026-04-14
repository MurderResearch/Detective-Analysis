#!/usr/bin/env bash
#
# refresh-token.sh — 一鍵把短效 User Token 換成「永不過期」的 Page Token
#
# 前置準備：
#   1. 在 https://developers.facebook.com/apps/ 建好 App，拿到 App ID / App Secret
#   2. 到 https://developers.facebook.com/tools/explorer/
#      - 右上 Application 選你的 App
#      - 按「Generate Access Token」，勾選權限：
#          pages_read_engagement
#          pages_manage_engagement
#          pages_messaging
#          pages_manage_metadata
#          pages_show_list
#      - 複製出現的那串 User Access Token（短效，1~2 小時有效）
#
# 用法：
#   bash scripts/refresh-token.sh
#   (互動式輸入 App ID、App Secret、短效 User Token)
#
# 輸出：
#   - 每個粉專的 Page ID + 長效 Page Access Token
#   - 若你的 .env 已存在且 FB_PAGE_ID 對得上，會問你要不要自動更新 .env

set -euo pipefail

GRAPH="${FB_GRAPH_VERSION:-v20.0}"

msg()  { printf "\033[1;34m==>\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m⚠\033[0m  %s\n" "$*"; }
err()  { printf "\033[1;31m✗\033[0m  %s\n" "$*" >&2; }

need() { command -v "$1" >/dev/null 2>&1 || { err "缺少指令 $1"; exit 1; }; }
need curl
need python3

read -r -p "App ID: " APP_ID
read -r -s -p "App Secret (輸入不會顯示): " APP_SECRET; echo
read -r -p "短效 User Token (Graph API Explorer 那串): " SHORT_USER_TOKEN
echo

# 1) 短效 user token → 長效 user token
msg "Step 1/3 — 換長效 User Token..."
LONG_USER_RESP=$(curl -sS -G "https://graph.facebook.com/$GRAPH/oauth/access_token" \
  --data-urlencode "grant_type=fb_exchange_token" \
  --data-urlencode "client_id=$APP_ID" \
  --data-urlencode "client_secret=$APP_SECRET" \
  --data-urlencode "fb_exchange_token=$SHORT_USER_TOKEN")

LONG_USER_TOKEN=$(echo "$LONG_USER_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token',''))")

if [ -z "$LONG_USER_TOKEN" ]; then
  err "換長效 User Token 失敗，回傳："
  echo "$LONG_USER_RESP" | python3 -m json.tool >&2 || echo "$LONG_USER_RESP" >&2
  exit 1
fi
msg "✅ 取得長效 User Token (60 天有效)"
echo

# 2) 用長效 user token 拿 page tokens
msg "Step 2/3 — 查詢你管理的粉專..."
PAGES_RESP=$(curl -sS -G "https://graph.facebook.com/$GRAPH/me/accounts" \
  --data-urlencode "access_token=$LONG_USER_TOKEN")

COUNT=$(echo "$PAGES_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('data',[])))")

if [ "$COUNT" = "0" ]; then
  err "沒有任何粉專。可能是權限沒給到 pages_show_list，或你不是任何粉專的管理員"
  echo "$PAGES_RESP" | python3 -m json.tool >&2
  exit 1
fi

msg "✅ 找到 $COUNT 個粉專："
echo

# 用環境變數傳 JSON 給 python3，避開 heredoc + stdin 衝突
PAGES_RESP="$PAGES_RESP" python3 <<'PY'
import os, json
data = json.loads(os.environ['PAGES_RESP']).get('data', [])
for i, p in enumerate(data, 1):
    name = p.get('name', '?')
    pid  = p.get('id', '?')
    tok  = p.get('access_token', '')
    print(f"  [{i}] {name}")
    print(f"      Page ID: {pid}")
    print(f"      Page Token (長效，永不過期):")
    print(f"      {tok}")
    print()
PY

# 3) 自動更新 .env？
ENV_FILE="$(cd "$(dirname "$0")/.." && pwd)/.env"
if [ -f "$ENV_FILE" ]; then
  CURRENT_PAGE_ID=$(grep -E '^FB_PAGE_ID=' "$ENV_FILE" | cut -d= -f2- | tr -d '"' | awk '{print $1}' || true)
  if [ -n "$CURRENT_PAGE_ID" ]; then
    # 找到對應的 page token（用 env var 傳進去，不做 shell 插值）
    NEW_TOKEN=$(PAGES_RESP="$PAGES_RESP" TARGET_PID="$CURRENT_PAGE_ID" python3 <<'PY'
import os, json
data = json.loads(os.environ['PAGES_RESP']).get('data', [])
target = os.environ['TARGET_PID']
for p in data:
    if p.get('id') == target:
        print(p.get('access_token', ''))
        break
PY
)
    if [ -n "$NEW_TOKEN" ]; then
      msg "Step 3/3 — .env 裡 FB_PAGE_ID=${CURRENT_PAGE_ID}，找到對應的長效 token"
      read -r -p "自動更新 .env 的 FB_PAGE_ACCESS_TOKEN？[Y/n] " ans
      if [[ ! "$ans" =~ ^[Nn]$ ]]; then
        # macOS sed 要 -i ''
        if sed --version >/dev/null 2>&1; then
          sed -i "s|^FB_PAGE_ACCESS_TOKEN=.*$|FB_PAGE_ACCESS_TOKEN=$NEW_TOKEN|" "$ENV_FILE"
        else
          sed -i '' "s|^FB_PAGE_ACCESS_TOKEN=.*$|FB_PAGE_ACCESS_TOKEN=$NEW_TOKEN|" "$ENV_FILE"
        fi
        msg "✅ .env 已更新"
      fi
    else
      warn ".env 裡的 FB_PAGE_ID (${CURRENT_PAGE_ID}) 不在這批粉專中，請自行複製上面的 token"
    fi
  fi
fi

msg "完成。建議立即跑：node scripts/test-read.js 驗證"
