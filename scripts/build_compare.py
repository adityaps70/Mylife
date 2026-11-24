"""Comparison pages (/cred-alternative, /walnut-alternative, /loop-habit-tracker-alternative) and the
credit card interest calculator. Called from build-pages.py.

Rules for comparison pages: every claim about another app has a source and an "as of" date, and each page
says plainly where the other app is the better choice. Re-check the sources before changing a claim."""
import html, json
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
dict(slug='habitify-alternative', nav='Habitify alternative', other='Habitify', tool='habit-tracker',
  title='Habitify Alternative with Money Tracking | Self Streak',
  desc='Habitify vs Self Streak: Habitify is a polished habit-only app; Self Streak adds budgets, bills, water and protein, rupee pricing and Hindi voice logging.',
  h1='A Habitify alternative that tracks your money and health too',
  lead='Habitify is a well-made habit tracker on Apple devices, Android and the web. If all you want is habits, it’s a good choice. If you also want your budget, bills, EMIs, water and protein in the same place, priced in rupees, Self Streak is the alternative.',
  short='Choose <b>Habitify</b> if you want a dedicated habit app with Apple Watch and Mac apps. Choose <b>Self Streak</b> if you want habits plus money and health in one app, voice logging in English, Hindi or Hinglish, and a ₹199/month price with habits free.',
  rows=[('Habits and streaks', 'Yes', 'Yes, with a heatmap and weekly view'),
        ('Platforms', 'iPhone, iPad, Apple Watch, Mac, Android and web', 'Android, iPhone and web (installs from the browser); no watch app'),
        ('Free plan', 'Yes; habits beyond the free limit become view-only', 'Habits, water, expenses and your streak are free'),
        ('Paid plans', 'Plus and Pro tiers (introduced April 2026)', 'Plus at ₹199/month, 7-day free trial'),
        ('Budget, bills, EMIs, credit cards', 'No', 'Yes'),
        ('Water and protein', 'No', 'Yes'),
        ('Log by voice in Hindi or Hinglish', 'No', 'Yes')],
  them_better=['You want an <b>Apple Watch</b> or Mac app for your habits.', 'You only track habits and want a dedicated, focused app.', 'You’re outside India and prefer pricing in your own currency.'],
  us_better=['You want habits, money and health in <b>one</b> app instead of three.', 'You’d like to log by voice: “did gym, spent 250 on Swiggy”.', 'You want bill, EMI and card reminders alongside habit reminders.', 'You want habits free, with an India-priced upgrade.'],
  faq=[('Can I move my habits from Habitify?', 'There’s no direct import. Adding your habits in Self Streak takes a couple of minutes, and you can keep Habitify’s export as your history.'),
       ('Is Self Streak free for habits?', 'Yes. Habits, streaks, water and expenses are on the free plan. Plus adds timed reminders, AI voice and photo logging and more.'),
       ('Does Self Streak have an Apple Watch app?', 'No. It runs on Android, iPhone and the web.')],
  sources=[('Habitify on the App Store (free plan: habits beyond the basic limit are view-only)', 'https://apps.apple.com/app/id1111447047'),
           ('Habitify changelog: new tiered pricing, 6 April 2026', 'https://feedback.habitify.me/changelog/new-tiered-pricing'),
           ('Headway: Habitify review (platforms)', 'https://makeheadway.com/blog/habitify/')]),
