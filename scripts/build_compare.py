"""Comparison pages (/cred-alternative, /walnut-alternative, /loop-habit-tracker-alternative) and the
credit card interest calculator. Called from build-pages.py.

Rules for comparison pages: every claim about another app has a source and an "as of" date, and each page
says plainly where the other app is the better choice. Re-check the sources before changing a claim."""
import html
import build_pages as bp

B = bp.B
AS_OF = '13 November 2026'

COMPARE = [
dict(slug='cred-alternative', nav='CRED alternative', other='CRED', tool='credit-card-bill-reminder',
  title='CRED Alternative to Track Card Bills and EMIs | Self Streak',
  desc='Self Streak vs CRED: CRED pays card bills and gives rewards; Self Streak tracks each card’s billing cycle, EMIs, budgets and habits. Which one fits you.',
  h1='A CRED alternative for tracking bills, not just paying them',
  lead='CRED is built around paying credit card bills and earning rewards for it. Self Streak is built around knowing what you owe before the bill arrives: each card’s billing cycle, every EMI, your budget and your habits. Many people use both.',
  short='Use <b>CRED</b> if you want to pay card bills in one place and collect CRED Coins. Use <b>Self Streak</b> if you want to see this bill and next bill as you spend, track EMIs and budgets, and get reminders before every due date, without sharing bank logins or card numbers.',
  rows=[('Pays your credit card bill', 'Yes: netbanking, debit card or UPI', 'No. It reminds you and you pay in your bank or UPI app'),
        ('Rewards for paying', 'CRED Coins and offers', 'No'),
        ('Bill reminder', 'When a card bill is generated', '2 days before and on the due date, until marked paid'),
        ('This bill vs next bill as you spend', 'Not its focus', 'Yes: spends before the statement date go on this bill, after it on the next'),
        ('EMIs, loans and debt-free date', 'Not its focus', 'Yes, with avalanche or snowball payoff plans'),
        ('Budget, expenses, habits, water', 'No', 'Yes, in the same app'),
        ('Card number or bank login needed', 'Card details are added to pay bills', 'Never. Only limit, statement day and due day'),
        ('Who can join', 'Members; aimed at people with a good credit score', 'Anyone'),
        ('Price', 'Free to use', 'Free plan; Plus ₹199/month (bill reminders are in Plus)')],
  them_better=['You want to <b>pay</b> all your card bills from one app.', 'You want rewards and cashback offers for paying on time.', 'You only need card payments, not budgets, EMIs or habits.'],
  us_better=['You want to see what’s on <b>this</b> bill and the <b>next</b> one while you’re still spending.', 'You have EMIs or loans and want one debt-free date and a payoff plan.', 'You’d rather not add card details or link a bank just to track.', 'You want money, bills, habits and health in one app.'],
  faq=[('Is Self Streak a replacement for CRED?', 'Not exactly. CRED pays bills; Self Streak tracks them. Many people keep paying through their bank, UPI or CRED and use Self Streak to know the amount, the minimum due and the date in advance.'),
       ('Does Self Streak need my card number?', 'No. You add a card with its limit, statement day, due day and minimum %. No card number, CVV or bank login.'),
       ('Can I track pay-later accounts too?', 'Yes. Set the minimum due to 100% and Self Streak treats it as “pay the full bill every month”.')],
  sources=[('BankBazaar: Credit card bill payment through CRED (payment methods, CRED Coins, bill reminders)', 'https://www.bankbazaar.com/credit-card/cred-credit-card-bill-payment.html'),
           ('Jagoinvestor: CRED app review (members-only, aimed at a good credit score)', 'https://www.jagoinvestor.com/?p=64713')]),
dict(slug='walnut-alternative', nav='Walnut alternative', other='Walnut (now axio)', tool='expense-tracker',
  title='Walnut (axio) Alternative, No SMS Reading | Self Streak',
  desc='Walnut is now axio, which tracks spends by reading transactional SMS. Self Streak logs by voice, photo or bank statement instead, with no SMS access.',
  h1='A Walnut alternative that doesn’t read your SMS',
  lead='Walnut, the expense tracker many people in India started with, is now called axio. It still tracks spending automatically from your transactional SMS, and it now also offers credit products. Self Streak takes the other route: you log by voice, photo or bank statement, and it never asks for SMS access.',
  short='Pick <b>axio (Walnut)</b> if you want spends logged automatically from bank SMS with no effort. Pick <b>Self Streak</b> if you’d rather not give an app SMS access: say “450 on Swiggy”, snap a receipt or upload a statement, and also track bills, EMIs and habits.',
  rows=[('How spends get in', 'Automatically from transactional SMS', 'Voice (English, Hindi, Hinglish), receipt photo or bank statement PDF/Excel/CSV'),
        ('SMS permission', 'Needed for automatic tracking', 'Never asked'),
        ('Company', 'axio, an RBI-registered NBFC (formerly Walnut / Capital Float)', 'Independent app built in Lucknow'),
        ('Credit products offered', 'Yes (loans, pay later; FDs added in 2026)', 'None. It doesn’t lend or sell financial products'),
        ('Bills, EMIs, credit card cycles', 'Bill detection from SMS', 'Yes, with reminders and a debt-free date'),
        ('Habits, water, protein', 'No', 'Yes, in the same app'),
        ('Price', 'Free', 'Free plan; Plus ₹199/month for AI logging, scans and reminders')],
  them_better=['You want spends to appear with <b>zero</b> typing, and you’re fine with SMS access.', 'You also want credit or FD products from the same company.', 'You only want an expense tracker, nothing else.'],
  us_better=['You don’t want any app reading your SMS.', 'You pay in cash too, and want to log it in two seconds by voice.', 'You want bills, EMIs and card cycles tracked with reminders.', 'You want habits and health next to your money.'],
  faq=[('Is Walnut still available?', f'Walnut was renamed axio. As of {AS_OF} the axio app is still updated on Android, according to APKMirror release listings.'),
       ('Can Self Streak import my old data?', 'You can upload bank statements (PDF, Excel, CSV or a photo) and Self Streak reads the payments. You review them before anything is saved.'),
       ('Is logging by hand slow?', 'Saying “did gym, spent 250 on Swiggy” logs both at once. Statement import catches anything you missed.')],
  sources=[('axio app listing (formerly Walnut; transactional SMS only; NBFC registered with the RBI)', 'https://appgoblin.info/apps/com.daamitt.walnut.app'),
           ('APKMirror: axio release notes (FD investments added in 8.9.6, July 2026)', 'https://www.apkmirror.com/apk/axio-digital-pvt-ltd/axio-expense-tracker-bnpl/axio-expense-tracker-budget-8-9-6-release/')]),
dict(slug='loop-habit-tracker-alternative', nav='Loop alternative', other='Loop Habit Tracker', tool='habit-tracker',
  title='Loop Habit Tracker Alternative for iPhone | Self Streak',
  desc='Loop is free, open source and Android-only. Self Streak works on Android, iPhone and the web, syncs, and adds money and health tracking. Honest comparison.',
  h1='A Loop Habit Tracker alternative that works on iPhone too',
  lead='Loop Habit Tracker is one of the best free habit apps: open source, offline and private. It’s also Android-only with no sync. If you switch phones, use an iPhone, or want your money and health in the same place as your habits, Self Streak is the alternative.',
  short='Stay with <b>Loop</b> if you’re on Android and want a free, open-source, offline habit tracker. Choose <b>Self Streak</b> if you need iPhone or web, sync across devices, reminders at each habit’s own time, or money and health tracking alongside habits.',
  rows=[('Platforms', 'Android', 'Android, iPhone and web (installs from the browser)'),
        ('Price', 'Free, no in-app purchases', 'Free plan for habits and streaks; Plus ₹199/month adds reminders and AI'),
        ('Open source', 'Yes (GPLv3)', 'No'),
        ('Works offline', 'Yes', 'Ticking habits works offline and syncs later'),
        ('Sync across devices', 'No cloud sync; export to CSV or SQLite', 'Yes, with your account'),
        ('Flexible schedules', 'Yes, e.g. 3 times a week', 'Daily, weekly, monthly, quarterly or yearly'),
        ('Money, bills, water, protein', 'No', 'Yes, in the same app')],
  them_better=['You’re on Android and want something <b>completely free</b>.', 'You want open-source software and no account at all.', 'You only track habits.'],
  us_better=['You use an iPhone, or switch between phone and laptop.', 'You want your habits backed up and synced.', 'You want reminders at each habit’s time that skip once it’s done.', 'You also want to track spending, bills, water or protein.'],
  faq=[('Can I move my habits from Loop?', 'There’s no direct import yet. Add your habits in Self Streak (it takes a couple of minutes) and keep Loop’s CSV export as your history.'),
       ('Is Self Streak free for habits?', 'Yes. Habits, streaks, water and expenses stay on the free plan. Plus adds timed reminders, voice and photo logging and AI summaries.'),
       ('Does Self Streak work without internet?', 'Yes for ticking habits and logging. It syncs when you’re back online.')],
  sources=[('Loop Habit Tracker on GitHub (Android app, GPLv3, no in-app purchases)', 'https://github.com/iSoron/uhabits'),
           ('F-Droid: Loop Habit Tracker (Android 9.0+)', 'https://f-droid.org/packages/org.isoron.uhabits/'),
           ('Techpoint Africa: Top free habit tracker apps (Android-only, no cloud sync, CSV/SQLite export)', 'https://techpoint.africa/guide/top-5-free-habit-tracker-apps/')]),
]

