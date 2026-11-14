#!/usr/bin/env python3
"""Builds the SEO feature pages in public/ from one template. Run: python3 scripts/build-pages.py"""
import json, html, os

B = 'https://selfstreak.com'
OUT = os.path.join(os.path.dirname(__file__), '..', 'public')
LOGO = '<svg viewBox="0 0 100 100" aria-hidden="true"><rect width="100" height="100" rx="26" fill="#d7f64a"/><path d="M68 31c-3-9-11-14-21-14-12 0-20 7-20 16 0 21 47 13 47 35 0 10-9 17-22 17-11 0-20-5-24-14" fill="none" stroke="#10120a" stroke-width="12" stroke-linecap="round"/><circle cx="77" cy="23" r="7" fill="#10120a"/></svg>'

CSS = """
:root{--bg:#09090b;--card:#141418;--card2:#1b1b20;--line:#26262c;--line2:#34343c;--text:#f4f4f5;--muted:#a1a1aa;--faint:#71717a;--lime:#d7f64a;--ink:#10120a;--cyan:#45dfe6;--red:#ff4f6e}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Plus Jakarta Sans',system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:var(--lime)}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
nav{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 85%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line);padding-top:env(safe-area-inset-top)}
nav .wrap{display:flex;align-items:center;gap:14px;height:64px;max-width:1100px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:700;font-size:17px}.brand svg{width:30px;height:30px}
nav .sp{flex:1}nav .lg{color:var(--muted);text-decoration:none;font-weight:600;font-size:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:46px;padding:0 22px;border-radius:999px;font-weight:700;font-size:15px;text-decoration:none;border:1px solid var(--line2);background:var(--card);color:var(--text);cursor:pointer;font-family:inherit}
.btn.lime{background:var(--lime);color:var(--ink);border-color:transparent}.btn.sm{height:38px;font-size:13.5px;padding:0 16px}
header{padding:56px 0 30px;background:radial-gradient(600px 300px at 10% 0%,color-mix(in srgb,var(--lime) 13%,transparent),transparent 70%)}
.crumb{font-size:13px;color:var(--faint);margin-bottom:14px}.crumb a{color:var(--muted);text-decoration:none}
.kick{color:var(--lime);font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase}
h1{font-size:clamp(32px,5vw,50px);line-height:1.08;letter-spacing:-.03em;margin:10px 0 16px;font-weight:800}
.lead{font-size:18px;color:var(--muted);max-width:680px}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
main section{padding:30px 0;border-top:1px solid var(--line)}
h2{font-size:clamp(22px,3vw,30px);letter-spacing:-.02em;line-height:1.2;margin-bottom:12px}
h3{font-size:18px;margin:18px 0 6px}
p,li{color:#d4d4d8;font-size:16px}p+p{margin-top:12px}
ul.list{padding-left:20px;display:grid;gap:8px;margin-top:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr));gap:12px;margin-top:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px}
.card b{display:block;font-size:16px;margin-bottom:4px}.card p{font-size:14.5px;color:var(--muted)}
.calc{background:linear-gradient(180deg,color-mix(in srgb,var(--lime) 7%,var(--card)),var(--card));border:1px solid color-mix(in srgb,var(--lime) 30%,var(--line));border-radius:22px;padding:22px;margin-top:16px}
.fields{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(180px,100%),1fr));gap:12px}
label{display:grid;gap:6px;font-size:13px;color:var(--muted);font-weight:600}
input,select{height:46px;border-radius:12px;border:1px solid var(--line2);background:var(--card2);color:var(--text);padding:0 14px;font:inherit;font-size:16px;width:100%}
.out{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(170px,100%),1fr));gap:10px;margin-top:16px}
.out div{background:var(--card2);border:1px solid var(--line);border-radius:14px;padding:12px 14px}.out small{display:block;color:var(--muted);font-size:12px}.out b{font-size:22px;letter-spacing:-.01em}
.note{font-size:13px;color:var(--faint);margin-top:12px}
details{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:0 18px;margin-top:10px}
summary{cursor:pointer;padding:16px 0;font-weight:600;list-style:none}summary::-webkit-details-marker{display:none}
details p{padding-bottom:16px;color:var(--muted)}
.final{margin:30px 0 10px;border-radius:24px;padding:34px 22px;text-align:center;background:radial-gradient(400px 200px at 50% 0%,color-mix(in srgb,var(--lime) 18%,transparent),transparent 70%),var(--card);border:1px solid var(--line)}
.final p{color:var(--muted);margin:8px auto 18px;max-width:520px}
.more{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.more a{border:1px solid var(--line2);border-radius:999px;padding:8px 14px;text-decoration:none;color:var(--text);font-size:14px;background:var(--card)}
footer{border-top:1px solid var(--line);margin-top:30px;padding:24px 0 40px;color:var(--faint);font-size:14px}
footer .wrap{display:flex;gap:16px;flex-wrap:wrap}footer a{color:var(--muted);text-decoration:none}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:12px}th,td{text-align:right;padding:8px 6px;border-bottom:1px solid var(--line)}th:first-child,td:first-child{text-align:left}th{color:var(--muted);font-weight:600}
"""

