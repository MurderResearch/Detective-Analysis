#!/usr/bin/env python3
"""
推理解剖室 — 靜態網站建置腳本
讀取所有 _analysis.md → 產生 HTML 文章頁 → 更新首頁 → 產生 FB 摘要
"""

import os
import re
import json
import glob
import markdown
from datetime import datetime, timezone, timedelta

# ===== 路徑設定 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ARTICLES_DIR = os.path.join(DOCS_DIR, "articles")
FB_DIR = os.path.join(DOCS_DIR, "fb-summaries")
WEBSITE_DIR = os.path.join(BASE_DIR, "website")

# 作者資料夾對應
AUTHOR_DIRS = ["poe", "doyle", "leblanc", "chesterton", "christie"]
AUTHOR_NAMES = {
    "poe": {"zh": "愛倫·坡", "en": "Edgar Allan Poe", "years": "1809–1849"},
    "doyle": {"zh": "柯南·道爾", "en": "Arthur Conan Doyle", "years": "1859–1930"},
    "leblanc": {"zh": "莫里斯·盧布朗", "en": "Maurice Leblanc", "years": "1864–1941"},
    "chesterton": {"zh": "卻斯特頓", "en": "G.K. Chesterton", "years": "1874–1936"},
    "christie": {"zh": "阿嘉莎·克莉絲蒂", "en": "Agatha Christie", "years": "1890–1976"},
}

# ===== 工具函式 =====

def ensure_dirs():
    """建立必要的輸出目錄"""
    for d in [DOCS_DIR, ARTICLES_DIR, FB_DIR]:
        os.makedirs(d, exist_ok=True)


def slugify(text):
    """將檔名轉成 URL-friendly slug"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text


def parse_analysis_md(filepath):
    """解析 _analysis.md，提取關鍵資訊"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    info = {}

    # 標題（第一個 # 開頭的行）
    title_match = re.search(r'^#\s+(.+?)(?:\s*—\s*推理分析)?$', content, re.MULTILINE)
    info['title'] = title_match.group(1).strip() if title_match else os.path.basename(filepath)

    # 從「基本資訊」區塊提取
    author_match = re.search(r'作者[：:]\s*(.+?)(?:\n|$)', content)
    info['author'] = author_match.group(1).strip() if author_match else ""

    year_match = re.search(r'出版年[：:]\s*(\d{4})', content)
    info['year'] = year_match.group(1) if year_match else ""

    type_match = re.search(r'類型[：:]\s*(.+?)(?:\n|$)', content)
    info['type'] = type_match.group(1).strip() if type_match else ""

    detective_match = re.search(r'偵探角色[：:]\s*(.+?)(?:\n|$)', content)
    info['detective'] = detective_match.group(1).strip() if detective_match else ""

    mystery_match = re.search(r'核心謎團類型[：:]\s*(.+?)(?:\n|$)', content)
    info['mystery_type'] = mystery_match.group(1).strip() if mystery_match else ""

    # 推理難度星等
    deducibility_match = re.search(r'推理難度.*?[|｜]\s*(⭐+)', content)
    info['deducibility_stars'] = deducibility_match.group(1) if deducibility_match else "⭐⭐⭐"
    info['deducibility_count'] = info['deducibility_stars'].count('⭐')

    # 迷霧等級星等
    fog_match = re.search(r'迷霧等級.*?[|｜]\s*(⭐+)', content)
    info['fog_stars'] = fog_match.group(1) if fog_match else "⭐⭐"
    info['fog_count'] = info['fog_stars'].count('⭐')

    # 推理難度說明
    ded_desc_match = re.search(r'推理難度.*?[|｜]\s*⭐+\s*[|｜]\s*(.+?)(?:\s*\||\s*$)', content, re.MULTILINE)
    info['deducibility_desc'] = ded_desc_match.group(1).strip() if ded_desc_match else ""

    # 迷霧等級說明
    fog_desc_match = re.search(r'迷霧等級.*?[|｜]\s*⭐+\s*[|｜]\s*(.+?)(?:\s*\||\s*$)', content, re.MULTILINE)
    info['fog_desc'] = fog_desc_match.group(1).strip() if fog_desc_match else ""

    # 故事大綱（取前 200 字作為摘要）
    synopsis_match = re.search(r'##\s*故事大綱\s*\n+([\s\S]+?)(?=\n##\s)', content)
    if synopsis_match:
        synopsis = synopsis_match.group(1).strip()
        # 清除 markdown 格式
        synopsis_clean = re.sub(r'[*_#`]', '', synopsis)
        synopsis_clean = re.sub(r'\n+', ' ', synopsis_clean)
        info['synopsis'] = synopsis_clean[:300] + ('…' if len(synopsis_clean) > 300 else '')
    else:
        info['synopsis'] = ""

    # 補充說明（取最後一段作為 excerpt）
    supplement_match = re.search(r'##\s*補充說明[^\n]*\n+([\s\S]+?)$', content)
    if supplement_match:
        supp = supplement_match.group(1).strip()
        supp_clean = re.sub(r'[*_#`]', '', supp)
        supp_clean = re.sub(r'\n+', ' ', supp_clean)
        info['supplement'] = supp_clean[:200] + ('…' if len(supp_clean) > 200 else '')
    else:
        info['supplement'] = ""

    # 全文 markdown → HTML
    info['content_html'] = markdown.markdown(
        content,
        extensions=['tables', 'fenced_code', 'toc'],
        output_format='html5'
    )

    # 原始 markdown
    info['content_md'] = content

    return info


