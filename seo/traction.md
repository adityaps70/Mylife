# Traction outside Google (drafts, 13 Nov 2026)

Nothing here has been posted or submitted. All of it is for the owner to review and publish.

## 1. Play Store listing (com.selfstreak.app)

Status on 13 Nov 2026: `play.google.com/store/apps/details?id=com.selfstreak.app` returns **Not found**, so the app is not public yet (it may be in review or internal testing). Use this copy when the listing goes live. Limits: title 30 characters, short description 80, full description 4,000.

**App name (29):** `Self Streak: Habits & Money`

**Short description (79):** `Habit tracker, expense tracker & bill reminders in one app. Voice logs in Hindi`

**Full description:**

> Self Streak keeps your habits, money and health in one place, built for life in India.
>
> **Habits and streaks**
> • Daily, weekly and monthly habits with streaks and a heatmap
> • Reminders at each habit's own time that skip once it's done
> • Water and protein tracking, a daily XP goal and leagues with friends
>
> **Money in rupees**
> • Log a spend in two seconds: say "450 on Swiggy", snap a receipt, or upload a bank statement (PDF, Excel, CSV)
> • Monthly budget with how much is left per day
> • Credit cards: see what's on this bill and the next one, with a reminder before every due date
> • EMIs and loans in one view, with your debt-free date and an avalanche or snowball payoff plan
>
> **Private by design**
> • No bank login, card number or CVV, ever
> • No SMS reading
> • Export or delete your data from Settings
>
> **Understands English, Hindi and Hinglish.**
>
> Free plan: habits, water, expenses and your streak. Self Streak Plus (₹199 a month, 7 days free, no card needed) adds AI logging by voice and photo, statement import, push reminders and leagues.

**Screenshots (phone, 1080×2340 or similar 9:19.5):** reuse the real demo screens in `public/img/app-*.webp` (taken from the local demo account), in this order, with a one-line caption on top of each:
1. `today` — "Build habits that stick"
2. `activity` — "Log spends by voice, photo or statement"
3. `bills` — "Never miss a bill or card due date"
4. `debt` — "See your debt-free date"
5. `health` — "Water, steps and sleep in one score"
6. `meals` — "Snap your thali, get protein and calories"

Feature graphic (1024×500): the share-card style from `scripts/build-og.py` with "Habits, money and health in one app".

Check before publishing: Play's Data safety form must match the privacy policy (account email, app data synced to your account, microphone and camera for voice and photo logging, steps and sleep from Health Connect if allowed; no SMS, no contacts). The Android manifest has no SMS permission, so "No SMS reading" is accurate.

## 2. Reels / YouTube Shorts (15–30 s each, screen recording + voice)

Record from the local demo account only (never real user data).

1. **"I said it, it logged it."** Hook: "Tracking expenses by typing is why you quit." Show: tap mic, say "did gym, spent 250 on Swiggy" → habit ticked and spend logged. End card: selfstreak.com.
2. **"This bill vs next bill."** Hook: "Swiped your card on the 6th? That's next month's bill." Show the card screen splitting spends across the statement date. End: link to /blog/credit-card-statement-date-vs-due-date.
3. **"Minimum due trap."** Hook: "₹60,000 card bill, paying only the minimum: 12 years." Show the /credit-card-interest-calculator page. (The 141 months / ₹1,11,917 figure is from the guide's worked example.)
4. **"50/30/20 on ₹40k salary."** Show the calculator in /blog/50-30-20-budget-rule-india with ₹40,000, then with rent filled in.
5. **"EMI कैसे निकालें"** (Hindi) — screen-record /hi/emi-calculator with ₹5 lakh, 12%, 5 years → ₹11,122; then add ₹2,000 extra a month.
6. **"Snap your thali."** Photo of a home meal → protein and calories.

Post the same clip to Instagram Reels and YouTube Shorts; put the page URL in the YouTube description and the Instagram bio link.

## 3. Referral incentive

Already built (`src/game.js`, `applyReferral`): a new user who signs up with a friend's code gets **7 extra free days**, and the referrer gets **7 days** added to their trial or paid plan (first 12 referrals), plus a push notification and a friend link.

Proposal (not implemented, needs the owner's decision): raise both rewards to **30 days of Plus**. It's a one-line change of `7 * DAY` to `30 * DAY` in two places, plus the push message and any in-app copy that says "7 free days". Consider the cost: each referral gives away up to ₹199 × 2 of Plus.

## 4. Weekly numbers

`node scripts/weekly-report.mjs` reads the live database (read-only) and writes `seo/reports/traffic-<date>.md`: page views, unique visitors, sign-ups, paid payments, top pages, referrers, devices, countries, with the week before for comparison. Run it every Monday and note changes in `seo/log.md`.