PAGES = []
def page(**k): PAGES.append(k)

page(slug='credit-card-bill-reminder', nav='Credit card bills',
  title='Credit Card Bill Reminder App India | Self Streak',
  desc='Track every credit card bill: this bill, next bill, minimum due and limit left. Get a reminder 2 days before each due date. Free for 7 days.', short='A credit card bill reminder app tells you how much is due and when, before the due date. Self Streak tracks each card’s statement date, due date, minimum due and limit, splits spends into this bill and next bill like your bank does, and reminds you 2 days before payment is due.',
  kick='Credit cards & pay later', h1='A credit card bill reminder that understands billing cycles',
  lead='Self Streak tracks each card like your bank does: spends before the statement date go on this bill, spends after it roll to the next one. You see the amount due, the minimum due and your available limit, and you get a reminder before every due date.',
  body='''
<section><h2>Why a normal reminder isn’t enough</h2>
<p>A calendar alert tells you a date. It doesn’t tell you <b>how much</b> is due, what the <b>minimum</b> is, or what you’ve already spent on the <b>next</b> bill. That’s how people end up paying only the minimum and carrying interest of around 3–3.75% a month, or missing a due date because two cards are due in the same week.</p>
<p>Self Streak keeps the numbers next to the date, so the reminder actually helps you decide what to pay.</p></section>
<section><h2>What you get</h2><div class="grid">
<div class="card"><b>This bill and next bill</b><p>Spends up to your statement date go on this bill; anything after rolls to the next one, exactly like your card.</p></div>
<div class="card"><b>Minimum due and full amount</b><p>Pay full, pay the minimum or any amount. Partial payments carry forward with an interest estimate.</p></div>
<div class="card"><b>Limit used</b><p>See how much of your limit is used and what’s available before you swipe again.</p></div>
<div class="card"><b>Reminders that stop when paid</b><p>A push notification 2 days before and on the due date. Mark it paid and the reminders stop.</p></div>
<div class="card"><b>Pay later too</b><p>Works for postpaid wallets and BNPL accounts that need the full bill every month.</p></div>
<div class="card"><b>Snap the statement</b><p>Take a photo of a bill or statement and the AI reads the amount and due date for you.</p></div></div></section>
<section><h2>How it works</h2><ol class="list">
<li>Add a card with its limit, statement day, due day and minimum %.</li>
<li>Log spends as you go, by typing or saying “spent 1,200 on Amazon on my HDFC card”.</li>
<li>Get reminded before each due date, and pay full or minimum in one tap.</li></ol></section>''',
  faq=[('Is my card number needed?','No. Self Streak never asks for card numbers, CVV or bank logins. You only enter the limit, statement day and due day.'),
       ('Does it work with pay-later and postpaid accounts?','Yes. Set the minimum due to 100% and it tracks them as “pay the full bill every month”.'),
       ('Will I get a notification on my phone?','Yes. Install Self Streak on your home screen and turn on notifications to get push reminders, even when the app is closed.'),
       ('What does it cost?','Every feature is free for 7 days, no card needed. Bill reminders are part of Self Streak Plus at ₹199 a month. If you don’t upgrade, you move to the free plan: you keep your data, and habits, water, expenses and your streak keep working.')])