def compare_page(c):
    path = '/' + c['slug']
    rows = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(s)}</td></tr>' for a, b, s in c['rows'])
    li = lambda xs: '<ul class="list">' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
    src = ''.join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a></li>' for t, u in c['sources'])
    faq = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in c['faq'])
    tool_name = {'credit-card-bill-reminder': 'Credit card bill reminder', 'expense-tracker': 'Expense tracker', 'habit-tracker': 'Habit tracker'}[c['tool']]
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Compare</div>
<h1>{html.escape(c["h1"])}</h1><p class="lead">{html.escape(c["lead"])}</p>
<div class="cta"><a class="btn lime" href="/app#signup">Try Self Streak free for 7 days →</a><a class="btn" href="/{c["tool"]}">See the {html.escape(tool_name.lower())}</a></div>
<p class="short">{c["short"]}</p><p class="upd">Facts about {html.escape(c["other"])} checked {AS_OF}, with sources below. Updated {bp.UPDATED}.</p></div></header>
<main class="wrap">
<section><h2>{html.escape(c["other"])} vs Self Streak at a glance</h2><div class="tw"><table class="cmp"><thead><tr><th></th><th>{html.escape(c["other"])}</th><th>Self Streak</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>When {html.escape(c["other"])} is the better choice</h2>{li(c["them_better"])}</section>
<section><h2>When Self Streak is the better choice</h2>{li(c["us_better"])}</section>
{bp.shots_html(c["tool"])}
<section><h2>Questions</h2>{faq}</section>
<section><h2>Sources</h2><ul class="list src">{src}</ul><p class="note">Features and prices change. If something here is out of date, <a href="/contact">tell us</a> and we’ll fix it.</p></section>
{bp.FINAL}
<section><h2 style="font-size:20px">More comparisons</h2><div class="more">{"".join(f'<a href="/{o["slug"]}">{html.escape(o["nav"])}</a>' for o in COMPARE if o is not c)}<a href="/{c["tool"]}">{html.escape(tool_name)}</a></div></section></main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": c['h1'], "description": c['desc'],
              "isPartOf": {"@id": B + "/#website"}, "about": {"@id": B + "/#app"}, "dateModified": bp.UPDATED, "inLanguage": "en-IN"},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq']]}]
    return path, bp.shell(path, c['title'], c['desc'], c['h1'], graph, [('Self Streak', '/'), (c['nav'], path)], inner)

