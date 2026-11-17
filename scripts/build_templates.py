"""Free template pages: /habit-tracker-template, /budget-template-india, /emi-tracker-template and /credit-card-tracker-template.

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
    grid = ''.join(f'<tr><td>{html.escape(n)}</td>' + ''.join(f'<td class="y">✓</td>' if x else '<td></td>' for x in v) + f'<td>{sum(v)}</td><td>{streak(v)}</td></tr>' for n, v in rows)
    body = f'''<section><h2>What’s in the free habit tracker</h2><ul class="list">
<li><b>12 month sheets</b> for 2027 (change the year on the first sheet and every date updates).</li>
<li><b>Tick, don’t type.</b> Click a day’s box and pick ✓ from the drop-down (or type x). The box turns green.</li>
<li><b>Up to 12 habits a month</b>, with weekends shaded and weekday labels above each date.</li>
<li><b>A day score row and a year Overview tab</b> show your best and worst days and months at a glance.</li>
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
<tr><td>Ticking a habit</td><td>Open the file, find the row and the date, pick ✓</td><td>One tap, or say “did gym and read”</td></tr>
<tr><td>Streaks and stats</td><td>Best streak and % per month</td><td>Live streak, heatmap, weekly and monthly view</td></tr>
<tr><td>Weekly or monthly habits</td><td>Daily only</td><td>Daily, weekly, monthly, quarterly or yearly</td></tr>
<tr><td>Money and health</td><td>Separate sheets</td><td>Budget, bills, water and protein in the same app</td></tr>
<tr><td>Your data</td><td>A file you own completely</td><td>Synced to your account; export or delete from Settings</td></tr></tbody></table></div>
<p>If you like planning on a laptop and reviewing once a week, the spreadsheet is enough. If you’ve tried trackers before and stopped after a week, it’s usually because nothing reminded you. That’s the gap an app fills. Read more in <a href="/blog/habit-tracker-app-vs-excel">habit tracker app vs Excel sheet vs paper</a> and <a href="/blog/how-long-does-it-take-to-form-a-habit">how long it takes to form a habit</a>.</p></section>'''
    faq = [('Is this habit tracker template really free?', 'Yes. Download it without signing up or giving an email. Use it, change it and share it for personal use.'),
           ('Does it work in Google Sheets?', 'Yes. In Google Sheets choose File, Import, Upload and pick the file. The formulas, colours and month sheets carry over.'),
           ('How does it count my streak?', 'Each row counts the longest run of consecutive ticked days in that month. An empty box ends the run.'),
           ('Can I use real checkboxes in Google Sheets?', 'Yes. Import the file, select the day boxes and choose Insert → Checkbox. Ticked boxes count as done and unticked ones count as missed.'),
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
<p>A spreadsheet works well if you enjoy a monthly money session on your laptop. Most people stop updating it in the second week because typing every UPI payment is tedious. If that’s you, try logging by voice in the <a href="/expense-tracker">expense tracker</a>. Paying more than one loan? The free <a href="/emi-tracker-template">EMI tracker sheet</a> shows what you still owe on each, and the <a href="/credit-card-tracker-template">credit card tracker sheet</a> shows when every card bill is due.</p></section>'''
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

def emi_template():
    rows = [('Home loan', '₹40,00,000', '8.5%', '240', 'May 2024', '₹34,713', '31', '₹37,79,707', 'Apr 2044'),
            ('Car loan', '₹6,00,000', '9.5%', '60', 'Jan 2025', '₹12,601', '23', '₹4,02,792', 'Dec 2029'),
            ('Phone on no-cost EMI', '₹60,000', '0%', '6', 'Sep 2026', '₹10,000', '3', '₹30,000', 'Feb 2027')]
    grid = ''.join('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in r) + '</tr>' for r in rows)
    body = f'''<section><h2>What’s in the free EMI tracker</h2><ul class="list">
<li><b>One row per loan, up to 30:</b> home, car, personal, education, two-wheeler and gold loans, credit card EMIs and no-cost EMIs on phones or appliances.</li>
<li><b>You type 6 things</b> (amount, yearly rate, tenure in months, first EMI date, name, lender). It works out the <b>EMI</b>, <b>EMIs paid so far</b>, <b>outstanding balance today</b>, <b>interest paid so far</b>, <b>interest still to pay</b> and the <b>month of the last EMI</b>.</li>
<li><b>A summary at the top:</b> total monthly EMIs, EMIs as a share of your salary, total outstanding and your <b>debt-free month</b> (the last EMI across all loans).</li>
<li><b>Schedule tab:</b> pick any loan from a drop-down to see every month’s interest, principal and closing balance.</li>
<li><b>A prepayment column:</b> type an extra payment against any month and the schedule shows how many EMIs and how much interest it saves.</li>
<li>Updates itself every day (it uses today’s date). No macros, so it opens safely anywhere.</li></ul></section>
<section><h2>What it looks like</h2><p>The three example loans in the file, as of 16 Nov 2026:</p>
<div class="tw"><table class="cmp"><thead><tr><th>Loan</th><th>Amount</th><th>Rate</th><th>Months</th><th>First EMI</th><th>EMI</th><th>EMIs paid</th><th>Outstanding</th><th>Last EMI</th></tr></thead><tbody>{grid}</tbody></table></div>
<p>Total EMIs: ₹57,314 a month, 38% of the example ₹1,50,000 salary. Outstanding: ₹42,12,499. Debt-free: April 2044.</p></section>
<section><h2>Worked example: what a ₹2 lakh prepayment does</h2>
<p>On the example home loan (₹40 lakh, 8.5%, 20 years), the schedule shows total interest of ₹43,31,065 over 240 EMIs. Type ₹2,00,000 into the extra-payment column at EMI number 12 and keep the EMI the same: the loan closes in <b>214 EMIs instead of 240</b>, and total interest falls to ₹36,17,959, <b>₹7,13,106 less</b>. The earlier in the loan you prepay, the bigger the saving, because more of each early EMI is interest.</p>
<p>Before prepaying, check your sanction letter. Floating-rate home loans to individuals usually have no prepayment charge; many fixed-rate car and personal loans do. The <a href="/emi-calculator/home-loan">home loan EMI calculator</a> and <a href="/emi-calculator/car-loan">car loan EMI calculator</a> explain the rules for each.</p></section>
<section><h2>How to use it</h2><ol class="list">
<li>Overwrite the three example rows with your loans. Take the amount, rate, tenure and first EMI date from your sanction letter or loan statement.</li>
<li>Check that the EMI column matches what your bank deducts. A difference of a few rupees is rounding. A bigger gap usually means the rate changed (floating loans) or the bank charged broken-period interest; in that case, start a new row from today with the outstanding amount, rate and months left from your latest statement.</li>
<li>Type your take-home salary at the top to see what share of it goes to EMIs.</li>
<li>Open the Schedule tab, pick a loan, and try extra payments to see which loan to prepay first. The <a href="/blog/debt-avalanche-vs-snowball">debt avalanche vs snowball guide</a> explains the two usual orders.</li>
<li><b>Google Sheets:</b> File → Import → Upload. The formulas and drop-downs carry over.</li></ol></section>
<section><h2>Spreadsheet or app?</h2>
<div class="tw"><table class="cmp"><thead><tr><th></th><th>EMI tracker sheet</th><th>Self Streak app</th></tr></thead><tbody>
<tr><td>Price</td><td>Free</td><td>Free plan; Plus ₹199/month adds reminders and AI logging</td></tr>
<tr><td>Outstanding and debt-free date</td><td>Yes, worked out from today’s date</td><td>Yes, for every loan and in total</td></tr>
<tr><td>Reminder before each EMI</td><td>No</td><td>Yes, before every EMI, bill and card due date</td></tr>
<tr><td>Prepayment what-ifs</td><td>Yes, on the Schedule tab</td><td>Yes, in the <a href="/debt-payoff-planner">debt payoff planner</a> (avalanche or snowball)</td></tr>
<tr><td>Bank login or SMS access</td><td>Not needed</td><td>Not needed either</td></tr>
<tr><td>Your data</td><td>A file you own completely</td><td>Synced to your account; export or delete any time</td></tr></tbody></table></div>
<p>If you review your loans once a month on a laptop, the sheet is enough. If you have several EMIs on different dates and want a nudge before each one, that’s what the app adds. Planning the whole month’s money? Pair it with the <a href="/budget-template-india">monthly budget sheet</a>.</p></section>'''
    faq = [('Is this EMI tracker Excel sheet free?', 'Yes. Download it without signing up or giving an email, and use it for as many loans as you have (up to 30 rows).'),
           ('How does it calculate the outstanding loan balance?', 'It counts the EMIs due between your first EMI date and today, then works out the balance left on a reducing-balance loan after that many EMIs. That is the same method banks use, so it should be within a few rupees of your statement unless the rate changed.'),
           ('Does it work for no-cost EMI and credit card EMI?', 'Yes. Enter 0% as the rate for a no-cost EMI and the card’s EMI rate for a credit card EMI. Note that banks may still charge a processing fee and GST on the interest of a card EMI, which the sheet does not add.'),
           ('Can I track a floating-rate home loan?', 'Yes, but when the rate changes, add a new row from that month using the outstanding amount, new rate and months left from your bank statement, and clear the old row.'),
           ('Does it work in Google Sheets?', 'Yes. In Google Sheets choose File, Import, Upload and pick the file. The formulas, drop-downs and the Schedule tab keep working.')]
    return page('/emi-tracker-template', 'Free EMI Tracker Excel Sheet for All Loans | Self Streak',
                'Free EMI tracker for Excel and Google Sheets: list every loan, see outstanding balance today, interest paid and your debt-free month. No signup.',
                'EMI tracker template', 'Free template', 'Free EMI tracker Excel sheet for all your loans',
                'One spreadsheet for every EMI you pay: home, car, personal and no-cost EMIs. It works out what you still owe today and the month you’ll be debt-free.',
                '<b>Download the free EMI tracker</b> above: enter each loan’s amount, rate, tenure and first EMI date, and it shows the EMI, EMIs paid, outstanding balance as of today, interest paid and left, and your debt-free month across all loans. A Schedule tab shows any loan month by month and how much a prepayment saves. It opens in Excel, Google Sheets and Numbers.',
                'self-streak-emi-tracker.xlsx', 'EMI tracker for Excel', body, faq, 'emi-calculator')

def cc_template():
    # Example values are what the file shows as of 17 Nov 2026 (checked with the `formulas` library).
    rows = [('HDFC card', '4th', '24th', '₹4,200 (paid)', '₹18,999', '24 Dec', '37'),
            ('SBI card', '15th', '5th', '₹8,750', '₹1,200', '5 Dec', '49'),
            ('Axis card', '22nd', '11th', '₹2,100 (paid)', '₹9,799', '11 Dec', '24')]
    grid = ''.join('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in r) + '</tr>' for r in rows)
    body = f'''<section><h2>What’s in the free credit card tracker</h2><ul class="list">
<li><b>One row per card, up to 10.</b> You type 5 things: card name, bank, credit limit, <b>statement day</b> and <b>due day</b>. No card number, CVV or login.</li>
<li><b>Dates that work themselves out:</b> last statement, when that bill is due, next statement and next payment due, all as of today.</li>
<li><b>This bill and next bill.</b> Log purchases on the Spends tab and each one lands on the right statement, the way your bank bills it: on or before the statement day goes on that bill, after it rolls to the next.</li>
<li><b>Interest-free days if you buy today</b> on every card, and which card gives you the most. It also shows the best day to buy next (the day after each statement).</li>
<li><b>Limit used and utilisation</b> per card and in total, in red above a level you choose (30% to start with).</li>
<li><b>Red warnings</b> when a payment is 3 days away or late. No macros, so it opens safely anywhere.</li></ul></section>
<section><h2>What it looks like</h2><p>The three example cards in the file, as of 17 Nov 2026:</p>
<div class="tw"><table class="cmp"><thead><tr><th>Card</th><th>Statement day</th><th>Due day</th><th>Last bill</th><th>On next bill so far</th><th>Next payment due</th><th>Interest-free days if bought today</th></tr></thead><tbody>{grid}</tbody></table></div>
<p>The summary at the top says the next payment is ₹8,750 on the SBI card by 5 Dec, and that a purchase today gets the longest time to pay on the SBI card (49 days). Limit used is ₹38,748 of ₹4,50,000 (9%).</p></section>
<section><h2>Why the statement day matters more than the due day</h2>
<p>Take a card with a statement on the 4th and payment due on the 24th (the example HDFC Bank uses in its own terms). Buy something on 4 December and it goes on that day’s bill, due 24 December: 20 days to pay. Buy it on 5 December and it goes on the January bill, due 24 January: <b>50 days</b>. Same card, same amount, one day apart. The tracker shows this number for every card each day, so you can pick the card that gives you the most time before a big purchase.</p>
<p>The interest-free period only applies if you paid the previous bill in full. Pay less and interest is charged from the date of each purchase; see the <a href="/credit-card-interest-calculator">credit card interest calculator</a> for what paying only the minimum costs. RBI rules require card issuers to give you at least a fortnight to pay after the bill is sent (<a href="https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12300" rel="noopener" target="_blank">RBI Master Direction on credit cards, 2022</a>). Your bank’s own dates: <a href="/credit-card-statement-date/hdfc-bank">HDFC Bank</a>, <a href="/credit-card-statement-date/sbi-card">SBI Card</a>, <a href="/credit-card-statement-date/icici-bank">ICICI Bank</a>, <a href="/credit-card-statement-date/axis-bank">Axis Bank</a>.</p></section>
<section><h2>How to use it</h2><ol class="list">
<li>Overwrite the three example cards. The statement date and payment due date are printed at the top of every card statement; type just the day of the month.</li>
<li>Add purchases to the Spends tab as you go, or once a week from your card app. Pick the card from the drop-down.</li>
<li>When you pay a bill in full, set “Last bill paid?” to Yes. When the next statement arrives, set it back to No.</li>
<li>Check the “Last bill” column against your statement. If it differs, a spend was posted a day late or you missed one; your statement is always right.</li>
<li><b>Google Sheets:</b> File → Import → Upload. The formulas, drop-downs and colours carry over.</li></ol></section>
<section><h2>Spreadsheet or app?</h2>
<div class="tw"><table class="cmp"><thead><tr><th></th><th>Credit card tracker sheet</th><th>Self Streak app</th></tr></thead><tbody>
<tr><td>Price</td><td>Free</td><td>Free for 7 days; bill reminders are part of Plus at ₹199/month</td></tr>
<tr><td>This bill and next bill</td><td>Yes, from the spends you type in</td><td>Yes, as you log each spend</td></tr>
<tr><td>Reminder before the due date</td><td>No. You have to open the file</td><td>A notification 2 days before and on the due date, which stops once you mark it paid</td></tr>
<tr><td>Adding a spend</td><td>Type a row</td><td>Say “1,200 on Amazon on my HDFC card”, or snap the statement</td></tr>
<tr><td>Minimum due</td><td>Not tracked</td><td>Yes, with full, minimum or any amount</td></tr>
<tr><td>Card number, SMS or bank login</td><td>Not needed</td><td>Not needed either</td></tr></tbody></table></div>
<p>If you check your cards once a week on a laptop, the sheet does the job. If two cards are due in the same week and you’ve paid a late fee before, that’s what a <a href="/credit-card-bill-reminder">credit card bill reminder</a> is for. Paying card EMIs or loans too? The free <a href="/emi-tracker-template">EMI tracker sheet</a> covers those.</p></section>'''
    faq = [('Is this credit card tracker Excel sheet free?', 'Yes. Download it without signing up or giving an email, and use it for up to 10 cards and 500 purchases.'),
           ('Do I need to enter my card number?', 'No. The sheet only needs a name for each card, the bank, the credit limit, the statement day and the due day. Never type a full card number or CVV into any spreadsheet.'),
           ('How does it know which bill a purchase goes on?', 'A purchase made on or before the statement day goes on that statement; anything after it rolls to the next one. Banks sometimes post a spend a day or two late, so a purchase on the statement day itself can land on either bill. Your statement is the final word.'),
           ('What if my statement date is the 30th or 31st?', 'Type 30 or 31. In shorter months the sheet uses the last day of the month, which is what most banks do. Check your statement for February.'),
           ('Does it work in Google Sheets?', 'Yes. In Google Sheets choose File, Import, Upload and pick the file. The formulas, drop-downs and colours keep working.')]
    return page('/credit-card-tracker-template', 'Free Credit Card Tracker Excel Sheet (India) | Self Streak',
                'Free credit card tracker for Excel and Google Sheets: statement and due dates, this bill and next bill, interest-free days and limit used. No signup.',
                'Credit card tracker template', 'Free template', 'Free credit card tracker Excel sheet',
                'Track every credit card in one spreadsheet: when each bill is due, what’s on the next one, and which card gives you the most interest-free days if you buy today.',
                '<b>Download the free credit card tracker</b> above: add each card’s limit, statement day and due day, log your spends, and it shows every card’s last bill and due date, what’s on the next bill so far, interest-free days if you buy today, and how much of your limit you’ve used. It opens in Excel, Google Sheets and Numbers, and never asks for a card number.',
                'self-streak-credit-card-tracker.xlsx', 'credit card tracker for Excel', body, faq, 'credit-card-bill-reminder')

LINKS = {'habit-tracker': ('/habit-tracker-template', 'Free habit tracker template (Excel & Google Sheets)', 'Download a 12-month habit tracking sheet with automatic streaks.'),
         'emi-calculator': ('/emi-tracker-template', 'Free EMI tracker Excel sheet for all your loans', 'Outstanding balance today, interest paid and your debt-free month.'),
         'debt-payoff-planner': ('/emi-tracker-template', 'Free EMI tracker Excel sheet', 'Every loan in one sheet, with a prepayment column to test what-ifs.'),
         'credit-card-bill-reminder': ('/credit-card-tracker-template', 'Free credit card tracker Excel sheet', 'Statement and due dates, this bill and next bill, and interest-free days for every card.'),
         'expense-tracker': ('/budget-template-india', 'Free monthly budget Excel sheet for India', 'Rupee categories, an expenses log and a 50/30/20 check.')}

def link_from_tools():
    for slug, link in LINKS.items():
        bp.GUIDES_FOR.setdefault(slug, []).insert(0, link)

def llms_lines():
    return ['', '## Free templates', f'- [Habit tracker template for Excel and Google Sheets]({B}/habit-tracker-template): 12 months, up to 12 habits, automatic streaks and completion %.',
            f'- [Monthly budget Excel sheet for India]({B}/budget-template-india): rupee categories, an expenses log and a 50/30/20 check.',
            f'- [EMI tracker Excel sheet]({B}/emi-tracker-template): every loan in one sheet, outstanding balance today, interest paid, debt-free month and a prepayment schedule.',
            f'- [Credit card tracker Excel sheet]({B}/credit-card-tracker-template): every card in one sheet, statement and due dates, this bill and next bill, interest-free days if you buy today, and limit used.']

def build():
    for fn in (habit_template, budget_template, emi_template, cc_template):
        path, pg = fn(); bp.write(path, pg)