page(slug='emi-calculator', nav='EMI calculator',
  title='EMI Calculator India: Loan EMI & Prepayment | Self Streak',
  desc='Free EMI calculator for home, car, personal and education loans. See your EMI, total interest and how much a monthly prepayment saves.', short='An EMI calculator works out the fixed monthly instalment on a loan from three inputs: loan amount, yearly interest rate and tenure. For example, ₹5 lakh at 12% for 5 years is an EMI of about ₹11,122, with roughly ₹1.67 lakh paid as interest. Paying a little extra each month cuts both.',
  kick='Loans & EMIs', h1='EMI calculator and loan tracker',
  lead='Work out your monthly EMI, the total interest you’ll pay, and how much time and interest a small extra payment each month can save. Then track all your loans and EMIs in one place.',
  calc='''<div class="calc" id="emi"><div class="fields">
<label>Loan amount (₹)<input id="eP" type="number" inputmode="numeric" value="500000" min="1000"></label>
<label>Interest rate (% a year)<input id="eR" type="number" inputmode="decimal" value="12" step="0.1" min="0"></label>
<label>Tenure (months)<input id="eN" type="number" inputmode="numeric" value="60" min="1"></label>
<label>Extra payment each month (₹)<input id="eX" type="number" inputmode="numeric" value="2000" min="0"></label></div>
<div class="out"><div><small>Monthly EMI</small><b id="oE">–</b></div><div><small>Total interest</small><b id="oI">–</b></div><div><small>Total paid</small><b id="oT">–</b></div><div><small>With the extra payment</small><b id="oS">–</b></div></div>
<p class="note" id="oNote"></p></div>
<script>
const f=n=>'₹'+Math.round(n).toLocaleString('en-IN');
function emiCalc(){const P=+eP.value||0,r=(+eR.value||0)/1200,n=Math.max(1,+eN.value||1),x=+eX.value||0;
const E=r?P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):P/n;oE.textContent=f(E);oI.textContent=f(E*n-P);oT.textContent=f(E*n);
let b=P,m=0,int=0;while(b>0.5&&m<1200){const i=b*r;int+=i;b=b+i-Math.min(E+x,b+i);m++}
const saved=(E*n-P)-int;oS.textContent=x>0?`${n-m} months sooner`:'–';oNote.textContent=x>0?`Paying ${f(x)} extra every month closes the loan in ${m} months instead of ${n} and saves about ${f(saved)} in interest.`:'Add an extra monthly amount to see how much interest a prepayment saves.'}
['eP','eR','eN','eX'].forEach(id=>document.getElementById(id).addEventListener('input',emiCalc));emiCalc();
</script>''',
  body='''
<section><h2>How EMI is calculated</h2>
<p>EMI = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1), where P is the loan amount, r is the monthly interest rate (yearly rate ÷ 12 ÷ 100) and n is the number of months. In the early months most of the EMI goes to interest; later, more of it repays the principal.</p>
<p>That’s why even a small extra payment each month makes a big difference. It reduces the principal directly, so every following month charges less interest.</p></section>
<section><h2>Track every loan, not just one</h2><div class="grid">
<div class="card"><b>All EMIs in one view</b><p>Home, personal, car, education, gold or family loans: outstanding, EMI, rate and months left.</p></div>
<div class="card"><b>Due-date reminders</b><p>A reminder 2 days before each EMI. Mark it paid and the outstanding updates.</p></div>
<div class="card"><b>Debt-free date</b><p>See the month you’ll be debt-free, and how avalanche or snowball payoff changes it.</p></div>
<div class="card"><b>AI repayment plan</b><p>Get a month-by-month plan built on your actual income, budget and loans.</p></div></div></section>''',
  faq=[('Is this EMI calculator free?','Yes, the calculator on this page is free to use. Tracking your loans with reminders is part of Self Streak (7 days free, then ₹199/month).'),
       ('Does prepaying a loan always save money?','Prepaying reduces interest, but some fixed-rate loans charge a prepayment fee. As per RBI rules, floating-rate loans to individuals have no foreclosure or prepayment charges. Check your loan agreement.'),
       ('Should I prepay my loan or invest?','A common rule: clear high-interest debt (credit cards, personal loans) first, and keep an emergency fund. Self Streak’s AI plan weighs this against your own numbers.')])

page(slug='water-reminder', nav='Water reminder',
  title='Water Reminder App & Daily Intake Calculator | Self Streak',
  desc='Work out how much water you need a day, then get drink-water reminders that adapt to what you have already logged. Tap a glass to log it.', short='Most adults need about 2 to 2.5 litres of water a day from drinks, more in hot weather or after exercise. A simple guide is around 33 ml per kg of body weight. Self Streak’s water reminder tracks the glasses you log and only nudges you when you are behind for the time of day.',
  kick='Health · Water', h1='A water reminder that knows how much you’ve had',
  lead='Most water reminders ping you on a timer, even when you’ve just had a glass. Self Streak tracks your glasses and only reminds you when you’re behind for the time of day.',
  calc='''<div class="calc" id="wc"><div class="fields">
<label>Your weight (kg)<input id="wW" type="number" inputmode="decimal" value="70" min="20"></label>
<label>Exercise today (minutes)<input id="wE" type="number" inputmode="numeric" value="30" min="0"></label>
<label>Weather<select id="wH"><option value="0">Normal</option><option value="500" selected>Hot / humid</option></select></label></div>
<div class="out"><div><small>Water a day (rough guide)</small><b id="wL">–</b></div><div><small>In 250 ml glasses</small><b id="wG">–</b></div><div><small>One glass about every</small><b id="wI">–</b></div></div>
<p class="note">A simple guide (about 33 ml per kg, plus extra for exercise and heat). Needs differ with health conditions and diet, so follow your doctor’s advice if you have one.</p></div>
<script>
function wCalc(){const w=+wW.value||0,e=+wE.value||0,h=+wH.value||0,ml=w*33+e*12+h,g=Math.round(ml/250);wL.textContent=(ml/1000).toFixed(1)+' L';wG.textContent=g+' glasses';wI.textContent=g?Math.round(15*60/g)+' min':'–'}
['wW','wE','wH'].forEach(id=>document.getElementById(id).addEventListener('input',wCalc));wCalc();
</script>''',
  body='''
<section><h2>Smarter than a timer</h2><div class="grid">
<div class="card"><b>Adapts to what you’ve logged</b><p>Had 3 glasses already? The next reminder waits. Behind for the day? It nudges you sooner.</p></div>
<div class="card"><b>Tap a glass</b><p>Twelve glasses on screen; tap one and it fills with a little splash. Or just say “drank 2 glasses”.</p></div>
<div class="card"><b>Quiet hours</b><p>No reminders while you sleep. Set your own wake and sleep times.</p></div>
<div class="card"><b>Part of your health score</b><p>Water, steps, sleep and habits add up to one daily score and streak.</p></div></div></section>
<section><h2>Tips that actually help</h2><ul class="list">
<li>Start the day with a glass before tea or coffee.</li>
<li>Keep a bottle on your desk; seeing it is half the battle.</li>
<li>Drink a glass with every meal, and one after any workout.</li>
<li>In Indian summers, add coconut water or nimbu paani for electrolytes.</li></ul></section>''',
  faq=[('How much water should I drink a day?','A common guide is roughly 30–35 ml per kg of body weight, more if you exercise or it’s hot. For a 70 kg adult that’s about 2.3–2.5 litres, or 9–10 glasses. Your doctor’s advice comes first.'),
       ('Will the reminders work when the app is closed?','Yes. Add Self Streak to your home screen and turn on notifications to get push reminders on iPhone and Android.'),
       ('Can I log water by voice?','Yes. Say or type “drank 2 glasses” or “1 litre of water” and it’s logged.')])