# ---------------- credit card interest calculator ----------------
CC_CALC = '''<div class="calc"><div class="fields">
<label>Bill amount (₹)<input id="cB" type="number" inputmode="numeric" value="50000" min="0"></label>
<label>Interest rate (% a month)<input id="cR" type="number" inputmode="decimal" value="3.5" step="0.05" min="0"></label>
<label>Minimum due (% of bill)<input id="cM" type="number" inputmode="decimal" value="5" step="0.5" min="1"></label>
<label>You pay each month (₹, optional)<input id="cP" type="number" inputmode="numeric" value="" min="0" placeholder="Only the minimum"></label></div>
<div class="out"><div><small>Minimum due this month</small><b id="oMin">–</b></div><div><small>Interest + GST next month</small><b id="oNext">–</b></div><div><small>Time to clear</small><b id="oT">–</b></div><div><small>Total interest + GST</small><b id="oI">–</b></div></div>
<p class="note" id="oN"></p></div>
<script>
const f=n=>'₹'+Math.round(n).toLocaleString('en-IN');
function ccCalc(){const B=+cB.value||0,r=(+cR.value||0)/100,m=(+cM.value||5)/100,P=+cP.value||0;
const minOf=b=>Math.min(b,Math.max(b*m,Math.min(200,b)));oMin.textContent=f(minOf(B));const i1=B*r*1.18;oNext.textContent=f(i1);
let b=B,mo=0,I=0;while(b>0.5&&mo<600){const pay=Math.max(P,minOf(b));b-=pay;if(b<=0.5)break;const i=b*r*1.18;I+=i;b+=i;mo++;if(pay<=b*r*1.18&&mo>2){mo=600;break}}
if(mo>=600){oT.textContent='Never';oI.textContent='Keeps growing';oN.textContent='At this payment the interest is larger than what you pay, so the balance never goes down.'}
else{const y=Math.floor((mo+1)/12),mm=(mo+1)%12;oT.textContent=(y?y+' yr ':'')+(mm?mm+' mo':'');oI.textContent=f(I);
oN.textContent=`Paying the full ${f(B)} by the due date costs ₹0 in interest. Paying ${P?f(P)+' a month':'only the minimum'} costs about ${f(I)} in interest and GST before it is cleared.`}}
['cB','cR','cM','cP'].forEach(id=>document.getElementById(id).addEventListener('input',ccCalc));ccCalc();
</script>'''

