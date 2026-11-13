# Backlink strategy: selfstreak.com

Written 2026-11-13. Re-check targets monthly (seo-autopilot Monthly step 5).

## Where we start
- The domain is about 3 months old with no known referring domains. The Pages report showed 0 indexed, but URL Inspection on 2026-11-13 showed the homepage and the main tool pages indexed (the report lags). The goal now is rankings, not just indexing.
- For a site this young, the first 10–20 *real* links matter more than anything on-page: they tell Google the site is a real business worth indexing.
- What we have that earns links: free **EMI calculators for 5 loan types** with ready tables, guides that cite **RBI directions** (statement vs due date, minimum due), **50/30/20 in rupees**, and an app with a clear angle: **habits plus money plus health, no SMS reading, no bank login, free plan, ₹199 Plus**.

## Rules
- **No paid links, PBNs, link farms, Fiverr "100 backlinks" packages, mass link exchanges or comment spam.** On a new domain these get the site ignored or penalised, and they are the fastest way to keep 0 pages indexed.
- Every link should be one a real person would click: a listing, a mention in a relevant article, a cited guide.
- Same name, URL and description everywhere (copy in `directories.md`).
- The owner sends every email, submission and post. Claude drafts.

## Phase 1: foundations (week 1). Easy, owned, trusted
Profiles the owner controls. Most are nofollow, but they're crawlable, confirm the brand is real, and feed the Organization `sameAs`.
| Where | Link to | Notes |
|---|---|---|
| Instagram bio (@selfstreak) | https://selfstreak.com | Already the sameAs profile |
| Google Play listing → Website field | https://selfstreak.com | If the Android app is live. High-trust domain |
| App Store listing → Marketing URL + Support URL | https://selfstreak.com, /contact | If the iOS app is live |
| YouTube channel + the reels in ~/Movies/SelfStreakReels as Shorts | Link in channel About and each description | The reels already exist |
| LinkedIn company page + founder profile "Website" | https://selfstreak.com | Founder post announcing the launch |
| X / Threads profile | https://selfstreak.com | Only if they'll be kept alive |
| Crunchbase company profile | https://selfstreak.com | Free; often ranks for brand queries |
After each profile goes live, add its URL to `ORG["sameAs"]` in `scripts/build-pages.py` and the homepage JSON-LD.

## Phase 2: launch and maker directories (weeks 1–3)
Dofollow or high-traffic listings where indie apps are expected. Spread them over 2–3 weeks so they don't all land in one day.
| Directory | Why | Priority |
|---|---|---|
| Product Hunt | Biggest launch site; auto-creates a hunted.space page too | High. Plan a Tuesday–Thursday launch with the reels as the gallery |
| Peerlist (Projects + Launchpad) | Indian maker community; Indian SaaS gets real users here | High |
| AlternativeTo | Ranks for "CRED alternative", "Walnut alternative", "Loop Habit Tracker alternative". List Self Streak as an alternative to each | High |
| SaaSHub | Free listing plus alternatives pages | Medium |
| There's An AI For That | AI voice and photo logging qualifies; high-DR, real traffic | Medium |
| Indie Hackers (product page + a launch post) | Founder story, dofollow profile | Medium |
| BetaList, Uneed, Microlaunch, Tiny Startups | Small launch sites; each is a real listing | Low (do in a batch) |
| Awesome Tools (awesome-tools skill installed) | Free JSON-API submission with a backlink | Low |

## Phase 3: get into existing roundups (weeks 2–6). The highest-value links
Articles that already rank for "best expense tracker app India" or "best habit tracker" and list competitors. One added line = a link on a page Google already trusts for the exact query.
| Article | Lists | Pitch angle |
|---|---|---|
| LoansJagat: best expense tracker apps in India 2026 (loansjagat.com/financial-glossary/best-expense-tracker-apps-in-india-2026) | Indian expense trackers | Only one in the list that does habits + money with no SMS/bank access; free plan |
| Moneyview: best money management apps in India (moneyview.in/loan-insights/best-money-management-apps-in-india) | Money apps | Bills + EMIs + credit-card cycle logic, built for India |
| Kripesh Adwani: 7 best habit tracker apps (kripeshadwani.com/best-habit-tracker-apps/) | Habitify, Streaks, Loop… | Indian creator; Self Streak is the India-built option with ₹ pricing and money tracking |
| toolfinder.co: best habit trackers (toolfinder.co/best/habit-trackers) | Habit apps | Accepts submissions; streaks + reminders at each habit's time |
| themeaningmovement.com: best habit tracker apps 2026 | Habit apps | Free plan, Android + iPhone + web |
| clickup / toggl / clockify habit tracker lists | Global habit apps | Low odds (vendor blogs), try once with a short note |
Skip lists written by direct competitors (Pocket Clear, Finny, TimelyBills, DhanRakh); they won't add a rival.
Drafts: `outreach/2026-11-13-roundups.md`.

## Phase 4: answer where buyers already ask (ongoing, 2–3 a week)
- **Reddit:** r/personalfinanceindia, r/IndiaInvestments (strict self-promo rules: link the *guide*, not the app, and only when it answers the question), r/getdisciplined, r/habits. Use the reddit-serp skill to find threads that already rank on Google for "expense tracker without SMS", "credit card statement date vs due date", "avalanche vs snowball India".
- **Quora (India-heavy):** questions on EMI prepayment, statement date vs due date, 50/30/20 on an Indian salary. Answer fully, then link the matching guide or calculator.
- These links are nofollow, but they bring real visitors and get the pages crawled.

## Phase 5: linkable assets and PR (month 2+)
- **Credit card interest calculator** (minimum due vs full payment, Indian card rates): finance bloggers link to calculators. It's in the backlog.
- **"State of Self Streak" data post** once there are enough users: anonymised, aggregated, opt-in numbers like "median streak length" or "share of spend on food delivery". Data stories are what journalists at Mint, ET Wealth and Moneycontrol cite. Never publish numbers we don't have.
- **Expert-quote platforms:** Qwoted, Featured.com, SourceBottle. The founder answers personal-finance and habit questions with a byline link.
- **Guest posts and syndication:** LinkedIn articles and Medium posts adapted from the guides, with a link back to the original (canonical where the platform allows).

## Targets
| By | Referring domains | Pages indexed |
|---|---|---|
| 2026-12-13 (30 days) | 10+ | 10+ |
| 2027-02-13 (90 days) | 25+, including 3+ from roundups | all 26 |
Track in `seo/reports/`. Search Console → Links shows referring domains as Google sees them (it lags 1–2 weeks).

## First 7 days, in order
1. ~~Request indexing~~ Done 2026-11-13 (5 recrawls requested; all 6 main pages already indexed).
2. Add the website link to Instagram, Play Store and App Store listings, LinkedIn.
3. Peerlist project + AlternativeTo listing (alternative to CRED, Walnut, Loop, Habitify).
4. Send the 3 roundup pitches marked "send first" in `outreach/2026-11-13-roundups.md`.
5. Upload 3 reels as YouTube Shorts with the link in the description.
6. Pick a Product Hunt launch date 2–3 weeks out; prepare gallery from the reels and app screenshots.
