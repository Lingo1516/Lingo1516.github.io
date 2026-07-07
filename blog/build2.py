#!/usr/bin/env python3
import re, os, urllib.parse

os.chdir('/Users/lingochen/Desktop/Lingo1516.github.io/blog')

with open('/tmp/blog_posts.sql', 'r') as f:
    lines = f.read().strip().split('\n')

posts = []
for row in lines[1:]:
    parts = row.split('\t')
    if len(parts) >= 5:
        posts.append({'id': parts[0], 'title': parts[1], 'content': parts[2], 'date': parts[3], 'slug': parts[4]})

local_images = set(os.listdir('images/'))

def find_local_image(url):
    fname = re.search(r'/([^/]+\.(?:jpg|jpeg|png|gif|webp|mp4))$', url)
    if not fname:
        return None
    name = fname.group(1)
    if name in local_images:
        return name
    # Try without UUID prefix
    base = name.split('_')[-1] if '_' in name else name
    for img in local_images:
        if base in img:
            return img
    return name

def clean(html):
    html = re.sub(r'<!-- wp:[^>]*-->', '', html)
    html = re.sub(r'<!-- /wp:[^>]*-->', '', html)
    def fix_tag(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]*)"', tag)
        if src:
            local = find_local_image(src.group(1))
            if local:
                tag = tag.replace(src.group(1), 'images/' + local)
        return tag
    html = re.sub(r'<img[^>]+>', fix_tag, html)
    html = re.sub(r'<video[^>]+src="([^"]*)"', lambda m: '<video controls src="images/' + (find_local_image(m.group(1)) or m.group(1)) + '"', html)
    html = re.sub(r'<figure[^>]*>', '', html)
    html = re.sub(r'</figure>', '', html)
    html = re.sub(r'<figcaption[^>]*>(.*?)</figcaption>', r'<p style="text-align:center;font-size:14px;color:#888;margin-top:-12px">\1</p>', html)
    return html

covers = {
    '423': 'day4_maedaya.jpg', '414': 'hanaori_dinner.jpg', '318': '20260519_breakfast_day3_01.jpg',
    '164': '20260518_sunshine_hotel_morning_view.jpg', '118': '20260518_yatai_night1.jpg',
    '47': 'lingo_kushida.jpg', '15': 'station1.jpg', '10': 'ippudo1.jpg',
}

def slug_to_fn(slug):
    return urllib.parse.unquote(slug).replace('/', '-')

# Build index
with open('index.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>Fukuoka Trip 2026</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft JhengHei",sans-serif;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#e0e0e0;min-height:100vh}
.h{text-align:center;padding:60px 20px 40px}
.h h1{font-size:42px;font-weight:700;background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px}
.h p{font-size:18px;color:#888}
.c{max-width:1200px;margin:0 auto;padding:20px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:30px}
.a{background:rgba(255,255,255,.05);border-radius:16px;overflow:hidden;transition:transform .3s,box-shadow .3s;text-decoration:none;color:inherit}
.a:hover{transform:translateY(-8px);box-shadow:0 20px 40px rgba(0,0,0,.3)}
.a img{width:100%;height:220px;object-fit:cover}
.a .b{padding:24px}
.a .d{font-size:14px;color:#888;margin-bottom:8px}
.a .t{font-size:22px;font-weight:600;margin-bottom:12px;line-height:1.4}
.a .e{font-size:16px;color:#aaa;line-height:1.6}
.ft{text-align:center;padding:40px 20px;color:#666;font-size:14px}
@media(max-width:768px){.h h1{font-size:32px}.g{grid-template-columns:1fr}}
</style></head><body>
<div class="h"><h1>Fukuoka Trip 2026</h1><p>May 2026 - 5 Days 4 Nights in Kyushu</p></div>
<div class="c"><div class="g">
''')
    for p in posts:
        fn = slug_to_fn(p['slug'])
        cover = covers.get(p['id'], '20260518_dazaifu1.jpg')
        exc = re.search(r'<p>(.*?)</p>', p['content'])
        exc = re.sub(r'<[^>]+>', '', exc.group(1))[:80] if exc else ''
        f.write(f'<a href="{fn}.html" class="a"><img src="images/{cover}"><div class="b"><div class="d">{p["date"][:10]}</div><div class="t">{p["title"]}</div><div class="e">{exc}...</div></div></a>\n')
    f.write('</div></div><div class="ft">Lingo Fukuoka Trip</div></body></html>')
print('index.html OK')

for p in posts:
    fn = slug_to_fn(p['slug'])
    cleaned = clean(p['content'])
    with open(fn + '.html', 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>{p["title"]}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft JhengHei",sans-serif;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#e0e0e0;min-height:100vh;line-height:1.8}}
.nv{{position:fixed;top:0;left:0;right:0;background:rgba(26,26,46,.95);padding:16px 24px;z-index:100;backdrop-filter:blur(10px)}}
.nv a{{color:#f5576c;text-decoration:none;font-size:16px}}
.ar{{max-width:800px;margin:0 auto;padding:80px 20px 40px}}
.ah{{text-align:center;margin-bottom:40px}}
.ah h1{{font-size:36px;font-weight:700;background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px;line-height:1.4}}
.ad{{font-size:16px;color:#888}}
.ac{{font-size:18px;line-height:1.9}}
.ac h2{{font-size:26px;margin:40px 0 20px;color:#fff}}
.ac h3{{font-size:22px;margin:30px 0 16px;color:#ddd}}
.ac p{{margin-bottom:20px;color:#ccc}}
.ac img{{width:100%;border-radius:12px;margin:20px 0;transition:transform .3s}}
.ac img:hover{{transform:scale(1.02)}}
.ac video{{width:100%;border-radius:12px;margin:20px 0}}
.ac ul,.ac ol{{margin:20px 0;padding-left:24px}}
.ac li{{margin-bottom:8px;color:#ccc}}
.ac strong{{color:#f5576c}}
.bt{{display:inline-block;margin-top:40px;padding:12px 24px;background:rgba(245,87,108,.2);color:#f5576c;text-decoration:none;border-radius:8px}}
.bt:hover{{background:rgba(245,87,108,.4)}}
hr{{border:none;border-top:1px solid rgba(255,255,255,.1);margin:40px 0}}
@media(max-width:768px){{.ah h1{{font-size:28px}}.ac{{font-size:17px}}}}
</style></head><body>
<div class="nv"><a href="index.html">Back</a></div>
<div class="ar"><div class="ah"><h1>{p["title"]}</h1><div class="ad">{p["date"][:10]}</div></div>
<div class="ac">{cleaned}</div>
<a href="index.html" class="bt">Back to Home</a></div></body></html>''')
    print(fn + '.html OK')

print('ALL DONE')