def cc_calculator():
    path = '/credit-card-interest-calculator'
    desc = 'See what paying only the minimum due on an Indian credit card really costs: interest at 3–4% a month plus 18% GST, and how long the bill takes to clear.'
    faq = [('How is credit card interest calculated in India?', 'If you don’t pay the full bill by the due date, most cards charge interest every month on the unpaid balance, typically around 3–3.75% a month, plus 18% GST on that interest. Most cards also stop giving an interest-free period on new spends until the old balance is cleared.'),
           ('What happens if I pay only the minimum due?', 'You avoid a late fee, but the rest of the bill carries interest. Because the minimum is small (often 5% of the bill), most of each payment goes to interest and the balance falls very slowly.'),
           ('Is this calculator exact?', 'It is an estimate. Banks calculate interest daily from each transaction date and may add fees, so your statement will differ slightly. The calculator assumes no new spending and a minimum due of at least ₹200.')]
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Calculator</div>
<h1>Credit card interest calculator</h1><p class="lead">Enter your bill to see what paying only the minimum costs in interest and GST, and how long it takes to clear. Try a fixed monthly payment to see how much faster it goes.</p>
{CC_CALC}<p class="short">Paying a ₹50,000 bill in full by the due date costs ₹0 in interest. Paying only a 5% minimum at 3.5% a month (plus 18% GST on interest) keeps the debt for years and costs far more than the bill itself. The calculator above shows the exact figures for your bill.</p>
<p class="upd">Estimate only, assuming no new spends. Updated {bp.UPDATED}.</p></div></header>
<main class="wrap">
<section><h2>Why the minimum due is so expensive</h2><p>The minimum due keeps your account in good standing, but it isn’t a plan to pay the bill. On a typical Indian card, interest of about 3.5% a month is close to 42% a year before GST. When you pay only the minimum, most of that payment goes to interest and very little reduces what you owe.</p>
<p>There’s a second cost that the calculator doesn’t show: while a balance is carried, most cards charge interest on new purchases from the day you make them, so the interest-free period disappears until the bill is cleared in full.</p></section>
<section><h2>Three ways out</h2><ul class="list"><li><b>Pay a fixed amount</b> well above the minimum every month. Try it in the calculator.</li><li><b>Clear the card before other debts.</b> Card interest is usually the most expensive debt you have; see <a href="/blog/debt-avalanche-vs-snowball">debt avalanche vs snowball</a>.</li><li><b>Consider a cheaper loan</b> to clear it, such as a personal loan at a lower rate, but only if you stop adding to the card. Compare with the <a href="/emi-calculator/personal-loan">personal loan EMI calculator</a>.</li></ul></section>
<section><h2>Know the dates</h2><p>Interest only starts when the full bill isn’t paid by the due date. Read <a href="/blog/credit-card-statement-date-vs-due-date">statement date vs due date</a> for how the interest-free period works, and let the <a href="/credit-card-bill-reminder">credit card bill reminder</a> warn you before every due date.</p></section>
{bp.shots_html('credit-card-bill-reminder', 'Track every card in Self Streak')}
<section><h2>Questions</h2>{"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)}</section>
<section><h2>Sources</h2><ul class="list src"><li><a href="https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12300" rel="noopener" target="_blank">RBI, Master Direction – Credit Card and Debit Card – Issuance and Conduct Directions, 2022 (updated March 2024)</a></li></ul><p class="note">General information, not financial advice. Check your card’s own interest rate and fees in its most important terms and conditions (MITC).</p></section>
{bp.FINAL}</main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": "Credit card interest calculator", "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "dateModified": bp.UPDATED, "inLanguage": "en-IN"},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    return path, bp.shell(path, 'Credit Card Interest Calculator India | Self Streak', desc,
                          'Credit card interest calculator · Self Streak', graph, [('Self Streak', '/'), ('Credit card interest calculator', path)], inner)

