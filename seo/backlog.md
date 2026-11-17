# SEO backlog

## Resolved 2026-11-14
The out-of-date copy was merged with main and deployed; `npm run deploy` now refuses copies that are behind GitHub or have uncommitted changes.

## Now
1. ~~Request indexing~~ Done 2026-11-13. URL Inspection showed `/`, `/emi-calculator`, `/emi-calculator/home-loan`, `/habit-tracker`, `/expense-tracker` and `/credit-card-bill-reminder` already **indexed**; the Pages report (0 indexed) was lagging. Recrawl requested for the first 5. The 6th hit the daily quota, but it's indexed anyway.
2. **Owner: deploy** branch `live-site-sync` (www/http redirects, pricing FAQ fixes). After deploying, check that `curl -I http://selfstreak.com/habit-tracker` and `curl -I https://www.selfstreak.com/habit-tracker` both return 301.
3. **First links (authority).** Follow `backlinks.md` (phases 1–3): owned profiles, Peerlist and AlternativeTo, then the 3 roundup pitches in `outreach/2026-11-13-roundups.md`. The owner sends; the copy is drafted.
4. **Ping IndexNow on deploy.** The key file already exists, so add a step after `wrangler deploy` that POSTs the sitemap URLs to api.indexnow.org. This gets Bing, Yandex and the AI search engines that use Bing indexed within days.

## Next
5. **Comparison page: /cred-alternative.** Query: "cred alternative" / "app like cred without sms access". Angle: tracks bills and spends without reading SMS or email. Be fair: CRED pays bills and gives rewards; we don't.
6. **Comparison page: /walnut-alternative.** The same no-SMS angle, plus habits and health in one app.
7. **Free tool: credit card interest calculator** (minimum due vs full payment, for Indian card rates). Close to the credit-card page and blog post; works without signup.
8. **Add a 50/30/20 calculator** to `/blog/50-30-20-budget-rule-india` (enter salary → see three rupee buckets).
9. **Thicken /debt-payoff-planner** (/expense-tracker got a no-SMS section and worked example on 2026-11-14; screenshots still wanted). Was: /expense-tracker (398 words) and /debt-payoff-planner (431 words)** with real product screenshots and one worked example each. The owner needs to supply screenshots.
10. ~~Article: credit card minimum due interest~~ Dropped 2026-11-14: /credit-card-interest-calculator owns this query. Was: **Article: credit card minimum due interest in India.** Show the real cost of paying only the minimum, with RBI-sourced rules. Links to item 7.

## Added 2026-11-14 (habit + money keywords)
- [x] ~~Request indexing for /habit-and-money-tracker and /health-and-finance-tracker~~ Already indexed (URL Inspection, 2026-11-17).
- [ ] /habit-tracker: add an Android app section (direct download from /download) and a "daily routine" section for "habit tracker app for android" and "daily routine habit tracker app".
- [ ] Links for the new pages: list Self Streak on AlternativeTo and Product Hunt as a "habit and money tracker"; pitch roundups of "habit tracker + budget app" lists (see backlinks.md).
- [ ] Article idea: "Money habits that actually stick (and how to track them)" targeting "money habits tracker" / "spending habits tracker", linking to /habit-and-money-tracker.
- [ ] Check positions for the new keyword rows in 3–4 weeks.

