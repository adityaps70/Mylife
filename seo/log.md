# SEO log

- 2026-11-13: Synced the live site's code to GitHub on branch `live-site-sync`. Before this, the blog, the EMI pages, llms.txt and the worker changes were only in an uncommitted local copy.
- 2026-11-13: www, http and workers.dev copies of every page, plus /landing, now 301 to https://selfstreak.com (`src/worker.js`, `wrangler.jsonc` run_worker_first). Before this, only the homepage redirected.
- 2026-11-13: Fixed pricing FAQs that said there is no free plan on /habit-tracker, /credit-card-bill-reminder and /calorie-protein-tracker (the code has a free plan, `src/worker.js:47`).
- 2026-11-13: Surfaced the free plan on /habit-tracker (meta description) and /expense-tracker (new FAQ and FAQ schema).
- 2026-11-13: Organization JSON-LD now has sameAs (Instagram) and founder. Blog posts have a Person author (Aditya Pratap Singh, /about) instead of the Organization.
- 2026-11-13: Dates are real: scripts/page-dates.json stores a content hash per URL, so dateModified, "Updated" and sitemap lastmod only change when the page changes. Blog datePublished is fixed per post.
- 2026-11-13: New /about page (author bio) and a styled 404 page that keeps the 404 status (assets.not_found_handling) and links to tools and guides.
- 2026-11-13: og-image.png went from 293 KB to 92 KB. Added per-page share images for 20 pages (public/og/, made by scripts/build-og.py).
- 2026-11-13: Images, icons and fonts are now cached for a year (immutable) via public/_headers.
- 2026-11-13: Each tool page links to 2 related guides, and each guide has a "Related guides" block led by its tool page. Each EMI loan page links to 2 guides.
- 2026-11-13: Added real app screenshots (WebP, alt, width/height, lazy) to the homepage, 7 tool pages and 5 loan pages. They come from a local demo account via scripts/app-screenshots.py.
- 2026-11-13: /privacy and /contact titles are now 49 and 55 characters.
- 2026-11-13: Wrote seo/backlinks.md (5-phase plan, 30/90-day targets), drafted 3 roundup inclusion pitches, expanded directories.md.
- 2026-11-13: URL Inspection: /, /emi-calculator, /emi-calculator/home-loan, /habit-tracker, /expense-tracker and /credit-card-bill-reminder are indexed (the Pages report still said 0; it lags). Requested recrawls for the first 5; the 6th hit the daily quota.