CC_CALC_LINK = ('/credit-card-interest-calculator', 'Credit card interest calculator', 'What paying only the minimum due costs in interest and GST, and how long it takes to clear.')

def link_from_tools():
    """Called before the tool pages render, so each one links to its comparison page."""
    for c in COMPARE:
        bp.GUIDES_FOR.setdefault(c['tool'], []).append(('/' + c['slug'], f"Self Streak vs {c['other']}", c['desc']))
    bp.GUIDES_FOR.setdefault('credit-card-bill-reminder', []).extend(
        (f'/credit-card-statement-date/{k["slug"]}', f'{k["name"]} credit card statement date and due date', f'Interest-free period, due date, grace days and changing the date, from {k["name"]}’s own terms.') for k in BANKS)
    for slug in ('credit-card-bill-reminder', 'debt-payoff-planner'):
        bp.GUIDES_FOR.setdefault(slug, []).insert(0, CC_CALC_LINK)

def llms_lines():
    return [f'- [Credit card interest calculator]({B}/credit-card-interest-calculator): cost of paying only the minimum due on an Indian credit card, with interest and 18% GST.', '', '## Card billing cycles by bank'] + [f"- [{k['name']} credit card statement date and due date]({B}/credit-card-statement-date/{k['slug']}): billing cycle, interest-free period and grace days from {k['name']}’s own terms." for k in BANKS] + ['', '## Comparisons'] + [f"- [Self Streak vs {c['other']}]({B}/{c['slug']}): {c['desc']}" for c in COMPARE]

def build():
    for c in COMPARE:
        path, page = compare_page(c); bp.write(path, page)
    path, page = cc_calculator(); bp.write(path, page)
    build_banks()

