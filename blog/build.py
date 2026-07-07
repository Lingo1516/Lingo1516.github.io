#!/usr/bin/env python3
"""Build static blog from WordPress SQL export"""
import re
import os

# Read SQL file
with open('/tmp/blog_posts.sql', 'r') as f:
    content = f.read()

# Split into rows (skip header)
lines = content.strip().split('\n')
header = lines[0]
rows = lines[1:]

posts = []
for row in rows:
    # Parse tab-separated values
    parts = row.split('\t')
    if len(parts) >= 5:
        post_id = parts[0]
        title = parts[1]
        post_content = parts[2]
        post_date = parts[3]
        slug = parts[4]
        posts.append({
            'id': post_id,
            'title': title,
            'content': post_content,
            'date': post_date,
            'slug': slug
        })

print(f"Found {len(posts)} posts")

# Extract images from content
def extract_images(html):
    """Extract image filenames from WordPress HTML"""
    imgs = re.findall(r'<img[^>]+src="[^"]*?/([^"/]+\.(?:jpg|jpeg|png|gif|webp))"', html)
    vids = re.findall(r'<video[^>]+src="[^"]*?/([^"/]+\.(?:mp4))"', html)
    return imgs, vids

# Map image URLs to local filenames
def url_to_local(url):
    """Convert URL to local filename"""
    # Extract filename from URL
    match = re.search(r'/([^/]+\.(?:jpg|jpeg|png|gif|webp|mp4))$', url)
    if match:
        return match.group(1)
    return None

# Check what images actually exist locally
local_images = set(os.listdir('/Users/lingochen/Desktop/Lingo1516.github.io/blog/images/'))

# Clean WordPress HTML to plain text + images
def clean_content(html):
    """Clean WordPress block HTML to clean HTML"""
    # Remove WP block comments
    html = re.sub(r'<!-- wp:[^>]*-->', '', html)
    html = re.sub(r'<!-- /wp:[^>]*-->', '', html)
    
    # Fix image paths to local
    def fix_img(match):
        tag = match.group(0)
        src_match = re.search(r'src="([^"]*)"', tag)
        if src_match:
            url = src_match.group(1)
            local = url_to_local(url)
            if local and local in local_images:
                tag = tag.replace(url, f'images/{local}')
            else:
                # Try to find a matching local image
                for img in local_images:
                    if local and local.split('.')[0] in img:
                        tag = tag.replace(url, f'images/{img}')
                        break
        return tag
    
    html = re.sub(r'<img[^>]+>', fix_img, html)
    
    # Fix video paths
    def fix_vid(match):
        tag = match.group(0)
        src_match = re.search(r'src="([^"]*)"', tag)
        if src_match:
            url = src_match.group(1)
            local = url_to_local(url)
            if local:
                tag = tag.replace(url, f'images/{local}')
        return tag
    
    html = re.sub(r'<video[^>]+>', fix_vid, html)
    
    # Clean up extra tags
    html = re.sub(r'<figure[^>]*>', '', html)
    html = re.sub(r'</figure>', '', html)
    html = re.sub(r'<figcaption[^>]*>(.*?)</figcaption>', r'<p class="caption">\1</p>', html)
    
    return html

# Build pages
os.makedirs('/Users/lingochen/Desktop/Lingo1516.github.io/blog', exist_ok=True)

# Cover images for each post
covers = {
    '423': 'day4_maedaya.jpg',  # Day 4 - 牛腸鍋
    '414': 'hanaori_dinner.jpg',  # 華味鳥
    '318': '20260519_breakfast_day3_01.jpg',  # Day 3
    '164': '20260518_sunshine_hotel_morning_view.jpg',  # Day 2
    '118': '20260518_yatai_night1.jpg',  # Day 1
    '47': 'lingo_kushida.jpg',  # 屋台與明太子
    '15': 'station1.jpg',  # 博多車站
    '10': 'ippudo1.jpg',  # 拉麵
}