## 2026-11-13 (traction round)
- Bing Webmaster Tools: site + sitemap already in place. IndexNow had never been used: added `scripts/indexnow.mjs` (runs after every `npm run deploy`, pings only URLs whose lastmod changed). First ping: 200 for 26 URLs.
- New pages: /cred-alternative, /walnut-alternative, /loop-habit-tracker-alternative (sourced, "as of 13 Nov 2026", each says when the other app is better); /credit-card-interest-calculator (minimum due vs full, 18% GST on interest); /credit-card-statement-date/{hdfc-bank,sbi-card,icici-bank,axis-bank} (facts only from each bank's MITC/FAQ).
- 50/30/20 calculator embedded in /blog/50-30-20-budget-rule-india.
- Hindi: /hi/emi-calculator and /hi/blog/credit-card-statement-date-vs-due-date, hreflang en-IN/hi-IN/x-default on both language versions, "हिंदी में पढ़ें" link on the English pages.
- `npm run report` (scripts/weekly-report.mjs): weekly views/visitors/sign-ups from D1. First week: 144 views, 82 visitors, 7 sign-ups, 0 paid; Google sent 3 views.
- Play Store: com.selfstreak.app is not public yet (404). Listing copy, reel scripts and referral proposal drafted in seo/traction.md.

## 2026-11-14 (daily autopilot, NOT deployed)
- **Live site regressed.** A deploy at 2026-11-14 10:16 UTC (sw cache `selfstreak-mwg92nqd`, not from `main`) replaced the site with a copy that has newer app work ("Speak a spend" quick-log, new rings, insight cards) but none of the 13 Nov SEO commits. Live now: /cred-alternative, /walnut-alternative, /loop-habit-tracker-alternative, /credit-card-interest-calculator, the 4 /credit-card-statement-date/* pages, /hi/*, /about → 404; live sitemap 25 URLs (main has 36); http:// and www. return 200 instead of 301; Organization sameAs/founder gone from the homepage. Deploying `main` would roll back the owner's new app features, so the autopilot did not deploy.
- /expense-tracker: new section "An expense tracker without SMS permission" (verified against `mobile/android/app/src/main/AndroidManifest.xml`: no SMS permission), a worked one-month example, a "Does Self Streak read my SMS?" FAQ (FAQ schema), and links to /walnut-alternative, /cred-alternative and the 50/30/20 calculator. On branch `seo/auto-2026-11-14`.
- Backlog item 10 (minimum-due article) dropped: /credit-card-interest-calculator already owns "minimum due credit card interest"; a second page would cannibalise it.
- Health check (live): the 25 sitemap URLs all return 200 in <0.65 s, canonicals correct, no noindex.
- `npm run report` (7 days to 14 Nov): 166 views, 92 visitors, 8 sign-ups, 0 paid; google.com sent 3 views. Saved in reports/traffic-2026-11-14.md.
- Search Console / Bing: skipped today; requesting indexing makes no sense while the new pages 404 and today's change isn't live.

## 2026-11-14 (fix + indexing)
- Live site restored: the out-of-date copy (Self Streak Main session folder) was merged with GitHub main and seo/auto-2026-11-14, then deployed. All 36 sitemap URLs return 200; www/http redirect again.
- Search Console: indexing requested for all 10 new pages (credit-card-interest-calculator, hi/emi-calculator, cred-alternative, hi/blog/credit-card-statement-date-vs-due-date, walnut-alternative, loop-habit-tracker-alternative, credit-card-statement-date/{hdfc-bank,sbi-card,icici-bank,axis-bank}). Each showed "URL is unknown to Google" before the request.
- Deploy guard added (scripts/predeploy-check.mjs): `npm run deploy` refuses to deploy a copy that is behind GitHub main or has uncommitted changes, and now pushes to main after deploying.

## 2026-11-14 (habit + money keywords)
- New page /habit-and-money-tracker: primary "habit and money tracker"; also habit and finance / budget / expense tracker, money and habit tracker, money habits tracker. Answers in the first paragraph, money-habit list, two-apps-vs-one table, FAQ schema, 3 app screenshots, share image.
- New page /health-and-finance-tracker: primary "finance and health tracker" / "health and finance app". Health side (water, meals, protein, Health Connect steps and sleep) and money side (spending, budget, bills, net worth).
- Homepage title: "Self Streak: Habit, Money & Health Tracker App India" (was "Habit Tracker, Expense & EMI App India"); expense and EMI queries are owned by their own pages.
- Contextual links to the new pages from /habit-tracker, /expense-tracker, /calorie-protein-tracker and the homepage footer; every feature page lists them under "More".
- Sitemap now 38 URLs (was 36). Keyword research: Google autocomplete (gl=in) and web search; SERPs for these queries are mostly iPhone App Store listings (Snowballer, HabitGenius, Wealthy, TRAKL) with few web pages.

## 2026-11-15 (templates + competitor pages)
- Shipped and deployed: /habit-tracker-template (free 12-month habit tracker .xlsx with automatic streaks), /budget-template-india (free rupee budget .xlsx with expenses log and 50/30/20 check), /blog/habit-tracker-app-vs-excel, /habitify-alternative, /streaks-app-alternative. Linked from /habit-tracker and /expense-tracker. Sitemap 44 URLs; IndexNow 200 for 15 URLs.
- Template formulas checked with the `formulas` library (days done, %, best streak, February length, budget totals).
- Search Console: indexing requested for /habit-tracker-template. Daily quota hit on the next request.

## 2026-11-16 (daily autopilot, deployed)
- Shipped and deployed: /emi-tracker-template, a free EMI tracker .xlsx (self-streak-emi-tracker.xlsx). Every loan in one sheet (EMI, EMIs paid, outstanding today, interest paid and left, last EMI, debt-free month, EMIs as % of salary), plus a Schedule tab per loan with a prepayment column. Targets "emi tracker excel", "loan tracker excel", "multiple loan emi tracker". Formulas checked with the `formulas` library against a Python reference (EMI ₹34,713 and outstanding ₹37,79,707 for the ₹40 lakh example; a ₹2 lakh prepayment at EMI 12 → 214 EMIs, ₹7,13,106 less interest).
- Links to it from /emi-calculator and /debt-payoff-planner (Related guides) and /budget-template-india (body). Sitemap 45 URLs; IndexNow 200 for 18 URLs.
- Search Console: indexing requested for /budget-template-india, /blog/habit-tracker-app-vs-excel, /habitify-alternative, /streaks-app-alternative (all were "Discovered/Crawled – currently not indexed") and /emi-tracker-template ("unknown to Google"). /streaks-app-alternative is "Crawled – currently not indexed", so Google has seen it and passed. Review its content and links at the weekly run.
- Health check: all 44 live sitemap URLs returned 200 with correct canonicals and no noindex before the deploy; http:// and www. still 301.
- No facts changed in commits since the last run (only the habit template's ✓ redesign).
- `npm run report` (9–16 Nov): 186 views, 102 visitors, 8 sign-ups, 0 paid; google.com sent 3 views. Saved in reports/traffic-2026-11-16.md.

## 2026-11-17 (daily autopilot, deployed)
- Shipped and deployed: /credit-card-tracker-template, a free credit card tracker .xlsx (self-streak-credit-card-tracker.xlsx). Up to 10 cards: last statement, last bill (from logged spends) and its due date, next statement, what's on the next bill so far, next payment due, interest-free days if you buy today, best day to buy next, limit used and utilisation (warning level set by the user). A Spends tab puts each purchase on the right statement. Targets "credit card tracker excel", "credit card due date tracker", "multiple credit card tracker". The top Google results are generic US/blog templates that list cards and dates; none works out this bill vs next bill or interest-free days.
- Formulas checked with the `formulas` library against hand calculations as of 17 Nov 2026 (e.g. SBI example: statement 15th, due 5th → last bill ₹8,750 due 5 Dec, 49 interest-free days if bought today). Statement days 29–31 clamp to month end.
- RBI "at least a fortnight to pay" rule cited to the Master Direction (rbi.org.in id=12300). The HDFC 4th/24th example comes from HDFC's MITC, already sourced on /credit-card-statement-date/hdfc-bank.
- Links to it from /credit-card-bill-reminder (Related guides), the 4 /credit-card-statement-date/* pages and /budget-template-india. Sitemap 46 URLs; IndexNow 200 for 10 URLs.
- Health check (before deploy): all 45 live sitemap URLs returned 200 with correct canonicals and no noindex; http:// and www. still 301.
- No product facts changed in commits since the last run.
- Search Console: **not done.** authuser=0 (the account that owns the property per earlier runs) sent the Chrome tab back to a new-tab page 3 times; authuser=1 has no properties, and 2 and 3 say "you don't have access". No indexing requested. Bing Webmaster: 0 clicks and 0 impressions (14–15 Nov).
- `npm run report` (10–17 Nov): 161 views, 82 visitors, 3 sign-ups, 0 paid; google.com sent 4 views. Saved in reports/traffic-2026-11-17.md.

## 2026-11-17 (manual, owner request)
- Search Console URL Inspection: requested indexing for /credit-card-tracker-template (was unknown to Google) and a recrawl of /habit-tracker-template (✓ tick redesign). Already indexed: /emi-tracker-template, /habit-and-money-tracker, /health-and-finance-tracker. Overview showed 22 indexed, 13 not indexed.

## 2026-11-18 (daily autopilot, deployed)
- Shipped and deployed: /debt-snowball-spreadsheet, a free debt snowball and avalanche spreadsheet in rupees (self-streak-debt-payoff-planner.xlsx). Up to 10 debts; avalanche, snowball and minimums-only plans side by side (debt-free month, total interest, saving vs minimums), the month each debt is cleared, and a 360-month plan tab for each. Targets "debt snowball spreadsheet", "debt avalanche spreadsheet", "debt payoff spreadsheet". The top Google results are US-dollar templates, some behind an email or a paywall; none is in rupees or shows the three plans side by side.
- Formulas checked with the `formulas` library against a Python month-by-month simulation. The example (card ₹60,000 at 42%, personal loan ₹1,50,000 at 14%, phone EMI ₹20,000 at 16%, ₹20,000 a month) reproduces /blog/debt-avalanche-vs-snowball exactly: avalanche 13 months ₹23,584, snowball 13 months ₹25,229, minimums only 30 months ₹66,935. Edge cases checked: monthly amount below the minimums (red warning, plans pay minimums) and a 0% debt with no minimum.
- Links to it from /debt-payoff-planner (Related guides), /blog/debt-avalanche-vs-snowball (body), /emi-tracker-template and /credit-card-tracker-template (body). Sitemap 47 URLs; IndexNow 200 for 11 URLs.
- Health check (before deploy): all 46 live sitemap URLs returned 200 in under 0.71 s with correct canonicals and no noindex; http:// and www. still 301.
- No product facts changed in commits since the last run (only SEO log commits).
- Search Console (authuser=0, property https://selfstreak.com/): indexing requested for /debt-snowball-spreadsheet ("URL is unknown to Google") and a recrawl of /blog/debt-avalanche-vs-snowball (indexed). Overview: 22 indexed, 13 not indexed, 2 web search clicks.
- `npm run report` (11–18 Nov): 108 views, 53 visitors, 1 sign-up, 0 paid; google.com sent 3 views. Saved in reports/traffic-2026-11-18.md.

## 2026-11-19 (daily autopilot, deployed)
- Shipped and deployed: internal links to the three newest templates. /emi-tracker-template is now linked from all 5 /emi-calculator/* loan pages (home, car, personal, education, two-wheeler); /credit-card-tracker-template from /blog/credit-card-statement-date-vs-due-date (interest-free period section); /debt-snowball-spreadsheet from /budget-template-india and /credit-card-interest-calculator ("Three ways out"). 8 pages changed; IndexNow 200 for 13 URLs. Closes the open link items from 17 and 18 Nov.
- Local checks before deploy: all 8 pages 200 on wrangler dev with correct title, canonical and parseable JSON-LD; nothing under src/, schema.sql or wrangler.jsonc changed. Live after deploy: the 4 spot-checked pages return 200 with the new links.
- Health check (before deploy): all 47 live sitemap URLs returned 200 in under 0.47 s with correct canonicals and no noindex; http:// and www. still 301.
- No product facts changed in commits since the last run (only SEO commits).
- Search Console (authuser=0, property https://selfstreak.com/): /debt-snowball-spreadsheet is already indexed (requested yesterday). Recrawl requested for /emi-calculator/home-loan and /blog/credit-card-statement-date-vs-due-date (both indexed). Overview: 22 indexed, 13 not indexed, 3 web search clicks (9–17 Nov). Bing Webmaster not checked today.
- `npm run report` (12–19 Nov): 82 views, 40 visitors, **0 sign-ups**, 0 paid; google.com sent 2 views; 54 of 82 views are the homepage. Saved in reports/traffic-2026-11-19.md.

## 2026-11-21 (daily + weekly autopilot, deployed)
- Page 2 → page 1: Search Console (28 days to 18 Nov) shows ~40 bank "billing cycle" / "statement date" queries at positions 5–17 with 0 clicks. Shipped: the 4 /credit-card-statement-date/* pages now say "Billing Cycle & Due Date" in the title, have the H1 "<Bank> credit card billing cycle, statement date and due date" and an opening paragraph that answers it, a "How to change your <Bank> billing cycle" section, and FAQs on bill generation and grace period (from the MITC facts already on each page; the RBI one-time-change rule is cited on the page). /blog/credit-card-statement-date-vs-due-date links all 4 with "billing cycle" anchors; llms.txt and /credit-card-bill-reminder anchors updated.
- Internal links: the 5 comparison pages link their matching free template (habit, budget, credit card tracker); /blog/how-long-does-it-take-to-form-a-habit links /habit-tracker-template and /blog/habit-tracker-app-vs-excel. /habit-tracker-template had only 2 inbound links.
- Local checks: 11 changed pages 200 on wrangler dev, correct titles (≤60), canonicals and parseable JSON-LD; nothing under src/, schema.sql or wrangler.jsonc changed. Deployed; IndexNow 200 for 18 URLs. Live spot-check: the 4 bank pages and the blog link are live.
- Health check (before deploy): all 47 sitemap URLs 200, canonicals correct, no noindex; http:// and www. 301. No product facts changed (no commits since 19 Nov).
- Search Console (authuser=0, property https://selfstreak.com/): Pages report 44 indexed, 2 not indexed (was 22/13). Indexing requested for the 4 bank pages (all indexed) and /blog/habit-tracker-app-vs-excel ("Crawled – currently not indexed", last crawl 16 Nov, found only via the sitemap). /credit-card-tracker-template inspected: indexed (Pages report lags). /streaks-app-alternative is no longer in the not-indexed list.
- Bing Webmaster (14–19 Nov): 6 impressions, 0 clicks.
- Competitors: habitify.me +8 URLs (Black Friday pages only); pocketclear.app +9 (posts incl. "switching from Money Manager", "budgeting app for couples"; help pages; /tools/); timelybills.app +40 (budget, net worth and retirement calculators in 10 languages; new English /networth-calculator). Snapshots updated.
- AI answers: not checked (no assistant access in unattended runs). A Google search for "best habit tracker app India habits and expenses together" did not show Self Streak.
- `npm run report` (14–21 Nov): 33 views, 25 visitors, 0 sign-ups, 0 paid. Saved in reports/traffic-2026-11-21.md. Weekly report: reports/2026-11-21.md.

## 2026-11-22 (daily autopilot, deployed)
- Shipped and deployed: /emi-calculator/education-loan now covers the moratorium. New "Education loan EMI after the moratorium" section: the EMI is worked out on the loan plus unpaid moratorium interest, with SBI's terms as the sourced example (simple interest during the moratorium, unpaid interest added at repayment, EMIs from 12 months after the course or 6 months after a job; 1% concession if interest is paid during the course; sbi.co.in Student Loan Scheme, as of 22 Nov 2026). Worked table for ₹15 lakh at 10.5%, 2-year course + 12 months, 10 years: pay nothing → ₹4,72,500 interest added, EMI ₹26,616; pay interest monthly (₹13,125) → EMI ₹20,240, about ₹2,92,581 less in total. Two new FAQs (in FAQPage JSON-LD). Title now "Education Loan EMI Calculator with Moratorium | Self Streak". Top results checked first (ICICI, IDFC FIRST, Lemonn, WeMakeScholars, EZTax): bank calculators mention the moratorium but few show the cost of not paying interest side by side.
- Builder change: LOANS entries accept optional title, desc and mor; only the education page changed (other loan pages byte-identical, no false lastmod bump).
- Local checks: page 200 on wrangler dev, title 59 chars, canonical correct, JSON-LD parses (WebPage, FAQPage, BreadcrumbList); nothing under src/, schema.sql or wrangler.jsonc changed. Deployed; IndexNow 200 for 12 URLs; live page shows the new title and section.
- Health check (before deploy): all 47 live sitemap URLs 200 (slowest 0.87 s), canonicals correct, no noindex; http:// and www. 301.
- No product facts changed in commits since the last run (only SEO commits).
- Search Console (authuser=0, property https://selfstreak.com/): /emi-calculator/education-loan is indexed; recrawl requested ("added to a priority crawl queue"). Overview: 44 indexed, 2 not indexed, 3 web search clicks. Bing not checked today.
- `npm run report` (15–22 Nov): 25 views, 21 visitors, 0 sign-ups, 0 paid; google.com sent 4 views. Saved in reports/traffic-2026-11-22.md.

## 2026-11-23 (daily autopilot, deployed)
- Shipped and deployed: /blog/credit-card-statement-date-vs-due-date now answers "what is statement date credit card" (23 impressions at position 68). New H1 "What is a credit card statement date? Statement date vs due date"; the first paragraph defines the statement date (last day of the billing cycle, when the bill is generated) and the due date in two sentences; the statement-date section adds the synonyms (billing date, bill generation date, closing date) and "where to find it" (on the statement and in the bank app); new FAQ "What is the statement date on a credit card?". Title unchanged (it holds the "vs due date" query). Top results checked first (NerdWallet, Chase, Amex, Citi, Paytm): all are short definition pages using "closing date"; none is India-specific with RBI rules.
- 8 other pages changed only because they link the guide with its H1 as anchor text (/blog, /about, /404, 2 blog posts, /credit-card-bill-reminder, /debt-payoff-planner, /expense-tracker), so the anchor now carries the query.
- Local checks: all 9 pages 200 on wrangler dev, titles ≤60, canonicals correct, JSON-LD parses; nothing under src/, schema.sql or wrangler.jsonc changed. Deployed; IndexNow 200 for 9 URLs; live H1 confirmed.
- Health check (before deploy): all 47 live sitemap URLs 200 (slowest 1.03 s), canonicals correct, no noindex; http:// and www. 301.
- No product facts changed in commits since the last run (only SEO commits).
- Search Console (authuser=0, property https://selfstreak.com/): the guide is indexed; recrawl requested ("added to a priority crawl queue"). Overview: 44 indexed, 2 not indexed, 3 web search clicks. Bing not checked today.
- `npm run report` (16–23 Nov): 23 views, 19 visitors, 0 sign-ups, 0 paid; google.com sent 3 views; /credit-card-tracker-template got 4 views. Saved in reports/traffic-2026-11-23.md.

## 2026-11-24 (daily autopilot, deployed)
- Shipped and deployed: https://selfstreak.com/net-worth-calculator, a free net worth calculator in rupees (no sign-up; numbers stay in the browser's localStorage). 8 asset boxes (savings, FDs/RDs, mutual funds and shares, EPF/PPF/NPS, gold, home you live in, other property, vehicles) and 5 debt boxes, plus optional monthly expenses. Outputs: net worth, total assets, total debts, net worth without your home (home and home loan left out), money you can reach in a few days, months of expenses it covers, debts as % of assets. Targets "net worth calculator india". Structured data: WebPage, WebApplication (free), FAQPage (6 questions), BreadcrumbList. Share image added.
- Top results read first (sum.money, SEBI Investor, fincalculator.in, Fermor, TimelyBills; ClearTax's page returns 410): all give one net worth figure from a list of boxes. SEBI leaves the home out, the others count it; none shows both figures side by side or turns ready money into months of expenses. The only outside fact on the page is SEBI's "Real Estate (not the house you live in)" label, cited and dated 24 Nov 2026. No net-worth-by-age benchmarks: no source we can stand behind.
- Links to it from /expense-tracker, /debt-payoff-planner, /emi-calculator, /habit-and-money-tracker (Related guides), /health-and-finance-tracker (Related guides and the net worth card) and llms.txt. Sitemap 48 URLs.
- Share images re-rendered for the statement date guide and the 4 bank pages, whose H1s changed on 21 and 23 Nov (the images still showed the old headings).
- Local checks: 6 changed pages 200 on wrangler dev, titles ≤60, canonicals correct, JSON-LD parses; calculator tested in a browser (example gives ₹35,60,000 / ₹17,60,000 / 15 months / 56%; negative net worth and Clear work); nothing under src/, schema.sql or wrangler.jsonc changed. Deployed; IndexNow 200 for 12 URLs; live page confirmed.
- Health check (before deploy): all 47 live sitemap URLs 200 (slowest 0.67 s), canonicals correct, no noindex, no duplicate titles; http:// and www. 301.
- No product facts changed in commits since the last run (only SEO commits).
- Search Console (authuser=0, property https://selfstreak.com/): /net-worth-calculator was "URL is unknown to Google"; indexing requested ("added to a priority crawl queue"). Overview: 44 indexed, 2 not indexed, 3 web search clicks. Bing not checked today.
- `npm run report` (17–24 Nov): 23 views, 19 visitors, 0 sign-ups, 0 paid; google.com sent 4 views, l.instagram.com 2. Saved in reports/traffic-2026-11-24.md.
