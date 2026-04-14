#!/usr/bin/env python3
"""
推理解剖室 — 靜態網站建置腳本（多語系版）
讀取所有 _analysis.md → 產生 HTML 文章頁 → 更新首頁 → 產生 FB 摘要
支援繁中／簡中／英／日／韓／德／西／法
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
FB_DIR = os.path.join(DOCS_DIR, "fb-summaries")
WEBSITE_DIR = os.path.join(BASE_DIR, "website")
I18N_DIR = os.path.join(BASE_DIR, "i18n")

# 作者資料夾對應
AUTHOR_DIRS = ["poe", "doyle", "leblanc", "chesterton", "christie"]
AUTHOR_NAMES = {
    "poe": {"zh-TW": "愛倫·坡", "zh-CN": "爱伦·坡", "en": "Edgar Allan Poe", "ja": "エドガー・アラン・ポー", "ko": "에드거 앨런 포", "de": "Edgar Allan Poe", "es": "Edgar Allan Poe", "fr": "Edgar Allan Poe", "en_name": "Edgar Allan Poe", "years": "1809–1849"},
    "doyle": {"zh-TW": "柯南·道爾", "zh-CN": "柯南·道尔", "en": "Arthur Conan Doyle", "ja": "アーサー・コナン・ドイル", "ko": "아서 코난 도일", "de": "Arthur Conan Doyle", "es": "Arthur Conan Doyle", "fr": "Arthur Conan Doyle", "en_name": "Arthur Conan Doyle", "years": "1859–1930"},
    "leblanc": {"zh-TW": "莫里斯·盧布朗", "zh-CN": "莫里斯·勒布朗", "en": "Maurice Leblanc", "ja": "モーリス・ルブラン", "ko": "모리스 르블랑", "de": "Maurice Leblanc", "es": "Maurice Leblanc", "fr": "Maurice Leblanc", "en_name": "Maurice Leblanc", "years": "1864–1941"},
    "chesterton": {"zh-TW": "卻斯特頓", "zh-CN": "切斯特顿", "en": "G.K. Chesterton", "ja": "G・K・チェスタトン", "ko": "G. K. 체스터턴", "de": "G. K. Chesterton", "es": "G. K. Chesterton", "fr": "G. K. Chesterton", "en_name": "G.K. Chesterton", "years": "1874–1936"},
    "christie": {"zh-TW": "阿嘉莎·克莉絲蒂", "zh-CN": "阿加莎·克里斯蒂", "en": "Agatha Christie", "ja": "アガサ・クリスティー", "ko": "애거사 크리스티", "de": "Agatha Christie", "es": "Agatha Christie", "fr": "Agatha Christie", "en_name": "Agatha Christie", "years": "1890–1976"},
}

# 各語系字體對應（Google Fonts 名稱）
FONT_MAP = {
    "zh-TW": {"serif": "Noto Serif TC", "sans": "Noto Sans TC", "url_serif": "Noto+Serif+TC", "url_sans": "Noto+Sans+TC"},
    "zh-CN": {"serif": "Noto Serif SC", "sans": "Noto Sans SC", "url_serif": "Noto+Serif+SC", "url_sans": "Noto+Sans+SC"},
    "ja":    {"serif": "Noto Serif JP", "sans": "Noto Sans JP", "url_serif": "Noto+Serif+JP", "url_sans": "Noto+Sans+JP"},
    "ko":    {"serif": "Noto Serif KR", "sans": "Noto Sans KR", "url_serif": "Noto+Serif+KR", "url_sans": "Noto+Sans+KR"},
    "en":    {"serif": "Noto Serif",    "sans": "Noto Sans",    "url_serif": "Noto+Serif",    "url_sans": "Noto+Sans"},
    "de":    {"serif": "Noto Serif",    "sans": "Noto Sans",    "url_serif": "Noto+Serif",    "url_sans": "Noto+Sans"},
    "es":    {"serif": "Noto Serif",    "sans": "Noto Sans",    "url_serif": "Noto+Serif",    "url_sans": "Noto+Sans"},
    "fr":    {"serif": "Noto Serif",    "sans": "Noto Sans",    "url_serif": "Noto+Serif",    "url_sans": "Noto+Sans"},
}

# ===== 載入字串包 =====

def load_strings():
    path = os.path.join(I18N_DIR, "strings.json")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

STRINGS = load_strings()
LANG_META = STRINGS["_meta"]["languages"]
LANG_CODES = [c for c in LANG_META.keys()]   # ordered: zh-TW first (default)
DEFAULT_LANG = next(c for c, m in LANG_META.items() if m.get("is_default"))


# ===== 工具函式 =====

def ensure_dirs():
    """為每個語系建立必要的輸出目錄"""
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(FB_DIR, exist_ok=True)
    for lang, meta in LANG_META.items():
        prefix = meta["path_prefix"]
        base = os.path.join(DOCS_DIR, prefix) if prefix else DOCS_DIR
        os.makedirs(os.path.join(base, "articles"), exist_ok=True)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text


def get_author_dir(filepath):
    parts = filepath.replace(BASE_DIR, '').split(os.sep)
    for part in parts:
        if part in AUTHOR_DIRS:
            return part
    return ""


def find_analysis_md(author_dir, slug, lang):
    """
    回傳該語系下該篇分析的 md 路徑。
    優先順序：{author}/translations/{slug}.{lang}.md → {author}/{slug}_analysis.md (zh-TW 原文)
    第二個回傳值 is_translated: 是否找到該語系譯本
    """
    if lang != DEFAULT_LANG:
        trans_path = os.path.join(BASE_DIR, author_dir, "translations", f"{slug}.{lang}.md")
        if os.path.exists(trans_path):
            return trans_path, True

    # fallback：以 slug 反查原始檔名
    pattern = os.path.join(BASE_DIR, author_dir, "*_analysis.md")
    for fp in glob.glob(pattern):
        if slugify(os.path.basename(fp).replace('_analysis.md', '')) == slug:
            return fp, False
    return None, False


# 多語系 metadata 標籤池（任一吻合即可）
META_LABELS = {
    "author":     r"(?:作者|Author|Autor|Auteur|저자|著者)",
    "year":       r"(?:出版年|Year|Published|Año|Année|Erscheinungsjahr|発表年|출판년도)",
    "type":       r"(?:類型|类型|Type|Typ|Género|Genre|ジャンル|장르)",
    "detective":  r"(?:偵探角色|侦探角色|Detective|Detektiv|Détective|探偵|탐정)",
    "rating_ded": r"(?:推理難度|推理难度|Deducibility|Déductibilité|Deducibilidad|Deduzierbarkeit|推理難易度|추리 난이도)",
    "rating_fog": r"(?:迷霧等級|迷雾等级|Fog\s*Rating|Indice de brume|Nivel de niebla|Nebelgrad|霧の濃度|안개 등급)",
    "synopsis":   r"(?:故事大綱|故事梗概|Synopsis|Sinopsis|Résumé|Zusammenfassung|あらすじ|줄거리)",
}

def parse_analysis_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    info = {}

    title_match = re.search(r'^#\s+(.+?)(?:\s*[—-]\s*(?:推理分析|Deducibility Analysis|推理分析|Analyse.*|Análisis.*|分析))?$', content, re.MULTILINE)
    info['title'] = title_match.group(1).strip() if title_match else os.path.basename(filepath)

    # metadata 欄位：接受任一語系的標籤，允許「作者 / Author：」這類並列形式
    def grab(field_key, value_pattern=r'(.+?)'):
        pat = META_LABELS[field_key] + r'[^\n]*?[：:]\s*' + value_pattern + r'(?:\n|$)'
        m = re.search(pat, content)
        return m.group(1).strip() if m else ""

    info['author'] = grab("author")
    info['year'] = grab("year", r'(\d{4})')
    info['type'] = grab("type")
    info['detective'] = grab("detective")

    # 評星：在該指標 label 所在 row 裡抓第一個 ⭐+
    ded_pat = META_LABELS["rating_ded"] + r'[^\n]*?[|｜][^\n]*?(⭐+)'
    ded_match = re.search(ded_pat, content)
    info['deducibility_stars'] = ded_match.group(1) if ded_match else "⭐⭐⭐"
    info['deducibility_count'] = info['deducibility_stars'].count('⭐')

    fog_pat = META_LABELS["rating_fog"] + r'[^\n]*?[|｜][^\n]*?(⭐+)'
    fog_match = re.search(fog_pat, content)
    info['fog_stars'] = fog_match.group(1) if fog_match else "⭐⭐"
    info['fog_count'] = info['fog_stars'].count('⭐')

    # 故事大綱：任意語系的 synopsis section
    synopsis_pat = r'##\s*' + META_LABELS["synopsis"] + r'[^\n]*\n+([\s\S]+?)(?=\n##\s)'
    synopsis_match = re.search(synopsis_pat, content)
    if synopsis_match:
        synopsis = synopsis_match.group(1).strip()
        synopsis_clean = re.sub(r'[*_#`]', '', synopsis)
        synopsis_clean = re.sub(r'\n+', ' ', synopsis_clean)
        info['synopsis'] = synopsis_clean[:300] + ('…' if len(synopsis_clean) > 300 else '')
    else:
        info['synopsis'] = ""

    info['content_html'] = markdown.markdown(content, extensions=['tables', 'fenced_code', 'toc'], output_format='html5')
    info['content_md'] = content
    return info


# ===== 多語系輔助 =====

def site_root_for(lang):
    """相對於某個 html 檔案的『該語系首頁 index.html』路徑。首頁用空字串。"""
    return "index.html"   # 同目錄


def hreflang_links(page_kind, slug=None):
    """
    產生 <link rel="alternate" hreflang="..."> 標籤（加上 x-default）。
    page_kind: "home" 或 "article"
    slug: 僅 article 需要
    回傳以根目錄為基礎的絕對路徑（/en/articles/foo.html 形式）。
    這樣無論頁面位置都能正確對應。
    """
    lines = []
    for lang, meta in LANG_META.items():
        prefix = meta["path_prefix"]
        if page_kind == "home":
            path = f"/{prefix}/" if prefix else "/"
        else:
            path = f"/{prefix}/articles/{slug}.html" if prefix else f"/articles/{slug}.html"
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{path}">')
    # x-default 指向預設語系（zh-TW）
    lines.append('<link rel="alternate" hreflang="x-default" href="/">')
    return "\n".join(lines)


def build_switcher_html(current_lang, page_kind, slug=None):
    """語言切換器下拉選單 HTML（對應頁在不同語系下的 URL）"""
    items = []
    for lang, meta in LANG_META.items():
        prefix = meta["path_prefix"]
        if page_kind == "home":
            href = f"/{prefix}/" if prefix else "/"
        else:
            href = f"/{prefix}/articles/{slug}.html" if prefix else f"/articles/{slug}.html"
        active = " active" if lang == current_lang else ""
        items.append(f'      <a class="lang-item{active}" data-lang="{lang}" href="{href}">{meta["name"]}</a>')

    current_label = LANG_META[current_lang]["name"]
    switcher_label = STRINGS[current_lang]["lang_switcher"]
    return f'''<div class="lang-switcher" id="lang-switcher">
    <button class="lang-switcher-btn" type="button" aria-label="{switcher_label}" onclick="document.getElementById('lang-menu').classList.toggle('open')">🌐 {current_label}</button>
    <div class="lang-switcher-menu" id="lang-menu">
{chr(10).join(items)}
    </div>
  </div>'''


def build_auto_detect_script():
    """
    第一次進站時讀 navigator.language 決定語系，跳轉一次（用 sessionStorage 防止無限迴圈）。
    使用者在切換器選過的語系寫入 localStorage，之後永遠尊重。
    """
    lang_pairs = ", ".join(f"'{c}': '{LANG_META[c]['path_prefix']}'" for c in LANG_CODES)
    return '''<script>
(function() {
  // 所有支援語系 → path_prefix 的對照
  var LANG_PREFIX = {''' + lang_pairs + '''};
  var DEFAULT_LANG = ''' + repr(DEFAULT_LANG) + ''';

  // 決定目前頁面位於哪個語系 prefix
  var path = window.location.pathname;
  var currentPrefix = '';
  for (var code in LANG_PREFIX) {
    var p = LANG_PREFIX[code];
    if (p && (path === '/' + p + '/' || path === '/' + p || path.indexOf('/' + p + '/') === 0)) {
      currentPrefix = p;
      break;
    }
  }
  var currentLang = DEFAULT_LANG;
  for (var code in LANG_PREFIX) {
    if (LANG_PREFIX[code] === currentPrefix) { currentLang = code; break; }
  }

  // 已跳轉過就不再跳（防迴圈）
  if (sessionStorage.getItem('lang_redirected')) return;
  sessionStorage.setItem('lang_redirected', '1');

  // 使用者手動選過語系？有的話尊重
  var userLang = localStorage.getItem('user_lang');
  var targetLang = userLang;

  // 否則用瀏覽器語系自動偵測
  if (!targetLang) {
    var nav = (navigator.language || navigator.userLanguage || '').toLowerCase();
    // 粗略匹配：zh-tw, zh-hant → zh-TW；zh-cn, zh-hans → zh-CN；en-* → en；其餘取前兩碼
    if (nav.indexOf('zh-tw') === 0 || nav.indexOf('zh-hant') === 0 || nav === 'zh-hk' || nav === 'zh-mo') targetLang = 'zh-TW';
    else if (nav.indexOf('zh') === 0) targetLang = 'zh-CN';
    else if (nav.indexOf('en') === 0) targetLang = 'en';
    else if (nav.indexOf('ja') === 0) targetLang = 'ja';
    else if (nav.indexOf('ko') === 0) targetLang = 'ko';
    else if (nav.indexOf('de') === 0) targetLang = 'de';
    else if (nav.indexOf('es') === 0) targetLang = 'es';
    else if (nav.indexOf('fr') === 0) targetLang = 'fr';
    else targetLang = DEFAULT_LANG;
  }

  if (targetLang === currentLang) return;

  // 組出目標 URL：把 /<oldPrefix>/ 或 / 替換成 /<newPrefix>/
  var newPrefix = LANG_PREFIX[targetLang];
  var tail;
  if (currentPrefix) {
    tail = path.substring(('/' + currentPrefix).length) || '/';
  } else {
    tail = path;
  }
  var newPath = (newPrefix ? '/' + newPrefix : '') + (tail.indexOf('/') === 0 ? tail : '/' + tail);
  newPath = newPath.replace(/\\/{2,}/g, '/');
  if (newPath === path) return;
  window.location.replace(newPath + window.location.search + window.location.hash);
})();
</script>'''


def build_switcher_js():
    """切換器按下之後把選擇寫入 localStorage 並清除 session flag，讓下次可重新判定。"""
    return '''<script>
(function() {
  var items = document.querySelectorAll('.lang-switcher-menu a.lang-item');
  items.forEach(function(a) {
    a.addEventListener('click', function(e) {
      localStorage.setItem('user_lang', a.getAttribute('data-lang'));
      sessionStorage.removeItem('lang_redirected');
    });
  });
  // 點外面關閉選單
  document.addEventListener('click', function(e) {
    var menu = document.getElementById('lang-menu');
    var btn  = document.querySelector('.lang-switcher-btn');
    if (!menu) return;
    if (!menu.contains(e.target) && e.target !== btn) menu.classList.remove('open');
  });
})();
</script>'''


# ===== 產生 HTML =====

def render_template(template, mapping):
    out = template
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def generate_article_html(info, author_key, slug, lang, is_translated):
    author = AUTHOR_NAMES.get(author_key, {})
    strings = STRINGS[lang]
    fonts = FONT_MAP[lang]

    # 未翻譯橫幅
    pending_banner = ""
    if not is_translated and lang != DEFAULT_LANG:
        pending_banner = f'<div style="background:#2a2a35;border:1px solid #d4a853;color:#d4a853;padding:14px 20px;border-radius:8px;margin:20px 0;font-size:0.9rem;">ℹ️ {strings["translation_pending"]}</div>'

    author_display = author.get(lang, author.get("en_name", ""))
    switcher = build_switcher_html(lang, "article", slug=slug)
    hreflang = hreflang_links("article", slug=slug)

    return f'''<!DOCTYPE html>
<html lang="{LANG_META[lang]["html_lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{info['title']} — {strings["site_title"]}</title>
<meta name="description" content="{info['synopsis'][:160]}">
{hreflang}
<link href="https://fonts.googleapis.com/css2?family={fonts["url_serif"]}:wght@400;700;900&family={fonts["url_sans"]}:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --bg-dark: #0a0a0f; --bg-card: #13131a; --bg-card-hover: #1a1a24;
  --gold: #d4a853; --gold-dim: #a07c3a;
  --text-primary: #e8e4dc; --text-secondary: #9a9590; --text-dim: #5a5652;
  --border: #2a2a35;
  --font-serif: '{fonts["serif"]}', serif;
  --font-sans: '{fonts["sans"]}', sans-serif;
}}
html {{ scroll-behavior: smooth; }}
body {{ background: var(--bg-dark); color: var(--text-primary); font-family: var(--font-sans); font-weight: 300; line-height: 1.8; min-height: 100vh; }}
.container {{ max-width: 800px; margin: 0 auto; padding: 0 24px; }}

nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(10,10,15,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 16px 0; }}
nav .container {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; max-width: 800px; }}
.nav-logo {{ font-family: var(--font-serif); font-weight: 900; font-size: 1.1rem; color: var(--gold); letter-spacing: 2px; text-decoration: none; white-space: nowrap; }}
.nav-right {{ display: flex; align-items: center; gap: 20px; }}
.nav-links {{ display: flex; gap: 22px; }}
.nav-links a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.85rem; font-weight: 400; letter-spacing: 1px; transition: color 0.3s; }}
.nav-links a:hover {{ color: var(--gold); }}

.lang-switcher {{ position: relative; font-size: 0.8rem; }}
.lang-switcher-btn {{ background: transparent; border: 1px solid var(--border); color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; cursor: pointer; font-size: 0.78rem; letter-spacing: 0.5px; font-family: inherit; transition: border-color 0.3s, color 0.3s; }}
.lang-switcher-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.lang-switcher-menu {{ position: absolute; top: calc(100% + 6px); right: 0; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; min-width: 140px; padding: 6px 0; display: none; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }}
.lang-switcher-menu.open {{ display: block; }}
.lang-switcher-menu a {{ display: block; padding: 8px 14px; color: var(--text-secondary); text-decoration: none; font-size: 0.82rem; transition: background 0.2s, color 0.2s; }}
.lang-switcher-menu a:hover {{ background: var(--bg-card-hover); color: var(--gold); }}
.lang-switcher-menu a.active {{ color: var(--gold); }}

.article-header {{ padding: 140px 0 60px; border-bottom: 1px solid var(--border); }}
.article-meta {{ font-size: 0.8rem; color: var(--gold-dim); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }}
.article-header h1 {{ font-family: var(--font-serif); font-weight: 900; font-size: clamp(1.6rem, 4vw, 2.4rem); line-height: 1.4; margin-bottom: 12px; }}
.article-header .subtitle {{ font-size: 1rem; color: var(--text-secondary); margin-bottom: 28px; }}
.ratings-bar {{ display: flex; gap: 24px; flex-wrap: wrap; }}
.rating-badge {{ text-align: center; padding: 10px 20px; border: 1px solid var(--border); border-radius: 8px; background: rgba(212, 168, 83, 0.04); }}
.rating-badge-label {{ font-size: 0.65rem; color: var(--text-dim); letter-spacing: 1px; margin-bottom: 4px; }}
.rating-badge-stars {{ color: var(--gold); font-size: 1rem; letter-spacing: 2px; }}

.article-body {{ padding: 60px 0 80px; }}
.article-body h1 {{ display: none; }}
.article-body h2 {{ font-family: var(--font-serif); font-size: 1.5rem; font-weight: 700; margin: 48px 0 20px; padding-bottom: 12px; border-bottom: 1px solid var(--border); color: var(--gold); }}
.article-body h3 {{ font-family: var(--font-serif); font-size: 1.2rem; font-weight: 700; margin: 36px 0 16px; color: var(--text-primary); }}
.article-body h4 {{ font-size: 1rem; font-weight: 500; margin: 24px 0 12px; color: var(--gold-dim); }}
.article-body p {{ font-size: 0.95rem; color: var(--text-secondary); line-height: 2; margin-bottom: 16px; }}
.article-body strong {{ color: var(--text-primary); font-weight: 500; }}
.article-body blockquote {{ border-left: 3px solid var(--gold-dim); padding: 12px 20px; margin: 20px 0; background: rgba(212,168,83,0.04); border-radius: 0 8px 8px 0; }}
.article-body blockquote p {{ color: var(--text-secondary); margin-bottom: 0; }}
.article-body table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.88rem; }}
.article-body th, .article-body td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border); color: var(--text-secondary); }}
.article-body th {{ color: var(--gold-dim); font-weight: 500; font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase; }}
.article-body tr:hover td {{ background: rgba(212,168,83,0.03); }}
.article-body ul, .article-body ol {{ margin: 12px 0 12px 24px; color: var(--text-secondary); }}
.article-body li {{ margin-bottom: 8px; font-size: 0.92rem; line-height: 1.8; }}
.article-body hr {{ border: none; border-top: 1px solid var(--border); margin: 48px 0; }}

.back-link {{ display: inline-block; margin-top: 40px; color: var(--gold); text-decoration: none; font-size: 0.85rem; letter-spacing: 1px; border-bottom: 1px solid transparent; transition: border-color 0.3s; }}
.back-link:hover {{ border-bottom-color: var(--gold); }}

footer {{ padding: 60px 0 40px; border-top: 1px solid var(--border); text-align: center; }}
footer p {{ font-size: 0.8rem; color: var(--text-dim); letter-spacing: 1px; }}

@media (max-width: 640px) {{
  .ratings-bar {{ gap: 12px; }}
  .article-body h2 {{ font-size: 1.3rem; }}
  .nav-links {{ gap: 12px; }}
}}
</style>
{build_auto_detect_script()}
</head>
<body>

<nav>
  <div class="container">
    <a href="../index.html" class="nav-logo">{strings["site_title"]}</a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="../index.html">{strings["nav_home"]}</a>
        <a href="../index.html#latest">{strings["nav_latest"]}</a>
      </div>
      {switcher}
    </div>
  </div>
</nav>

<header class="article-header">
  <div class="container">
    <div class="article-meta">{author_display} · {info.get('year', '')}</div>
    <h1>{info['title']}</h1>
    <div class="subtitle">{info.get('author', '')} · {info.get('type', '')}</div>
    <div class="ratings-bar">
      <div class="rating-badge">
        <div class="rating-badge-label">{strings["rating_deducibility"]}</div>
        <div class="rating-badge-stars">{info['deducibility_stars']}</div>
      </div>
      <div class="rating-badge">
        <div class="rating-badge-label">{strings["rating_fog"]}</div>
        <div class="rating-badge-stars">{info['fog_stars']}</div>
      </div>
    </div>
  </div>
</header>

<article class="article-body">
  <div class="container">
    {pending_banner}
    {info['content_html']}
    <a href="../index.html" class="back-link">{strings["article_back"]}</a>
  </div>
</article>

<footer>
  <div class="container">
    <p style="color: var(--gold-dim); font-family: var(--font-serif); font-size: 0.9rem; margin-bottom: 12px;">{strings["site_title"]}</p>
    <p>{strings["footer_tagline"]}</p>
  </div>
</footer>

{build_switcher_js()}

</body>
</html>'''


def generate_article_card_html(info, slug, lang):
    strings = STRINGS[lang]
    excerpt = info.get('synopsis', '')
    if not excerpt:
        excerpt = f"{strings['rating_deducibility']} {info['deducibility_stars']}, {strings['rating_fog']} {info['fog_stars']}."
    short_excerpt = excerpt[:120] + ('…' if len(excerpt) > 120 else '')

    title_parts = info['title'].split('（')
    title_primary = title_parts[0]
    title_en = title_parts[1].rstrip('）') if len(title_parts) > 1 else ''
    author_short = info.get('author', '').split('（')[0]

    return f'''      <a href="articles/{slug}.html" class="article-card">
        <div class="article-card-meta">{author_short} · {info.get('year', '')}</div>
        <div>
          <div class="article-card-title">{title_primary}</div>
          {"<div class='article-card-sub'>" + title_en + "</div>" if title_en else ""}
        </div>
        <div class="article-card-ratings">
          <div class="article-card-badge">{strings['rating_deducibility']} <span>{info['deducibility_stars']}</span></div>
          <div class="article-card-badge">{strings['rating_fog']} <span>{info['fog_stars']}</span></div>
        </div>
        <div class="article-card-excerpt">{short_excerpt}</div>
        <div class="article-card-link">{strings['read_more']}</div>
      </a>'''


def generate_fb_summary(info, slug, site_url=""):
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


def build_index_for_lang(lang, articles_cards):
    """為單一語系產生 index.html"""
    template_path = os.path.join(WEBSITE_DIR, "index.template.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    strings = STRINGS[lang]
    fonts = FONT_MAP[lang]
    meta = LANG_META[lang]
    prefix = meta["path_prefix"]
    out_dir = os.path.join(DOCS_DIR, prefix) if prefix else DOCS_DIR

    mapping = {k.upper(): v for k, v in strings.items()}
    mapping["HTML_LANG"] = meta["html_lang"]
    mapping["FONT_SERIF"] = fonts["serif"]
    mapping["FONT_SANS"] = fonts["sans"]
    mapping["FONT_SERIF_URL"] = fonts["url_serif"]
    mapping["FONT_SANS_URL"] = fonts["url_sans"]
    mapping["HREFLANG_ALTERNATES"] = hreflang_links("home")
    mapping["LANG_SWITCHER"] = build_switcher_html(lang, "home")
    mapping["AUTO_DETECT_SCRIPT"] = build_auto_detect_script()
    mapping["LANG_SWITCHER_JS"] = build_switcher_js()
    mapping["HOME_URL"] = "#"
    mapping["ARTICLES_GRID"] = "\n".join(reversed(articles_cards))   # 新的在前

    html = render_template(template, mapping)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"     → {prefix or '(root)'}/index.html")


def build_article_for_lang(lang, slug, author_key):
    """為單一語系產生單篇文章 HTML，回傳 article card HTML 以供 index 使用"""
    filepath, is_translated = find_analysis_md(author_key, slug, lang)
    if not filepath:
        return None
    info = parse_analysis_md(filepath)
    html = generate_article_html(info, author_key, slug, lang, is_translated)

    prefix = LANG_META[lang]["path_prefix"]
    out_dir = os.path.join(DOCS_DIR, prefix, "articles") if prefix else os.path.join(DOCS_DIR, "articles")
    with open(os.path.join(out_dir, f"{slug}.html"), 'w', encoding='utf-8') as f:
        f.write(html)

    card = generate_article_card_html(info, slug, lang)
    return card, info


# ===== 主建置流程 =====

def build():
    print("🔨 推理解剖室 — 多語系建置\n")
    ensure_dirs()

    # ── 讀取已發布清單 ──
    published_path = os.path.join(DOCS_DIR, "published.json")
    if os.path.exists(published_path):
        with open(published_path, 'r', encoding='utf-8') as f:
            published = json.load(f)
    else:
        published = []
    published_slugs = [p['slug'] for p in published]

    # ── 掃描分析檔 ──
    analysis_files = []
    for author_dir in AUTHOR_DIRS:
        pattern = os.path.join(BASE_DIR, author_dir, "*_analysis.md")
        analysis_files.extend(glob.glob(pattern))
    if not analysis_files:
        print("⚠️  未找到任何 _analysis.md")
        return

    all_slugs_files = {}
    for fp in sorted(analysis_files):
        fn = os.path.basename(fp)
        all_slugs_files[slugify(fn.replace('_analysis.md', ''))] = fp

    new_slugs = [s for s in sorted(all_slugs_files.keys()) if s not in published_slugs]

    # 今日是否發過？
    now_tw = datetime.now(timezone(timedelta(hours=8)))
    today_date = now_tw.date().isoformat()
    last_published_date = published[-1]['published_at'][:10] if published else None
    today_slug = None
    if new_slugs and last_published_date != today_date:
        today_slug = new_slugs[0]
        published.append({"slug": today_slug, "published_at": now_tw.isoformat()})
        published_slugs.append(today_slug)
        print(f"🆕 今日新發布：{today_slug}\n")
    elif new_slugs:
        print(f"ℹ️  今日（{today_date}）已發布過新文章\n")
    else:
        print("ℹ️  所有分析稿均已發布\n")

    # ── 為每個語系逐一建置 ──
    latest_fb = None
    for lang in LANG_CODES:
        meta = LANG_META[lang]
        print(f"🌐 [{lang}] {meta['name']}")
        cards = []
        for slug in published_slugs:
            if slug not in all_slugs_files:
                continue
            author_key = get_author_dir(all_slugs_files[slug])
            result = build_article_for_lang(lang, slug, author_key)
            if result is None:
                continue
            card, info = result
            cards.append(card)
            # FB summary 只用預設語系（繁中）版本生一次
            if lang == DEFAULT_LANG:
                fb = generate_fb_summary(info, slug, site_url="https://murderresearch.github.io/Detective-Analysis")
                fb_path = os.path.join(FB_DIR, f"{slug}.json")
                if os.path.exists(fb_path) and slug != today_slug:
                    with open(fb_path, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                    fb['generated_at'] = existing.get('generated_at', fb['generated_at'])
                with open(fb_path, 'w', encoding='utf-8') as f:
                    json.dump(fb, f, ensure_ascii=False, indent=2)
                if slug == today_slug:
                    latest_fb = fb
        build_index_for_lang(lang, cards)

    # ── 儲存已發布清單 ──
    with open(published_path, 'w', encoding='utf-8') as f:
        json.dump(published, f, ensure_ascii=False, indent=2)

    # ── 寫入最新 FB 摘要 ──
    if latest_fb:
        with open(os.path.join(FB_DIR, "latest.json"), 'w', encoding='utf-8') as f:
            json.dump(latest_fb, f, ensure_ascii=False, indent=2)
        with open(os.path.join(FB_DIR, "latest.txt"), 'w', encoding='utf-8') as f:
            f.write(latest_fb['post_text'])
        print(f"\n✅ 最新 FB 摘要已更新")

    print(f"\n🎉 建置完成！共 {len(LANG_CODES)} 語系 × {len(published_slugs)} 文章")
    print(f"   輸出：{DOCS_DIR}")


if __name__ == "__main__":
    build()