page(slug='habit-tracker', nav='Habit tracker',
  title='Habit Tracker App with Streaks & Reminders | Self Streak',
  desc='Track daily, weekly and monthly habits with streaks, reminders on time, and goals that count themselves. Free plan, plus a 7-day free trial of everything.', short='A habit tracker is an app where you tick off habits each day and see your streak grow. Research from University College London found new habits took a median of 66 days to become automatic. Self Streak reminds you at the time each habit happens and keeps your streak and goals counting.',
  kick='Habits & streaks', h1='A habit tracker that keeps your streak going',
  lead='Track daily, weekly and monthly habits, get a reminder at the time each habit happens, and watch your streak grow. Goals like “10,000 steps on 300 days” count themselves every time you tick the habit.',
  body='''
<section><h2>Built for real days</h2><div class="grid">
<div class="card"><b>Reminders at the right time</b><p>Gym at 6:30 pm, sunscreen at 7:30 am, reading at 9:45 pm. Each habit reminds you at its own time, and skips if it’s already done.</p></div>
<div class="card"><b>Streaks and a daily score</b><p>See your streak for each habit and one health score for the day.</p></div>
<div class="card"><b>Goals that count themselves</b><p>“Gym 200 days this year” counts every day you tick Gym. No manual updates.</p></div>
<div class="card"><b>Log by voice</b><p>Say “did gym, 10k steps, slept 7 hours” and three things are logged at once.</p></div>
<div class="card"><b>Today view</b><p>What you missed, what’s up next and what’s done, on one screen.</p></div>
<div class="card"><b>AI day summary</b><p>Each evening, see what went well, what you missed and a plan for tomorrow.</p></div></div></section>
<section><h2>Habits people track with Self Streak</h2><ul class="list">
<li>10,000 steps, gym or a workout, morning sunlight</li><li>Water, protein target, fruits and vegetables</li>
<li>Reading, journaling, no screens before bed</li><li>Skincare, sunscreen, haircut every 4 weeks</li><li>Weekly: meal prep, review spending, call family</li></ul></section>''',
  faq=[('Is there a free habit tracker plan?','Yes. Every feature is free for 7 days, no card needed. After that, habits, streaks, water and expenses stay free. Plus (₹199 a month) adds reminders at each habit’s time, voice and photo logging, the AI day summary and leagues.'),
       ('Can I track weekly and monthly habits?','Yes. Habits can be daily, weekly, monthly, quarterly or yearly, each with their own reminder.'),
       ('Does it work offline?','Yes. Ticking habits works offline and syncs when you’re back online.')])

page(slug='expense-tracker', nav='Expense tracker',
  title='Expense Tracker App India: Budget & Bills | Self Streak',
  desc='Track spending in rupees by voice, photo or bank statement. Set monthly budgets and get reminders for bills and EMIs. No bank login needed.', short='An expense tracker records where your money goes so you can stick to a budget. Self Streak logs spends in rupees three ways: say it (“450 on Swiggy”), snap a receipt, or import a bank statement PDF or Excel file. It never asks for your bank login.',
  kick='Money · Spending', h1='An expense tracker that fills itself in',
  lead='Say “spent 450 on Zomato”, snap a receipt, or upload your bank statement, and Self Streak sorts every payment into your budget. No bank login, no manual spreadsheets.',
  body='''
<section><h2>Three ways to log, all fast</h2><div class="grid">
<div class="card"><b>Say it</b><p>“Paid rent 12,000”, “450 on Swiggy”, “petrol 1,500”. It understands English, Hindi and Hinglish.</p></div>
<div class="card"><b>Snap it</b><p>Photo of a receipt or bill: the AI reads the amount, shop and date and logs it once.</p></div>
<div class="card"><b>Import a statement</b><p>Upload your bank statement PDF and every payment is categorised. Your login is never needed.</p></div></div></section>
<section><h2>See where the month went</h2><ul class="list">
<li>Monthly budget by category, with a warning when one is running over.</li>
<li>Bills, EMIs and spending together, so “saved this month” is real.</li>
<li>Year summary from the month you started tracking.</li>
<li>Export to CSV any time.</li></ul></section>''',
  faq=[('Do I need to connect my bank account?','No. Self Streak never asks for bank logins. You can upload a statement PDF or photo instead, and it reads the payments.'),
       ('Does it work with UPI payments?','Yes. Log UPI spends by voice or text, or import them from your bank statement.'),
       ('Is my financial data private?','Your data is stored in your own account, never sold or used for ads, and you can export or delete it any time.'),
       ('Is the expense tracker free?','Yes. Logging expenses, budgets and your streak are on the free plan. Every feature is free for 7 days, no card needed; voice and photo logging, statement import and bill reminders are part of Plus at ₹199 a month.')])