dict(slug='streaks-app-alternative', nav='Streaks alternative', other='Streaks', tool='habit-tracker',
  title='Streaks App Alternative for Android and Web | Self Streak',
  desc='Streaks is a one-time-purchase habit app for Apple devices only. Self Streak works on Android, iPhone and the web, and adds money and health tracking.',
  h1='A Streaks app alternative that works on Android too',
  lead='Streaks is a popular habit tracker for iPhone, iPad, Apple Watch and Mac, sold as a one-time purchase. It isn’t available on Android. If you use an Android phone, switch between devices, or want money and health tracked alongside habits, Self Streak is the alternative.',
  short='Pick <b>Streaks</b> if you live in Apple’s world and want to pay once with no subscription. Pick <b>Self Streak</b> if you use Android or the web, want habits free, or want your budget, bills, water and protein in the same app.',
  rows=[('Platforms', 'Apple only: iPhone, iPad, Apple Watch, Mac', 'Android, iPhone and web'),
        ('Price', 'One-time purchase, no subscription (price varies by country)', 'Free plan for habits; Plus ₹199/month for reminders and AI'),
        ('Apple Watch app', 'Yes', 'No'),
        ('Habits and streaks', 'Yes', 'Yes, with a heatmap and weekly view'),
        ('Budget, bills, EMIs, credit cards', 'No', 'Yes'),
        ('Water and protein', 'No', 'Yes'),
        ('Log by voice in Hindi or Hinglish', 'No', 'Yes')],
  them_better=['You only use Apple devices and want an <b>Apple Watch</b> app.', 'You prefer paying <b>once</b> instead of a subscription.', 'You only track habits.'],
  us_better=['You use an <b>Android</b> phone, or switch between phone and laptop.', 'You want habit tracking free.', 'You want money, bills and health next to your habits.', 'You’d like to log by voice in English, Hindi or Hinglish.'],
  faq=[('Is Streaks available on Android?', f'No. As of {AS_OF}, Streaks is only available for Apple devices.'),
       ('Is Self Streak a one-time purchase?', 'No. Habits are free; Self Streak Plus is ₹199 a month with a 7-day free trial, and you can stay on the free plan.'),
       ('Can I use both?', 'Yes. Some people keep Streaks on their Apple Watch for habits and use Self Streak for money and bills.')],
  sources=[('Headway: Streaks app review (Apple-only, one-time purchase, no subscription)', 'https://makeheadway.com/blog/streaks-app-review/'),
           ('iMore: Streaks for iPhone, iPad, Apple Watch and Mac', 'https://www.imore.com/apps/hate-losing-a-daily-streak-this-iphone-app-is-perfect-for-your-habit-tracking')]),
]