def get_author_dir(filepath):
    """從檔案路徑判斷作者資料夾"""
    parts = filepath.replace(BASE_DIR, '').split(os.sep)
    for part in parts:
        if part in AUTHOR_DIRS:
            return part
    return ""


def generate_article_html(info, author_key, slug):
    """產生單篇文章的 HTML 頁面"""
    author = AUTHOR_NAMES.get(author_key, {"zh": "", "en": "", "years": ""})

    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{info['title']} — 推理解剖室</title>
<meta name="description" content="{info['synopsis'][:160]}">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700;900&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --bg-dark: #0a0a0f;
  --bg-card: #13131a;
  --bg-card-hover: #1a1a24;
  --gold: #d4a853;
  --gold-dim: #a07c3a;
  --gold-glow: rgba(212, 168, 83, 0.15);
  --red: #8b3a3a;
  --red-light: #c45c5c;
  --text-primary: #e8e4dc;
  --text-secondary: #9a9590;
  --text-dim: #5a5652;
  --border: #2a2a35;
  --font-serif: 'Noto Serif TC', serif;
  --font-sans: 'Noto Sans TC', sans-serif;
}}
html {{ scroll-behavior: smooth; }}
body {{
  background: var(--bg-dark);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-weight: 300;
  line-height: 1.8;
  min-height: 100vh;
}}
.container {{ max-width: 800px; margin: 0 auto; padding: 0 24px; }}

/* NAV */
nav {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  background: rgba(10, 10, 15, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 16px 0;
}}
nav .container {{
  display: flex; justify-content: space-between; align-items: center;
  max-width: 800px;
}}
.nav-logo {{
  font-family: var(--font-serif); font-weight: 900;
  font-size: 1.1rem; color: var(--gold); letter-spacing: 2px;
  text-decoration: none;
}}
.nav-links {{ display: flex; gap: 28px; }}
.nav-links a {{
  color: var(--text-secondary); text-decoration: none;
  font-size: 0.85rem; font-weight: 400; letter-spacing: 1px;
  transition: color 0.3s;
}}
.nav-links a:hover {{ color: var(--gold); }}

/* ARTICLE HEADER */
.article-header {{
  padding: 140px 0 60px;
  border-bottom: 1px solid var(--border);
}}
.article-meta {{
  font-size: 0.8rem; color: var(--gold-dim);
  letter-spacing: 3px; text-transform: uppercase;
  margin-bottom: 20px;
}}
.article-header h1 {{
  font-family: var(--font-serif); font-weight: 900;
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  line-height: 1.4; margin-bottom: 12px;
}}
.article-header .subtitle {{
  font-size: 1rem; color: var(--text-secondary);
  margin-bottom: 28px;
}}
.ratings-bar {{
  display: flex; gap: 24px; flex-wrap: wrap;
}}
.rating-badge {{
  text-align: center; padding: 10px 20px;
  border: 1px solid var(--border); border-radius: 8px;
  background: rgba(212, 168, 83, 0.04);
}}
.rating-badge-label {{
  font-size: 0.65rem; color: var(--text-dim);
  letter-spacing: 1px; margin-bottom: 4px;
}}
.rating-badge-stars {{
  color: var(--gold); font-size: 1rem; letter-spacing: 2px;
}}