page(slug='debt-payoff-planner', nav='Debt payoff planner',
  title='Debt Payoff Planner: Avalanche vs Snowball | Self Streak',
  desc='Plan how to repay credit cards, personal loans and EMIs on your income. Compare avalanche and snowball and see your debt-free date.', short='A debt payoff planner shows the order to repay your debts and the month you will be debt-free. The avalanche method pays extra on the highest-interest debt first and saves the most interest; the snowball method clears the smallest balance first for quick wins. Self Streak compares both on your real numbers.',
  kick='Get debt-free', h1='A debt payoff planner built on your real income',
  lead='Add your loans, cards and salary. Self Streak shows your debt-free date, compares avalanche and snowball, and makes a month-by-month plan that never skips an EMI or your essentials.',
  body='''
<section><h2>Avalanche or snowball?</h2>
<p><b>Avalanche</b> pays extra on the highest-interest debt first (usually credit cards at 36–45% a year), which saves the most money. <b>Snowball</b> clears the smallest balance first, which gives quick wins and keeps you motivated. Self Streak shows both and how many months and how much interest each saves.</p></section>
<section><h2>What the AI plan gives you</h2><div class="grid">
<div class="card"><b>Free money each month</b><p>What’s left after rent, food, bills and EMIs, and how much of it to put towards debt.</p></div>
<div class="card"><b>Payoff order</b><p>Which debt to clear first, why, and the month each one will be gone.</p></div>
<div class="card"><b>Where the extra comes from</b><p>Specific cuts in your own budget categories, with amounts.</p></div>
<div class="card"><b>Honest warnings</b><p>If EMIs take too much of your income, it says so and suggests talking to your lender, not more borrowing.</p></div></div></section>''',
  faq=[('Is the AI plan financial advice?','No. It’s a planning tool based on the numbers you enter. For big decisions, talk to your lender or a registered adviser.'),
       ('Can it handle credit cards with minimum due?','Yes. Cards and pay-later accounts are tracked with statement dates, minimum due and interest, and included in the plan.'),
       ('What if my EMIs are more than my income?','The plan will tell you plainly and suggest options like restructuring, extending tenure or consolidating high-interest debt.')])

page(slug='calorie-protein-tracker', nav='Calorie & protein tracker',
  title='Calorie & Protein Tracker for Indian Food | Self Streak',
  desc='Snap a photo of dal chawal, roti sabzi or dosa and get calories and protein in seconds. Track your daily protein target. Free for 7 days.', short='A calorie and protein tracker estimates what you eat each day against a target. ICMR-NIN’s 2020 guidelines put the protein requirement for healthy Indian adults at about 0.83 g per kg of body weight a day. Self Streak estimates calories and protein from a photo or description of Indian meals.',
  kick='Food & protein', h1='Track calories and protein from a photo of your plate',
  lead='Snap your meal or just type “2 rotis, dal and paneer sabzi”. Self Streak estimates calories, protein, carbs and fat for Indian portions, tracks your daily protein target, and tells you what was missing at the end of the day.',
  calc='''<div class="calc" id="pc"><div class="fields">
<label>Your weight (kg)<input id="pW" type="number" inputmode="decimal" value="70" min="20"></label>
<label>Activity<select id="pA"><option value="1.0">Mostly sitting</option><option value="1.2">Light exercise</option><option value="1.6" selected>Gym 3–5 days a week</option><option value="2.0">Heavy training</option></select></label></div>
<div class="out"><div><small>Daily protein (guide)</small><b id="pG">–</b></div><div><small>Per meal (3 meals)</small><b id="pM">–</b></div></div>
<p class="note">A general guide (about 1.0–2.0 g per kg depending on activity). People with kidney conditions or other health issues should follow their doctor’s advice.</p></div>
<script>
function pCalc(){const w=+pW.value||0,a=+pA.value||1,g=Math.round(w*a);pG.textContent=g+' g';pM.textContent=Math.round(g/3)+' g'}
['pW','pA'].forEach(id=>document.getElementById(id).addEventListener('input',pCalc));pCalc();
</script>''',
  body='''
<section><h2>Made for Indian food</h2><div class="grid">
<div class="card"><b>Snap a photo</b><p>Thali, poha, biryani, dosa, paneer roll: the AI identifies items and realistic portions.</p></div>
<div class="card"><b>Or describe it</b><p>“2 eggs and toast”, “dal chawal and salad” in English, Hindi or Hinglish.</p></div>
<div class="card"><b>Protein target</b><p>See protein and calories against your target through the day.</p></div>
<div class="card"><b>Daily food check</b><p>The evening summary flags oily or sugary meals, low fibre, and nutrients you likely missed, with Indian foods to fix them.</p></div></div></section>
<section><h2>Easy protein for Indian diets</h2><ul class="list">
<li>Paneer (about 18 g per 100 g), curd and dahi, milk</li><li>Dal, rajma, chole, sprouts, soya chunks</li>
<li>Eggs, chicken, fish</li><li>Peanuts, roasted chana, seeds</li></ul></section>''',
  faq=[('How accurate is the photo calorie estimate?','It’s an estimate based on the dish and a typical portion. You can edit the numbers before logging. Describing quantities (“2 rotis, 1 katori dal”) makes it more accurate.'),
       ('Does it track micronutrients?','The daily summary points out nutrients your meals were likely low in, such as fibre, calcium, iron or magnesium, based on what you ate. It’s guidance, not a lab test.'),
       ('Is it free?','Every feature is free for 7 days, no card needed. Photo calorie scans are part of Self Streak Plus at ₹199 a month. After the trial, the free plan keeps habits, water, expenses and your streak.')])

