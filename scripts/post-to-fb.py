#!/usr/bin/env python3
"""
推理解剖室 — 每日 FB 粉專自動發文工具

讀取 docs/fb-summaries/latest.txt 作為貼文內容，呼叫 Facebook Graph API 發文
到粉專 feed，成功後更新 docs/fb-summaries/fb-posted.json。

特性：
- 冪等（idempotent）：若 fb-posted.json 今天日期已存在，直接跳出
- credentials 從 fb-reply-bot/.env 讀取（與 fb-reply-bot 共用一組 token）
- --dry-run 模式：不真的發文，只印出會發的內容

用法：
    python3 scripts/post-to-fb.py           # 實際發文
    python3 scripts/post-to-fb.py --dry-run # 試跑
    python3 scripts/post-to-fb.py --force   # 強制發文（忽略今日已發）
"""

import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "fb-reply-bot" / ".env"
LATEST_TXT = BASE_DIR / "docs" / "fb-summaries" / "latest.txt"
LATEST_JSON = BASE_DIR / "docs" / "fb-summaries" / "latest.json"
POSTED_JSON = BASE_DIR / "docs" / "fb-summaries" / "fb-posted.json"

TW_TZ = timezone(timedelta(hours=8))


def load_env(path):
    """讀取 .env 格式檔案，回傳 dict。忽略註解與空行。"""
    env = {}
    if not path.exists():
        return env
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.strip().strip('"').strip("'")
            env[k.strip()] = v
    return env


def today_tw_date():
    return datetime.now(TW_TZ).date().isoformat()


def already_posted_today():
    """檢查 fb-posted.json 今日日期是否已寫入。"""
    if not POSTED_JSON.exists():
        return False
    try:
        with open(POSTED_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("date") == today_tw_date()
    except (json.JSONDecodeError, OSError):
        return False


def load_post_content():
    """優先讀 latest.json，再 fallback 到 latest.txt。"""
    if LATEST_JSON.exists():
        with open(LATEST_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            "text": data.get("post_text", ""),
            "title": data.get("title", ""),
            "url": data.get("url", ""),
        }
    if LATEST_TXT.exists():
        return {
            "text": LATEST_TXT.read_text(encoding='utf-8'),
            "title": "",
            "url": "",
        }
    return None


def post_to_facebook(page_id, access_token, message, graph_version="v20.0"):
    """
    呼叫 FB Graph API 發文到粉專 feed。
    成功回傳 {"id": "..."}；失敗拋出 RuntimeError。
    """
    url = f"https://graph.facebook.com/{graph_version}/{page_id}/feed"
    data = urllib.parse.urlencode({
        "message": message,
        "access_token": access_token,
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f"FB API HTTP {e.code}: {err_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"FB API network error: {e.reason}") from e


def update_posted_record(post_id, title):
    """成功發文後更新 fb-posted.json。"""
    record = {
        "date": today_tw_date(),
        "post_id": post_id,
        "title": title,
        "posted_at": datetime.now(TW_TZ).isoformat(),
    }
    POSTED_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(POSTED_JSON, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="推理解剖室 FB 自動發文")
    parser.add_argument('--dry-run', action='store_true', help='不實際發文，只印出內容')
    parser.add_argument('--force', action='store_true', help='即使今日已發過也強制再發')
    args = parser.parse_args()

    # ── 冪等檢查 ──
    if already_posted_today() and not args.force:
        print(f"✅ 今日（{today_tw_date()}）已發文過，跳過。")
        print(f"   若要強制重發：python3 {sys.argv[0]} --force")
        return 0

    # ── 讀 credentials ──
    env = load_env(ENV_PATH)
    token = env.get("FB_PAGE_ACCESS_TOKEN")
    page_id = env.get("FB_PAGE_ID")
    graph_ver = env.get("FB_GRAPH_VERSION", "v20.0")

    if not token or not page_id:
        print(f"❌ 缺少 FB 憑證。請確認 {ENV_PATH} 內有：")
        print("   FB_PAGE_ACCESS_TOKEN=...")
        print("   FB_PAGE_ID=...")
        return 1

    # ── 讀貼文內容 ──
    content = load_post_content()
    if not content or not content["text"].strip():
        print(f"❌ 找不到貼文內容。請確認 {LATEST_JSON} 或 {LATEST_TXT} 存在且非空。")
        return 1

    message = content["text"]

    print(f"📖 標題：{content.get('title', '(未知)')}")
    print(f"🔗 連結：{content.get('url', '(未知)')}")
    print(f"📝 字數：{len(message)}")
    print(f"─── 貼文內容 ───")
    print(message)
    print(f"────────────────")

    if args.dry_run:
        print("🧪 dry-run 模式，不實際發文。")
        return 0

    # ── 真的發文 ──
    print(f"📤 發送到 Facebook（page_id={page_id}）...")
    try:
        result = post_to_facebook(page_id, token, message, graph_ver)
    except RuntimeError as e:
        print(f"❌ 發文失敗：{e}")
        return 1

    post_id = result.get("id", "")
    if not post_id:
        print(f"❌ 發文回應異常：{result}")
        return 1

    update_posted_record(post_id, content.get("title", ""))
    print(f"✅ 發文成功！post_id = {post_id}")
    print(f"   已更新 {POSTED_JSON.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