/* ARTICLE BODY */
.article-body {{
  padding: 60px 0 80px;
}}
.article-body h1 {{ display: none; }}  /* 隱藏重複的頂層標題 */
.article-body h2 {{
  font-family: var(--font-serif); font-size: 1.5rem;
  font-weight: 700; margin: 48px 0 20px;
  padding-bottom: 12px; border-bottom: 1px solid var(--border);
  color: var(--gold);
}}
.article-body h3 {{
  font-family: var(--font-serif); font-size: 1.2rem;
  font-weight: 700; margin: 36px 0 16px;
  color: var(--text-primary);
}}
.article-body h4 {{
  font-size: 1rem; font-weight: 500;
  margin: 24px 0 12px; color: var(--gold-dim);
}}
.article-body p {{
  font-size: 0.95rem; color: var(--text-secondary);
  line-height: 2; margin-bottom: 16px;
}}
.article-body strong {{ color: var(--text-primary); font-weight: 500; }}
.article-body blockquote {{
  border-left: 3px solid var(--gold-dim);
  padding: 12px 20px; margin: 20px 0;
  background: rgba(212, 168, 83, 0.04);
  border-radius: 0 8px 8px 0;
}}
.article-body blockquote p {{ color: var(--text-secondary); margin-bottom: 0; }}
.article-body table {{
  width: 100%; border-collapse: collapse;
  margin: 20px 0; font-size: 0.88rem;
}}
.article-body th, .article-body td {{
  padding: 10px 14px; text-align: left;
  border-bottom: 1px solid var(--border);
  color: var(--text-secondary);
}}
.article-body th {{
  color: var(--gold-dim); font-weight: 500;
  font-size: 0.8rem; letter-spacing: 1px;
  text-transform: uppercase;
}}
.article-body tr:hover td {{ background: rgba(212, 168, 83, 0.03); }}
.article-body ul, .article-body ol {{
  margin: 12px 0 12px 24px; color: var(--text-secondary);
}}
.article-body li {{ margin-bottom: 8px; font-size: 0.92rem; line-height: 1.8; }}
.article-body hr {{
  border: none; border-top: 1px solid var(--border);
  margin: 48px 0;
}}

/* BACK LINK */
.back-link {{
  display: inline-block; margin-top: 40px;
  color: var(--gold); text-decoration: none;
  font-size: 0.85rem; letter-spacing: 1px;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}}
.back-link:hover {{ border-bottom-color: var(--gold); }}

/* FOOTER */
footer {{
  padding: 60px 0 40px;
  border-top: 1px solid var(--border);
  text-align: center;
}}
footer p {{
  font-size: 0.8rem; color: var(--text-dim);
  letter-spacing: 1px;
}}

@media (max-width: 640px) {{
  .ratings-bar {{ gap: 12px; }}
  .article-body h2 {{ font-size: 1.3rem; }}
}}
</style>
</head>
<body>

<nav>
  <div class="container">
    <a href="../index.html" class="nav-logo">推理解剖室</a>
    <div class="nav-links">
      <a href="../index.html">首頁</a>
      <a href="../index.html#latest">所有分析</a>
    </div>
  </div>
</nav>

<header class="article-header">
  <div class="container">
    <div class="article-meta">{author['zh']} · {info.get('year', '')}</div>
    <h1>{info['title']}</h1>
    <div class="subtitle">{info.get('author', '')} · {info.get('type', '')}</div>
    <div class="ratings-bar">
      <div class="rating-badge">
        <div class="rating-badge-label">推理難度</div>
        <div class="rating-badge-stars">{info['deducibility_stars']}</div>
      </div>
      <div class="rating-badge">
        <div class="rating-badge-label">迷霧等級</div>
        <div class="rating-badge-stars">{info['fog_stars']}</div>
      </div>
    </div>
  </div>
</header>

<article class="article-body">
  <div class="container">
    {info['content_html']}
    <a href="../index.html" class="back-link">← 回到首頁</a>
  </div>
</article>

<footer>
  <div class="container">
    <p style="color: var(--gold-dim); font-family: var(--font-serif); font-size: 0.9rem; margin-bottom: 12px;">推理解剖室</p>
    <p>五位作者 · 八十八部作品 · 一百三十五年推理文學的難度演化</p>
  </div>
</footer>

