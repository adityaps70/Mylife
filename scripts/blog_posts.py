"""Guides published at /blog/<slug>. Every number here is either worked out (see the comments) or
taken from the linked source. Keep `updated` honest: change it only when the content really changes."""

RBI_CC = ('RBI, Master Direction – Credit Card and Debit Card – Issuance and Conduct Directions, 2022 (updated March 2024)',
          'https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12300')

POSTS = [
dict(slug='credit-card-statement-date-vs-due-date', nav='Statement date vs due date', kicker='Credit cards',
  title='Credit Card Statement Date vs Due Date | Self Streak',
  desc='What the statement date and due date mean, how the interest-free period works, why paying only the minimum costs so much, and RBI rules that protect you.',
  h1='Credit card statement date vs due date: what each one means',
  lead='Two dates decide what you pay on a credit card and when. Get them right and a card is an interest-free loan for up to about 50 days. Get them wrong and you pay 3–4% interest a month.',
  short='The <b>statement date</b> is the day your card closes the month’s bill; everything you spent since the last statement is on it. The <b>due date</b> is the last day to pay that bill, usually 15–20 days later. Pay the full amount due by the due date and you pay no interest.',
  date='2026-11-13', hubs=['credit-card-bill-reminder', 'expense-tracker', 'debt-payoff-planner'],
  related=[('Credit card bill reminder', '/credit-card-bill-reminder'), ('Debt avalanche vs snowball', '/blog/debt-avalanche-vs-snowball'), ('50/30/20 budget in rupees', '/blog/50-30-20-budget-rule-india')],
  sources=[RBI_CC],
  body='''
<section><h2 id="statement-date">What is the statement date?</h2>
<p>The statement date (also called the billing date) is the day your card issuer closes a billing cycle and creates your bill. Every purchase from the day after the previous statement date up to this date appears on the new statement. Anything you spend after the statement date goes on next month’s bill.</p>
<p>Example: your statement date is the 5th of every month. A ₹4,000 purchase on 3 March is on the 5 March statement. A ₹4,000 purchase on 6 March is on the 5 April statement.</p></section>
<section><h2 id="due-date">What is the payment due date?</h2>
<p>The due date is the last day to pay the bill created on the statement date. Most Indian cards give 15 to 20 days between the two. If your statement date is the 5th, your due date might be the 23rd or 25th.</p>
<p>The statement shows two amounts: the <b>total amount due</b> (everything on this bill) and the <b>minimum amount due</b> (usually around 5% of the total, plus any EMIs and fees). Only paying the total amount due keeps you interest-free.</p></section>
<section><h2 id="interest-free-period">How the interest-free period works</h2>
<p>The interest-free period is the time between a purchase and the due date of the bill it lands on. It depends on when in the cycle you spend:</p>
<div class="tw"><table><thead><tr><th>Purchase date</th><th>On which bill</th><th>Due date</th><th>Interest-free days</th></tr></thead><tbody>
<tr><td>6 March (day after statement)</td><td>5 April statement</td><td>25 April</td><td>about 50 days</td></tr>
<tr><td>20 March</td><td>5 April statement</td><td>25 April</td><td>about 36 days</td></tr>
<tr><td>4 April (day before statement)</td><td>5 April statement</td><td>25 April</td><td>about 21 days</td></tr></tbody></table></div>
<p>So a big planned purchase made just after your statement date gets the longest time to pay. The exact number of days depends on your card’s cycle.</p>
<p>The interest-free period disappears if you carry a balance. RBI requires card issuers to explain in their terms that the interest-free credit period is suspended if any balance from the previous bill is still outstanding. In practice, once you pay less than the full amount, new purchases start charging interest from the day you make them.</p></section>
<section><h2 id="minimum-due">Why paying only the minimum is so expensive</h2>
<p>Paying the minimum due keeps your account in good standing and avoids a late fee, but interest is charged on the rest, usually 3–3.75% a month (about 36–45% a year).</p>
<p>A worked example: a ₹60,000 balance at 3.5% a month, paying only a 5% minimum (at least ₹500) and spending nothing more on the card, takes about <b>141 months</b> (nearly 12 years) to clear and costs about <b>₹1,11,917</b> in interest, almost twice the original balance. RBI requires every billing statement to warn that paying only the minimum results in repayment stretching over months or years with compounded interest.</p></section>
<section><h2 id="rbi-rules">RBI rules that protect you</h2>
<p>The RBI’s Master Direction on credit and debit cards (2022, updated March 2024) sets several rules worth knowing:</p>
<ul class="list">
<li><b>3-day grace for late fees and credit reports.</b> Card issuers can levy late payment charges, or report your account as past due to credit bureaus, only when the account stays past due for more than three days after the due date.</li>
<li><b>Late fees only on what is overdue.</b> Late payment charges are levied only on the amount outstanding after the due date, not on the total amount due.</li>
<li><b>You can change your billing cycle.</b> Card issuers must let you modify the billing cycle at least once, choosing the date that suits you, through channels like the helpline, app or internet banking.</li>
<li><b>Interest only on what you owe.</b> Interest is levied only on the outstanding amount, adjusted for payments, refunds and reversed transactions.</li></ul>
<p>The 3-day grace is a safety net, not a plan. Interest on the unpaid balance can still apply from the due date, so pay on time.</p></section>
<section><h2 id="choose-dates">How to choose the best statement date</h2>
<p>If your salary arrives on the 1st, a due date around the 5th to 10th means the bill is paid while money is in your account. Work back 15–20 days to find the statement date to ask for. If you hold two cards, staggering their due dates spreads payments across the month.</p></section>
<section><h2 id="payment-timing">When does a payment count as made?</h2>
<p>A payment counts when your card issuer receives it, not when you send it. Payments through the card issuer’s own app, UPI or net banking to the same bank usually reflect the same day. Payments from another bank, by cheque or through third-party apps can take one to three working days, and weekends and bank holidays can add more.</p>
<p>The safe habit is to pay at least two to three working days before the due date, and check that the payment shows on your card account. Keep the payment reference until it does. If the due date falls on a Sunday or holiday, do not assume it moves to the next working day; check your statement or ask your card issuer.</p>
<p>Refunds work the other way. RBI rules say a credit from a refund, failed or reversed transaction before the due date should be adjusted against the amount due, so a large refund can reduce what you need to pay. Check the updated amount in your card app before you pay.</p></section>
<section><h2 id="never-miss">How to never miss a due date</h2>
<ol class="list">
<li>Set up an auto-debit for at least the minimum due, as a safety net.</li>
<li>Pay the full amount manually a few days before the due date.</li>
<li>Track what you have already spent on the next bill, so it is not a surprise.</li>
<li>Get a reminder that shows the amount, not just the date.</li></ol>
<p><a href="/credit-card-bill-reminder">Self Streak’s credit card tracker</a> follows each card’s statement and due dates, splits spends into this bill and next bill, and reminds you two days before each due date.</p></section>
<section><h2 id="faq">Common questions</h2>
<h3>Is the statement date the same as the due date?</h3><p>No. The statement date closes the bill; the due date, usually 15–20 days later, is the deadline to pay it.</p>
<h3>What happens if I pay one day late?</h3><p>Under RBI rules, late fees and credit bureau reporting apply only if the account is past due for more than three days. Interest on the unpaid balance can still be charged, and the interest-free period on new purchases is lost until you clear the balance.</p>
<h3>Does paying the minimum due affect my credit score?</h3><p>Paying at least the minimum on time avoids a late payment mark. But a high balance relative to your limit can still lower your score, and the interest adds up quickly.</p></section>
'''),

dict(slug='50-30-20-budget-rule-india', nav='50/30/20 budget', kicker='Budgeting',
  title='50/30/20 Budget Rule India: Rupee Examples | Self Streak',
  desc='How the 50/30/20 budget rule works on an Indian salary, with worked examples for ₹40,000, ₹75,000 and ₹1.5 lakh a month, and how to adjust it for rent and EMIs.',
  h1='The 50/30/20 budget rule in India, with rupee examples',
  lead='The 50/30/20 rule splits your take-home pay into three buckets: needs, wants and savings. It is simple enough to follow without a spreadsheet, and it works on Indian salaries with a few adjustments.',
  short='The 50/30/20 rule puts <b>50% of take-home pay on needs</b> (rent, groceries, bills, EMIs), <b>30% on wants</b> (eating out, shopping, trips) and <b>20% on savings and extra debt repayment</b>. On a ₹75,000 salary that is ₹37,500 for needs, ₹22,500 for wants and ₹15,000 to save.',
  date='2026-11-13', hubs=['expense-tracker', 'credit-card-bill-reminder', 'emi-calculator'],
  related=[('Expense tracker', '/expense-tracker'), ('Debt avalanche vs snowball', '/blog/debt-avalanche-vs-snowball'), ('Statement date vs due date', '/blog/credit-card-statement-date-vs-due-date')],
  sources=[('Elizabeth Warren and Amelia Warren Tyagi, All Your Worth: The Ultimate Lifetime Money Plan (2005), where the 50/30/20 split was popularised', '')],
  body='''
<section><h2 id="what-is-it">What is the 50/30/20 rule?</h2>
<p>The 50/30/20 rule is a budgeting guideline popularised by Elizabeth Warren and Amelia Warren Tyagi in their 2005 book <i>All Your Worth</i>. It divides your monthly take-home pay (salary after tax, PF and other deductions) into three parts:</p>
<ul class="list">
<li><b>50% needs:</b> things you must pay to live and work. Rent or home loan EMI, groceries, electricity, phone and internet, school fees, insurance premiums, commuting, and minimum payments on loans.</li>
<li><b>30% wants:</b> things you choose. Eating out, Swiggy and Zomato orders, OTT subscriptions, shopping, gadgets, holidays.</li>
<li><b>20% savings:</b> emergency fund, SIPs, PPF, extra loan prepayments and any goal you are saving for.</li></ul></section>
<section><h2 id="examples">50/30/20 on an Indian salary: three examples</h2>
<div class="tw"><table><thead><tr><th>Take-home pay</th><th>Needs (50%)</th><th>Wants (30%)</th><th>Savings (20%)</th></tr></thead><tbody>
<tr><td>₹40,000</td><td>₹20,000</td><td>₹12,000</td><td>₹8,000</td></tr>
<tr><td>₹75,000</td><td>₹37,500</td><td>₹22,500</td><td>₹15,000</td></tr>
<tr><td>₹1,50,000</td><td>₹75,000</td><td>₹45,000</td><td>₹30,000</td></tr></tbody></table></div>
<p>Saving ₹15,000 a month adds up to ₹1.8 lakh a year before any returns. At ₹8,000 a month, six months of savings builds a ₹48,000 emergency cushion.</p></section>
<section><h2 id="worked-month">A real month on ₹60,000 take-home</h2>
<p>Here is how one month might look for someone earning ₹60,000 a month in Pune and sharing a flat. The 50/30/20 limits are ₹30,000 for needs, ₹18,000 for wants and ₹12,000 for savings.</p>
<div class="tw"><table><thead><tr><th>Bucket</th><th>Item</th><th>Amount</th></tr></thead><tbody>
<tr><td>Needs</td><td>Rent share</td><td>₹14,000</td></tr>
<tr><td>Needs</td><td>Groceries and milk</td><td>₹6,000</td></tr>
<tr><td>Needs</td><td>Electricity, phone, internet</td><td>₹2,500</td></tr>
<tr><td>Needs</td><td>Commute and fuel</td><td>₹3,000</td></tr>
<tr><td>Needs</td><td>Health insurance and two-wheeler EMI</td><td>₹4,500</td></tr>
<tr><td><b>Needs total</b></td><td></td><td><b>₹30,000 (50%)</b></td></tr>
<tr><td>Wants</td><td>Eating out and food delivery</td><td>₹7,000</td></tr>
<tr><td>Wants</td><td>Shopping, OTT, gym</td><td>₹6,000</td></tr>
<tr><td>Wants</td><td>Weekend trips and outings</td><td>₹5,000</td></tr>
<tr><td><b>Wants total</b></td><td></td><td><b>₹18,000 (30%)</b></td></tr>
<tr><td>Savings</td><td>Emergency fund</td><td>₹5,000</td></tr>
<tr><td>Savings</td><td>SIP</td><td>₹7,000</td></tr>
<tr><td><b>Savings total</b></td><td></td><td><b>₹12,000 (20%)</b></td></tr></tbody></table></div>
<p>If eating out creeps up to ₹11,000, the plan still works as long as another want gives way. The point is not to hit every line exactly but to keep the three totals in balance.</p></section>
<section><h2 id="needs-vs-wants">How to tell a need from a want</h2>
<p>A simple test: if you stopped paying it, would your health, home, job or credit suffer? If yes, it is a need. A basic phone plan is a need; the latest phone on EMI is mostly a want. Groceries are a need; daily food delivery is a want.</p>
<p>Minimum loan and credit card payments count as needs because missing them hurts your credit. Anything you pay above the minimum to clear debt faster counts as savings.</p></section>
<section><h2 id="emergency-fund">Build an emergency fund first</h2>
<p>An emergency fund is money set aside for job loss, a medical bill or an urgent repair. A common target is three to six months of essential expenses, which for the example above is ₹90,000 to ₹1,80,000. Until it exists, put most of the 20% here, in a savings account or liquid fund you can reach within a day. Without it, the first surprise expense goes on a credit card and the budget falls apart.</p></section>
<section><h2 id="adjust-india">Adjusting the rule for Indian cities</h2>
<p>In Mumbai, Bengaluru, Delhi NCR or Pune, rent alone can take 30–40% of a starting salary, which makes 50% for needs hard to hit. Two common adjustments:</p>
<ul class="list">
<li><b>60/20/20:</b> allow 60% for needs, cut wants to 20%, and keep savings at 20%.</li>
<li><b>Savings first:</b> move your savings amount to a separate account or SIP on salary day, then split the rest between needs and wants.</li></ul>
<p>Keep the 20% savings target if you can. If you cannot, start at 10% and raise it by 1–2% with every increment.</p></section>
<section><h2 id="emis">Where do EMIs fit?</h2>
<p>EMIs on a home, car or personal loan are needs, because missing them hurts. A widely used rule of thumb is to keep total EMIs under about 30–40% of take-home pay. If EMIs alone take more than half your salary, the 50/30/20 split will not fit until you reduce debt. A <a href="/debt-payoff-planner">debt payoff plan</a> helps you choose which loan to clear first.</p></section>
<section><h2 id="start">How to start in 15 minutes</h2>
<ol class="list">
<li>Find your take-home pay from your last salary slip.</li>
<li>Multiply by 0.5, 0.3 and 0.2 to get your three limits.</li>
<li>List fixed needs (rent, EMIs, bills). If they exceed 50%, use 60/20/20 for now.</li>
<li>Set up an auto-transfer or SIP for the savings amount on salary day.</li>
<li>Track spending for one month and compare it with your limits.</li></ol>
<p>Tracking is the step most people skip. An <a href="/expense-tracker">expense tracker</a> that logs spends by voice, photo or bank statement makes it take seconds a day.</p></section>
<section><h2 id="mistakes">Common mistakes to avoid</h2>
<ul class="list">
<li><b>Budgeting on gross salary.</b> Use what actually reaches your account.</li>
<li><b>Forgetting yearly costs.</b> Insurance premiums, school fees, festivals and annual subscriptions. Divide them by 12 and set that amount aside every month.</li>
<li><b>Counting credit card spends when you pay the bill.</b> Count a spend in the month you make it, or you will think you have more money than you do.</li>
<li><b>Treating every want as a need.</b> Be honest about food delivery, upgrades and subscriptions.</li>
<li><b>Giving up after one bad month.</b> Look at a three-month average before changing the plan.</li></ul></section>
<section><h2 id="faq">Common questions</h2>
<h3>Is the 50/30/20 rule based on gross or net salary?</h3><p>On take-home (net) pay: what reaches your bank account after tax, PF and other deductions. Your PF contribution is extra saving on top of the 20%.</p>
<h3>Does the 20% include investments like SIPs?</h3><p>Yes. Savings covers your emergency fund, SIPs, PPF, NPS contributions you make yourself and extra loan prepayments.</p>
<h3>What if I cannot save 20%?</h3><p>Start with any fixed amount on salary day and increase it with each raise. Consistency matters more than the exact percentage.</p></section>
'''),

dict(slug='debt-avalanche-vs-snowball', nav='Avalanche vs snowball', kicker='Getting debt-free',
  title='Debt Avalanche vs Snowball: Which Is Better? | Self Streak',
  desc='Avalanche vs snowball debt payoff, compared on a real Indian example with a credit card, personal loan and phone EMI: months to debt-free and interest paid.',
  h1='Debt avalanche vs snowball: which pays off debt faster?',
  lead='Both methods pay the minimum on every debt and put any extra money towards one debt at a time. They differ only in which debt gets the extra first, and that choice changes how much interest you pay and how motivated you stay.',
  short='The <b>avalanche</b> method puts extra money on the highest-interest debt first and costs the least interest. The <b>snowball</b> method clears the smallest balance first for quick wins. In our example below, avalanche saves about ₹1,645 more than snowball, while both are debt-free in 13 months.',
  date='2026-11-13', hubs=['debt-payoff-planner', 'emi-calculator'],
  related=[('Debt payoff planner', '/debt-payoff-planner'), ('Personal loan EMI calculator', '/emi-calculator/personal-loan'), ('Statement date vs due date', '/blog/credit-card-statement-date-vs-due-date')],
  sources=[('Gal, D. and McShane, B. B. (2012), “Can Small Victories Help Win the War? Evidence from Consumer Debt Management”, Journal of Marketing Research', 'https://doi.org/10.1509/jmr.11.0272'), RBI_CC],
  body='''
<section><h2 id="avalanche">What is the debt avalanche method?</h2>
<p>The debt avalanche method pays the minimum on every debt, then puts every extra rupee towards the debt with the highest interest rate. When that debt is gone, its payment rolls on to the next-highest rate. Because the most expensive debt shrinks first, avalanche always costs the least total interest.</p>
<p>In India the highest rate is almost always a credit card balance (about 36–45% a year), followed by personal loans, consumer durable EMIs, car loans and home loans.</p></section>
<section><h2 id="snowball">What is the debt snowball method?</h2>
<p>The debt snowball method pays the minimum on every debt, then puts every extra rupee towards the <b>smallest balance</b>, whatever its rate. Each cleared debt frees up its payment for the next one, so the amount you put towards debt grows like a rolling snowball. You get early wins, which helps many people stick with the plan.</p></section>
<section><h2 id="example">Avalanche vs snowball: a worked example</h2>
<p>Three debts and ₹20,000 a month to put towards them in total:</p>
<div class="tw"><table><thead><tr><th>Debt</th><th>Balance</th><th>Rate (a year)</th><th>Minimum a month</th></tr></thead><tbody>
<tr><td>Credit card</td><td>₹60,000</td><td>42%</td><td>₹3,000</td></tr>
<tr><td>Personal loan</td><td>₹1,50,000</td><td>14%</td><td>₹5,000</td></tr>
<tr><td>Phone EMI</td><td>₹20,000</td><td>16%</td><td>₹2,000</td></tr></tbody></table></div>
<p>Minimums add up to ₹10,000, so ₹10,000 a month is extra. Simulating month by month, with interest added monthly:</p>
<div class="tw"><table><thead><tr><th>Plan</th><th>Debt-free in</th><th>Total interest</th><th>Order cleared</th></tr></thead><tbody>
<tr><td>Avalanche</td><td>13 months</td><td>₹23,584</td><td>Card and phone (month 6), loan (month 13)</td></tr>
<tr><td>Snowball</td><td>13 months</td><td>₹25,229</td><td>Phone (month 2), card (month 6), loan (month 13)</td></tr>
<tr><td>Minimums only</td><td>30 months</td><td>₹66,935</td><td>Phone (11), card (23), loan (30)</td></tr></tbody></table></div>
<p>Two lessons stand out. First, avalanche saves money (₹1,645 here), but the gap is small when balances are modest. Second, the big win is paying extra at all: either plan saves over ₹41,000 and 17 months compared with paying only the minimums.</p></section>
<section><h2 id="research">What the research says about motivation</h2>
<p>A 2012 study in the <i>Journal of Marketing Research</i> by David Gal and Blakeley McShane looked at people in a debt settlement programme. People who closed off individual debt accounts were more likely to clear all their debt, independent of the amount they had repaid. Small victories seem to help people keep going.</p>
<p>That is the case for snowball: if seeing a debt disappear in month 2 keeps you on the plan, the extra interest can be worth it.</p></section>
<section><h2 id="find-extra">Where the extra money comes from</h2>
<p>Both methods depend on paying more than the minimums. Common places to find it:</p>
<ul class="list">
<li>Cut wants for a few months: food delivery, subscriptions, shopping. Even ₹3,000–5,000 a month speeds things up.</li>
<li>Put bonuses, tax refunds and gifts straight towards the first debt in your list.</li>
<li>Sell unused items, or take on short-term extra work, and use all of it for debt.</li>
<li>When a debt is cleared, keep paying the same total. Do not let lifestyle absorb the freed EMI.</li></ul></section>
<section><h2 id="which">Which method should you choose?</h2>
<ul class="list">
<li><b>Choose avalanche</b> if you have a high-interest credit card balance, if the balances are large, or if you are motivated by numbers.</li>
<li><b>Choose snowball</b> if you have several small debts, if you have tried and given up before, or if quick wins keep you going.</li>
<li><b>Hybrid:</b> clear any tiny balance first for a quick win, then switch to avalanche.</li></ul>
<p>Whichever you choose, stop adding new debt to the cards you are paying off, and keep a small emergency fund so one surprise bill does not undo your progress.</p></section>
<section><h2 id="too-much">If the minimums alone are too much</h2>
<p>If minimum payments and EMIs already take more than your income can bear, neither method works yet. Steps to consider:</p>
<ul class="list">
<li><b>Talk to your lender early,</b> before you miss a payment. Ask about restructuring, a longer tenure or converting a card balance into an EMI at a lower rate.</li>
<li><b>Consolidate expensive debt.</b> A personal loan or balance transfer at a lower rate can replace card interest, but only if you stop using the card.</li>
<li><b>Never pay one loan with another expensive loan,</b> such as instant loan apps, which often charge very high fees.</li>
<li><b>Get help.</b> Banks have grievance and customer service channels, and RBI’s complaint system is there if a lender does not respond.</li></ul></section>
<section><h2 id="plan">How to make your own plan</h2>
<ol class="list">
<li>List every debt with its balance, interest rate and minimum payment.</li>
<li>Work out how much you can put towards debt each month after essentials.</li>
<li>Pick avalanche or snowball and order the list.</li>
<li>Pay minimums on all, and the extra on the first debt in your order.</li>
<li>When a debt is cleared, add its payment to the next one.</li></ol>
<p><a href="/debt-payoff-planner">Self Streak’s debt payoff planner</a> runs both methods on your own numbers, shows your debt-free date and reminds you before every EMI and card due date.</p></section>
<section><h2 id="faq">Common questions</h2>
<h3>Should I take a personal loan to pay off a credit card?</h3><p>It can save a lot, since personal loans usually cost far less than card interest. It only helps if you stop adding new spending to the card.</p>
<h3>Should I prepay my home loan before other debts?</h3><p>Usually not. Home loans have the lowest rates; clear credit cards and personal loans first.</p></section>
'''),

dict(slug='how-long-does-it-take-to-form-a-habit', nav='How long to form a habit', kicker='Habits',
  title='How Long Does It Take to Form a Habit? | Self Streak',
  desc='Research found new habits took a median of 66 days to become automatic, with a range of 18 to 254 days. What that means, and how to make a habit stick.',
  h1='How long does it take to form a habit?',
  lead='You have probably heard that it takes 21 days to form a habit. The best-known study on the question found something different, and the details are more encouraging than the myth.',
  short='In a 2010 study at University College London, new daily habits took a <b>median of 66 days</b> to become automatic, ranging from <b>18 to 254 days</b> depending on the person and the habit. Missing a single day did not meaningfully set people back.',
  date='2026-11-13', hubs=['habit-tracker', 'water-reminder'],
  related=[('Habit tracker', '/habit-tracker'), ('How much water to drink', '/blog/how-much-water-should-i-drink-a-day'), ('Protein on an Indian diet', '/blog/protein-intake-indian-diet')],
  sources=[('Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W. and Wardle, J. (2010), “How are habits formed: Modelling habit formation in the real world”, European Journal of Social Psychology, 40(6)', 'https://doi.org/10.1002/ejsp.674')],
  body='''
<section><h2 id="study">What the research found</h2>
<p>In the study by Phillippa Lally and colleagues at University College London, 96 volunteers each chose a new healthy behaviour to do once a day in the same situation, such as eating a piece of fruit with lunch or going for a 15-minute walk before dinner. For 12 weeks they reported every day whether they did it and how automatic it felt.</p>
<p>For the people whose data showed a clear pattern, automaticity rose quickly at first and then levelled off. The time to reach that plateau had a median of <b>66 days</b>, and individual results ranged from <b>18 to 254 days</b>. Simpler behaviours, like drinking a glass of water, tended to become automatic faster than harder ones, like doing sit-ups.</p></section>
<section><h2 id="21-days">Where does “21 days” come from?</h2>
<p>The 21-day figure is usually traced to a 1960s self-help book by the plastic surgeon Maxwell Maltz, who observed that patients took a minimum of about 21 days to adjust to changes. Over time “a minimum of about 21 days” became “21 days”. It was never a measured result for building habits.</p></section>
<section><h2 id="missing-days">Does missing a day break a habit?</h2>
<p>Not much. In the UCL study, missing one opportunity to perform the behaviour did not materially affect the habit-forming process. What matters is coming back the next day. The real risk of a missed day is the story you tell yourself afterwards (“I’ve broken it, so why bother?”), not the missed day itself.</p>
<p>That is why a good habit tracker should show your streak and your overall consistency, so one miss does not erase weeks of effort.</p></section>
<section><h2 id="make-it-stick">How to make a habit stick</h2>
<ol class="list">
<li><b>Pick one specific cue.</b> “After I brush my teeth at night, I read for 10 minutes” beats “read more”. The study’s habits were tied to a daily situation for this reason.</li>
<li><b>Start smaller than you think.</b> Five push-ups or one glass of water every morning builds the routine; you can grow it later.</li>
<li><b>Same time, same place.</b> Consistent context is what makes a behaviour automatic.</li>
<li><b>Track it visibly.</b> Ticking a habit off and seeing a streak gives an immediate reward that the long-term benefit cannot.</li>
<li><b>Plan for misses.</b> Decide now: “If I miss a day, I do it the next day, no matter what.”</li>
<li><b>Give it two to three months.</b> Expect around 66 days for a daily habit, longer for hard ones. If it still feels like effort after three weeks, that is normal.</li></ol></section>
<section><h2 id="streaks">Do streaks help or hurt?</h2>
<p>Streaks help because they turn an invisible long-term benefit into something you can see today. A 30-day streak feels worth protecting. They can backfire when a single miss feels like failure and you quit. Two ways to keep the benefit without the trap:</p>
<ul class="list">
<li>Track consistency as well as streak: “26 of the last 30 days” still shows a habit forming.</li>
<li>Set goals in days per year, such as “gym on 200 days this year”. A missed day lowers the pace slightly instead of resetting everything to zero.</li></ul></section>
<section><h2 id="stacking">Habit stacking with Indian routines</h2>
<p>Habit stacking means attaching a new habit to one you already do every day. Daily routines give natural anchors:</p>
<ul class="list">
<li>After morning chai: 5 minutes of stretching.</li>
<li>After puja or prayer: write down the day’s top three tasks.</li>
<li>While the pressure cooker whistles: log today’s spends.</li>
<li>After dinner: a 10-minute walk, a common evening habit in many families.</li>
<li>After locking the door at night: put the phone on charge outside the bedroom.</li></ul></section>
<section><h2 id="examples">Habit ideas that are easy to start</h2>
<div class="tw"><table><thead><tr><th>Goal</th><th>Tiny daily version</th><th>Cue</th></tr></thead><tbody>
<tr><td>Fitness</td><td>10-minute walk</td><td>After lunch</td></tr>
<tr><td>Hydration</td><td>1 glass of water</td><td>Before morning tea</td></tr>
<tr><td>Reading</td><td>5 pages</td><td>After switching off the TV</td></tr>
<tr><td>Money</td><td>Log today’s spends</td><td>Before bed</td></tr>
<tr><td>Sleep</td><td>No phone in bed</td><td>Phone on charge at 10:30 pm</td></tr></tbody></table></div></section>
<section><h2 id="tracking">Why reminders at the right time help</h2>
<p>A reminder works best when it arrives at the moment the habit should happen, not at a random time. A gym reminder at 6:30 pm, sunscreen at 7:30 am and reading at 9:45 pm each match their cue. <a href="/habit-tracker">Self Streak’s habit tracker</a> reminds you at each habit’s own time, skips the reminder if you have already done it, and keeps your streak and goals counting.</p></section>
<section><h2 id="review">Review once a week</h2>
<p>A five-minute weekly check keeps habits from quietly fading. Look at which habits you did most days, which you missed, and why. If a habit keeps failing at the same point, change the cue or make it smaller instead of relying on willpower. Drop a habit that no longer matters to you; fewer habits done well beat a long list you ignore.</p></section>
<section><h2 id="faq">Common questions</h2>
<h3>Is it 21, 66 or 90 days?</h3><p>None of these is a rule. The median in the best-known study was 66 days, with a huge range. Plan for two to three months for a daily habit.</p>
<h3>Are weekly habits harder to form?</h3><p>Usually, because there are fewer repetitions to build the link between cue and action. Tie them to a fixed day and time.</p></section>
'''),

dict(slug='how-much-water-should-i-drink-a-day', nav='How much water a day', kicker='Health',
  title='How Much Water to Drink a Day, by Weight | Self Streak',
  desc='How much water adults need each day, a simple per-kg guide with a table from 50 to 100 kg, extra for heat and exercise in India, and signs you need more.',
  h1='How much water should you drink a day?',
  lead='There is no single number that fits everyone, but there are good reference values and a simple way to work out your own target, with extra for hot Indian summers and workouts.',
  short='European Food Safety Authority guidance puts adequate total water intake at about <b>2.0 litres a day for women and 2.5 litres for men</b>, from drinks and food together, with roughly 70–80% coming from drinks. A simple personal guide is about <b>30–35 ml per kg</b> of body weight, plus more in heat or after exercise.',
  date='2026-11-13', hubs=['water-reminder', 'habit-tracker', 'calorie-protein-tracker'],
  related=[('Water reminder and calculator', '/water-reminder'), ('How long to form a habit', '/blog/how-long-does-it-take-to-form-a-habit'), ('Protein on an Indian diet', '/blog/protein-intake-indian-diet')],
  sources=[('EFSA Panel on Dietetic Products, Nutrition and Allergies (2010), “Scientific Opinion on Dietary Reference Values for water”, EFSA Journal 8(3):1459', 'https://doi.org/10.2903/j.efsa.2010.1459')],
  body='''
<section><h2 id="reference">How much water do adults need?</h2>
<p>The European Food Safety Authority (EFSA) set adequate intakes of total water at <b>2.0 litres a day for women</b> and <b>2.5 litres a day for men</b> in temperate conditions with moderate activity. “Total water” includes water from food. Since food usually provides around 20–30% of it, that works out to roughly 1.5–1.6 litres from drinks for women and 2.0 litres for men.</p>
<p>These are averages for healthy adults. Heat, humidity, physical activity, pregnancy, breastfeeding and illness all raise the need.</p></section>
<section><h2 id="by-weight">Water intake by body weight</h2>
<p>A simple per-kg guide many people use is about 30–35 ml of fluid per kg of body weight a day. At 33 ml per kg:</p>
<div class="tw"><table><thead><tr><th>Body weight</th><th>Litres a day</th><th>250 ml glasses</th></tr></thead><tbody>
<tr><td>50 kg</td><td>1.7 L</td><td>about 7</td></tr>
<tr><td>60 kg</td><td>2.0 L</td><td>about 8</td></tr>
<tr><td>70 kg</td><td>2.3 L</td><td>about 9</td></tr>
<tr><td>80 kg</td><td>2.6 L</td><td>about 11</td></tr>
<tr><td>90 kg</td><td>3.0 L</td><td>about 12</td></tr>
<tr><td>100 kg</td><td>3.3 L</td><td>about 13</td></tr></tbody></table></div>
<p>This is a rough guide, not a prescription. <a href="/water-reminder">Our water calculator</a> adds exercise and weather to give you a personal target.</p></section>
<section><h2 id="heat-exercise">Extra for Indian summers and exercise</h2>
<p>Sweat losses rise sharply in hot, humid weather and during exercise. Practical adjustments:</p>
<ul class="list">
<li><b>Hot or humid day:</b> add about 0.5 litre (two glasses).</li>
<li><b>Exercise:</b> add roughly 0.4–0.8 litre for each hour of moderate workout, sipping during and after.</li>
<li><b>Heavy sweating:</b> plain water alone may not be enough; nimbu paani with a pinch of salt, coconut water or ORS replaces electrolytes.</li></ul></section>
<section><h2 id="food">Water from food</h2>
<p>Food provides a meaningful share of daily water, and many Indian foods are water-rich: dal, sambar, rasam and curries, curd and buttermilk, cucumber, tomato, watermelon, oranges and khichdi. A meal with dal, curd and salad adds noticeably more water than a dry snack. That is part of why the drinks target is lower than the total water figure.</p></section>
<section><h2 id="myths">Common myths</h2>
<ul class="list">
<li><b>“Wait until you are thirsty.”</b> Thirst works well for most healthy adults at rest, but in heat, during exercise and in older age it can lag behind.</li>
<li><b>“Tea and coffee dehydrate you.”</b> In normal amounts they still add to fluid intake overall.</li>
<li><b>“More water is always better.”</b> Beyond your needs it simply passes through, and very large amounts at once can be harmful.</li>
<li><b>“Clear urine is the goal.”</b> Pale yellow is enough; completely clear urine all day can mean you are drinking more than you need.</li></ul></section>
<section><h2 id="signs">Signs you need more water</h2>
<ul class="list"><li>Dark yellow urine (pale straw colour is the usual goal).</li><li>Thirst, dry mouth, headache or feeling tired in the afternoon.</li><li>Urinating rarely during the day.</li></ul>
<p>Too much water is also possible. Drinking very large amounts in a short time can dilute the body’s sodium, which is dangerous. Spread intake across the day rather than drinking litres at once.</p></section>
<section><h2 id="medical">When to follow your doctor instead</h2>
<p>People with kidney disease, heart failure, liver disease or some hormonal conditions may be told to limit fluids. Some medicines also change how much you should drink. If a doctor has given you a fluid limit, follow it over any general guide, including this one.</p></section>
<section><h2 id="habit">How to drink enough without thinking about it</h2>
<ol class="list">
<li>Drink a glass when you wake up, before tea or coffee.</li>
<li>Have a glass with every meal.</li>
<li>Keep a 1-litre bottle on your desk and finish it twice a day.</li>
<li>Use reminders that adapt to what you have already drunk, not a fixed timer.</li></ol>
<p><a href="/water-reminder">Self Streak’s water reminder</a> lets you tap a glass to log it and only nudges you when you are behind for the time of day.</p></section>
<section><h2 id="travel-work">At work, while travelling and while fasting</h2>
<p>Long meetings, train journeys and busy shifts are when intake drops. Carry a bottle and set a simple rule, such as finishing half of it by lunch. On days of religious fasting that allow water, drink steadily through the allowed hours rather than all at once. On fasts without water, avoid heavy exercise and heat, and break the fast with water and something salty, such as nimbu paani or buttermilk.</p></section>
<section><h2 id="faq">Common questions</h2>
<h3>Do tea, coffee and milk count?</h3><p>Yes. All drinks count towards fluid intake. Moderate tea and coffee still hydrate overall, though water is the best everyday choice.</p>
<h3>Is 8 glasses a day right?</h3><p>Eight 250 ml glasses is 2 litres, which is close to the reference values for many adults but too little for a large or active person in summer.</p></section>
'''),

dict(slug='protein-intake-indian-diet', nav='Protein on an Indian diet', kicker='Food & protein',
  title='Protein Intake on an Indian Diet | Self Streak',
  desc='How much protein Indian adults need per kg, how to hit it on a vegetarian or non-vegetarian Indian diet, with a sample day and protein in common Indian foods.',
  h1='How much protein do you need on an Indian diet?',
  lead='Protein is the nutrient many Indian diets fall short on, especially vegetarian ones built around rice and roti. Here is how much you need and how to get it from everyday Indian food.',
  short='ICMR-NIN’s 2020 nutrient requirements for Indians set the recommended protein intake for healthy adults at about <b>0.83 g per kg of body weight a day</b>, so about 58 g for a 70 kg adult. People who train regularly often aim higher, around 1.2–1.6 g per kg.',
  date='2026-11-13', hubs=['calorie-protein-tracker'],
  related=[('Calorie and protein tracker', '/calorie-protein-tracker'), ('How much water a day', '/blog/how-much-water-should-i-drink-a-day'), ('How long to form a habit', '/blog/how-long-does-it-take-to-form-a-habit')],
  sources=[('ICMR – National Institute of Nutrition (2020), Nutrient Requirements for Indians: Recommended Dietary Allowances and Estimated Average Requirements', 'https://www.nin.res.in/'),
           ('Indian Food Composition Tables (ICMR-NIN, 2017) for typical protein values of Indian foods', 'https://www.nin.res.in/')],
  body='''
<section><h2 id="how-much">How much protein do Indian adults need?</h2>
<p>The ICMR-National Institute of Nutrition’s 2020 report on nutrient requirements for Indians recommends about <b>0.83 g of protein per kg of body weight a day</b> for healthy adults, assuming good-quality protein. The average requirement behind it is about 0.66 g per kg; the recommended figure adds a margin so it covers nearly everyone.</p>
<div class="tw"><table><thead><tr><th>Body weight</th><th>At 0.83 g/kg</th><th>At 1.2 g/kg (active)</th><th>At 1.6 g/kg (strength training)</th></tr></thead><tbody>
<tr><td>50 kg</td><td>42 g</td><td>60 g</td><td>80 g</td></tr>
<tr><td>60 kg</td><td>50 g</td><td>72 g</td><td>96 g</td></tr>
<tr><td>70 kg</td><td>58 g</td><td>84 g</td><td>112 g</td></tr>
<tr><td>80 kg</td><td>66 g</td><td>96 g</td><td>128 g</td></tr></tbody></table></div>
<p>The higher columns are common targets for people who exercise or lift weights; they are not part of the ICMR-NIN recommendation. Pregnant and breastfeeding women need more, and people with kidney disease should follow their doctor’s limit.</p></section>
<section><h2 id="foods">Protein in common Indian foods</h2>
<p>Approximate values; they vary with brand, recipe and portion.</p>
<div class="tw"><table><thead><tr><th>Food</th><th>Portion</th><th>Protein (about)</th></tr></thead><tbody>
<tr><td>Soya chunks (dry)</td><td>30 g</td><td>15 g</td></tr>
<tr><td>Paneer</td><td>100 g</td><td>18 g</td></tr>
<tr><td>Chicken breast (cooked)</td><td>100 g</td><td>25–30 g</td></tr>
<tr><td>Eggs</td><td>2 large</td><td>12 g</td></tr>
<tr><td>Dal, rajma or chole (cooked)</td><td>1 katori (about 150 g)</td><td>7–9 g</td></tr>
<tr><td>Curd / dahi</td><td>1 katori (about 150 g)</td><td>5–6 g</td></tr>
<tr><td>Milk</td><td>1 glass (250 ml)</td><td>8 g</td></tr>
<tr><td>Peanuts</td><td>30 g handful</td><td>7–8 g</td></tr>
<tr><td>Roti (whole wheat)</td><td>1 medium</td><td>3 g</td></tr>
<tr><td>Cooked rice</td><td>1 katori</td><td>3–4 g</td></tr></tbody></table></div></section>
<section><h2 id="vegetarian">Getting enough protein as a vegetarian</h2>
<p>A typical vegetarian day of tea, poha, dal-rice, roti-sabzi and a snack often lands around 35–45 g of protein, below the target for most adults. The fix is to add one protein-rich item to each meal rather than overhaul the diet:</p>
<ul class="list">
<li>Swap one katori of rice for an extra katori of dal, rajma or chole.</li>
<li>Add curd or a glass of milk to lunch or dinner.</li>
<li>Add paneer, tofu or soya chunks to one sabzi a day.</li>
<li>Snack on roasted chana, peanuts or sprouts instead of biscuits.</li>
<li>Combine cereals and pulses (dal-chawal, rajma-rice, idli-sambar): together they give a better mix of amino acids.</li></ul></section>
<section><h2 id="quality">Protein quality: why dal-chawal works</h2>
<p>Protein quality depends on how well a food supplies the essential amino acids your body cannot make. Cereals like rice and wheat are low in lysine; pulses are low in methionine. Eaten together, as in dal-chawal, rajma-rice, khichdi or idli-sambar, they cover each other’s gaps. Milk, curd, paneer, eggs, fish and chicken provide complete protein on their own. You do not need to combine foods at every meal; across the day is enough.</p></section>
<section><h2 id="nonveg">If you eat eggs, fish or chicken</h2>
<p>Non-vegetarian foods make the target easier: two eggs give about 12 g, and 100 g of cooked chicken breast or fish gives about 20–30 g. Choose grilled, tandoori or curry preparations over deep-fried ones, and keep pulses and curd in the diet for fibre and variety.</p></section>
<section><h2 id="sample-day">A sample 60 g protein day</h2>
<div class="tw"><table><thead><tr><th>Meal</th><th>What</th><th>Protein</th></tr></thead><tbody>
<tr><td>Breakfast</td><td>2-egg omelette or besan chilla with curd</td><td>12–14 g</td></tr>
<tr><td>Lunch</td><td>2 rotis, 1 katori dal, sabzi, 1 katori curd</td><td>18–21 g</td></tr>
<tr><td>Snack</td><td>Roasted chana or peanuts (30 g), tea with milk</td><td>8–10 g</td></tr>
<tr><td>Dinner</td><td>Rice with paneer sabzi (75 g paneer)</td><td>17–20 g</td></tr>
<tr><td><b>Total</b></td><td></td><td><b>about 55–65 g</b></td></tr></tbody></table></div></section>
<section><h2 id="spread">Spread protein across the day</h2>
<p>Getting 15–30 g at each main meal is easier to digest and more useful than one big protein-heavy dinner. Breakfast is where most Indian diets are lightest, so start there.</p></section>
<section><h2 id="track">How to check what you actually eat</h2>
<p>Most people overestimate their protein. Tracking for even one week shows where the gaps are. <a href="/calorie-protein-tracker">Self Streak’s calorie and protein tracker</a> estimates protein from a photo or a description like “2 rotis, dal and paneer sabzi”, and shows your progress against your daily target.</p></section>
<section><h2 id="mistakes">Common mistakes</h2>
<ul class="list">
<li><b>Counting raw dal weight as cooked.</b> 100 g of raw dal has about three to four times the protein of 100 g of cooked dal.</li>
<li><b>Relying on one big meal.</b> A light breakfast and lunch rarely get made up at dinner.</li>
<li><b>Assuming “healthy” snacks are high-protein.</b> Most biscuits, namkeen and fruit juices add very little.</li>
<li><b>Ignoring older family members.</b> Appetite often falls with age; milk, curd, eggs and soft dals help keep intake up.</li></ul></section>
<section><h2 id="faq">Common questions</h2>
<h3>Do I need protein powder?</h3><p>Not usually. Most people can meet their target from food. Powder is a convenience if you train hard and struggle to eat enough.</p>
<h3>Is too much protein harmful?</h3><p>For healthy adults, intakes up to about 1.6–2 g per kg are commonly used by athletes. People with kidney disease should not raise protein without medical advice.</p></section>
'''),
]
