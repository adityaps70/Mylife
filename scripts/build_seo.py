"""SEO pages built on top of build-pages.py: EMI pages per loan type (computed tables), the /blog guides,
and llms.txt. Run `python3 scripts/build-pages.py` (it calls build() here)."""
import html, json, os, re
import build_pages as bp
from blog_posts import POSTS

B, UPDATED = bp.B, bp.UPDATED
def inr(n):
    """Indian digit grouping: 12,34,567."""
    n = round(n); s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        head = re.sub(r'(\d)(?=(\d{2})+$)', r'\1,', head)
        s = head + ',' + tail
    return ('-' if n < 0 else '') + '₹' + s

def lakh(n):
    return f'₹{n/1e5:g} lakh' if n < 1e7 else f'₹{n/1e7:g} crore'

def emi(P, rate, n):
    r = rate / 1200
    return P * r * (1 + r) ** n / ((1 + r) ** n - 1) if r else P / n

def payoff(P, rate, n, extra):
    r, E = rate / 1200, emi(P, rate, n)
    b, m, I = P, 0, 0.0
    while b > 0.5 and m < 1200:
        i = b * r; I += i; b = b + i - min(E + extra, b + i); m += 1
    return m, I

def yearly(P, rate, n):
    r, E = rate / 1200, emi(P, rate, n)
    b, rows = P, []
    for y in range(n // 12):
        pi = pp = 0.0
        for _ in range(12):
            i = b * r; p = E - i; b -= p; pi += i; pp += p
        rows.append((y + 1, pp, pi, max(b, 0)))
    return rows

LOANS = [
    dict(slug='home-loan', name='Home loan', rate=8.5, P=3000000, n=240, amounts=[1500000, 2500000, 3000000, 5000000, 7500000],
         tenures=[120, 180, 240, 300], extra=5000,
         intro='A home loan is usually the largest and longest loan you will take, often 15 to 30 years. Because the tenure is so long, interest can add up to more than the amount you borrowed, which is why small prepayments make a big difference.',
         tax='Under the old tax regime, interest on a home loan for a self-occupied house can be deducted up to ₹2 lakh a year under Section 24(b), and principal repayment counts towards the ₹1.5 lakh limit of Section 80C. The new tax regime does not allow these deductions for a self-occupied home. Check with a tax adviser for your case.',
         prepay='Most home loans in India are on a floating rate. RBI rules do not allow banks to charge foreclosure or prepayment penalties on floating-rate term loans to individual borrowers for non-business purposes, so you can usually prepay any amount without a fee.',
         tips=['Ask your lender whether a prepayment reduces your EMI or your tenure. Reducing tenure saves more interest.',
               'When the repo rate rises, lenders often extend your tenure instead of raising the EMI. Check your statement every year.',
               'A 20% down payment lowers both the loan amount and, often, the rate offered.']),
    dict(slug='car-loan', name='Car loan', rate=9.5, P=800000, n=60, amounts=[400000, 600000, 800000, 1000000, 1500000],
         tenures=[36, 48, 60, 84], extra=2000,
         intro='A car loan typically runs 3 to 7 years. A longer tenure lowers the EMI, but the car loses value faster than you repay the loan in the early years, so a shorter tenure is usually the safer choice.',
         tax='For a car used personally, there is no income tax deduction on the loan. If the car is used for business, the interest and depreciation may be claimed as business expenses.',
         prepay='Many car loans are on a fixed rate, and lenders may charge a foreclosure fee (often a few percent of the outstanding amount). Read the sanction letter before prepaying, and compare the fee with the interest you would save.',
         tips=['Keep the car EMI under about 10–15% of your monthly take-home pay.',
               'Compare the on-road price, not the ex-showroom price, when choosing the loan amount.',
               'Dealer-arranged loans are convenient, but check your bank’s pre-approved rate first.']),
    dict(slug='personal-loan', name='Personal loan', rate=13, P=500000, n=60, amounts=[100000, 200000, 300000, 500000, 1000000],
         tenures=[12, 24, 36, 60], extra=2000,
         intro='A personal loan is unsecured, so it costs more than a home or car loan. Rates depend heavily on your credit score and income. It is still far cheaper than carrying a credit card balance, which often costs 36% a year or more.',
         tax='There is generally no tax deduction on personal loan interest. An exception: if the money is used to buy, build or renovate a house, the interest may qualify under Section 24(b) under the old regime, with proof of how the money was used.',
         prepay='Personal loans are usually fixed-rate, and many lenders charge a foreclosure fee or allow prepayment only after a lock-in period (often 6 to 12 months). Check your loan agreement for the exact terms.',
         tips=['Look at the processing fee and APR, not just the interest rate.',
               'Use a personal loan to clear credit card debt only if you stop adding to the card.',
               'Shorter tenures cost much less interest; pick the highest EMI you can comfortably pay.']),
    dict(slug='education-loan', name='Education loan', rate=10.5, P=1500000, n=120, amounts=[500000, 1000000, 1500000, 2500000, 4000000],
         tenures=[60, 84, 120, 180], extra=3000,
         intro='An education loan usually has a moratorium: you start repaying after the course ends plus a grace period (often 6 to 12 months). Interest builds up during that time, so paying even the interest while studying lowers your future EMI.',
         tax='Under Section 80E (old tax regime), the entire interest paid on an education loan for higher studies can be deducted, with no upper limit, for up to 8 years from the year you start repaying. Principal repayment is not deductible.',
         prepay='Many education loans are on a floating rate, so prepaying is usually free under RBI rules for individual borrowers. Some private lenders use fixed rates with a foreclosure fee; check the sanction letter.',
         tips=['Ask whether interest during the moratorium is simple or compounded.',
               'Government schemes and some banks offer interest concessions for girl students or for paying interest during the course.',
               'Start small prepayments from your first salary; the 80E benefit applies only to interest actually paid.']),
    dict(slug='two-wheeler-loan', name='Two-wheeler loan', rate=12, P=100000, n=36, amounts=[60000, 80000, 100000, 150000, 200000],
         tenures=[12, 24, 36, 48], extra=500,
         intro='A two-wheeler loan is small and short, usually 1 to 4 years. Because the amounts are small, the processing fee and any “low EMI” offers can matter as much as the interest rate.',
         tax='There is no tax deduction for a two-wheeler used personally. If it is used for business, interest may be claimed as a business expense.',
         prepay='Two-wheeler loans are usually fixed-rate, and some lenders charge a foreclosure fee. On a short loan the interest saved by prepaying is modest, so check that the fee does not cancel it out.',
         tips=['“Zero down payment” offers usually mean a higher loan amount and more interest.',
               'Compare the effective rate: a flat rate of 7% can be close to 13% on a reducing balance.',
               'Keep the EMI under about 5% of your take-home pay.']),
]

def loan_page(L):
    P, rate, n, x = L['P'], L['rate'], L['n'], L['extra']
    E = emi(P, rate, n); TI = E * n - P
    m2, I2 = payoff(P, rate, n, x)
    yrs = n // 12
    path = f"/emi-calculator/{L['slug']}"
    name = L['name']
    head = ''.join(f'<th>{t//12} yrs</th>' if t % 12 == 0 else f'<th>{t} mo</th>' for t in L['tenures'])
    grid = ''.join(f'<tr><td>{lakh(a)}</td>' + ''.join(f'<td>{inr(emi(a, rate, t))}</td>' for t in L['tenures']) + '</tr>' for a in L['amounts'])
    rates = [rate - 1, rate - 0.5, rate, rate + 0.5, rate + 1]
    rrows = ''.join(f'<tr><td>{r:g}%</td><td>{inr(emi(P, r, n))}</td><td>{inr(emi(P, r, n) * n - P)}</td></tr>' for r in rates)
    yr = yearly(P, rate, n)
    pick = yr if len(yr) <= 7 else [yr[i] for i in sorted(set([0, 1, 2, len(yr)//4, len(yr)//2, 3*len(yr)//4, len(yr)-1]))]
    arows = ''.join(f'<tr><td>Year {y}</td><td>{inr(pp)}</td><td>{inr(pi)}</td><td>{inr(b)}</td></tr>' for y, pp, pi, b in pick)
    first_int_share = round(100 * yr[0][2] / (yr[0][1] + yr[0][2]))
    title = f"{name} EMI Calculator India | Self Streak"
    desc = f"{name} EMI calculator with ready tables: EMI by amount and tenure, total interest, year-by-year split and prepayment savings. Free, no sign-up."
    if len(desc) > 160: desc = desc[:157].rsplit(' ', 1)[0] + '…'
    short = (f"For a {lakh(P)} {name.lower()} at {rate:g}% a year for {yrs} years, the EMI is about {inr(E)} a month and the total interest is about {inr(TI)}. "
             f"Paying {inr(x)} extra every month would close it {n - m2} months early and save about {inr(TI - I2)} in interest.")
    calc = f'''<div class="calc"><div class="fields">
<label>Loan amount (₹)<input id="eP" type="number" inputmode="numeric" value="{P}" min="1000"></label>
<label>Interest rate (% a year)<input id="eR" type="number" inputmode="decimal" value="{rate:g}" step="0.05" min="0"></label>
<label>Tenure (months)<input id="eN" type="number" inputmode="numeric" value="{n}" min="1"></label>
<label>Extra payment each month (₹)<input id="eX" type="number" inputmode="numeric" value="{x}" min="0"></label></div>
<div class="out"><div><small>Monthly EMI</small><b id="oE">{inr(E)}</b></div><div><small>Total interest</small><b id="oI">{inr(TI)}</b></div><div><small>Total paid</small><b id="oT">{inr(E*n)}</b></div><div><small>With the extra payment</small><b id="oS">{n-m2} months sooner</b></div></div>
<p class="note" id="oNote"></p></div>
<script>
const f=n=>'₹'+Math.round(n).toLocaleString('en-IN');
function emiCalc(){{const P=+eP.value||0,r=(+eR.value||0)/1200,n=Math.max(1,+eN.value||1),x=+eX.value||0;
const E=r?P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):P/n;oE.textContent=f(E);oI.textContent=f(E*n-P);oT.textContent=f(E*n);
let b=P,m=0,int=0;while(b>0.5&&m<1200){{const i=b*r;int+=i;b=b+i-Math.min(E+x,b+i);m++}}
const saved=(E*n-P)-int;oS.textContent=x>0?`${{n-m}} months sooner`:'–';oNote.textContent=x>0?`Paying ${{f(x)}} extra every month closes the loan in ${{m}} months instead of ${{n}} and saves about ${{f(saved)}} in interest.`:'Add an extra monthly amount to see how much interest a prepayment saves.'}}
['eP','eR','eN','eX'].forEach(id=>document.getElementById(id).addEventListener('input',emiCalc));emiCalc();
</script>'''
    others = ''.join(f'<a href="/emi-calculator/{o["slug"]}">{html.escape(o["name"])} EMI</a>' for o in LOANS if o is not L)
    faq = [(f'What is the EMI for a {lakh(P)} {name.lower()}?', f'At {rate:g}% a year for {yrs} years, the EMI on {lakh(P)} is about {inr(E)} a month. Use the calculator above for your own rate and tenure.'),
           (f'How much interest will I pay on a {name.lower()}?', f'On {lakh(P)} at {rate:g}% for {yrs} years, total interest is about {inr(TI)}, so you repay {inr(E*n)} in all. A shorter tenure or regular prepayments cut this.'),
           (f'Can I prepay my {name.lower()}?', L['prepay'])]
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">EMI calculator</div>
<h1>{html.escape(name)} EMI calculator</h1><p class="lead">{html.escape(L["intro"])}</p>
{calc}<p class="short">{html.escape(short)}</p><p class="upd">Example rate of {rate:g}% used for the tables below. Rates change with the RBI repo rate and your credit profile, so enter the rate your lender offers. Updated {UPDATED}.</p></div></header>
<main class="wrap">
<section><h2>{html.escape(name)} EMI by amount and tenure</h2><p>Monthly EMI at {rate:g}% a year for common {name.lower()} amounts.</p>
<div class="tw"><table><thead><tr><th>Loan amount</th>{head}</tr></thead><tbody>{grid}</tbody></table></div></section>
<section><h2>How much does a 1% rate change cost?</h2><p>For {lakh(P)} over {yrs} years, every 0.5% on the rate changes the EMI and the total interest like this:</p>
<div class="tw"><table><thead><tr><th>Rate</th><th>EMI</th><th>Total interest</th></tr></thead><tbody>{rrows}</tbody></table></div></section>
<section><h2>Where your EMI goes, year by year</h2><p>In year 1, about {first_int_share}% of what you pay on {lakh(P)} at {rate:g}% goes to interest. The share falls every year as the balance shrinks.</p>
<div class="tw"><table><thead><tr><th>Year</th><th>Principal paid</th><th>Interest paid</th><th>Balance left</th></tr></thead><tbody>{arows}</tbody></table></div></section>
<section><h2>What a small prepayment does</h2><p>Paying {inr(x)} extra every month on {lakh(P)} at {rate:g}% closes the loan in {m2} months instead of {n}, and total interest falls from {inr(TI)} to {inr(I2)}: a saving of about {inr(TI - I2)}.</p>
<p>{html.escape(L["prepay"])}</p></section>
<section><h2>Tax on a {html.escape(name.lower())}</h2><p>{html.escape(L["tax"])}</p></section>
{bp.shots_html('loan', 'Track this loan in Self Streak')}
<section><h2>Tips before you borrow</h2><ul class="list">{"".join(f"<li>{html.escape(t)}</li>" for t in L["tips"])}</ul></section>
<section><h2>How EMI is calculated</h2><p>EMI = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1), where P is the loan amount, r is the monthly rate (yearly rate ÷ 12 ÷ 100) and n is the number of months. All tables on this page use this reducing-balance formula.</p>
<p>Once you have the loan, <a href="/emi-calculator">Self Streak tracks every EMI</a> with a reminder before each due date and shows your <a href="/debt-payoff-planner">debt-free date</a>.</p></section>
<section><h2>Questions</h2>{"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)}</section>
<section><h2>Related guides</h2><div class="guides">{"".join(f'<a href="/blog/{q["slug"]}">{html.escape(q["h1"])}<span>{html.escape(q["desc"])}</span></a>' for q in POSTS if q["slug"] in LOAN_GUIDES)}</div></section>
{bp.FINAL}
<section><h2 style="font-size:20px">Other EMI calculators</h2><div class="more"><a href="/emi-calculator">All loans</a>{others}</div></section></main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": f"{name} EMI calculator", "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "dateModified": UPDATED, "inLanguage": "en-IN"},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    return path, bp.shell(path, title, desc, f'{name} EMI calculator · Self Streak', graph,
                          [('Self Streak', '/'), ('EMI calculator', '/emi-calculator'), (f'{name} EMI', path)], inner)

# ---------------- blog ----------------
AUTHOR_NAME = 'Aditya Pratap Singh'
AUTHOR = {"@type": "Person", "@id": B + "/about#aditya", "name": AUTHOR_NAME, "url": B + "/about",
          "jobTitle": "Founder", "worksFor": {"@id": B + "/#org"},
          "description": "Founder of Self Streak, based in Lucknow. Writes the Self Streak guides on budgeting, credit cards, EMIs, habits, water and protein."}

# Each tool page's own guides come from POSTS[*]['hubs']; loan pages share these two.
LOAN_GUIDES = ['debt-avalanche-vs-snowball', '50-30-20-budget-rule-india']
TOOL_NAMES = {'credit-card-bill-reminder': 'Credit card bill reminder', 'expense-tracker': 'Expense tracker', 'debt-payoff-planner': 'Debt payoff planner',
              'habit-tracker': 'Habit tracker', 'water-reminder': 'Water reminder and calculator', 'calorie-protein-tracker': 'Calorie and protein tracker',
              'emi-calculator': 'EMI calculator'}

def post_page(p):
    path = '/blog/' + p['slug']
    words = len(re.sub('<[^>]+>', ' ', p['body']).split())
    toc = ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p['body']))
    src = ''.join((f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a></li>' if u else f'<li>{html.escape(t)}</li>') for t, u in p['sources'])
    tool = p['hubs'][0]
    others = [q for q in POSTS if q is not p and set(q['hubs']) & set(p['hubs'])] or [q for q in POSTS if q is not p]
    rel = (f'<a href="/{tool}">{html.escape(TOOL_NAMES[tool])}<span>Try it: the Self Streak tool this guide is about.</span></a>'
           + ''.join(f'<a href="/blog/{q["slug"]}">{html.escape(q["h1"])}<span>{html.escape(q["desc"])}</span></a>' for q in others[:2]))
    inner = f'''<article><header style="padding-top:20px"><div class="wrap"><div class="kick">{html.escape(p["kicker"])}</div>
<h1>{html.escape(p["h1"])}</h1><p class="lead">{html.escape(p["lead"])}</p>
<p class="byline">By <a href="/about">{AUTHOR_NAME}</a> · Published {p["date"]} · Updated {bp.UPDATED} · {max(1, round(words/220))} min read</p>
<p class="short"><b>Short answer:</b> {p["short"]}</p></div></header>
<main class="wrap">
<section><h2 style="font-size:18px">In this guide</h2><ol class="list">{toc}</ol></section>
{p["body"]}
<section><h2>Sources</h2><ul class="list src">{src}</ul><p class="note">This guide is general information, not financial, tax or medical advice. Check with a qualified professional for your situation.</p></section>
{bp.FINAL}
<section><h2>Related guides</h2><div class="guides">{rel}</div><div class="more" style="margin-top:12px"><a href="/blog">All guides</a></div></section></main></article>'''
    graph = [{"@type": "BlogPosting", "@id": B + path + "#post", "headline": p['h1'], "description": p['desc'], "url": B + path,
              "mainEntityOfPage": B + path, "datePublished": p['date'], "dateModified": bp.UPDATED, "author": AUTHOR,
              "publisher": {"@id": B + "/#org"}, "image": bp.og_for(path), "inLanguage": "en-IN", "wordCount": words,
              "isPartOf": {"@id": B + "/blog#blog"}, "about": p.get('about', [])}]
    head = f'<meta property="article:published_time" content="{p["date"]}"><meta property="article:modified_time" content="{bp.UPDATED}"><meta name="author" content="{AUTHOR_NAME}">\n'
    return path, words, bp.shell(path, p['title'], p['desc'], p['h1'], graph,
                                 [('Self Streak', '/'), ('Guides', '/blog'), (p['nav'], path)], inner, og_type='article', head_extra=head)

def blog_index(posts):
    path = '/blog'
    cards = ''.join(f'<a href="/blog/{p["slug"]}">{html.escape(p["h1"])}<span>{html.escape(p["desc"])}</span></a>' for p in posts)
    loans = ''.join(f'<a href="/emi-calculator/{L["slug"]}">{html.escape(L["name"])} EMI calculator<span>EMI tables by amount and tenure, interest by year and prepayment savings.</span></a>' for L in LOANS)
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Guides</div><h1>Money, habit and health guides</h1>
<p class="lead">Clear, practical guides for everyday life in India: budgeting in rupees, credit cards, loans and EMIs, building habits that stick, water and protein. Every number is worked out, and every claim links to its source.</p></div></header>
<main class="wrap"><section><h2>Latest guides</h2><div class="guides">{cards}</div></section>
<section><h2>EMI calculators by loan type</h2><div class="guides">{loans}</div></section>{bp.FINAL}</main>'''
    desc = 'Practical guides on budgeting in rupees, credit card bills, EMIs, paying off debt, building habits, water and protein, with worked examples.'
    graph = [{"@type": "Blog", "@id": B + "/blog#blog", "name": "Self Streak guides", "url": B + path, "description": desc, "publisher": {"@id": B + "/#org"}, "inLanguage": "en-IN",
              "blogPost": [{"@id": f"{B}/blog/{p['slug']}#post"} for p in posts]}]
    return bp.shell(path, 'Money, Habit & Health Guides for India | Self Streak', desc, 'Self Streak guides', graph, [('Self Streak', '/'), ('Guides', path)], inner)

def build():
    for L in LOANS:
        path, page = loan_page(L); bp.write(path, page)
    for p in POSTS:
        path, words, page = post_page(p); bp.write(path, page)
        assert words >= 700, (p['slug'], words)
        print(f'  {path}: {words} words')
        for slug in p['hubs']:
            bp.GUIDES_FOR.setdefault(slug, []).append((path, p['h1'], p['desc']))
    bp.GUIDES_FOR.setdefault('emi-calculator', [])[0:0] = [(f'/emi-calculator/{L["slug"]}', f'{L["name"]} EMI calculator', 'Ready EMI tables, interest by year and prepayment savings.') for L in LOANS]
    bp.write('/blog', blog_index(POSTS))

def extra_pages():
    """/about (the author page blog posts link to) and the styled 404 page."""
    path = '/about'
    desc = 'Self Streak is built in Lucknow by Aditya Pratap Singh, who also writes its guides on budgeting, credit cards, EMIs, habits, water and protein.'
    guides = ''.join(f'<a href="/blog/{p["slug"]}">{html.escape(p["h1"])}<span>{html.escape(p["desc"])}</span></a>' for p in POSTS)
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">About</div><h1>About Self Streak</h1>
<p class="lead">Self Streak is one app for the things people in India try to keep on track every day: habits and streaks, spending in rupees, credit card bills and EMIs, water and protein.</p></div></header>
<main class="wrap">
<section id="aditya"><h2>{AUTHOR_NAME}</h2>
<p>{AUTHOR_NAME} is the founder of Self Streak and builds it from Lucknow, Uttar Pradesh. Aditya also writes the guides on this site. Each one works through real rupee examples and lists its sources, such as RBI directions for credit cards and loans and published research for habits, water and protein.</p>
<p>Questions, corrections or feedback on a guide: <a href="/contact">contact us</a>, or find Self Streak on <a href="https://instagram.com/selfstreak" rel="noopener">Instagram</a>.</p></section>
<section><h2>What Self Streak does</h2><ul class="list">
<li>Habits and streaks with reminders at each habit’s own time.</li>
<li>Expenses, budgets, bills, EMIs and credit cards, logged by voice, photo or bank statement, with no bank login.</li>
<li>Water and protein tracking, made for Indian food.</li>
<li>A free plan for habits, water, expenses and your streak. Plus is ₹199 a month, with every feature free for 7 days.</li></ul></section>
<section><h2>Guides by {AUTHOR_NAME}</h2><div class="guides">{guides}</div></section>
{bp.FINAL}</main>'''
    graph = [{"@type": "AboutPage", "@id": B + path + "#page", "url": B + path, "name": "About Self Streak", "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "about": {"@id": B + "/#org"}, "mainEntity": AUTHOR, "dateModified": bp.UPDATED, "inLanguage": "en-IN"}]
    bp.write(path, bp.shell(path, 'About Self Streak and Its Founder, Aditya Pratap Singh', desc, 'About Self Streak', graph,
                            [('Self Streak', '/'), ('About', path)], inner))
    # 404: Cloudflare serves public/404.html with a 404 status (assets.not_found_handling in wrangler.jsonc).
    tools = ''.join(f'<a href="/{s}">{html.escape(n)}</a>' for s, n in bp.ALL)
    loans = ''.join(f'<a href="/emi-calculator/{L["slug"]}">{html.escape(L["name"])} EMI</a>' for L in LOANS)
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Error 404</div><h1>This page doesn’t exist</h1>
<p class="lead">The link may be old or mistyped. Here’s everything that does exist on Self Streak.</p>
<div class="cta"><a class="btn lime" href="/">Go to the homepage</a><a class="btn" href="/blog">Read the guides</a></div></div></header>
<main class="wrap"><section><h2>Tools</h2><div class="more">{tools}</div></section>
<section><h2>EMI calculators</h2><div class="more"><a href="/emi-calculator">All loans</a>{loans}</div></section>
<section><h2>Guides</h2><div class="guides">{guides}</div></section>{bp.FINAL}</main>'''
    page = bp.shell('/404', 'Page Not Found · Self Streak Habit, Money & Health Tools', 'This page does not exist. Find the Self Streak habit tracker, expense tracker, EMI calculators and guides on budgeting, habits, water and protein.',
                    'Page not found · Self Streak', [], [('Self Streak', '/'), ('Page not found', '/404')], inner, robots='noindex, follow')
    page = re.sub(r'<link rel="canonical"[^>]*>\n?', '', page).replace(bp.UPDATED, bp.TODAY)
    with open(os.path.join(bp.OUT, '404.html'), 'w') as f: f.write(page)

def llms(urls):
    pages = {p['slug']: p for p in bp.PAGES}
    lines = ['# Self Streak', '',
             '> Self Streak is an India-first app for habits and streaks, money (budget, expenses, bills, EMIs, credit cards, debt payoff) and health (water, meals, protein), with AI logging by voice, photo and bank statement. Free plan; Plus is ₹199/month.', '',
             'Self Streak runs on the web at https://selfstreak.com/app, with iPhone and Android apps. It never asks for bank logins or card numbers. Prices are in Indian rupees.', '',
             '## Product']
    lines += [f'- [{pages[s]["h1"]}]({B}/{s}): {pages[s]["desc"]}' for s in pages]
    lines += ['', '## Free calculators'] + [f'- [{L["name"]} EMI calculator]({B}/emi-calculator/{L["slug"]}): EMI tables by amount and tenure, interest by year and prepayment savings at an example {L["rate"]:g}% rate.' for L in LOANS]
    lines += ['', '## Guides'] + [f'- [{p["h1"]}]({B}/blog/{p["slug"]}): {p["desc"]}' for p in POSTS]
    lines += ['', '## Key facts',
              '- Price: free plan for habits, water, expenses and streaks. Plus (₹199 a month, 7-day free trial) adds AI logging, photo scans, reminders and more. Paid on the web via Razorpay or Cashfree.',
              '- Platforms: web app, iPhone, Android. Works offline for ticking habits and logging.',
              '- Privacy: no bank login, card number or CVV is ever needed. Data can be exported or deleted from Settings.',
              '- Languages: understands English, Hindi and Hinglish for voice and text logging.',
              '', '## Company',
              f'- [About]({B}/about): who builds Self Streak and writes the guides.',
              f'- [Contact]({B}/contact): support email and how to reach us.',
              f'- [Privacy policy]({B}/privacy)', f'- [Terms]({B}/terms)', f'- [Refunds]({B}/refunds)', '']
    with open(os.path.join(bp.OUT, 'llms.txt'), 'w') as f:
        f.write('\n'.join(lines))