ALL = [(p['slug'], p['nav']) for p in PAGES]
UPDATED = '@@MODIFIED@@'   # replaced per page in write() with the date its content last changed (see page-dates.json)
TODAY = __import__('datetime').date.today().isoformat()
ORG = {"@type": "Organization", "@id": B + "/#org", "name": "Self Streak", "url": B + "/",
       "logo": {"@type": "ImageObject", "url": B + "/icon-512.png", "width": 512, "height": 512},
       "email": "adityaps700@gmail.com", "areaServed": "IN",
       "address": {"@type": "PostalAddress", "addressLocality": "Lucknow", "addressRegion": "Uttar Pradesh", "addressCountry": "IN"},
       "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": "adityaps700@gmail.com", "url": B + "/contact", "availableLanguage": ["en", "hi"]},
       "sameAs": ["https://instagram.com/selfstreak"],
       "founder": {"@id": B + "/about#aditya"},
       "knowsAbout": ["habit tracking", "personal budgeting", "expense tracking", "EMI and loan management", "credit card bill management", "debt repayment", "water intake", "protein intake for Indian diets"]}
SITE = {"@type": "WebSite", "@id": B + "/#website", "name": "Self Streak", "url": B + "/", "inLanguage": "en-IN", "publisher": {"@id": B + "/#org"}}
EXTRA_CSS = """
.short{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--lime);border-radius:14px;padding:16px 18px;margin-top:22px;color:#e4e4e7;font-size:16.5px}
.upd{font-size:13px;color:var(--faint);margin-top:14px}
.guides{display:grid;gap:10px;margin-top:12px}.guides a{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-decoration:none;color:var(--text);font-weight:600}
.guides a span{display:block;color:var(--muted);font-weight:400;font-size:14px;margin-top:2px}
article p,article li{font-size:17px}article h2{margin-top:8px}article section{padding:26px 0}
.byline{font-size:14px;color:var(--muted);margin-top:14px}
.src{font-size:14px;color:var(--muted)}.src li{font-size:14px;color:var(--muted)}
.tw{overflow-x:auto}
.cmp td:first-child{font-weight:600;color:var(--text)}.cmp th:nth-child(3),.cmp td:nth-child(3){background:color-mix(in srgb,var(--lime) 6%,transparent)}
.brand,nav .lg,nav .btn{white-space:nowrap}nav .wrap{gap:12px}
@media (max-width:440px){nav .lg.gd{display:none}nav .btn.sm{padding:0 13px}}
"""
FOOT = '<footer><div class="wrap"><span>© 2026 Self Streak</span><a href="/">Home</a><a href="/blog">Guides</a><a href="/emi-calculator">EMI calculator</a><a href="/about">About</a><a href="/contact">Contact</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a><a href="/refunds">Refunds</a><a href="/shipping">Shipping</a></div></footer>'
BEACON = "<script>try{if(!/bot|crawl|spider/i.test(navigator.userAgent))navigator.sendBeacon('/api/hit',new Blob([JSON.stringify({p:location.pathname,r:document.referrer})],{type:'application/json'}))}catch(e){}</script>"

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": B + u} for i, (n, u) in enumerate(items)]}

def og_for(path):
    """Per-page share image if scripts/build-og.py made one, else the site default."""
    name = path.strip('/').replace('/', '-') or 'home'
    return f'{B}/og/{name}.jpg' if os.path.exists(os.path.join(OUT, 'og', name + '.jpg')) else f'{B}/og-image.png'

