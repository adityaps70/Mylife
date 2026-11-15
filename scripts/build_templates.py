"""Free template pages: /habit-tracker-template and /budget-template-india.

People searching "habit tracker excel" or "monthly budget excel sheet India" want a file, so these pages give
a real, free one (made by scripts/make-templates.py, no signup), explain how to use it, and say honestly when
an app does the job better. Called from build-pages.py."""
import html
import build_pages as bp

B = bp.B
CSS = '''<style>.dl{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}.grid7{overflow-x:auto;margin-top:12px}
.grid7 table{border-collapse:collapse;font-size:13px}.grid7 th,.grid7 td{border:1px solid var(--line);padding:4px 7px;text-align:center}
.grid7 td:first-child,.grid7 th:first-child{text-align:left;white-space:nowrap}.grid7 .y{background:var(--lime);color:#10120a;font-weight:700}</style>'''

def faq_block(faq):
    return '<section><h2>Questions</h2>' + ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faq) + '</section>'

def page(path, title, desc, nav, kick, h1, lead, short, file, file_label, body, faq, shots):
    inner = f'''{CSS}<header style="padding-top:20px"><div class="wrap"><div class="kick">{kick}</div>
<h1>{html.escape(h1)}</h1><p class="lead">{html.escape(lead)}</p>
<div class="dl"><a class="btn lime" href="/templates/{file}" download>Download {html.escape(file_label)} (free) ↓</a><a class="btn" href="/app#signup">Or use the app, free for 7 days</a></div>
<p class="short">{short}</p><p class="upd">No signup, no email needed. Works in Excel, Google Sheets and Apple Numbers. Updated {bp.UPDATED}.</p></div></header>
<main class="wrap">{body}{bp.shots_html(shots, 'The same thing as an app')}{faq_block(faq)}{bp.FINAL}</main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": h1, "description": desc, "isPartOf": {"@id": B + "/#website"},
              "dateModified": bp.UPDATED, "inLanguage": "en-IN",
              "mainEntity": {"@type": "DigitalDocument", "name": file_label, "url": f"{B}/templates/{file}", "encodingFormat": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             "isAccessibleForFree": True, "publisher": {"@id": B + "/#org"}}},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    return path, bp.shell(path, title, desc, h1, graph, [('Self Streak', '/'), (nav, path)], inner)

def habit_template():
    days = 10
    rows = [('Drink 8 glasses of water', [1, 1, 1, 0, 1, 1, 1, 1, 0, 1]), ('Walk 8,000 steps', [1, 0, 1, 1, 1, 0, 1, 1, 1, 1]), ('Read 10 pages', [1, 1, 0, 0, 1, 1, 1, 0, 1, 1])]
    def streak(v):
        best = cur = 0
        for x in v: cur = cur + 1 if x else 0; best = max(best, cur)
        return best
    grid = ''.join(f'<tr><td>{html.escape(n)}</td>' + ''.join(f'<td class="y">1</td>' if x else '<td></td>' for x in v) + f'<td>{sum(v)}</td><td>{streak(v)}</td></tr>' for n, v in rows)
    body = f'''<section><h2>What’s in the free habit tracker</h2><ul class="list">