def compare_page(c):
    path = '/' + c['slug']
    rows = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(s)}</td></tr>' for a, b, s in c['rows'])
    li = lambda xs: '<ul class="list">' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
    src = ''.join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a></li>' for t, u in c['sources'])
    faq = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in c['faq'])
    tmpl = {'credit-card-bill-reminder': ('/credit-card-tracker-template', 'Free credit card tracker Excel'), 'expense-tracker': ('/budget-template-india', 'Free budget template (Excel)'), 'habit-tracker': ('/habit-tracker-template', 'Free habit tracker Excel template')}[c['tool']]
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
<section><h2 style="font-size:20px">More comparisons</h2><div class="more">{"".join(f'<a href="/{o["slug"]}">{html.escape(o["nav"])}</a>' for o in COMPARE if o is not c)}<a href="/{c["tool"]}">{html.escape(tool_name)}</a><a href="{tmpl[0]}">{tmpl[1]}</a></div></section></main>'''
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
<section><h2>Three ways out</h2><ul class="list"><li><b>Pay a fixed amount</b> well above the minimum every month. Try it in the calculator.</li><li><b>Clear the card before other debts.</b> Card interest is usually the most expensive debt you have; see <a href="/blog/debt-avalanche-vs-snowball">debt avalanche vs snowball</a>, or put your own debts in the free <a href="/debt-snowball-spreadsheet">debt snowball and avalanche spreadsheet</a> to see your debt-free month and total interest under each plan.</li><li><b>Consider a cheaper loan</b> to clear it, such as a personal loan at a lower rate, but only if you stop adding to the card. Compare with the <a href="/emi-calculator/personal-loan">personal loan EMI calculator</a>.</li></ul></section>
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

# ---------------- net worth calculator ----------------
NW_AS_OF = '24 November 2026'
NW_ASSETS = [('nA1', 'Savings accounts and cash', 150000, 'q'), ('nA2', 'Fixed and recurring deposits', 200000, 'q'),
             ('nA3', 'Mutual funds and shares', 400000, 'q'), ('nA4', 'EPF, PPF and NPS', 600000, ''),
             ('nA5', 'Gold and jewellery', 300000, ''), ('nA6', 'Home you live in (today’s value)', 6000000, 'h'),
             ('nA7', 'Other property and land', 0, ''), ('nA8', 'Vehicles and other assets', 400000, '')]
NW_DEBTS = [('nD1', 'Home loan outstanding', 4200000, 'h'), ('nD2', 'Car or two-wheeler loan', 250000, ''),
            ('nD3', 'Personal and education loans', 0, ''), ('nD4', 'Credit card and pay-later dues', 40000, ''),
            ('nD5', 'Other borrowings (gold loan, family)', 0, '')]
def _nw_fields(rows):
    return ''.join(f'<label>{html.escape(t)} (₹)<input id="{i}" type="number" inputmode="numeric" value="{v}" min="0"></label>' for i, t, v, _ in rows)
NW_CALC = '''<div class="calc" id="nw"><h3 style="margin-top:0">What you own</h3><div class="fields">''' + _nw_fields(NW_ASSETS) + '''</div>
<h3>What you owe</h3><div class="fields">''' + _nw_fields(NW_DEBTS) + '''</div>
<h3>Optional</h3><div class="fields"><label>Monthly expenses, including EMIs (₹)<input id="nE" type="number" inputmode="numeric" value="50000" min="0"></label></div>
<div class="out"><div><small>Net worth</small><b id="nN">–</b></div><div><small>Total assets</small><b id="nTA">–</b></div><div><small>Total debts</small><b id="nTD">–</b></div>
<div><small>Net worth without your home</small><b id="nNH">–</b></div><div><small>Money you can reach in a few days</small><b id="nQ">–</b></div><div><small>Months of expenses it covers</small><b id="nM">–</b></div><div><small>Debts as % of assets</small><b id="nR">–</b></div></div>
<p class="note" id="nNote"></p><p class="note">Your numbers stay in this browser. Nothing is sent to Self Streak. <a href="#" id="nClr">Clear the form</a></p></div>
<script>
(function(){const f=n=>(n<0?'−':'')+'₹'+Math.abs(Math.round(n)).toLocaleString('en-IN');
const A=''' + json.dumps([[i, k] for i, _, _, k in NW_ASSETS]) + ''',D=''' + json.dumps([[i, k] for i, _, _, k in NW_DEBTS]) + ''',ids=A.concat(D).map(x=>x[0]).concat(['nE']),$=id=>document.getElementById(id),v=id=>Math.max(0,+$(id).value||0),K='ss-networth';
try{const s=JSON.parse(localStorage.getItem(K)||'null');if(s)ids.forEach(id=>{if(id in s)$(id).value=s[id]})}catch(e){}
function calc(){let a=0,d=0,q=0,ha=0,hd=0;A.forEach(([id,k])=>{const x=v(id);a+=x;if(k=='q')q+=x;if(k=='h')ha+=x});D.forEach(([id,k])=>{const x=v(id);d+=x;if(k=='h')hd+=x});
const n=a-d,nh=(a-ha)-(d-hd),e=v('nE');$('nN').textContent=f(n);$('nN').style.color=n<0?'var(--red)':'var(--lime)';$('nTA').textContent=f(a);$('nTD').textContent=f(d);$('nNH').textContent=f(nh);$('nQ').textContent=f(q);
const mo=e?(q/e).toFixed(1).replace(/\\.0$/,''):'';$('nM').textContent=mo||'–';$('nR').textContent=a?Math.round(d/a*100)+'%':'–';
let t=n<0?`You owe ${f(-n)} more than you own. That is common in the first years of a big loan; what matters is that the number rises each month.`:`You own ${f(n)} more than you owe.`;
if(ha||hd)t+=` Leave out your home and its loan and it is ${f(nh)}: the part you could actually spend or invest.`;
if(e)t+=q/e<3?` The money you can reach quickly covers ${mo} months of expenses; a common rule of thumb is to keep 3 to 6 months.`:` The money you can reach quickly covers about ${mo} months of expenses.`;
$('nNote').textContent=t;try{const o={};ids.forEach(id=>o[id]=$(id).value);localStorage.setItem(K,JSON.stringify(o))}catch(e){}}
ids.forEach(id=>$(id).addEventListener('input',calc));$('nClr').addEventListener('click',ev=>{ev.preventDefault();ids.forEach(id=>$(id).value='');try{localStorage.removeItem(K)}catch(e){}calc()});calc()})();
</script>'''

def net_worth_calculator():
    path = '/net-worth-calculator'
    h1 = 'Net worth calculator in rupees'
    desc = 'Free net worth calculator for India: add savings, EPF, PPF, gold, property and loans in rupees. See net worth with and without your home. No sign-up.'
    faq = [('How do I calculate my net worth?', 'Add up everything you own at today’s value (bank balances, deposits, mutual funds and shares, EPF, PPF and NPS, gold, property, vehicles) and subtract everything you owe (home, car, personal and education loans, credit card dues and other borrowings). Net worth = total assets − total liabilities.'),
           ('Should I count the house I live in?', 'Both ways are used, which is why this calculator shows both. Your home is an asset, so the total includes it. But you can’t spend it without moving out, so the second figure leaves out the home and its loan. SEBI’s own net worth calculator lists real estate as “not the house you live in”.'),
           ('Do EPF, PPF and NPS count towards net worth?', 'Yes. They are your money, so they are part of your net worth. They are locked in for years, though, so this calculator does not count them as money you can reach in a few days.'),
           ('Can net worth be negative?', 'Yes. If your loans and card dues add up to more than what you own, net worth is negative. It is common just after taking an education loan or early in a home loan. The useful question is whether it rises month after month.'),
           ('How often should I check my net worth?', 'Once a month is enough for most people, on the same day each month, so that salary and EMI dates don’t distort the comparison.'),
           ('Is my data saved or shared?', 'The numbers are kept only in your own browser so they are still there when you come back. Nothing is sent to Self Streak and no sign-up is needed. Use “Clear the form” to remove them.')]
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Calculator</div>
<h1>{h1}</h1><p class="lead">Your net worth is everything you own minus everything you owe. Enter your savings, investments, gold, property and loans below to see it in rupees, with and without the home you live in, and how many months of expenses your ready money covers.</p>
{NW_CALC}<p class="short"><b>Net worth = total assets − total liabilities.</b> In the example filled in above, assets of ₹80,50,000 minus debts of ₹44,90,000 give a net worth of ₹35,60,000. Leave out the ₹60 lakh home and its ₹42 lakh loan and it is ₹17,60,000, of which ₹7,50,000 can be reached within a few days.</p>
<p class="upd">Free, no sign-up. Updated {bp.UPDATED}.</p></div></header>
<main class="wrap">
<section><h2>What to count as an asset</h2><p>Use today’s value, not what you paid.</p><ul class="list">
<li><b>Savings accounts and cash:</b> the balance today, plus cash at home and wallet balances.</li>
<li><b>Fixed and recurring deposits:</b> the amount deposited so far, plus interest already credited.</li>
<li><b>Mutual funds and shares:</b> the current value in your fund or demat statement, not the amount invested.</li>
<li><b>EPF, PPF and NPS:</b> the latest balance in your passbook or statement. Easy to forget because you never see this money, and often the largest financial asset a salaried person has.</li>
<li><b>Gold and jewellery:</b> the weight at today’s gold price. Leave out making charges; you don’t get them back on resale.</li>
<li><b>Property:</b> a realistic selling price today. The home you live in has its own box, so it can be shown separately.</li>
<li><b>Vehicles and other assets:</b> the resale value of a car or bike, and money others owe you that you really expect back.</li></ul>
<p>Leave out things that have no resale value to speak of (furniture, phones, clothes) and term insurance, which pays nothing while you are alive.</p></section>
<section><h2>What to count as a liability</h2><ul class="list">
<li><b>Loans:</b> the outstanding principal today, not the original loan amount and not EMI × months left (that includes future interest). Your lender’s app or loan statement shows it; the <a href="/emi-calculator">EMI calculator</a> can estimate it.</li>
<li><b>Credit cards and pay-later:</b> everything you owe right now, including spends that are not billed yet and any card EMIs.</li>
<li><b>Other borrowings:</b> gold loans, loans against an FD or a policy, and money borrowed from family or friends.</li></ul></section>
<section><h2>Three numbers, not one</h2><p>One net worth figure hides a lot when most of it is a house. This calculator shows three:</p>
<div class="tw"><table class="cmp"><thead><tr><th></th><th>What it counts</th><th>In the example</th></tr></thead><tbody>
<tr><td>Net worth</td><td>All assets minus all debts</td><td>₹35,60,000</td></tr>
<tr><td>Net worth without your home</td><td>The same, leaving out the home you live in and its home loan</td><td>₹17,60,000</td></tr>
<tr><td>Money you can reach in a few days</td><td>Savings, deposits, mutual funds and shares</td><td>₹7,50,000 (15 months of ₹50,000 expenses)</td></tr></tbody></table></div>
<p>The first tells you where you stand overall. The second is what you could spend or invest without selling the roof over your head; SEBI’s investor net worth calculator takes the same view and lists real estate as “not the house you live in” (as of {NW_AS_OF}). The third is your cushion if your income stops: EPF, PPF and NPS are locked in, and gold and property take time to sell.</p></section>
<section><h2>How to raise your net worth</h2><ul class="list">
<li><b>Clear the most expensive debt first.</b> Every rupee of principal repaid raises net worth by a rupee, and on a credit card it also stops interest of around 3–3.75% a month. See the <a href="/credit-card-interest-calculator">credit card interest calculator</a> and the <a href="/debt-payoff-planner">debt payoff planner</a>.</li>
<li><b>Save before you spend.</b> Decide the amount on payday; the <a href="/blog/50-30-20-budget-rule-india">50/30/20 budget calculator</a> gives a starting split.</li>
<li><b>Know where the month goes.</b> Net worth only rises if you spend less than you earn, and that takes an <a href="/expense-tracker">expense tracker</a> or the free <a href="/budget-template-india">monthly budget sheet</a>.</li>
<li><b>Check it monthly.</b> One reading means little. Twelve readings show the direction.</li></ul></section>
<section><h2>Track it every month without retyping</h2><p>This page gives you today’s number. Self Streak keeps it up to date: add your savings and investment accounts and your loans once, and the Overview screen shows your net worth, what you set aside this month and the month you’ll be debt-free, without retyping every box each month. It never asks for a bank login, card number or SMS access.</p></section>
{bp.shots_html('net-worth-calculator', 'Net worth in the Self Streak app')}
<section><h2>Questions</h2>{"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)}</section>
<section><h2>Sources</h2><ul class="list src"><li><a href="https://investor.sebi.gov.in/calculators/Networth_Calculator.html" rel="noopener" target="_blank">SEBI Investor: Net Worth Calculator (asset and liability heads; real estate listed as “not the house you live in”), checked {NW_AS_OF}</a></li></ul><p class="note">General information, not financial advice. The figures are only as accurate as the values you enter.</p></section>
{bp.FINAL}
<section><h2 style="font-size:20px">More free tools</h2><div class="more"><a href="/emi-calculator">EMI calculator</a><a href="/credit-card-interest-calculator">Credit card interest calculator</a><a href="/debt-snowball-spreadsheet">Debt snowball spreadsheet</a><a href="/budget-template-india">Budget template (Excel)</a><a href="/emi-tracker-template">EMI tracker Excel</a><a href="/expense-tracker">Expense tracker</a></div></section></main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": h1, "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "dateModified": bp.UPDATED, "inLanguage": "en-IN"},
             {"@type": "WebApplication", "name": "Net worth calculator (India, ₹)", "url": B + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "publisher": {"@id": B + "/#org"}},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    return path, bp.shell(path, 'Net Worth Calculator India (in Rupees) | Self Streak', desc,
                          'Net worth calculator in rupees · Self Streak', graph, [('Self Streak', '/'), ('Net worth calculator', path)], inner)

NW_CALC_LINK = ('/net-worth-calculator', 'Net worth calculator in rupees', 'Add what you own and what you owe: net worth with and without your home, and months of expenses covered.')

CC_CALC_LINK = ('/credit-card-interest-calculator', 'Credit card interest calculator', 'What paying only the minimum due costs in interest and GST, and how long it takes to clear.')

def link_from_tools():
    """Called before the tool pages render, so each one links to its comparison page."""
    for c in COMPARE:
        bp.GUIDES_FOR.setdefault(c['tool'], []).append(('/' + c['slug'], f"Self Streak vs {c['other']}", c['desc']))
    bp.GUIDES_FOR.setdefault('credit-card-bill-reminder', []).extend(
        (f'/credit-card-statement-date/{k["slug"]}', f'{k["name"]} credit card billing cycle and due date', f'Interest-free period, due date, grace days and changing the date, from {k["name"]}’s own terms.') for k in BANKS)
    for slug in ('credit-card-bill-reminder', 'debt-payoff-planner'):
        bp.GUIDES_FOR.setdefault(slug, []).insert(0, CC_CALC_LINK)
    bp.SHOTS_FOR['net-worth-calculator'] = ['overview', 'debt']
    for slug in ('expense-tracker', 'debt-payoff-planner', 'emi-calculator', 'health-and-finance-tracker', 'habit-and-money-tracker'):
        bp.GUIDES_FOR.setdefault(slug, []).append(NW_CALC_LINK)

def llms_lines():
    return [f'- [Credit card interest calculator]({B}/credit-card-interest-calculator): cost of paying only the minimum due on an Indian credit card, with interest and 18% GST.', f'- [Net worth calculator in rupees]({B}/net-worth-calculator): assets minus liabilities for Indian households (EPF, PPF, NPS, gold, property, loans), shown with and without the home you live in, plus months of expenses covered. No sign-up.', '', '## Card billing cycles by bank'] + [f"- [{k['name']} credit card billing cycle and due date]({B}/credit-card-statement-date/{k['slug']}): billing cycle, interest-free period and grace days from {k['name']}’s own terms." for k in BANKS] + ['', '## Comparisons'] + [f"- [Self Streak vs {c['other']}]({B}/{c['slug']}): {c['desc']}" for c in COMPARE]

def build():
    for c in COMPARE:
        path, page = compare_page(c); bp.write(path, page)
    path, page = cc_calculator(); bp.write(path, page)
    path, page = net_worth_calculator(); bp.write(path, page)
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
    title = f'{n} Credit Card Billing Cycle & Due Date | Self Streak'
    if len(title) > 60: title = f'{n} Card Billing Cycle & Due Date | Self Streak'
    h1 = f'{n} credit card billing cycle, statement date and due date'
    change = next(f for f in k['facts'] if 'chang' in f)
    grace = next((f for f in k['facts'] if 'grace' in f), None)
    desc = f'{n} credit card billing cycle explained from its official terms: interest-free period of {k["free"].split(",")[0]}, when the bill is due, grace days and changing the date.'
    if len(desc) > 160: desc = f'{n} credit card billing cycle from its official terms: interest-free period, when the bill is due, grace days and how to change the date.'
    faq = [(f'What is the interest-free period on a {n} credit card?', f'{k["free"][0].upper() + k["free"][1:]}, according to {n}’s own terms, as long as you pay the full previous bill and don’t withdraw cash.'),
           (f'When is my {n} credit card bill generated?', f'On your statement date (also called the billing date or bill generation date), once a month. The bill covers every transaction since the previous statement date. It is printed on each {n} statement, and the payment due date comes after it.'),
           (f'Can I change my {n} credit card billing cycle?', change),
           *([(f'Is there a grace period after the {n} credit card due date?', grace)] if grace else []),
           ('Do I need my card number to track this in Self Streak?', 'No. Add the card’s limit, statement day and due day, and Self Streak tracks this bill and next bill and reminds you before each due date.')]
    others = ''.join(f'<a href="/credit-card-statement-date/{o["slug"]}">{html.escape(o["name"])}</a>' for o in BANKS if o is not k)
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">Credit cards</div>
<h1>{html.escape(h1)}</h1>
<p class="lead">Your {html.escape(n)} credit card billing cycle is the month between two statement dates. The bill is generated on the statement date, and you pay it by the due date printed on that statement. Below is how {html.escape(n)}’s own most important terms and conditions (MITC) set the interest-free period, grace days and the rules for changing your cycle.</p>
<p class="short"><b>Short answer:</b> On {html.escape(n)} cards the interest-free period is {html.escape(k["free"])}. Pay the <b>total amount due</b> by the due date on your statement and you pay no interest. Your exact dates are printed on each statement.</p>
<p class="upd">Checked against {html.escape(n)}’s published terms on {AS_OF}. Terms differ by card; your card’s MITC wins. Updated {bp.UPDATED}.</p></div></header>
<main class="wrap">
<section><h2>What {html.escape(n)}’s terms say</h2><ul class="list">{"".join(f"<li>{html.escape(f)}</li>" for f in k["facts"])}</ul></section>
<section><h2>How to change your {html.escape(n)} billing cycle</h2><p>{html.escape(change)}</p>
<p>RBI’s credit card rules require every card issuer to give cardholders at least a one-time option to change the billing cycle to suit them. Choose a statement date whose due date falls a few days after your salary arrives, so the money is in your account when the bill is due.</p></section>
<section><h2>What this means for you</h2><ul class="list"><li>Make big planned purchases just after your statement date to get the longest time to pay.</li>
<li>Pay a few working days before the due date, so the money reaches the card account in time.</li>
<li>Paying only the minimum keeps the account in good standing but costs a lot of interest; see the <a href="/credit-card-interest-calculator">credit card interest calculator</a>.</li>
<li>Have more than one card? The free <a href="/credit-card-tracker-template">credit card tracker Excel sheet</a> shows every card’s due date and how many interest-free days a purchase today gets.</li>
<li>For how the dates work on any card, read <a href="/blog/credit-card-statement-date-vs-due-date">statement date vs due date</a> (<a href="/hi/blog/credit-card-statement-date-vs-due-date" lang="hi" hreflang="hi-IN">हिंदी में</a>).</li></ul></section>
{bp.shots_html('credit-card-bill-reminder', 'Track every card in Self Streak')}
<section><h2>Questions</h2>{"".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)}</section>
<section><h2>Sources</h2><ul class="list src">{"".join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a></li>' for t, u in k["sources"])}<li><a href="https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12300" rel="noopener" target="_blank">RBI, Master Direction – Credit Card and Debit Card – Issuance and Conduct Directions, 2022</a></li></ul>
<p class="note">Self Streak is not affiliated with {html.escape(n)}. This page summarises the bank’s published terms and is not financial advice. If something is out of date, <a href="/contact">tell us</a>.</p></section>
{bp.FINAL}
<section><h2 style="font-size:20px">Other banks</h2><div class="more">{others}<a href="/credit-card-bill-reminder">Credit card bill reminder</a></div></section></main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": h1, "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "dateModified": bp.UPDATED, "inLanguage": "en-IN"},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    return path, bp.shell(path, title, desc, h1, graph,
                          [('Self Streak', '/'), ('Credit card bills', '/credit-card-bill-reminder'), (n, path)], inner)

def build_banks():
    for k in BANKS:
        path, page = bank_page(k); bp.write(path, page)