# Pages that exist in more than one language: every version lists all of them (hreflang), English is x-default.
ALTERNATES = {'/emi-calculator': {'en-IN': '/emi-calculator', 'hi-IN': '/hi/emi-calculator'},
              '/blog/credit-card-statement-date-vs-due-date': {'en-IN': '/blog/credit-card-statement-date-vs-due-date', 'hi-IN': '/hi/blog/credit-card-statement-date-vs-due-date'}}
ALTERNATES.update({v['hi-IN']: v for v in list(ALTERNATES.values())})
NAV_TEXT = {'en-IN': ('Guides', 'Log in', 'Start free trial'), 'hi-IN': ('गाइड', 'लॉग इन', 'फ़्री ट्रायल शुरू करें')}

def shell(path, title, desc, og_title, graph, crumbs, inner, og_type='website', head_extra='', robots='index, follow, max-image-preview:large, max-snippet:-1', lang='en-IN'):
    url = B + path
    alt = ALTERNATES.get(path)
    if alt:
        head_extra += ''.join(f'<link rel="alternate" hreflang="{l}" href="{B}{u}">' for l, u in alt.items()) + f'<link rel="alternate" hreflang="x-default" href="{B}{alt["en-IN"]}">\n'
    g_txt, l_txt, s_txt = NAV_TEXT[lang]
    hi_link = f' · <a href="{alt["hi-IN"]}" hreflang="hi-IN" lang="hi">हिंदी में पढ़ें</a>' if alt and lang == 'en-IN' else ''
    og = og_for(path)
    assert len(title) <= 60, (path, len(title), title)
    assert 110 <= len(desc) <= 160, (path, len(desc), desc)
    ld = {"@context": "https://schema.org", "@graph": [ORG, SITE, crumbs_ld(crumbs)] + graph}
    crumb_html = ' › '.join([f'<a href="{u}">{html.escape(n)}</a>' for n, u in crumbs[:-1]] + [html.escape(crumbs[-1][0])])
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#09090b">
<link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Self Streak"><meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(og_title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="{lang.replace('-', '_')}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(og_title[:70])}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{og}">
{head_extra}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}{EXTRA_CSS}{SHOT_CSS}</style></head><body>
<nav><div class="wrap"><a class="brand" href="/">{LOGO}Self Streak</a><span class="sp"></span><a class="lg gd" href="/blog">{g_txt}</a><a class="lg" href="/app">{l_txt}</a><a class="btn lime sm" href="/app#signup">{s_txt}</a></div></nav>
<div class="wrap" style="padding-top:18px"><div class="crumb">{crumb_html}{hi_link}</div></div>
{inner}
{FOOT}
{BEACON}
</body></html>"""

# Real app screenshots (made by scripts/app-screenshots.py from a local demo account). 780x1688 files shown at 390x844.
SHOT_ALT = {
    'overview': 'Self Streak overview screen: net worth of ₹1,78,000, income ₹65,000 and spending ₹42,079 this month, with a 6-month chart',
    'today': 'Self Streak Today screen: a 22-day streak, daily quests and counts of habits done, missed and up next',
    'health': 'Self Streak Health screen: health score dial built from steps, sleep and daily habits, plus a water tracker with glasses',
    'meals': 'Self Streak Food today card: protein 43 of 104 g and calories 1,020 of 2,000 kcal from photos of poha and dal, rice and paneer',
    'activity': 'Self Streak Activity screen: money in and out for 30 days with UPI payments to Swiggy and Big Basket',
    'budget': 'Self Streak Budget screen: 52% of a ₹24,000 monthly budget used, with how much is left per day',
    'bills': 'Self Streak Bills screen: monthly and yearly bill totals and upcoming bills like electricity and broadband with Mark paid buttons',
    'debt': 'Self Streak Debt screen: ₹2,27,000 outstanding, 42% repaid, ₹13,000 of EMIs a month and a debt-free date of Aug 2028',
    'streak': 'Self Streak streak and rewards screen: a 22-day streak with this week’s days and the daily XP goal',
}
SHOTS_FOR = {
    'habit-tracker': ['today', 'streak', 'health'], 'expense-tracker': ['activity', 'budget', 'overview'],
    'credit-card-bill-reminder': ['bills', 'budget', 'debt'], 'debt-payoff-planner': ['debt', 'overview'],
    'emi-calculator': ['debt', 'bills'], 'water-reminder': ['health', 'today'], 'calorie-protein-tracker': ['meals', 'health'],
    'loan': ['debt', 'bills'],
}
SHOT_CSS = """
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));gap:14px;margin-top:16px}
.shots figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:22px;padding:10px}
.shots img{display:block;width:100%;height:auto;border-radius:14px}
.shots figcaption{font-size:13px;color:var(--muted);padding:8px 4px 2px}
"""
def shots_html(key, heading='See it in the app'):
    names = SHOTS_FOR.get(key, [])
    if not names: return ''
    figs = ''.join(f'<figure><img src="/img/app-{n}.webp" alt="{html.escape(SHOT_ALT[n])}" width="390" height="844" loading="lazy" decoding="async">'
                   f'<figcaption>{html.escape(SHOT_ALT[n].split(": ", 1)[0].replace("Self Streak ", ""))}</figcaption></figure>' for n in names)
    return f'<section><h2>{heading}</h2><p>Real screens from the Self Streak app, with sample data.</p><div class="shots">{figs}</div></section>'

FINAL = '<div class="final"><h2>Start your streak today</h2><p>Habits, money, reminders and health in one app. Set up in two minutes, free for 7 days.</p><a class="btn lime" href="/app#signup">Start free trial</a></div>'
GUIDES_FOR = {}   # slug -> [(path, title, blurb)] filled in by build-blog

def render(p):
    path = '/' + p['slug']
    faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in p['faq'])
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": p['h1'], "description": p['desc'], "isPartOf": {"@id": B + "/#website"},
              "about": {"@id": B + "/#app"}, "dateModified": UPDATED, "inLanguage": "en-IN"},
             {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}]
    more = ''.join(f'<a href="/{s}">{html.escape(n)}</a>' for s, n in ALL if s != p['slug'])
    g = GUIDES_FOR.get(p['slug'], [])
    guides = (f'<section><h2>Related guides</h2><div class="guides">' + ''.join(f'<a href="{u}">{html.escape(t)}<span>{html.escape(b)}</span></a>' for u, t, b in g) + '</div></section>') if g else ''
    inner = f"""<header style="padding-top:20px"><div class="wrap"><div class="kick">{html.escape(p['kick'])}</div>