## Later
11. **Comparison: Loop Habit Tracker / Streaks alternative**, for Android plus iPhone with money and health in the same app.
12. **`/index.html` returns 307 → /** (Cloudflare's default asset handling). It's harmless, but a 301 would be cleaner.
13. **Add analytics** (for example Cloudflare Web Analytics) so signups can be attributed to landing pages.

## Added 2026-11-13
- [ ] Re-check comparison page facts (CRED, axio, Loop) every 3 months; update AS_OF in scripts/build_compare.py.
- [ ] Re-read bank MITC PDFs every 6 months (scripts/build_compare.py BANKS).
- [ ] Decide on referral reward (7 days now; proposal: 30 days of Plus for both) — seo/traction.md.
- [ ] Publish the Play Store listing using seo/traction.md once the app is approved.
- [ ] Record reels from the local demo account (scripts in seo/traction.md).
- [ ] Run `npm run report` every Monday.

## Added 2026-11-15 (templates and competitor pages)
Shipped: /habit-tracker-template and /budget-template-india (free .xlsx), /blog/habit-tracker-app-vs-excel, /habitify-alternative, /streaks-app-alternative. Search volumes are "unknown" because no keyword tool is connected; Search Console impressions will show which of these to push.
Next, one per autopilot run, highest value first:
- [x] ~~Request indexing for /budget-template-india, /blog/habit-tracker-app-vs-excel, /habitify-alternative, /streaks-app-alternative~~ Done 2026-11-16.
- [ ] Printable PDF version of the habit tracker on /habit-tracker-template ("habit tracker printable", "habit tracker pdf").
- [x] ~~EMI tracker Excel template~~ Shipped 2026-11-16 as /emi-tracker-template.
- [x] ~~Credit card tracker Excel~~ Shipped 2026-11-17 as /credit-card-tracker-template.
- [ ] Debt snowball / avalanche spreadsheet on /debt-payoff-planner ("debt snowball spreadsheet").
- [ ] "Notion habit tracker vs app" guide, honest about when Notion is enough ("notion habit tracker template").
- [ ] 30-day challenge tracker template + guide ("30 day challenge tracker", "75 day challenge tracker").
- [ ] Study habit tracker for students guide ("study habit tracker").
- [ ] Hindi versions of the two template pages (/hi/habit-tracker-template, /hi/budget-template-india) with hreflang.
- [ ] Competitor pages only with sourced facts and an "as of" date: HealthifyMe (calories/protein), Money Manager (expenses), Fabulous (habits). Each must say where the competitor is better.
- [ ] Get links to the templates: submit to template roundups and Reddit threads answering "habit tracker excel" questions (draft only, owner posts).

## Added 2026-11-16
- [ ] Weekly run (due 2026-11-20, as the last report is from 13 Nov): /streaks-app-alternative is "Crawled – currently not indexed". Check whether it's thin next to /habitify-alternative and /loop-habit-tracker-alternative, and add unique content or more internal links.
- [ ] Link /emi-tracker-template from the 5 /emi-calculator/* loan pages (body sentence near "Once you have the loan"), so it gets more than 3 internal links.
- [ ] Hindi version /hi/emi-tracker-template ("emi tracker excel hindi"), next to /hi/emi-calculator.
- [x] ~~Next template: credit card tracker Excel~~ Shipped 2026-11-17.

## Added 2026-11-17
- [x] ~~Request indexing for /credit-card-tracker-template and /emi-tracker-template~~ 2026-11-17: requested for /credit-card-tracker-template ("URL is unknown to Google"); /emi-tracker-template was already indexed. Search Console works on authuser=0: open https://search.google.com/search-console?resource_id=https%3A%2F%2Fselfstreak.com%2F&authuser=0 and use the top search bar (the direct /inspect?id= URL returns a Google 404).
- [ ] Weekly run is due 2026-11-20: page 2 → page 1, /streaks-app-alternative "Crawled – not indexed", AI answer check (ai-prompts.md not checked yet), competitor sitemap diffs, report.
- [ ] Next template: debt snowball / avalanche spreadsheet on /debt-payoff-planner ("debt snowball spreadsheet").
- [ ] Link /emi-tracker-template and /credit-card-tracker-template from /blog/credit-card-statement-date-vs-due-date and the 5 /emi-calculator/* loan pages.
- [ ] Sign-ups per 100 visitors fell to 3.7 (10–17 Nov) from 23.8 the week before, on a much bigger visitor count (82 vs 21). Most views are the homepage; check where the new visitors come from before reading anything into it.
