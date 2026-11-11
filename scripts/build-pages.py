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
  title='Credit Card Bill Reminder App India · Never Miss a Due Date | Self Streak',
  desc='Track every credit card and pay-later bill in one place. See this bill, next bill, minimum due and limit left, and get reminders 2 days before the due date. 7-day free trial.',
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
       ('What does it cost?','7 days free, then ₹499 a month for everything in Self Streak, including habits, money, reminders and AI logging.')])

page(slug='emi-calculator', nav='EMI calculator',
  title='EMI Calculator & Loan Tracker India · See Interest and Prepayment Savings | Self Streak',
  desc='Free EMI calculator for home, personal, car and education loans. See monthly EMI, total interest and how much a prepayment saves. Then track every EMI with reminders in Self Streak.',
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
  faq=[('Is this EMI calculator free?','Yes, the calculator on this page is free to use. Tracking your loans with reminders is part of Self Streak (7 days free, then ₹499/month).'),
       ('Does prepaying a loan always save money?','Prepaying reduces interest, but some fixed-rate loans charge a prepayment fee. As per RBI rules, floating-rate loans to individuals have no foreclosure or prepayment charges. Check your loan agreement.'),
       ('Should I prepay my loan or invest?','A common rule: clear high-interest debt (credit cards, personal loans) first, and keep an emergency fund. Self Streak’s AI plan weighs this against your own numbers.')])

page(slug='water-reminder', nav='Water reminder',
  title='Water Reminder App · Daily Water Intake Calculator & Drink Water Alerts | Self Streak',
  desc='Work out how much water you need a day and get gentle drink-water reminders that adapt to what you have already logged. Tap a glass to log water. Try Self Streak free for 7 days.',
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
  title='Habit Tracker App India · Daily Habits, Streaks & Smart Reminders | Self Streak',
  desc='A habit tracker for daily, weekly and monthly habits with streaks, reminders at the right time and goals that count automatically, like 10,000 steps on 300 days. Free for 7 days.',
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
  faq=[('Is there a free habit tracker plan?','You get every feature free for 7 days. After that Self Streak is ₹499 a month, which includes money tracking, reminders and AI features too.'),
       ('Can I track weekly and monthly habits?','Yes. Habits can be daily, weekly, monthly, quarterly or yearly, each with their own reminder.'),
       ('Does it work offline?','Yes. Ticking habits works offline and syncs when you’re back online.')])

page(slug='expense-tracker', nav='Expense tracker',
  title='Expense Tracker India · Budget, Bank Statement Import & Bill Reminders | Self Streak',
  desc='Track spending in rupees by voice, photo or bank statement. Set monthly budgets, see where money goes, and get reminders for bills and EMIs. No bank login needed. 7 days free.',
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
       ('Is my financial data private?','Your data is stored in your own account, never sold or used for ads, and you can export or delete it any time.')])

page(slug='debt-payoff-planner', nav='Debt payoff planner',
  title='Debt Payoff Planner India · Get Debt-Free Faster with an AI Plan | Self Streak',
  desc='Plan how to repay credit cards, personal loans and EMIs on your income. Compare avalanche vs snowball, see your debt-free date, and get a month-by-month AI repayment plan.',
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
  title='Calorie & Protein Tracker for Indian Food · Snap Your Meal with AI | Self Streak',
  desc='Take a photo of dal chawal, roti sabzi or a dosa and get calories and protein in seconds. Track your daily protein target and get a daily AI food summary. 7 days free.',
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
       ('Is it free?','All features are free for 7 days, then ₹499 a month for the whole app.')])

ALL = [(p['slug'], p['nav']) for p in PAGES]

def render(p):
    url = f"{B}/{p['slug']}"
    faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in p['faq'])
    ld = [
        {"@context": "https://schema.org", "@type": "WebPage", "name": p['h1'], "url": url, "description": p['desc'], "isPartOf": {"@type": "WebSite", "name": "Self Streak", "url": B + "/"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Self Streak", "item": B + "/"},
            {"@type": "ListItem", "position": 2, "name": p['nav'], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
    ]
    more = ''.join(f'<a href="/{s}">{html.escape(n)}</a>' for s, n in ALL if s != p['slug'])
    return f'''<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(p['title'])}</title>
<meta name="description" content="{html.escape(p['desc'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#09090b">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Self Streak"><meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(p['h1'])} · Self Streak"><meta property="og:description" content="{html.escape(p['desc'])}">
<meta property="og:image" content="{B}/og-image.png"><meta property="og:locale" content="en_IN"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<nav><div class="wrap"><a class="brand" href="/">{LOGO}Self Streak</a><span class="sp"></span><a class="lg" href="/app">Log in</a><a class="btn lime sm" href="/app#signup">Start free trial</a></div></nav>
<header><div class="wrap"><div class="crumb"><a href="/">Self Streak</a> › {html.escape(p['nav'])}</div><div class="kick">{html.escape(p['kick'])}</div>
<h1>{html.escape(p['h1'])}</h1><p class="lead">{html.escape(p['lead'])}</p>
<div class="cta"><a class="btn lime" href="/app#signup">Try it free for 7 days →</a><a class="btn" href="/#tour">See the app</a></div>
{p.get('calc','')}</div></header>
<main class="wrap">{p['body']}
<section><h2>Questions</h2>{faq_html}</section>
<div class="final"><h2>Start your streak today</h2><p>Habits, money, reminders and health in one app. Set up in two minutes, free for 7 days.</p><a class="btn lime" href="/app#signup">Start free trial</a></div>
<section><h2 style="font-size:20px">More from Self Streak</h2><div class="more">{more}</div></section></main>
<footer><div class="wrap"><span>© 2026 Self Streak</span><a href="/">Home</a><a href="/contact">Contact</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a><a href="/refunds">Refunds</a><a href="/shipping">Shipping</a></div></footer>
<script>try{{if(!/bot|crawl|spider/i.test(navigator.userAgent))navigator.sendBeacon('/api/hit',new Blob([JSON.stringify({{p:location.pathname,r:document.referrer}})],{{type:'application/json'}}))}}catch(e){{}}</script>
</body></html>'''

for p in PAGES:
    with open(os.path.join(OUT, p['slug'] + '.html'), 'w') as f:
        f.write(render(p))
print('built', len(PAGES), 'pages')

# sitemap
core = [('/', '1.0', 'weekly')] + [('/' + s, '0.8', 'monthly') for s, _ in ALL] + [('/terms', '0.3', 'yearly'), ('/privacy', '0.3', 'yearly'), ('/refunds', '0.3', 'yearly'), ('/shipping', '0.3', 'yearly'), ('/contact', '0.4', 'yearly')]
with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{B}{u}</loc><lastmod>2026-11-10</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n' for u, pr, c in core) + '</urlset>\n')
print('sitemap updated')