<h1>{html.escape(p['h1'])}</h1><p class="lead">{html.escape(p['lead'])}</p>
<div class="cta"><a class="btn lime" href="/app#signup">Try it free for 7 days →</a><a class="btn" href="/#tour">See the app</a></div>
{p.get('calc','')}<p class="short">{html.escape(p['short'])}</p><p class="upd">Updated {UPDATED}</p></div></header>
<main class="wrap">{p['body']}{shots_html(p['slug'])}{p.get('extra','')}
<section><h2>Questions</h2>{faq_html}</section>
{guides}{FINAL}
<section><h2 style="font-size:20px">More from Self Streak</h2><div class="more">{more}</div></section></main>"""
    return shell(path, p['title'], p['desc'], p['h1'] + ' · Self Streak', graph, [('Self Streak', '/'), (p['nav'], path)], inner)

SITEMAP = []   # (path, lastmod)
DATES_FILE = os.path.join(os.path.dirname(__file__), 'page-dates.json')
DATES = json.load(open(DATES_FILE)) if os.path.exists(DATES_FILE) else {}
def modified(path, content):
    """Date this URL's content last changed: kept from page-dates.json unless the content hash differs."""
    import hashlib
    h = hashlib.sha256(content.encode()).hexdigest()[:16]
    rec = DATES.get(path)
    if not rec or rec['hash'] != h:
        rec = DATES[path] = {'hash': h, 'modified': TODAY}
    return rec['modified']
def write(path, content, sitemap=True):
    d = modified(path, content)
    fp = os.path.join(OUT, path.strip('/') + '.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w') as f: f.write(content.replace(UPDATED, d))
    if sitemap: SITEMAP.append((path, d))
def static_lastmod(path, file):
    """Hand-written pages (landing, legal): date from their file's content hash."""
    return modified(path, open(os.path.join(OUT, file), encoding='utf8').read())

if __name__ == '__main__':
    import importlib.util, sys
    sys.modules['build_pages'] = sys.modules[__name__]
    spec = importlib.util.spec_from_file_location('build_seo', os.path.join(os.path.dirname(__file__), 'build_seo.py'))
    seo = importlib.util.module_from_spec(spec); spec.loader.exec_module(seo)
    seo.build()   # loan pages + blog; fills GUIDES_FOR
    spec = importlib.util.spec_from_file_location('build_compare', os.path.join(os.path.dirname(__file__), 'build_compare.py'))
    cmp_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(cmp_)
    cmp_.link_from_tools(); cmp_.build()   # comparison pages + card interest calculator
    spec = importlib.util.spec_from_file_location('build_hi', os.path.join(os.path.dirname(__file__), 'build_hi.py'))
    hi = importlib.util.module_from_spec(spec); spec.loader.exec_module(hi)
    hi.build()   # Hindi pages (/hi/...)
    for p in PAGES:
        write('/' + p['slug'], render(p))
    print('built', len(SITEMAP), 'pages')
    seo.extra_pages()   # /about and the 404 page
    legal = [(u, static_lastmod(u, u.strip('/') + '.html')) for u in ('/terms', '/privacy', '/refunds', '/shipping', '/contact')]
    urls = [('/', static_lastmod('/', 'landing.html'))] + sorted(SITEMAP) + legal
    with open(DATES_FILE, 'w') as f: json.dump(DATES, f, indent=1, sort_keys=True)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{B}{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls) + '</urlset>\n')
    seo.llms(urls, cmp_.llms_lines())
    print('sitemap and llms.txt updated:', len(urls), 'urls')
