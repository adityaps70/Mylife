#!/usr/bin/env python3
"""Real app screenshots for the marketing pages, taken from a LOCAL dev server with a demo account and sample data.

Never point this at the live site: it signs up a demo account and overwrites that account's data.

    npx wrangler d1 execute self-streak --local --file=schema.sql      # once
    npx wrangler dev --port 8799 --host localhost                      # in another terminal
    python3 -m venv .venv && .venv/bin/pip install pillow playwright
    .venv/bin/python scripts/app-screenshots.py && python3 scripts/build-pages.py

Writes public/img/app-<screen>.webp (phone-sized, 2x) using the installed Google Chrome.
"""
import asyncio, io, json, os, random, time
from datetime import date, timedelta
from PIL import Image
from playwright.async_api import async_playwright

BASE = os.environ.get('LOCAL_URL', 'http://127.0.0.1:8799')
assert BASE.startswith(('http://127.0.0.1', 'http://localhost')), 'local dev server only'
DEMO = {'email': 'demo@selfstreak.test', 'password': 'demo-screens-2026', 'name': 'Riya'}   # local-only demo account
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'img')
W, H = 390, 844

def uid(): return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))
def ds(d): return d.isoformat()

def seed(d):
    """Fill the onboarded demo account with a believable month: income, bills, loans, a card, spends and habit history."""
    random.seed(7); t = date.today()
    d['profile'].update(name='Riya', first='Riya', city='Lucknow', age='27')
    d['income'] = [{'id': uid(), 'name': 'Salary', 'amount': 65000, 'notes': ''}]
    d['bills'] = [
        {'id': uid(), 'name': 'Rent', 'category': 'Rent / Home', 'amount': 12000, 'freq': 'monthly', 'dueDay': 5, 'startMonth': 0, 'autopay': False},
        {'id': uid(), 'name': 'Electricity (UPPCL)', 'category': 'Utilities', 'amount': 1800, 'freq': 'monthly', 'dueDay': 15, 'startMonth': 0, 'autopay': False},
        {'id': uid(), 'name': 'Broadband', 'category': 'Phone & Internet', 'amount': 699, 'freq': 'monthly', 'dueDay': 10, 'startMonth': 0, 'autopay': True},
        {'id': uid(), 'name': 'Mobile recharge', 'category': 'Phone & Internet', 'amount': 349, 'freq': 'monthly', 'dueDay': 21, 'startMonth': 0, 'autopay': False},
        {'id': uid(), 'name': 'Gym membership', 'category': 'Fitness', 'amount': 1500, 'freq': 'monthly', 'dueDay': 1, 'startMonth': 0, 'autopay': False},
        {'id': uid(), 'name': 'Netflix', 'category': 'Subscriptions', 'amount': 199, 'freq': 'monthly', 'dueDay': 24, 'startMonth': 0, 'autopay': True},
        {'id': uid(), 'name': 'Health insurance', 'category': 'Insurance', 'amount': 12000, 'freq': 'yearly', 'dueDay': 10, 'startMonth': 2, 'autopay': False}]
    d['loans'] = [
        {'id': uid(), 'name': 'Personal loan', 'lender': 'SBI', 'type': 'Personal loan', 'principal': 300000, 'outstanding': 186000, 'rate': 12.5, 'emi': 10050, 'dueDay': 5, 'startDate': '2025-06-05', 'notes': ''},
        {'id': uid(), 'name': 'Scooter loan', 'lender': 'Bajaj Finance', 'type': 'Vehicle loan', 'principal': 90000, 'outstanding': 41000, 'rate': 11, 'emi': 2950, 'dueDay': 12, 'startDate': '2025-03-12', 'notes': ''}]
    d['cards'] = [{'id': uid(), 'name': 'HDFC Millennia', 'kind': 'Credit card', 'limit': 150000, 'openBal': 18450, 'stmtDay': 3, 'dueDay': 23,
                   'minPct': 5, 'rate': 3.5, 'lateFee': 600, 'notes': '', 'openDate': ds(t.replace(day=3) if t.day >= 3 else (t.replace(day=1) - timedelta(days=1)).replace(day=3))}]
    d['savings'] = [
        {'id': uid(), 'name': 'Emergency fund', 'type': 'Emergency fund', 'current': 95000, 'target': 240000, 'monthly': 6000},
        {'id': uid(), 'name': 'Nifty 50 index SIP', 'type': 'Mutual fund SIP', 'current': 142000, 'target': 0, 'monthly': 8000},
        {'id': uid(), 'name': 'EPF', 'type': 'EPF', 'current': 168000, 'target': 0, 'monthly': 3900}]
    spends = [('Swiggy', 'Eating out & Swiggy/Zomato', 386, 'UPI'), ('Big Basket', 'Groceries & household', 2140, 'UPI'), ('Indian Oil', 'Fuel & transport', 600, 'Card'),
              ('Uber', 'Fuel & transport', 214, 'UPI'), ('Myntra', 'Shopping & clothes', 1299, 'Card'), ('Chai & samosa', 'Eating out & Swiggy/Zomato', 80, 'Cash'),
              ('PVR', 'Entertainment & outings', 640, 'Card'), ('Sabzi mandi', 'Groceries & household', 420, 'Cash'), ('Zomato', 'Eating out & Swiggy/Zomato', 512, 'UPI'),
              ('Apollo Pharmacy', 'Personal care & grooming', 365, 'UPI'), ('Blinkit', 'Groceries & household', 780, 'UPI'), ('Rapido', 'Fuel & transport', 96, 'UPI')]
    tx = [{'id': uid(), 'date': ds(t - timedelta(days=i % 12)), 'payee': p, 'category': c, 'amount': a, 'dir': 'out', 'method': m, 'note': ''} for i, (p, c, a, m) in enumerate(spends)]
    tx += [{'id': uid(), 'date': ds(t - timedelta(days=6)), 'payee': 'Sent to Mummy', 'category': 'Family support / home contribution', 'amount': 5000, 'dir': 'out', 'method': 'UPI', 'note': ''}]
    d['tx'] = tx
    # Habit history: a solid last 3 weeks, patchier before, so the heatmap and streak look real.
    daily = [h for h in d['health']['habits'] if h.get('period') == 'daily']
    checks, logs = {}, {}
    for i in range(0, 120):
        day = t - timedelta(days=i)
        rate = 0.92 if i < 21 else 0.6 if i < 60 else 0.35
        if i == 0: rate = 0.55
        checks['d:' + ds(day)] = {h['id']: True for h in daily if random.random() < rate}
        logs[ds(day)] = {'water': random.choice([8, 9, 10, 11, 12]) if i else 7, 'steps': random.choice([7200, 9100, 10400, 11800, 12650]) if i else 6420}
    d['health']['checks'], d['health']['logs'] = checks, logs
    g = d['game']; g['start'] = ds(t - timedelta(days=121)); g['days'] = {ds(t - timedelta(days=i)): 70 + (i * 7) % 40 for i in range(1, 22)}
    d['meals'] = {ds(t): [{'id': uid(), 't': int(time.time() * 1000) - 5 * 3600e3, 'name': 'Poha with peanuts', 'kcal': 330, 'p': 9, 'c': 52, 'f': 10, 'src': 'photo'},
                          {'id': uid(), 't': int(time.time() * 1000) - 1 * 3600e3, 'name': 'Dal, rice, paneer bhurji, salad', 'kcal': 690, 'p': 34, 'c': 78, 'f': 24, 'src': 'photo'}]}
    return d