# ---------------- per-bank statement date / due date pages ----------------
# Only facts stated in each bank's own MITC (most important terms and conditions) or FAQ, checked AS_OF. Re-read the PDF before changing a line.
BANKS = [
dict(slug='hdfc-bank', name='HDFC Bank', free='20 to 50 days, depending on the card',
  facts=['The interest-free period ranges from 20 to 50 days depending on the card. It does not apply if the previous month’s balance was not cleared in full, or if you withdrew cash from an ATM.',
         'In HDFC Bank’s own example, a billing date of the 4th has a payment due date of the 24th, so a purchase on 14 April gets 41 days of credit and one on 2 May gets 23 days.',
         'The due date on the statement is the date by which the money must reach the card account. 3 grace days are given before the account is reported as past due and a late fee is charged, but days past due and late fees are counted from the printed due date.',
         'You can change your billing cycle at least once by raising a service request. If you never choose one, a default cycle is set from your account opening date.'],
  sources=[('HDFC Bank credit card MITC (version 1.64, updated 6 Nov 2025)', 'https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/?path=/Personal/Pay/Cards/Credit%20Card/Credit%20Card%20Landing%20Page/Manage%20Your%20Credit%20Cards%20PDFs/MITC%201.64.pdf')]),
dict(slug='sbi-card', name='SBI Card', free='20 to 50 days',
  facts=['The interest-free period on purchases ranges from 20 to 50 days, subject to the merchant submitting the transaction on time. It does not apply if the previous month’s balance was not cleared in full, or if you withdrew cash from an ATM.',
         'In SBI Card’s worked example, the payment is due 20 days after the statement date, and you can pay anything from the minimum amount due to the full amount.',
         'Your own statement shows your exact statement and due dates; check it rather than counting days yourself.',
         'Like every card issuer, SBI Card must let you change the billing cycle at least once under RBI rules. Ask through its app, website or helpline.'],
  sources=[('SBI Card Most Important Terms & Conditions (English MITC)', 'https://www.sbicard.com/sbi-card-en/assets/docs/pdf/most-important-terms-and-conditions/english-mitc.pdf')]),
dict(slug='icici-bank', name='ICICI Bank', free='18 to 48 days',
  facts=['The interest-free period ranges from 18 to 48 days depending on when you buy, and a grace period of 3 days is given after the payment due date.',
         'If you don’t pay the total amount due by the due date and grace period, the interest-free period is cancelled.',
         'Cash withdrawals have no interest-free period: interest applies from the date of the transaction.',
         'ICICI Bank’s FAQ says the billing cycle can be changed once every six months, if the feature is available on your card and subject to the bank’s approval. Request it through Customer Care, the iMobile app or internet banking.'],
  sources=[('ICICI Bank credit card MITC (last updated 6 Nov 2026)', 'https://www.icicibank.com/managed-assets/docs/personal/cards/mitc_cc.pdf'),
           ('ICICI Bank credit card FAQs', 'https://www.icicibank.com/Personal-Banking/faq/card/credit-card-faqs.page')]),
dict(slug='axis-bank', name='Axis Bank', free='20 to 50 days, depending on the date of the transaction',
  facts=['The interest-free period ranges from 20 to 50 days depending on the transaction date. It is suspended for the current statement if any balance from the previous bill was not paid by the due date.',
         'Billing cycle dates are the 1st, 7th, 10th, 12th, 13th, 15th, 18th, 20th, 22nd or 25th of the month, and the payment due date falls 20 days after the billing date.',
         'You have a one-time option to change your statement date by calling Axis Phone Banking.',
         'A late payment fee applies if nothing, or less than the minimum amount due, is received by the due date. A grace period of 3 days from the due date is allowed. If you pay by auto-debit and the due date is a Sunday, the debit happens on the next working day.',
         'Cash withdrawals always carry interest from the transaction date.'],
  sources=[('Axis Bank credit card Most Important Terms and Conditions', 'https://www.axisbank.com/docs/default-source/ld/soc/credit-cards/mitc-credit-cards')]),
]

