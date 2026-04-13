# GitHub Pages 部署設定指南

## 第一步：在 GitHub 建立 Repo

1. 到 https://github.com/new 建立新 repo
2. **Repo 名稱建議：** `murder-research` 或 `detective-analysis`
3. 設為 **Public**（GitHub Pages 免費版需要公開 repo）
4. **不要**勾選「Add a README file」（我們已有內容）

## 第二步：在本機初始化並推送

打開 Terminal，進入專案資料夾執行：

```bash
cd ~/Library/CloudStorage/Dropbox/Working/MurderResearch

# 初始化 git
git init
git branch -m main

# 設定使用者（如果還沒設定過）
git config user.email "letranger@gm.tnfsh.tn.edu.tw"
git config user.name "Letranger"

# 加入所有檔案並提交
git add -A
git commit -m "初始化推理解剖室網站"

# 連結遠端 repo（請替換成你的 repo 網址）
git remote add origin https://github.com/你的帳號/murder-research.git

# 推送
git push -u origin main
```

## 第三步：啟用 GitHub Pages

1. 到你的 repo → **Settings** → **Pages**
2. **Source** 選擇 **GitHub Actions**
3. 推送後 GitHub Actions 會自動跑 `.github/workflows/deploy.yml`
4. 等 1-2 分鐘，你的網站就會出現在 `https://你的帳號.github.io/murder-research/`

## 日常更新流程

每次有新的分析文章，只要：

```bash
cd ~/Library/CloudStorage/Dropbox/Working/MurderResearch

# 建置網站（將 _analysis.md 轉成 HTML）
python3 build.py

# 提交並推送
git add -A
git commit -m "新增分析：書名"
git push
```

GitHub Actions 會自動完成部署。

## 注意事項

- 原始小說 `.txt` 檔已在 `.gitignore` 中排除，不會上傳到 GitHub
- `docs/` 資料夾是建置輸出，由 `build.py` 自動產生
- `docs/fb-summaries/latest.txt` 是給 openclaw 讀取的最新 FB 貼文