</body>
</html>'''


def generate_article_card_html(info, slug):
    """產生首頁用的小格卡片 HTML（符合 articles-grid 格式）"""
    excerpt = info.get('synopsis', '') or info.get('supplement', '')
    if not excerpt:
        excerpt = f"推理難度 {info['deducibility_stars']}，迷霧等級 {info['fog_stars']}。"
    # 擷取前 120 字做卡片摘要
    short_excerpt = excerpt[:120] + ('…' if len(excerpt) > 120 else '')

    title_parts = info['title'].split('（')
    title_zh = title_parts[0]
    title_en = title_parts[1].rstrip('）') if len(title_parts) > 1 else ''
    author_short = info.get('author', '').split('（')[0]

    return f'''      <a href="articles/{slug}.html" class="article-card">
        <div class="article-card-meta">{author_short} · {info.get('year', '')}</div>
        <div>
          <div class="article-card-title">{title_zh}</div>
          {"<div class='article-card-sub'>" + title_en + "</div>" if title_en else ""}
        </div>
        <div class="article-card-ratings">
          <div class="article-card-badge">推理難度 <span>{info['deducibility_stars']}</span></div>
          <div class="article-card-badge">迷霧等級 <span>{info['fog_stars']}</span></div>
        </div>
        <div class="article-card-excerpt">{short_excerpt}</div>
        <div class="article-card-link">閱讀完整分析 →</div>
      </a>'''


def generate_fb_summary(info, slug, site_url=""):
    """產生給 openclaw 的 FB 貼文摘要"""
    stars_text = f"推理難度 {'★' * info['deducibility_count']}{'☆' * (5 - info['deducibility_count'])} | 迷霧等級 {'★' * info['fog_count']}{'☆' * (5 - info['fog_count'])}"

    synopsis = info.get('synopsis', '')[:400]
    if len(info.get('synopsis', '')) > 400:
        synopsis += '…'

    article_url = f"{site_url}/articles/{slug}.html" if site_url else f"articles/{slug}.html"

    post = f"""📖 【推理解剖室】{info['title']}
✍️ {info.get('author', '')} · {info.get('year', '')}

{stars_text}

{synopsis}

🔗 完整分析 → {article_url}

#推理小說 #推理解剖室 #{info.get('author', '').split('（')[0].replace('·', '').replace(' ', '')}"""

    return {
        "title": info['title'],
        "author": info.get('author', ''),
        "year": info.get('year', ''),
        "deducibility": info['deducibility_count'],
        "fog": info['fog_count'],
        "synopsis": synopsis,
        "url": article_url,
        "post_text": post,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat()
    }


def update_index_html(articles_data):
    """更新首頁 index.html 的文章列表"""
    # 讀取原始 index.html（從 website/ 或 docs/）
    source_index = os.path.join(WEBSITE_DIR, "index.html")
    if not os.path.exists(source_index):
        print(f"⚠️  找不到 {source_index}")
        return

    with open(source_index, 'r', encoding='utf-8') as f:
        html = f.read()

    # 產生所有文章卡片（最新的在前）
    cards_html = ""
    for art in reversed(articles_data):
        cards_html += art['card_html'] + "\n"

    # 替換 articles-grid 區塊內的卡片（最新的在最前）
    pattern = r'(<div class="articles-grid">)([\s\S]*?)(</div>\s*</div>\s*</div>)'
    replacement = f'\\1\n{cards_html}    \\3'
    new_html = re.sub(pattern, replacement, html)

    # 寫入 docs/index.html
    output_path = os.path.join(DOCS_DIR, "index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"✅ 首頁已更新：{output_path}")


def build():
    """主建置流程：每次只發布一篇新文章（每日一篇機制）"""
    print("🔨 推理解剖室 — 開始建置\n")
    ensure_dirs()

    # ── 讀取已發布清單 ──────────────────────────────────────────
    published_path = os.path.join(DOCS_DIR, "published.json")
    if os.path.exists(published_path):
        with open(published_path, 'r', encoding='utf-8') as f:
            published = json.load(f)   # [{"slug": ..., "published_at": ...}, ...]
    else:
        published = []
    published_slugs = [p['slug'] for p in published]

    # ── 掃描所有 _analysis.md ───────────────────────────────────
    analysis_files = []
    for author_dir in AUTHOR_DIRS:
        pattern = os.path.join(BASE_DIR, author_dir, "*_analysis.md")
        analysis_files.extend(glob.glob(pattern))

    if not analysis_files:
        print("⚠️  未找到任何 _analysis.md 檔案")
        return

    # ── 找出今天要新發布的一篇 ──────────────────────────────────
    all_slugs_files = {}
    for filepath in sorted(analysis_files):
        filename = os.path.basename(filepath)
        slug = slugify(filename.replace('_analysis.md', ''))
        all_slugs_files[slug] = filepath

    new_slugs = [s for s in sorted(all_slugs_files.keys()) if s not in published_slugs]

    # 今天（台灣時間）是否已發布過新文章？
    now_tw = datetime.now(timezone(timedelta(hours=8)))
    today_date = now_tw.date().isoformat()
    last_published_date = published[-1]['published_at'][:10] if published else None

    if new_slugs and last_published_date != today_date:
        today_slug = new_slugs[0]   # 按字母順序取第一篇
        published.append({"slug": today_slug, "published_at": now_tw.isoformat()})
        published_slugs.append(today_slug)
        print(f"🆕 今日新發布：{today_slug}")
    elif new_slugs and last_published_date == today_date:
        today_slug = None
        print(f"ℹ️  今日（{today_date}）已發布過新文章，略過")
    else:
        today_slug = None
        print("ℹ️  今日無新文章（所有分析稿均已發布）")

    print(f"📚 已發布 {len(published_slugs)} 篇\n")

    # ── 建置所有已發布的文章頁 ──────────────────────────────────
    articles_data = []
    latest_fb = None

    for slug in published_slugs:
        if slug not in all_slugs_files:
            continue
        filepath = all_slugs_files[slug]
        filename = os.path.basename(filepath)
        author_key = get_author_dir(filepath)

        print(f"  📖 處理：{filename}")

        info = parse_analysis_md(filepath)

        # 產生文章頁 HTML
        article_html = generate_article_html(info, author_key, slug)
        article_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(article_html)
        print(f"     → 文章頁：articles/{slug}.html")

        card_html = generate_article_card_html(info, slug)

        fb_summary = generate_fb_summary(info, slug, site_url="https://murderresearch.github.io/Detective-Analysis")
        fb_path = os.path.join(FB_DIR, f"{slug}.json")
        # 若 JSON 已存在且非今日新文章，保留原有 generated_at（避免每次 build 都產生 git diff）
        if os.path.exists(fb_path) and slug != today_slug:
            with open(fb_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            fb_summary['generated_at'] = existing.get('generated_at', fb_summary['generated_at'])
        with open(fb_path, 'w', encoding='utf-8') as f:
            json.dump(fb_summary, f, ensure_ascii=False, indent=2)
        print(f"     → FB 摘要：fb-summaries/{slug}.json")

        articles_data.append({
            'info': info,
            'slug': slug,
            'card_html': card_html,
            'fb_summary': fb_summary
        })

        # latest = 今天新發布的那篇
        if slug == today_slug:
            latest_fb = fb_summary

    # ── 更新首頁（只顯示已發布的文章）────────────────────────────
    print(f"\n🏠 更新首頁...")
    update_index_html(articles_data)

    # ── 儲存已發布清單 ──────────────────────────────────────────
    with open(published_path, 'w', encoding='utf-8') as f:
        json.dump(published, f, ensure_ascii=False, indent=2)
    print(f"✅ 發布清單：docs/published.json")

    # ── 寫入最新 FB 摘要（供 openclaw 讀取）───────────────────────
    if latest_fb:
        latest_path = os.path.join(FB_DIR, "latest.json")
        with open(latest_path, 'w', encoding='utf-8') as f:
            json.dump(latest_fb, f, ensure_ascii=False, indent=2)
        print(f"✅ 最新 FB 摘要：fb-summaries/latest.json")

        latest_txt_path = os.path.join(FB_DIR, "latest.txt")
        with open(latest_txt_path, 'w', encoding='utf-8') as f:
            f.write(latest_fb['post_text'])
        print(f"✅ 最新 FB 貼文：fb-summaries/latest.txt")
    else:
        print("ℹ️  今日無新文章，latest.json / latest.txt 未更新")

    print(f"\n🎉 建置完成！共發布 {len(articles_data)} 篇分析報告")
    print(f"   輸出目錄：{DOCS_DIR}")


if __name__ == "__main__":
    build()
