# fb-reply-bot

**每小時檢查一次**的 Facebook 自動回覆機器人。不用 webhook、不用 ngrok。跑一次就結束，交給系統排程（cron / launchd）每小時叫它起來看看有沒有新留言、新私訊沒回。

## 功能

- 粉絲專頁貼文**留言**：抓最近的貼文和底下留言，沒回過的就自動回
- Messenger **私訊**：最新一則是客戶發的就自動回（24 小時視窗內）
- 回覆內容由 **Claude (Anthropic)** 或 **OpenAI** 產生，在 `.env` 切換
- 用本地 JSON 檔記錄已回覆的 ID，避免重複回覆
- 社團：目前沒實作自動回覆（Meta Groups API 寫入權限從 2024 起幾乎無法申請）

## 架構

```
排程器 (launchd / cron)  ─每小時─►  node src/index.js
                                         │
                                         ▼
                                     poller.runOnce()
                                    ┌────┴────┐
                                 comment    messenger
                                    ▼         ▼
                             Graph API     Graph API
                                    ▼         ▼
                                   LLM (Claude / OpenAI)
                                         ▼
                                   .fb-reply-bot-state.json
```

## 目錄結構

```
fb-reply-bot/
├─ package.json
├─ .env.example
├─ .gitignore
├─ README.md
├─ scripts/
│  └─ com.user.fbreplybot.plist   # macOS launchd 範本
└─ src/
   ├─ index.js            # CLI 進入點（one-shot / --watch）
   ├─ poller.js           # 一次 poll 的主流程
   ├─ config.js
   ├─ handlers/
   │  ├─ comment.js       # 決定一則留言要不要回、怎麼回
   │  ├─ message.js       # Messenger 對話處理
   │  └─ group.js         # 停用（保留空殼）
   ├─ services/
   │  ├─ facebook.js      # Graph API 封裝
   │  └─ llm.js           # Claude / OpenAI 封裝
   ├─ store/
   │  └─ state.js         # 已回覆 ID 的 JSON 持久化
   └─ utils/
      └─ logger.js
```

> `src/webhook.js` 和 `src/utils/signature.js` 是舊架構遺留的空檔案（檔案無法刪除），可以忽略。

## 設定

### 1. 安裝

```bash
cd fb-reply-bot
npm install
cp .env.example .env
```

### 2. 填 `.env`

至少需要：

- `FB_PAGE_ID`：粉專 ID
- `FB_PAGE_ACCESS_TOKEN`：**長效** Page Access Token（見下節）
- `LLM_PROVIDER`：`anthropic` 或 `openai`
- `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`

其他選項：

| 變數 | 預設 | 說明 |
|---|---|---|
| `INTERVAL_MINUTES` | 60 | `--watch` 模式的間隔 |
| `LOOKBACK_HOURS` | 24 | 往回抓多少小時內的貼文 |
| `POST_LIMIT` | 10 | 每次抓幾篇貼文 |
| `CONVERSATION_LIMIT` | 20 | 每次抓幾通對話 |
| `REPLY_KEYWORDS` | 空 | 只回符合關鍵字的留言，空字串=全部都回 |
| `BOT_PERSONA` | 預設人設 | 會塞進 LLM 的 system prompt |
| `MAX_REPLY_CHARS` | 280 | 回覆長度上限 |
| `STATE_FILE` | `./.fb-reply-bot-state.json` | 已回覆 ID 檔 |
| `STATE_TTL_DAYS` | 30 | 超過幾天就從 state 移除 |

### 3. 拿長效 Page Access Token

```bash
# 1) 在 https://developers.facebook.com/tools/explorer 選你的 App + Page
#    勾 pages_read_engagement, pages_manage_engagement, pages_messaging
#    取得短期 user token

# 2) 用短期 user token 換長效 user token
curl "https://graph.facebook.com/v20.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id=APP_ID&\
client_secret=APP_SECRET&\
fb_exchange_token=SHORT_USER_TOKEN"

# 3) 用長效 user token 拿「永不過期」的 Page Token
curl "https://graph.facebook.com/v20.0/me/accounts?access_token=LONG_USER_TOKEN"
# 每個 page 的 access_token 欄位就是長效 Page Token
```

必要的 Meta 權限：
- `pages_read_engagement`（讀留言/對話）
- `pages_manage_engagement`（回留言）
- `pages_messaging`（回私訊）
- `pages_manage_metadata`（基本管理）

上線給一般使用者前要送 App Review，本機 + 開發者帳號可直接用。

## 執行

### 手動跑一次（推薦給排程器用）

```bash
npm run once
# 等同 node src/index.js
```

跑完會印出類似：