<li><b>12 month sheets</b> for 2027 (change the year on the first sheet and every date updates).</li>
<li><b>Up to 12 habits a month.</b> Type 1 on a day you did it and the box turns green.</li>
<li><b>Counts itself:</b> days done, completion % and your <b>best streak</b> for each habit.</li>
<li>Short months handled: February stops at 28 or 29, so your % is right.</li>
<li>No macros, so it opens safely anywhere.</li></ul></section>
<section><h2>What it looks like</h2><p>The first 10 days of a month, with three example habits:</p>
<div class="grid7"><table><thead><tr><th>Habit</th>{"".join(f"<th>{d}</th>" for d in range(1, days + 1))}<th>Done</th><th>Best streak</th></tr></thead><tbody>{grid}</tbody></table></div></section>
<section><h2>How to use it</h2><ol class="list">
<li><b>Excel:</b> open the file, go to this month’s tab and replace the example habits with yours.</li>
<li><b>Google Sheets:</b> open sheets.google.com, then File → Import → Upload, and pick the file. It keeps the formulas and colours.</li>
<li><b>On your phone:</b> it works in the Google Sheets or Excel app, but typing into small cells every day is fiddly. That’s the main reason people move to an app.</li>
<li>Start with 2 or 3 habits. Add more once those are automatic.</li></ol></section>
<section><h2>Spreadsheet or app: which should you use?</h2>
<div class="tw"><table class="cmp"><thead><tr><th></th><th>Excel / Sheets template</th><th>Self Streak app</th></tr></thead><tbody>
<tr><td>Price</td><td>Free</td><td>Free plan for habits and streaks; Plus ₹199/month for reminders and AI</td></tr>
<tr><td>Reminders</td><td>None. You have to remember to open it</td><td>A notification at each habit’s own time, skipped once it’s done</td></tr>
<tr><td>Ticking a habit</td><td>Open the file, find the row and the date, type 1</td><td>One tap, or say “did gym and read”</td></tr>
<tr><td>Streaks and stats</td><td>Best streak and % per month</td><td>Live streak, heatmap, weekly and monthly view</td></tr>
<tr><td>Weekly or monthly habits</td><td>Daily only</td><td>Daily, weekly, monthly, quarterly or yearly</td></tr>
<tr><td>Money and health</td><td>Separate sheets</td><td>Budget, bills, water and protein in the same app</td></tr>
<tr><td>Your data</td><td>A file you own completely</td><td>Synced to your account; export or delete from Settings</td></tr></tbody></table></div>
<p>If you like planning on a laptop and reviewing once a week, the spreadsheet is enough. If you’ve tried trackers before and stopped after a week, it’s usually because nothing reminded you. That’s the gap an app fills. Read more in <a href="/blog/habit-tracker-app-vs-excel">habit tracker app vs Excel sheet vs paper</a> and <a href="/blog/how-long-does-it-take-to-form-a-habit">how long it takes to form a habit</a>.</p></section>'''
    faq = [('Is this habit tracker template really free?', 'Yes. Download it without signing up or giving an email. Use it, change it and share it for personal use.'),
           ('Does it work in Google Sheets?', 'Yes. In Google Sheets choose File, Import, Upload and pick the file. The formulas, colours and month sheets carry over.'),
           ('How does it count my streak?', 'Each row counts the longest run of consecutive days marked 1 in that month. A blank day ends the run.'),
           ('Can I print it?', 'Yes. Each month fits on one landscape page. Tick boxes by hand and copy the totals in later if you want the counts.')]
    return page('/habit-tracker-template', 'Free Habit Tracker Excel Template 2027 | Self Streak',
                'Download a free habit tracker for Excel and Google Sheets: 12 months, up to 12 habits, automatic streaks and completion %. No signup needed.',
                'Habit tracker template', 'Free template', 'Free habit tracker template for Excel and Google Sheets',
                'A ready-made habit tracking sheet for 2027: one tab per month, tick a box each day, and it works out your completion rate and best streak for you.',
                '<b>Download the free habit tracker spreadsheet</b> above: 12 monthly tabs, room for 12 habits, and formulas that count days done, % and your best streak. It opens in Excel, Google Sheets and Numbers. If you’d rather get a reminder at the right time and tick habits in one tap, the Self Streak app does the same job on your phone.',
                'self-streak-habit-tracker-2027.xlsx', 'habit tracker for Excel', body, faq, 'habit-tracker')

def budget_template():
    body = '''<section><h2>What’s in the free budget sheet</h2><ul class="list">
