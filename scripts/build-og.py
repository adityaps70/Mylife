#!/usr/bin/env python3
"""Makes the 1200x630 share images (og:image) for blog posts and tool pages, and keeps og-image.png under 100 KB.

Run after scripts/build-pages.py, then run build-pages.py again so pages point at their new image:
    python3 -m venv .venv && .venv/bin/pip install pillow
    .venv/bin/python scripts/build-og.py && python3 scripts/build-pages.py

Each card is rendered from the page's own kicker and H1 with headless Google Chrome, then saved as JPEG.
Only pages whose card text changed are re-rendered (the text is stored in public/og/index.json).
"""
import html, json, os, re, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PUB = os.path.join(ROOT, 'public')
OGDIR = os.path.join(PUB, 'og')
CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
MAX_BYTES = 100_000

TOOLS = ['credit-card-bill-reminder', 'emi-calculator', 'expense-tracker', 'debt-payoff-planner', 'habit-tracker', 'water-reminder', 'calorie-protein-tracker']

def pages():
    out = [t for t in TOOLS] + ['blog', 'about']
    out += ['emi-calculator/' + f[:-5] for f in sorted(os.listdir(os.path.join(PUB, 'emi-calculator'))) if f.endswith('.html')]
    out += ['blog/' + f[:-5] for f in sorted(os.listdir(os.path.join(PUB, 'blog'))) if f.endswith('.html')]
    return out

def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def card_text(path):
    s = open(os.path.join(PUB, path + '.html'), encoding='utf8').read()
    kick = re.search(r'<div class="kick">(.*?)</div>', s, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return text(kick.group(1)) if kick else 'Self Streak', text(h1.group(1))

LOGO = '<svg viewBox="0 0 100 100"><rect width="100" height="100" rx="26" fill="#d7f64a"/><path d="M68 31c-3-9-11-14-21-14-12 0-20 7-20 16 0 21 47 13 47 35 0 10-9 17-22 17-11 0-20-5-24-14" fill="none" stroke="#10120a" stroke-width="12" stroke-linecap="round"/><circle cx="77" cy="23" r="7" fill="#10120a"/></svg>'

def card_html(kick, h1):
    size = 76 if len(h1) <= 40 else 64 if len(h1) <= 62 else 54
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;800&display=block" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:#09090b;color:#f4f4f5;font-family:'Plus Jakarta Sans',system-ui,sans-serif;padding:72px 80px;display:flex;flex-direction:column;
background-image:radial-gradient(700px 420px at 0% 0%,rgba(215,246,74,.20),transparent 70%),radial-gradient(600px 400px at 100% 100%,rgba(69,223,230,.10),transparent 70%)}}
.k{{color:#d7f64a;font-weight:800;font-size:26px;letter-spacing:.12em;text-transform:uppercase}}
h1{{font-weight:800;font-size:{size}px;line-height:1.08;letter-spacing:-.03em;margin-top:22px;max-width:1000px}}
.f{{margin-top:auto;display:flex;align-items:center;gap:18px;font-weight:800;font-size:34px}}.f svg{{width:64px;height:64px}}
.f span{{margin-left:auto;color:#a1a1aa;font-weight:600;font-size:28px}}</style></head>
<body><div class="k">{html.escape(kick)}</div><h1>{html.escape(h1)}</h1><div class="f">{LOGO}Self Streak<span>selfstreak.com</span></div></body></html>'''

def render(src_html, png):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf8') as f:
        f.write(src_html)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=1200,630', '--virtual-time-budget=4000', f'--screenshot={png}', 'file://' + f.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(f.name)

def save_jpeg(png, out):
    im = Image.open(png).convert('RGB').crop((0, 0, 1200, 630))
    for q in (86, 80, 74, 68, 60):
        im.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
        if os.path.getsize(out) <= MAX_BYTES: return q
    raise SystemExit(f'{out} is still over {MAX_BYTES} bytes')

def shrink_default():
    p = os.path.join(PUB, 'og-image.png')
    if os.path.getsize(p) <= MAX_BYTES: return
    im = Image.open(p).convert('RGB')
    for colors in (256, 192, 128, 96, 64):
        im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(p, optimize=True)
        if os.path.getsize(p) <= MAX_BYTES:
            print(f'og-image.png: {os.path.getsize(p):,} bytes ({colors} colours)'); return
    raise SystemExit('og-image.png is still over 100 KB')

def main():
    os.makedirs(OGDIR, exist_ok=True)
    idx_path = os.path.join(OGDIR, 'index.json')
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
    force = '--force' in sys.argv
    for path in pages():
        kick, h1 = card_text(path)
        name = path.replace('/', '-')
        out = os.path.join(OGDIR, name + '.jpg')
        if not force and idx.get(name) == [kick, h1] and os.path.exists(out): continue
        png = os.path.join(tempfile.gettempdir(), f'og-{name}.png')
        render(card_html(kick, h1), png)
        q = save_jpeg(png, out); os.unlink(png)
        idx[name] = [kick, h1]
        print(f'og/{name}.jpg  {os.path.getsize(out):,} bytes  q{q}')
    json.dump(idx, open(idx_path, 'w'), indent=1, ensure_ascii=False, sort_keys=True)
    shrink_default()

if __name__ == '__main__':
    main()