```
[...INFO] === poll start ===
[...INFO] fetched posts { count: 10 }
[...INFO] replied to comment { cid: "...", reply: "..." }
[...INFO] fetched conversations { count: 5 }
[...INFO] === poll done === { durMs: 8321, comments: {...}, dms: {...} }
```

### Watch 模式（常駐，測試用）

```bash
npm run watch
# 啟動後立即 poll 一次，之後每 INTERVAL_MINUTES 分鐘再 poll 一次
```

### Dry run（只抓資料不回覆，debug 用）

```bash
npm run dry
```

## 設定每小時自動跑

三種方式任選一種。**請不要同時啟用多種**，否則每小時會被觸發多次、可能重複回覆（`state.js` 雖然有 dedupe，但同秒的 race condition 不能保證擋掉）。

### 方法 A：macOS launchd ⭐ 推薦

有一鍵安裝腳本，會自動偵測 node 路徑、填寫 plist、載入 agent：

```bash
bash scripts/install-launchd.sh
```

安裝後：

```bash
# 立即觸發一次（測試）
launchctl kickstart -k gui/$(id -u)/com.user.fbreplybot

# 看 log
tail -f logs/bot.log logs/bot.err.log

# 檢查狀態
launchctl print gui/$(id -u)/com.user.fbreplybot | head -40

# 卸載
bash scripts/uninstall-launchd.sh
```

`StartInterval=3600` 代表每 3600 秒跑一次，從 load 那刻算起。系統重開機後會自動恢復。

### 方法 B：cron（最簡單）

```bash
crontab -e
```

加入：

```cron
# 每小時第 0 分鐘跑一次
0 * * * * cd /絕對路徑/fb-reply-bot && /usr/local/bin/node src/index.js >> logs/bot.log 2>&1
```

先 `mkdir -p logs` 確保日誌目錄存在。`which node` 查你的 node 絕對路徑。

### 方法 C：Cowork 排程

已經透過 `schedule` skill 建立一個叫 **`fb-reply-bot-hourly`** 的 Cowork scheduled task，cron 設為 `0 * * * *`（每小時整點）。它會呼叫 Claude 去執行 `node src/index.js` 並簡短回報結果。

- 管理位置：Cowork 側邊欄 → Scheduled
- 相關檔案：`~/Documents/Claude/Scheduled/fb-reply-bot-hourly/SKILL.md`

這個方式的好處是有 Claude 幫你解析 log、發現錯誤會特別提醒；壞處是每次要等 Claude 啟動一個 session，延遲比 launchd 高。

### ⚠️ 不要同時啟用多個

若你已經用 `install-launchd.sh` 裝好 launchd agent，**請去 Cowork 側邊欄把 `fb-reply-bot-hourly` 停用**（或反之）。兩個同時跑沒有好處。

## 怎麼判斷該不該回覆？

### 粉專留言
1. 抓最近 `POST_LIMIT` 篇貼文（`LOOKBACK_HOURS` 小時內）
2. 每篇貼文抓前 50 則留言
3. 略過：粉專自己的留言、state 標記過的、空的、不符合 `REPLY_KEYWORDS` 的
4. 如果留言底下已經有粉專的回覆 → 標記並略過
5. 其他都叫 LLM 產生回覆，透過 Graph API 送出

### Messenger
1. 抓最近 `CONVERSATION_LIMIT` 通對話
2. 看每通對話的**最新一則**訊息：如果是粉專發的 → 已回過，略過
3. 訊息超過 24 小時 → 略過（FB 規則，非 message tag 就不能主動送）
4. 其他都叫 LLM 回覆

## 常見問題

**Q：為什麼有些留言沒被回？**  
看 `.fb-reply-bot-state.json` 是不是已經標記為回過了。也可能是 `LOOKBACK_HOURS` 太短，貼文已超出時間窗。

**Q：怎麼重置 state？**  
`rm .fb-reply-bot-state.json`，下次 poll 會當作全新開始（注意可能會重複回之前回過的留言，建議停掉自動回覆 token 再清）。

**Q：可以在社團裡用嗎？**  
目前不行。`src/handlers/group.js` 是空殼。Meta 從 2024 起對 Groups API 寫入權限幾乎不核准了。

**Q：怎麼測試不小心發出錯誤回覆？**  
先跑 `npm run dry`，它只會 log 會回什麼、不會真的送出。

## Roadmap

- [ ] 用 Redis / sqlite 取代 JSON state（多實例可用）
- [ ] 多粉專支援（現在一個實例對一個 Page）
- [ ] 貼文 context 一併餵給 LLM（目前只帶 post.message）
- [ ] Messenger 24h 視窗外改用 message tag
- [ ] 簡單 Web UI 看 log、手動觸發、白黑名單

## 授權

MIT
