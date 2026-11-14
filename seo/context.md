# Self Streak: SEO context

Built 2026-11-13 from the code and live site. Every fact has its source. If the product and a page disagree, the product wins.

## Inputs
- Site: https://selfstreak.com
- Product: India-first app for habits and streaks, money (expenses, budgets, bills, EMIs, credit cards, debt payoff) and health (water, meals, protein), with AI logging by voice and photo. Source: `scripts/build_seo.py` (llms.txt text), `public/landing.html`.
- Buyer: young working adults in India who juggle UPI spends, credit cards, EMIs and self-improvement habits, and want one app. Prices are in ₹ and the copy references Swiggy/Zomato, UPI and RBI rules. Source: `scripts/build-pages.py`, `scripts/blog_posts.py`.
- Conversion: trial signup at `/app#signup` (no card needed), then a Plus subscription. Source: `public/landing.html` CTAs.
- Competitors: found on 2026-11-13, see the Competitors section below.
- Ship mode: PR for review. The owner deploys with `npm run deploy` (wrangler).

## Plans and price
- Free plan: the app and manual logging keep working (habits, water, expenses, streak). Source: `src/worker.js:47`, and the pricing FAQ in `public/landing.html`.
- Plus: ₹199/month, paid by autopay (UPI or card) or one month at a time. Includes AI logging, photo scans, reminders (push), leagues. Sources: `wrangler.jsonc` `PRICE_INR`, `public/landing.html`.
- Trial: 7 days with every feature and no card. After it ends you get 3 extra days with everything on, then the free plan. Sources: `wrangler.jsonc` `TRIAL_DAYS`, `public/landing.html` FAQ.
- Push reminders are sent only to Plus, trial or owner accounts. Source: `src/worker.js` `sendDuePushes`.
- Payments go through Cashfree (production) and Razorpay. In-app purchases for the stores are coded but switched off until the store accounts exist. Sources: `wrangler.jsonc`, `mobile/STORE-SETUP.md`.

## Features (from code and pages)
- Habits: daily, weekly, monthly, quarterly or yearly habits, each reminding at its own time. Also streaks, a health score, goals that count themselves, and an AI day summary. Source: `scripts/build-pages.py` habit-tracker.
- Money: expenses logged by voice, receipt photo or bank statement import (PDF/Excel/CSV/photo), with no bank login. Also budgets, bills, EMIs, credit cards with statement-cycle logic, a debt payoff planner (avalanche/snowball), and CSV export. Sources: `README.md`, `scripts/build-pages.py`.
- Health: water reminders and an intake calculator, plus calorie and protein estimates from a plate photo, aimed at Indian food. Source: `scripts/build-pages.py`.
- Platforms: web app (PWA) at /app, with Android and iOS apps (Capacitor) that load selfstreak.com/app. Source: `mobile/capacitor.config.json`.
- Privacy claims: never asks for card numbers, CVV or bank logins. Data is not sold or used for ads. Source: page FAQs in `scripts/build-pages.py`.

## Site mechanics
- Cloudflare Worker (`src/worker.js`) with static assets in `public/`. `/` serves `public/landing.html` to logged-out visitors and the app to logged-in ones.
- SEO pages are generated: `python3 scripts/build-pages.py` builds the feature pages, `/emi-calculator/*`, `/blog/*`, `sitemap.xml` and `llms.txt` (the content is in `scripts/build-pages.py`, `scripts/build_seo.py` and `scripts/blog_posts.py`). Never hand-edit the generated HTML.
- The builder enforces descriptions of 110–160 characters.
- robots.txt allows everything except /app and /api/, and names AI crawlers explicitly. There is an IndexNow key file at `public/51efd8f1dd95adbc4a9dd3e40e8ec21d.txt`.
- Search Console: URL-prefix property `https://selfstreak.com/`, on the first Google account signed in to Chrome. The sitemap was submitted and read successfully on 2026-11-13 (25 URLs).

## Competitors (found 2026-11-13 with web search)
- Money and bills: CRED (reads SMS and email), Walnut/axio (reads SMS), Money Manager (manual), TimelyBills (bill reminders), Pocket Clear (₹149/month Pro, per a third-party roundup).
- Habits: Streaks (iOS only), Loop Habit Tracker (Android, free), Habitify, Habitica.
- Food: HealthifyMe (category leader in India; not yet checked against our pages).
- Angle to own: one app for habits, money and health, with no SMS reading and no bank login, in rupees and for Indian food.

## Data sources
- Search Console: connected through the owner's browser.
- Keyword volume and difficulty: no tool connected. An Ahrefs, Semrush or DataForSEO key would fill the volume and difficulty columns of keyword-map.csv.
- Analytics: none found in the code, so signups by landing page can't be measured.