# Generate index.html
index_html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>福岡之旅 | Lingo's Blog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            padding: 60px 20px 40px;
            background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, transparent 100%);
        }
        .header h1 {
            font-size: 42px;
            font-weight: 700;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 18px;
            color: #888;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }
        .card {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
        }
        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .card-img {
            width: 100%;
            height: 220px;
            object-fit: cover;
        }
        .card-body {
            padding: 24px;
        }
        .card-date {
            font-size: 14px;
            color: #888;
            margin-bottom: 8px;
        }
        .card-title {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        .card-excerpt {
            font-size: 16px;
            color: #aaa;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 14px;
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 32px; }
            .grid { grid-template-columns: 1fr; }
            .card-title { font-size: 20px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>✈️ 福岡之旅</h1>
        <p>2026年5月 · 五天四夜的九州冒險</p>
    </div>
    <div class="container">
        <div class="grid">
'''

for post in posts:
    cover = covers.get(post['id'], '20260518_dazaifu1.jpg')
    # Get first paragraph as excerpt
    excerpt_match = re.search(r'<p>(.*?)</p>', post['content'])
    excerpt = excerpt_match.group(1) if excerpt_match else ''
    excerpt = re.sub(r'<[^>]+>', '', excerpt)[:100]
    
    index_html += f'''
            <a href="{post['slug']}.html" class="card">
                <img src="images/{cover}" alt="{post['title']}" class="card-img">
                <div class="card-body">
                    <div class="card-date">{post['date'][:10]}</div>
                    <div class="card-title">{post['title']}</div>
                    <div class="card-excerpt">{excerpt}...</div>
                </div>
            </a>
'''

index_html += '''
        </div>
    </div>
    <div class="footer">
        <p>🍀 Lingo's Fukuoka Trip Blog</p>
    </div>
</body>
</html>'''

with open('/Users/lingochen/Desktop/Lingo1516.github.io/blog/index.html', 'w') as f:
    f.write(index_html)

print("✅ index.html built")

# Generate post pages
for post in posts:
    cleaned = clean_content(post['content'])
    
    post_html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>{post['title']} | Lingo's Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft JhengHei", sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
            line-height: 1.8;
        }}
        .nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(26,26,46,0.95);
            padding: 16px 24px;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}
        .nav a {{
            color: #f5576c;
            text-decoration: none;
            font-size: 16px;
        }}
        .article {{
            max-width: 800px;
            margin: 0 auto;
            padding: 80px 20px 40px;
        }}
        .article-header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .article-header h1 {{
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        .article-date {{
            font-size: 16px;
            color: #888;
        }}
        .article-content {{
            font-size: 18px;
            line-height: 1.9;
        }}
        .article-content h2 {{
            font-size: 26px;
            margin: 40px 0 20px;
            color: #fff;
        }}
        .article-content h3 {{
            font-size: 22px;
            margin: 30px 0 16px;
            color: #ddd;
        }}
        .article-content p {{
            margin-bottom: 20px;
            color: #ccc;
        }}
        .article-content img {{
            width: 100%;
            border-radius: 12px;
            margin: 20px 0;
            transition: transform 0.3s ease;
        }}
        .article-content img:hover {{
            transform: scale(1.02);
        }}
        .article-content video {{
            width: 100%;
            border-radius: 12px;
            margin: 20px 0;
        }}
        .article-content ul, .article-content ol {{
            margin: 20px 0;
            padding-left: 24px;
        }}
        .article-content li {{
            margin-bottom: 8px;
            color: #ccc;
        }}
        .article-content strong {{
            color: #f5576c;
        }}
        .caption {{
            text-align: center;
            font-size: 14px;
            color: #888;
            margin-top: -12px;
            margin-bottom: 20px;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin: 20px 0;
        }}
        .gallery img {{
            width: 100%;
            border-radius: 8px;
            margin: 0;
        }}
        .back-btn {{
            display: inline-block;
            margin-top: 40px;
            padding: 12px 24px;
            background: rgba(245,87,108,0.2);
            color: #f5576c;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.3s ease;
        }}
        .back-btn:hover {{
            background: rgba(245,87,108,0.4);
        }}
        hr {{
            border: none;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin: 40px 0;
        }}
        @media (max-width: 768px) {{
            .article-header h1 {{ font-size: 28px; }}
            .article-content {{ font-size: 17px; }}
            .gallery {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="index.html">← 返回首頁</a>
    </div>
    <div class="article">
        <div class="article-header">
            <h1>{post['title']}</h1>
            <div class="article-date">{post['date'][:10]}</div>
        </div>
        <div class="article-content">
            {cleaned}
        </div>
        <a href="index.html" class="back-btn">← 返回首頁</a>
    </div>
</body>
</html>'''
    
    with open(f'/Users/lingochen/Desktop/Lingo1516.github.io/blog/{post["slug"]}.html', 'w') as f:
        f.write(post_html)
    print(f"✅ {post['slug']}.html built")

print("\n🎉 All pages built!")
