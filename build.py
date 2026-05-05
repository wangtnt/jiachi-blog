#!/usr/bin/env python3
"""Convert Notion-exported Markdown articles to a static HTML blog."""
import os
import re
import csv
import json
from pathlib import Path
from urllib.parse import unquote

BASE = Path(r"C:\Users\MOREFINE\.qclaw\workspace")
SRC = BASE / "notion-export" / "content" / "嘉驰科技Blog" / "文章列表"
DST = BASE / "jiachi-blog"
POSTS_DIR = DST / "posts"
IMAGES_DIR = DST / "images"
CSV_PATH = BASE / "notion-export" / "content" / "嘉驰科技Blog" / "文章列表 19855ba2f5bf81d6b7a5cfdc848132d0.csv"

POSTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Read CSV metadata ---
metadata = {}
with open(CSV_PATH, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row.get("Title", "").strip()
        if title:
            metadata[title] = {
                "title": title,
                "author": row.get("Author", "").strip(),
                "date": row.get("Created at", "").strip(),
                "tags": row.get("Tags", "").strip(),
            }

# --- HTML Template ---
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 嘉驰科技Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; color: #333; line-height: 1.8; background: #f8f9fa; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; }}
        header h1 {{ font-size: 1.5rem; font-weight: 600; }}
        header h1 a {{ color: white; text-decoration: none; }}
        header nav a {{ color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 20px; font-size: 0.9rem; transition: color 0.2s; }}
        header nav a:hover {{ color: white; }}
        .post-meta {{ color: #666; margin-bottom: 20px; font-size: 0.9rem; display: flex; gap: 15px; flex-wrap: wrap; align-items: center; }}
        .post-meta .tag {{ display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; }}
        .post-content {{ background: white; padding: 30px 40px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .post-content h1 {{ font-size: 1.8rem; margin-bottom: 10px; color: #1a1a1a; }}
        .post-content h2 {{ font-size: 1.4rem; margin: 25px 0 10px; color: #1a1a1a; border-left: 3px solid #1a73e8; padding-left: 10px; }}
        .post-content h3 {{ font-size: 1.2rem; margin: 20px 0 8px; color: #333; }}
        .post-content p {{ margin-bottom: 15px; }}
        .post-content img {{ max-width: 100%; height: auto; border-radius: 4px; margin: 15px 0; display: block; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
        .post-content code {{ background: #f1f3f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; color: #d63384; }}
        .post-content pre {{ background: #282c34; color: #abb2bf; padding: 15px; border-radius: 6px; overflow-x: auto; margin: 15px 0; }}
        .post-content pre code {{ background: none; color: inherit; padding: 0; }}
        .post-content blockquote {{ border-left: 3px solid #1a73e8; padding: 10px 15px; margin: 15px 0; background: #f0f6ff; color: #555; }}
        .post-content ul, .post-content ol {{ padding-left: 25px; margin-bottom: 15px; }}
        .post-content li {{ margin-bottom: 5px; }}
        .post-content table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        .post-content th, .post-content td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
        .post-content th {{ background: #f5f5f5; font-weight: 600; }}
        .post-content a {{ color: #1a73e8; text-decoration: none; }}
        .post-content a:hover {{ text-decoration: underline; }}
        footer {{ text-align: center; padding: 20px; color: #999; font-size: 0.85rem; margin-top: 30px; }}
        .back-link {{ display: inline-block; margin-bottom: 20px; color: #1a73e8; text-decoration: none; font-size: 0.95rem; }}
        .back-link:hover {{ text-decoration: underline; }}
        @media (max-width: 600px) {{
            .post-content {{ padding: 20px 15px; }}
            header .container {{ flex-direction: column; gap: 10px; }}
            header nav a {{ margin-left: 10px; margin-right: 10px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="../index.html">嘉驰科技Blog</a></h1>
            <nav>
                <a href="../index.html">首页</a>
                <a href="../articles.html">文章</a>
                <a href="../about.html">关于</a>
                <a href="../contact.html">联系</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <a href="../articles.html" class="back-link">← 返回文章列表</a>
        <article class="post-content">
            <h1>{title}</h1>
            <div class="post-meta">
                <span>📅 {date}</span>
                {author_html}
                {tags_html}
            </div>
            {content}
        </article>
        <footer>© 2025 嘉驰科技Blog. All rights reserved.</footer>
    </div>
</body>
</html>"""


def slugify(text):
    """Create URL-safe filename from Chinese text."""
    # Keep Chinese chars, alphanumerics, hyphens
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    text = text.strip().replace(' ', '-')
    return text


def md_to_html(md_text, article_dir_name):
    """Convert Notion Markdown to HTML, fixing image paths."""
    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    list_type = None
    in_code_block = False
    in_blockquote = False

    # Skip the first # title line and metadata lines
    skip_header = True
    first_heading = True

    i = 0
    while i < len(lines):
        line = lines[i]

        # Handle code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                if in_list:
                    html_lines.append(f'</{list_type}>')
                    in_list = False
                if in_blockquote:
                    html_lines.append('</blockquote>')
                    in_blockquote = False
                lang = line.strip()[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">' if lang else '<pre><code>')
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            html_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue

        # Skip header and metadata from Notion export
        if skip_header and line.startswith('# '):
            skip_header = False
            i += 1
            # Skip Created at, Tags, 日期 lines
            while i < len(lines) and (lines[i].startswith('Created at:') or lines[i].startswith('Tags:') or lines[i].startswith('日期:')):
                i += 1
            continue

        # Skip empty lines after header
        if skip_header and line.strip() == '':
            i += 1
            continue

        # Close list if needed
        stripped = line.strip()
        if in_list and not stripped.startswith(('- ', '* ', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            html_lines.append(f'</{list_type}>')
            in_list = False

        if in_blockquote and not stripped.startswith('>'):
            html_lines.append('</blockquote>')
            in_blockquote = False

        # Empty line = paragraph break
        if stripped == '':
            i += 1
            continue

        # Headings
        if stripped.startswith('### '):
            text = inline_md(stripped[4:])
            html_lines.append(f'<h3>{text}</h3>')
            i += 1
            continue
        if stripped.startswith('## '):
            text = inline_md(stripped[3:])
            html_lines.append(f'<h2>{text}</h2>')
            i += 1
            continue
        if stripped.startswith('# '):
            text = inline_md(stripped[2:])
            if first_heading:
                first_heading = False
                i += 1
                continue
            html_lines.append(f'<h1>{text}</h1>')
            i += 1
            continue

        # Blockquote
        if stripped.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            text = inline_md(stripped[2:])
            html_lines.append(f'<p>{text}</p>')
            i += 1
            continue

        # Unordered list
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list or list_type != 'ul':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ul>')
                list_type = 'ul'
                in_list = True
            text = inline_md(stripped[2:])
            html_lines.append(f'<li>{text}</li>')
            i += 1
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if ol_match:
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ol>')
                list_type = 'ol'
                in_list = True
            text = inline_md(ol_match.group(2))
            html_lines.append(f'<li>{text}</li>')
            i += 1
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            html_lines.append('<hr>')
            i += 1
            continue

        # Regular paragraph
        text = inline_md(stripped)
        html_lines.append(f'<p>{text}</p>')
        i += 1

    # Close any open tags
    if in_list:
        html_lines.append(f'</{list_type}>')
    if in_code_block:
        html_lines.append('</code></pre>')
    if in_blockquote:
        html_lines.append('</blockquote>')

    result = '\n'.join(html_lines)

    return result


def inline_md(text):
    """Convert inline markdown (bold, italic, code, links, images) to HTML."""
    # Images: ![alt](url) - must be processed BEFORE links
    def img_replacer(match):
        alt = match.group(1)
        path = match.group(2)
        # Already absolute URL
        if path.startswith('http'):
            return f'<img src="{path}" alt="{alt}" loading="lazy">'
        # URL-decode the path
        decoded = unquote(path)
        # Extract the directory name (article folder name)
        parts = decoded.split('/')
        if len(parts) >= 2:
            img_name = parts[-1]
            folder = '/'.join(parts[:-1])
            new_path = f'../images/{folder}/{img_name}'
        else:
            new_path = f'../images/{decoded}'
        return f'<img src="{new_path}" alt="{alt}" loading="lazy">'
    
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', img_replacer, text)
    # Links: [text](url) - but not images (already processed above)
    text = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Line breaks within list items
    text = text.replace('  \n', '<br>')
    return text


# --- Process all articles ---
articles_data = []
skip_titles = {'Standard Post Template', '无标题'}

md_files = list(SRC.glob("*.md"))
print(f"Found {len(md_files)} markdown files")

for md_file in sorted(md_files):
    # Extract title from filename (before the Notion ID)
    filename = md_file.stem
    # Notion format: "Title NotionID"
    # Find the last space followed by a hex string
    match = re.match(r'^(.+?)\s+[0-9a-f]{12,}$', filename)
    title = match.group(1) if match else filename

    if title in skip_titles:
        print(f"  SKIP: {title}")
        continue

    # Read markdown
    md_text = md_file.read_text(encoding="utf-8")

    # Get metadata
    meta = metadata.get(title, {})
    date = meta.get("date", "")
    author = meta.get("author", "")
    tags = meta.get("tags", "")

    # Convert to HTML
    article_dir_name = title  # The directory name under images/
    content_html = md_to_html(md_text, article_dir_name)

    # Build author/tags HTML
    author_html = f'<span>✍️ {author}</span>' if author else ''
    tags_html = f'<span class="tag">{tags}</span>' if tags else ''

    # Generate final HTML
    page_html = HTML_TEMPLATE.format(
        title=title,
        date=date,
        author_html=author_html,
        tags_html=tags_html,
        content=content_html,
    )

    # Write file
    slug = slugify(title)
    out_path = POSTS_DIR / f"{slug}.html"
    out_path.write_text(page_html, encoding="utf-8")
    print(f"  OK: {title} -> {slug}.html")

    articles_data.append({
        "title": title,
        "date": date,
        "author": author,
        "tags": tags,
        "slug": slug,
        "filename": f"{slug}.html",
    })

# Sort by date descending
articles_data.sort(key=lambda x: x["date"], reverse=True)

# --- Save articles data as JSON ---
json_path = DST / "articles-data.json"
json_path.write_text(json.dumps(articles_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved articles-data.json ({len(articles_data)} articles)")

# --- Generate Index Page ---
index_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>嘉驰科技Blog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; color: #333; line-height: 1.8; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        header .container { display: flex; justify-content: space-between; align-items: center; }
        header h1 { font-size: 1.5rem; font-weight: 600; }
        header nav a { color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 20px; font-size: 0.9rem; }
        header nav a:hover { color: white; }
        .hero { background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%); color: white; padding: 60px 0; text-align: center; }
        .hero h2 { font-size: 2rem; margin-bottom: 10px; }
        .hero p { font-size: 1.1rem; opacity: 0.9; }
        .section-title { font-size: 1.3rem; margin: 30px 0 15px; color: #1a1a1a; border-left: 3px solid #1a73e8; padding-left: 10px; }
        .article-list { list-style: none; }
        .article-list li { background: white; padding: 15px 20px; margin-bottom: 10px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); transition: box-shadow 0.2s; }
        .article-list li:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
        .article-list a { color: #1a1a1a; text-decoration: none; font-size: 1.05rem; font-weight: 500; }
        .article-list a:hover { color: #1a73e8; }
        .article-meta { color: #888; font-size: 0.85rem; margin-top: 4px; }
        .tag { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-right: 5px; }
        .view-all { display: inline-block; margin-top: 15px; color: #1a73e8; text-decoration: none; font-size: 0.95rem; }
        .view-all:hover { text-decoration: underline; }
        footer { text-align: center; padding: 20px; color: #999; font-size: 0.85rem; margin-top: 30px; }
        @media (max-width: 600px) {
            .hero { padding: 40px 0; }
            .hero h2 { font-size: 1.5rem; }
            header .container { flex-direction: column; gap: 10px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>嘉驰科技Blog</h1>
            <nav>
                <a href="index.html">首页</a>
                <a href="articles.html">文章</a>
                <a href="about.html">关于</a>
                <a href="contact.html">联系</a>
            </nav>
        </div>
    </header>
    <div class="hero">
        <div class="container">
            <h2>嘉驰科技Blog</h2>
            <p>网络技术 · 监控安防 · 实用经验分享</p>
        </div>
    </div>
    <div class="container">
        <h3 class="section-title">最新文章</h3>
        <ul class="article-list">
"""

for art in articles_data[:10]:
    index_html += f"""            <li>
                <a href="posts/{art['filename']}">{art['title']}</a>
                <div class="article-meta">📅 {art['date']} {'<span class="tag">' + art['tags'] + '</span>' if art['tags'] else ''}</div>
            </li>
"""

index_html += """        </ul>
        <a href="articles.html" class="view-all">查看全部文章 →</a>
        <footer>© 2025 嘉驰科技Blog. All rights reserved.</footer>
    </div>
</body>
</html>"""

(DST / "index.html").write_text(index_html, encoding="utf-8")
print("Generated index.html")

# --- Generate Articles List Page ---
articles_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全部文章 - 嘉驰科技Blog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; color: #333; line-height: 1.8; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        header .container { display: flex; justify-content: space-between; align-items: center; }
        header h1 { font-size: 1.5rem; font-weight: 600; }
        header h1 a { color: white; text-decoration: none; }
        header nav a { color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 20px; font-size: 0.9rem; }
        header nav a:hover { color: white; }
        h2 { font-size: 1.3rem; margin: 25px 0 10px; color: #1a1a1a; border-left: 3px solid #1a73e8; padding-left: 10px; }
        .article-list { list-style: none; }
        .article-list li { background: white; padding: 15px 20px; margin-bottom: 8px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); transition: box-shadow 0.2s; }
        .article-list li:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
        .article-list a { color: #1a1a1a; text-decoration: none; font-size: 1.05rem; font-weight: 500; }
        .article-list a:hover { color: #1a73e8; }
        .article-meta { color: #888; font-size: 0.85rem; margin-top: 4px; }
        .tag { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-right: 5px; }
        .tag-filter { display: inline-block; background: white; border: 1px solid #ddd; padding: 5px 12px; border-radius: 15px; font-size: 0.85rem; cursor: pointer; margin: 3px; text-decoration: none; color: #555; transition: all 0.2s; }
        .tag-filter:hover, .tag-filter.active { background: #1a73e8; color: white; border-color: #1a73e8; }
        .tags-section { margin: 15px 0 20px; }
        footer { text-align: center; padding: 20px; color: #999; font-size: 0.85rem; margin-top: 30px; }
        @media (max-width: 600px) {
            header .container { flex-direction: column; gap: 10px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">嘉驰科技Blog</a></h1>
            <nav>
                <a href="index.html">首页</a>
                <a href="articles.html">文章</a>
                <a href="about.html">关于</a>
                <a href="contact.html">联系</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <h2>全部文章</h2>
        <div class="tags-section">
"""

# Collect unique tags
all_tags = sorted(set(a["tags"] for a in articles_data if a["tags"]))
articles_html += '            <a class="tag-filter" href="#" onclick="filterTag(\'\')">全部</a>\n'
for tag in all_tags:
    articles_html += f'            <a class="tag-filter" href="#" onclick="filterTag(\'{tag}\')">{tag}</a>\n'

articles_html += """        </div>
        <ul class="article-list" id="articleList">
"""

for art in articles_data:
    tag_attr = art['tags'] if art['tags'] else ''
    articles_html += f"""            <li data-tag="{tag_attr}">
                <a href="posts/{art['filename']}">{art['title']}</a>
                <div class="article-meta">📅 {art['date']} {'<span class="tag">' + art['tags'] + '</span>' if art['tags'] else ''}</div>
            </li>
"""

articles_html += """        </ul>
        <script>
        function filterTag(tag) {
            var items = document.querySelectorAll('#articleList li');
            items.forEach(function(item) {
                if (!tag || item.getAttribute('data-tag') === tag) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
            // Update active state
            document.querySelectorAll('.tag-filter').forEach(function(btn) {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            return false;
        }
        </script>
        <footer>© 2025 嘉驰科技Blog. All rights reserved.</footer>
    </div>
</body>
</html>"""

(DST / "articles.html").write_text(articles_html, encoding="utf-8")
print("Generated articles.html")

# --- Generate About Page ---
about_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>关于 - 嘉驰科技Blog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; color: #333; line-height: 1.8; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        header .container { display: flex; justify-content: space-between; align-items: center; }
        header h1 { font-size: 1.5rem; font-weight: 600; }
        header h1 a { color: white; text-decoration: none; }
        header nav a { color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 20px; font-size: 0.9rem; }
        header nav a:hover { color: white; }
        .page-content { background: white; padding: 30px 40px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .page-content h2 { font-size: 1.4rem; margin-bottom: 15px; color: #1a1a1a; border-left: 3px solid #1a73e8; padding-left: 10px; }
        .page-content p { margin-bottom: 15px; }
        footer { text-align: center; padding: 20px; color: #999; font-size: 0.85rem; margin-top: 30px; }
        @media (max-width: 600px) {
            .page-content { padding: 20px 15px; }
            header .container { flex-direction: column; gap: 10px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">嘉驰科技Blog</a></h1>
            <nav>
                <a href="index.html">首页</a>
                <a href="articles.html">文章</a>
                <a href="about.html">关于</a>
                <a href="contact.html">联系</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <div class="page-content">
            <h2>关于嘉驰科技Blog</h2>
            <p>嘉驰科技Blog 是一个专注于网络技术、监控安防、设备管理工具和实用经验分享的技术博客。</p>
            <p>我们的内容涵盖：</p>
            <ul style="padding-left:25px;margin-bottom:15px;">
                <li>🔗 网络技术：路由器配置、网络搭建、系统安装技巧</li>
                <li>📹 监控安防：海康威视、萤石云等设备设置与维护</li>
                <li>🔧 管理工具：各类监控设备管理软件使用教程</li>
                <li>📋 项目交付：综合布线交工文件与项目记录</li>
                <li>💡 实用经验：日常工作中积累的技术心得</li>
            </ul>
            <p>如果您有任何问题或合作需求，欢迎通过联系页面与我们沟通。</p>
        </div>
        <footer>© 2025 嘉驰科技Blog. All rights reserved.</footer>
    </div>
</body>
</html>"""

(DST / "about.html").write_text(about_html, encoding="utf-8")
print("Generated about.html")

# --- Generate Contact Page ---
contact_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>联系 - 嘉驰科技Blog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; color: #333; line-height: 1.8; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white; padding: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        header .container { display: flex; justify-content: space-between; align-items: center; }
        header h1 { font-size: 1.5rem; font-weight: 600; }
        header h1 a { color: white; text-decoration: none; }
        header nav a { color: rgba(255,255,255,0.85); text-decoration: none; margin-left: 20px; font-size: 0.9rem; }
        header nav a:hover { color: white; }
        .page-content { background: white; padding: 30px 40px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .page-content h2 { font-size: 1.4rem; margin-bottom: 15px; color: #1a1a1a; border-left: 3px solid #1a73e8; padding-left: 10px; }
        .page-content p { margin-bottom: 15px; }
        .contact-item { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
        .contact-item:last-child { border-bottom: none; }
        .contact-icon { font-size: 1.2rem; }
        footer { text-align: center; padding: 20px; color: #999; font-size: 0.85rem; margin-top: 30px; }
        @media (max-width: 600px) {
            .page-content { padding: 20px 15px; }
            header .container { flex-direction: column; gap: 10px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">嘉驰科技Blog</a></h1>
            <nav>
                <a href="index.html">首页</a>
                <a href="articles.html">文章</a>
                <a href="about.html">关于</a>
                <a href="contact.html">联系</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <div class="page-content">
            <h2>联系我们</h2>
            <p>如有技术问题、合作咨询或内容建议，欢迎通过以下方式联系：</p>
            <div class="contact-item">
                <span class="contact-icon">📧</span>
                <span>wangtnt2019@gmail.com</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">🐙</span>
                <a href="https://github.com/wangtnt" target="_blank" style="color:#1a73e8;text-decoration:none;">GitHub: wangtnt</a>
            </div>
            <p style="margin-top:20px;color:#888;font-size:0.9rem;">我们会在收到消息后尽快回复。</p>
        </div>
        <footer>© 2025 嘉驰科技Blog. All rights reserved.</footer>
    </div>
</body>
</html>"""

(DST / "contact.html").write_text(contact_html, encoding="utf-8")
print("Generated contact.html")

print(f"\n=== BUILD COMPLETE ===")
print(f"Articles: {len(articles_data)}")
print(f"Pages: index.html, articles.html, about.html, contact.html")
print(f"Images: {sum(1 for _ in IMAGES_DIR.rglob('*') if _.is_file())} files")
