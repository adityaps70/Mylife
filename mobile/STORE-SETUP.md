# Turning on Plus purchases in the iPhone and Android apps

The code is ready. Purchases stay switched off (the apps keep the current Razorpay/Cashfree flow) until the
store accounts below are set up and the keys are added to the server. Each step needs your own account, so
only you can do them.

Use the same product ID in both stores: **`plus_monthly`**. On Google Play the base plan ID is **`monthly`**.
(If you pick different IDs, set `STORE_PRODUCT_ID` / `PLAY_BASE_PLAN` in `wrangler.jsonc` to match.)

## Apple (App Store Connect)

1. **Agreements, Tax, and Banking**: accept the *Paid Apps* agreement and add your bank and tax details.
   Nothing can be sold until this is active.
2. Optional but worth it: join the **App Store Small Business Program** (Apple takes 15% instead of 30%).
3. **Your app → Monetization → Subscriptions**: create a subscription group (for example "Self Streak Plus"),
   then a subscription with product ID `plus_monthly`, duration 1 month, price ₹199 (or your choice).
   Add a display name, a description and the review screenshot Apple asks for.
4. **Users and Access → Integrations → In-App Purchase**: generate a key. Download the `.p8` file
   (you can only download it once) and note the **Key ID** and the **Issuer ID** shown on that page.
5. Add the keys to the server. Run these in a terminal in the `Mylife` folder and paste each value when asked.
   For the private key, paste the whole contents of the `.p8` file.
   ```
   npx wrangler secret put APPLE_IAP_KEY_ID
   npx wrangler secret put APPLE_IAP_ISSUER_ID
   npx wrangler secret put APPLE_IAP_PRIVATE_KEY
   ```
6. To test before release: **Users and Access → Sandbox → Testers**, create a sandbox tester, then on your
   iPhone go to Settings → App Store → Sandbox Account and sign in with it. Purchases in the dev build are free.

## Google (Play Console)

1. **Settings → Payments profile**: set up the merchant account (bank and tax details).
2. **Your app → Monetize → Subscriptions**: create a subscription with product ID `plus_monthly`, add a
   base plan with ID `monthly`, auto-renewing every 1 month, price ₹199. Activate it.
   (Play only shows subscriptions once an app bundle with billing has been uploaded to a testing track:
   upload the new build to Internal testing first.)
3. In **Google Cloud Console** (the project linked to Play): create a **service account**, create a JSON key
   for it, and enable the *Google Play Android Developer API*.
4. **Play Console → Users and permissions**: invite the service account's email and give it
   *View financial data* and *Manage orders and subscriptions* for this app.
5. Add the key to the server (paste the whole JSON file contents):
   ```
   npx wrangler secret put GOOGLE_PLAY_SA_JSON
   ```
6. To test: **Settings → License testing**, add your Google account. Test purchases are then free.

## After the keys are in

- Ship the new app builds (iOS build with the purchase plugin and offline mode; Android build with Play Billing).
- In the apps, Plus buttons switch to the App Store / Google Play automatically once the server has the keys.
  The website keeps Razorpay and Cashfree.
- Renewals and cancellations are checked with Apple/Google automatically when someone's month is about to end.
- Apple requires a **Restore purchase** button and the renewal wording on the purchase screen: both are included.

## Android release signing key

- The key is `mobile/android/selfstreak-release.jks`; its password is in `mobile/android/keystore.properties`.
  Both are kept out of git. **Back both files up somewhere safe** (a password manager or a private cloud
  folder). Without them, APKs you share can never be updated in place.
- Build a shareable APK and the Play Store bundle (needs JDK 21):
  `cd mobile/android && ./gradlew assembleRelease bundleRelease`
  Raise `versionCode` in `app/build.gradle` by 1 for every new build you share or upload.
- Google sign-in on Android: in Google Cloud Console → APIs & Services → Credentials (the same project as
  the website's Google login), create an OAuth client of type **Android** with package `com.selfstreak.app`
  and SHA-1 `F8:B4:E4:05:4A:92:4F:B3:0C:8C:AC:4C:6F:08:F3:3C:E4:15:20:27`.
  When you turn on Play App Signing, also add the SHA-1 that Play Console shows under App integrity.
- On Play Console, upload `app-release.aab` and choose Play App Signing; this key becomes your upload key.

## Store listing checklist (before you submit)

**Both stores**
- [ ] Purchases set up and keys added (sections above). Tell Claude when done: it checks the server sees them
      and that the Plus button opens the App Store / Google Play sheet instead of Razorpay/Cashfree.
- [ ] A demo account for reviewers (email + password, with some sample data). Put it in the review notes.
- [ ] Privacy policy: https://selfstreak.com/privacy · Terms: https://selfstreak.com/terms
- [ ] Support URL / email.

**Apple (App Store Connect)**
- [ ] Screenshots: 6.9" iPhone (1320×2868) at minimum.
- [ ] Description, keywords, subtitle, category (Productivity or Health & Fitness).
- [ ] App Privacy questionnaire (email, name, health data, financial info, photos you process, purchases).
- [ ] Age rating questionnaire.
- [ ] Add the `plus_monthly` subscription to the version you submit.
- [ ] Upload the build: Xcode → Product → Archive → Distribute App → App Store Connect (Claude can do this).
- [ ] Review notes: list the phone features (camera bill/meal scanning, Apple Health, Face ID lock,
      notifications and reminders, haptics, offline mode) to avoid a "just a website" (4.2) rejection.

**Google (Play Console)**
- [ ] Upload `SelfStreak-playstore.aab` to Internal testing first, then Closed testing.
- [ ] Personal developer account made after Nov 2023: closed test with at least 12 testers for 14 days
      before Production is unlocked.
- [ ] Store listing: icon 512×512, feature graphic 1024×500, at least 2 phone screenshots, descriptions.
- [ ] Data safety form, content rating, target audience, ads declaration (no ads).
- [ ] Health Connect: declare each health permission and why (steps, sleep, weight, workouts, mindfulness
      read; water write).
- [ ] Financial features declaration (the app tracks spending, bills and loans; it does not lend money).
- [ ] Account deletion: a web link where people can ask for deletion (or the in-app steps).
- [ ] Raise `versionCode` for every new upload.
