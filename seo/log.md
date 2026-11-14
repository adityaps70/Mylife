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