def bank_page(k):
    path = f'/credit-card-statement-date/{k["slug"]}'
    n = k['name']
    title = f'{n} Credit Card Statement Date & Due Date | Self Streak'
    if len(title) > 60: title = f'{n} Card Statement & Due Date | Self Streak'
    desc = f'{n} credit card billing cycle explained from its official terms: interest-free period of {k["free"].split(",")[0]}, when the bill is due, grace days and changing the date.'
    if len(desc) > 160: desc = f'{n} credit card billing cycle from its official terms: interest-free period, when the bill is due, grace days and how to change the date.'
    faq = [(f'What is the interest-free period on a {n} credit card?', f'{k["free"][0].upper() + k["free"][1:]}, according to {n}’s own terms, as long as you pay the full previous bill and don’t withdraw cash.'),
           (f'Can I change my {n} card statement date?', next(f for f in k['facts'] if 'chang' in f)),
           ('Do I need my card number to track this in Self Streak?', 'No. Add the card’s limit, statement day and due day, and Self Streak tracks this bill and next bill and reminds you before each due date.')]
    others = ''.join(f'<a href="/credit-card-statement-date/{o["slug"]}">{html.escape(o["name"])}</a>' for o in BANKS if o is not k)
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Credit cards</div>
<h1>{html.escape(n)} credit card statement date and due date</h1>
<p class="lead">How the billing cycle, payment due date and interest-free period work on {html.escape(n)} credit cards, taken from the bank’s own most important terms and conditions (MITC).</p>
<p class="short"><b>Short answer:</b> On {html.escape(n)} cards the interest-free period is {html.escape(k["free"])}. Pay the <b>total amount due</b> by the due date on your statement and you pay no interest. Your exact dates are printed on each statement.</p>
<p class="upd">Checked against {html.escape(n)}’s published terms on {AS_OF}. Terms differ by card; your card’s MITC wins. Updated {bp.UPDATED}.</p></div></header>
<main class="wrap">
<section><h2>What {html.escape(n)}’s terms say</h2><ul class="list">{"".join(f"<li>{html.escape(f)}</li>" for f in k["facts"])}</ul></section>
<section><h2>What this means for you</h2><ul class="list"><li>Make big planned purchases just after your statement date to get the longest time to pay.</li>
<li>Pay a few working days before the due date, so the money reaches the card account in time.</li>
<li>Paying only the minimum keeps the account in good standing but costs a lot of interest; see the <a href="/credit-card-interest-calculator">credit card interest calculator</a>.</li>
<li>For how the dates work on any card, read <a href="/blog/credit-card-statement-date-vs-due-date">statement date vs due date</a> (<a href="/hi/blog/credit-card-statement-date-vs-due-date" lang="hi" hreflang="hi-IN">हिंदी में</a>).</li></ul></section>
{bp.shots_html('credit-card-bill-reminder', 'Track every card in Self Streak')}
<section><h2>Questions</h2>{"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)}</section>
<section><h2>Sources</h2><ul class="list src">{"".join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a></li>' for t, u in k["sources"])}<li><a href="https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12300" rel="noopener" target="_blank">RBI, Master Direction – Credit Card and Debit Card – Issuance and Conduct Directions, 2022</a></li></ul>
<p class="note">Self Streak is not affiliated with {html.escape(n)}. This page summarises the bank’s published terms and is not financial advice. If something is out of date, <a href="/contact">tell us</a>.</p></section>
{bp.FINAL}
<section><h2 style="font-size:20px">Other banks</h2><div class="more">{others}<a href="/credit-card-bill-reminder">Credit card bill reminder</a></div></section></main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": f'{n} credit card statement date and due date', "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "dateModified": bp.UPDATED, "inLanguage": "en-IN"},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    return path, bp.shell(path, title, desc, f'{n} credit card statement date and due date', graph,
                          [('Self Streak', '/'), ('Credit card bills', '/credit-card-bill-reminder'), (n, path)], inner)

def build_banks():
    for k in BANKS:
        path, page = bank_page(k); bp.write(path, page)
