# SEO backlog

Ordered by expected signups per hour of work. Context: on 2026-11-13 the Pages report showed 0 indexed, but URL Inspection the same day showed the homepage and the main tool pages indexed. The report lags. On-page basics are fine. The site is about 3 months old and has no known backlinks, so Google doesn't trust it yet. Until pages are indexed, nothing else on this list can bring traffic.

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
9. **Thicken /expense-tracker (398 words) and /debt-payoff-planner (431 words)** with real product screenshots and one worked example each. The owner needs to supply screenshots.
10. **Article: credit card minimum due interest in India.** Show the real cost of paying only the minimum, with RBI-sourced rules. Links to item 7.

## Later
11. **Comparison: Loop Habit Tracker / Streaks alternative**, for Android plus iPhone with money and health in the same app.
12. **`/index.html` returns 307 → /** (Cloudflare's default asset handling). It's harmless, but a 301 would be cleaner.
13. **Add analytics** (for example Cloudflare Web Analytics) so signups can be attributed to landing pages.