SHOTS = [  # (file, app page, heading text to scroll to or None)
    ('overview', 'overview', None), ('today', 'today', None), ('health', 'health', None), ('meals', 'health', 'Food today'),
    ('activity', 'activity', None), ('budget', 'budget', None), ('bills', 'bills', None), ('debt', 'debt', None), ('streak', 'streak', None)]
HIDE = """document.querySelectorAll('.toast,.tip,.coach,.bubble').forEach(e=>e.remove());
for (const el of document.querySelectorAll('body *')) { const cs = getComputedStyle(el); if (cs.position !== 'fixed') continue;
  const r = el.getBoundingClientRect(); if (r.top > innerHeight * 0.6 && r.left > innerWidth * 0.4 && r.width < innerWidth * 0.8) el.style.visibility = 'hidden'; }"""

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        ctx = await br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, color_scheme='dark')
        pg = await ctx.new_page()
        await pg.goto(BASE + '/robots.txt')
        r = await pg.evaluate("d=>fetch('/api/login',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)}).then(r=>r.status)", DEMO)
        if r != 200: raise SystemExit('Log in failed: sign up the demo account by opening /app once (see onboarding) first.')
        cur = await pg.evaluate("fetch('/api/data').then(r=>r.json())")
        if not cur.get('data') or not cur['data'].get('profile', {}).get('onboarded'): raise SystemExit('Finish onboarding for the demo account first.')
        data = seed(cur['data'])
        st = await pg.evaluate("b=>fetch('/api/data',{method:'PUT',headers:{'content-type':'application/json'},body:JSON.stringify(b)}).then(r=>r.status)", {'data': data, 'updated': int(time.time() * 1000)})
        assert st == 200, st
        await pg.goto(BASE + '/app'); await pg.wait_for_timeout(3500)
        await pg.evaluate("document.querySelectorAll('.toast,.tip,.coach,.bubble').forEach(e=>e.remove())")
        for name, page, target in SHOTS:
            await pg.evaluate(f"go('{page}')"); await pg.wait_for_timeout(1800)
            await pg.evaluate("window.scrollTo(0,0)")
            if target:
                el = pg.locator(f'h2:text-is("{target}"), h3:text-is("{target}"), .card :text-is("{target}")').first
                await el.scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-90)")
            await pg.evaluate(HIDE)
            await pg.wait_for_timeout(400)
            png = await pg.screenshot()
            im = Image.open(io.BytesIO(png)).convert('RGB')
            out = os.path.join(OUT, f'app-{name}.webp')
            im.save(out, 'WEBP', quality=78, method=6)
            print(f'img/app-{name}.webp  {im.size[0]}x{im.size[1]}  {os.path.getsize(out):,} bytes')
        await br.close()

if __name__ == '__main__':
    asyncio.run(main())