<li><b>Budget tab</b> with rupee categories that fit Indian households: rent or home loan EMI, groceries, electricity, mobile, other EMIs, fuel, school fees, Swiggy/Zomato, OTT, festivals, SIPs, emergency fund and PPF.</li>
<li><b>50/30/20 check built in:</b> it compares your needs, wants and savings with 50%, 30% and 20% of your take-home pay.</li>
<li><b>Expenses tab:</b> add each spend with a date, a category from a drop-down and how you paid (UPI, card, cash). The Budget tab adds them up and turns a category red when it goes over.</li>
<li>Sample figures for a ₹75,000 salary, so you can see how it works before typing yours.</li></ul></section>
<section><h2>How to use it</h2><ol class="list">
<li>Type your take-home salary in the lime cell, then a budget for each category.</li>
<li>Every day or two, add what you spent to the Expenses tab. Pick the category from the list.</li>
<li>Check the summary at the top: if “Wants” is over its target, that’s where to cut first.</li>
<li>Start a fresh copy each month (File → Save as), so each month keeps its own record.</li></ol>
<p>New to the rule? The <a href="/blog/50-30-20-budget-rule-india">50/30/20 budget guide</a> has worked examples for ₹40,000, ₹75,000 and ₹1.5 lakh salaries, and a calculator.</p></section>
<section><h2>Spreadsheet or app?</h2>
<div class="tw"><table class="cmp"><thead><tr><th></th><th>Excel / Sheets budget</th><th>Self Streak app</th></tr></thead><tbody>
<tr><td>Price</td><td>Free</td><td>Free plan for expenses and budgets; Plus ₹199/month for AI logging and reminders</td></tr>
<tr><td>Adding a spend</td><td>Open the file and type a row</td><td>Say “450 on Swiggy”, snap a receipt, or import a bank statement</td></tr>
<tr><td>Bills and EMIs</td><td>You track due dates yourself</td><td>Reminders before every bill, EMI and card due date</td></tr>
<tr><td>Credit cards</td><td>One row per spend</td><td>Shows what’s on this bill and the next one as you spend</td></tr>
<tr><td>Bank login or SMS access</td><td>Not needed</td><td>Not needed either</td></tr>
<tr><td>Your data</td><td>A file you own completely</td><td>Synced to your account; export or delete any time</td></tr></tbody></table></div>
<p>A spreadsheet works well if you enjoy a monthly money session on your laptop. Most people stop updating it in the second week because typing every UPI payment is tedious. If that’s you, try logging by voice in the <a href="/expense-tracker">expense tracker</a>.</p></section>'''
    faq = [('Is this budget template free?', 'Yes, free to download and use, with no signup or email.'),
           ('Does it work in Google Sheets?', 'Yes. In Google Sheets choose File, Import, Upload and pick the file. The drop-downs and totals keep working.'),
           ('Which categories does it use?', 'Needs (rent or home loan, groceries, utilities, mobile, EMIs, transport, insurance, fees, medicines), wants (eating out, shopping, outings, subscriptions, travel, festivals) and savings (SIPs, emergency fund, PPF or EPF top-up, extra loan payments). Rename any of them.'),
           ('Can I use it for a family budget?', 'Yes. Enter the household’s combined take-home pay and add every member’s spends to the Expenses tab.')]
    return page('/budget-template-india', 'Free Monthly Budget Excel Sheet for India | Self Streak',
                'Download a free monthly budget Excel sheet in rupees with Indian categories, an expenses log and a built-in 50/30/20 check. Works in Google Sheets too.',
                'Budget template', 'Free template', 'Free monthly budget Excel sheet for India',
                'A household budget spreadsheet in rupees, built for Indian salaries: plan each category, log what you spend, and see if you’re on track for 50/30/20.',
                '<b>Download the free monthly budget sheet</b> above. Enter your take-home salary and a budget per category, log spends on the Expenses tab, and it totals everything and checks your needs, wants and savings against the 50/30/20 rule. It opens in Excel, Google Sheets and Numbers.',
                'self-streak-monthly-budget-india.xlsx', 'monthly budget for Excel', body, faq, 'expense-tracker')

LINKS = {'habit-tracker': ('/habit-tracker-template', 'Free habit tracker template (Excel & Google Sheets)', 'Download a 12-month habit tracking sheet with automatic streaks.'),
         'expense-tracker': ('/budget-template-india', 'Free monthly budget Excel sheet for India', 'Rupee categories, an expenses log and a 50/30/20 check.')}

def link_from_tools():
    for slug, link in LINKS.items():
        bp.GUIDES_FOR.setdefault(slug, []).insert(0, link)

def llms_lines():
    return ['', '## Free templates', f'- [Habit tracker template for Excel and Google Sheets]({B}/habit-tracker-template): 12 months, up to 12 habits, automatic streaks and completion %.',
            f'- [Monthly budget Excel sheet for India]({B}/budget-template-india): rupee categories, an expenses log and a 50/30/20 check.']

def build():
    for fn in (habit_template, budget_template):
        path, pg = fn(); bp.write(path, pg)
