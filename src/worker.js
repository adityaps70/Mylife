// Self Streak API: accounts, per-user data, AI (Claude) with daily limits, push reminders, billing hooks.
import Anthropic from '@anthropic-ai/sdk';
import { sendPush } from './webpush.js';
import { gameRoutes, gameCron, applyReferral } from './game.js';
import { rzpRoutes, rzpWebhook, rzpReady, autopayOf } from './razorpay.js';
import { storeRoutes, storeRefresh, storeCfg, storeSubOf } from './store.js';
import { renewalReminders } from './renew.js';

const DAY = 86400000;
const MODEL = 'claude-haiku-5-5';
const te = new TextEncoder();
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
const unhex = (h) => new Uint8Array(h.match(/.{2}/g).map((x) => parseInt(x, 16)));
const sha256 = async (s) => hex(await crypto.subtle.digest('SHA-256', te.encode(s)));
const randHex = (n) => hex(crypto.getRandomValues(new Uint8Array(n)));
const json = (d, status = 200, headers = {}) => new Response(JSON.stringify(d), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...headers } });
const err = (status, error, extra = {}) => json({ error, ...extra }, status);
const istDay = (t = Date.now()) => new Date(t + 5.5 * 3600e3).toISOString().slice(0, 10);

async function hashPassword(pw, saltHex) {
  const key = await crypto.subtle.importKey('raw', te.encode(pw), 'PBKDF2', false, ['deriveBits']);
  return hex(await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: unhex(saltHex), iterations: 100000 }, key, 256));
}
function safeEqual(a, b) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }
function cookie(req, name) { const m = (req.headers.get('cookie') || '').match(new RegExp('(?:^|; )' + name + '=([^;]+)')); return m ? m[1] : null; }
function sessionCookie(req, token, maxAge) {
  const secure = new URL(req.url).protocol === 'https:' ? '; Secure' : '';
  return `ss_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAge}${secure}`;
}
async function newSession(env, req, userId) {
  const token = randHex(32);
  await env.DB.prepare('INSERT INTO sessions (token_hash, user_id, expires) VALUES (?, ?, ?)').bind(await sha256(token), userId, Date.now() + 30 * DAY).run();
  return sessionCookie(req, token, 30 * 86400);
}
async function currentUser(env, req) {
  const token = cookie(req, 'ss_session'); if (!token) return null;
  const row = await env.DB.prepare('SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ? AND s.expires > ?').bind(await sha256(token), Date.now()).first();
  return row || null;
}
const GRACE = 3 * DAY; // everything keeps working for 3 days after Plus/trial ends
function planStatus(u) {
  const now = Date.now();
  if (u.plan === 'owner') return 'owner';
  if (u.paid_until > now) return 'active';
  if (u.trial_ends > now) return 'trial';
  if (Math.max(u.paid_until || 0, u.trial_ends || 0) + GRACE > now) return 'grace';
  return 'expired'; // Free plan: app + manual logging work; Plus features are locked
}
async function usageToday(env, uid) {
  const r = await env.DB.prepare('SELECT count FROM usage WHERE user_id = ? AND day = ?').bind(uid, istDay()).first();
  return r ? r.count : 0;
}
async function me(env, u) {
  const limit = Number(env.DAILY_AI_LIMIT || 100);
  return { googleClientId: env.GOOGLE_CLIENT_ID || '', user: { id: u.id, email: u.email, name: u.name, plan: u.plan, status: planStatus(u), trialEnds: u.trial_ends, paidUntil: u.paid_until, plusEnds: Math.max(u.paid_until || 0, u.trial_ends || 0), graceDays: GRACE / DAY, created: u.created },
    usage: { used: await usageToday(env, u.id), limit }, price: Number(env.PRICE_INR || 199), vapidPublicKey: env.VAPID_PUBLIC_KEY,
    autopayReady: rzpReady(env) && (env.AUTOPAY_LIVE === '1' || String(env.AUTOPAY_TESTERS || '').toLowerCase().split(',').map((x) => x.trim()).includes(u.email)), autopay: await autopayOf(env, u.id).catch(() => null),
    store: { ...storeCfg(env), sub: await storeSubOf(env, u.id).catch(() => null) } };
}

/* ---------------- AI tasks (prompts and schemas live on the server) ---------------- */
const BILL_CATS = ['Rent / Home', 'Utilities', 'Phone & Internet', 'Subscriptions', 'Insurance', 'Credit card', 'Tax', 'Fitness', 'Household help', 'Other'];
const LOG_KINDS = ['habit_done', 'habit_undo', 'steps', 'water_add', 'water_set', 'sleep', 'weight', 'expense', 'income', 'bill_paid', 'emi_paid', 'haircut', 'product_bought', 'goal_progress', 'checklist_done', 'journal', 'reminder_add', 'meal', 'goal_add'];
const APP_PAGES = ['overview', 'today', 'health', 'goals', 'reminders', 'budget', 'bills', 'debt', 'savings', 'activity', 'grooming', 'checklist', 'notes', 'streak', 'year', 'history', 'settings', 'notify'];
const strList = (a, max = 60) => (Array.isArray(a) ? a : []).map((x) => String(x).slice(0, 80)).filter(Boolean).slice(0, max);
const obj = (props) => ({ type: 'object', additionalProperties: false, required: Object.keys(props), properties: props });
const S = { type: 'string' }, N = { type: 'number' };
const MEAL = obj({ name: S, items: { type: 'array', items: obj({ name: S, quantity: S }) }, calories: N, protein_g: N, carbs_g: N, fat_g: N, note: S });
function fileBlock(input) {
  const media = String(input.media || ''), data = String(input.data || '');
  if (!data || data.length > 30_000_000) throw new Error('bad_file');
  if (media === 'application/pdf') return { type: 'document', source: { type: 'base64', media_type: media, data } };
  if (/^image\/(jpeg|png|webp|gif)$/.test(media)) return { type: 'image', source: { type: 'base64', media_type: media, data } };
  throw new Error('bad_file');
}
const docProps = (kinds, catEnum) => ({ kind: { type: 'string', enum: kinds }, title: S, merchant: S, amount: N, bill_date: S, due_date: S, recurring: { type: 'boolean' }, frequency: { type: 'string', enum: ['monthly', 'quarterly', 'half-yearly', 'yearly', 'none'] }, bill_category: { type: 'string', enum: BILL_CATS }, spend_category: { type: 'string', enum: catEnum }, matched_bill: S, already_paid: { type: 'boolean' }, billing_period: S, summary: S });
const docSchema = (kinds, catEnum) => obj(docProps(kinds, catEnum));
function buildTask(task, input) {
  const cats = strList(input.cats, 40);
  const catEnum = cats.length ? cats : ['Other'];
  switch (task) {
    case 'log': {
      const today = /^\d{4}-\d{2}-\d{2}$/.test(input.today || '') ? input.today : istDay();
      return {
        effort: 'low', maxTokens: 8000,
        system: `You turn what the user says or writes (English, Hindi or Hinglish) into updates for their personal life dashboard. Today is ${today}, a ${String(input.weekday || '').slice(0, 12)}. Use only ids that appear in the lists.
- "completed my daily steps", "10k done" → steps 10000 and habit_done for the steps habit. "8k" means 8000.
- Water: glasses → water_add. Litres → glasses = litres × 4. "finished my water" → water_set 12.
- "gym", "workout", "exercise" → habit_done for the gym habit. Match other habits by meaning.
- Money spent → expense (value = rupees, text = who was paid, ref = best budget category). Money received → income.
- Paying a known bill → bill_paid with the bill id. Paying an EMI → emi_paid with the loan id.
- Food or drink eaten → meal: text = short meal name, value = estimated calories, protein/carbs/fat = estimated grams for typical Indian portions.
- "got a haircut" → haircut. Bought a listed grooming product → product_bought.
- A note about the day → journal (value = mood 1-5 if they said how the day felt, else 0).
- "remind me to …" → reminder_add with a date.
- A goal, plan or life priority ("I'll get married in 2 years and need ₹50 lakh before that", "buy a house by 2030", "save 6 months of expenses", "create a goal …") → goal_add: text = short title ("Get married", "Buy a house"), value = target in rupees (0 if no amount; "50 lakh" = 5000000, "1 crore" = 10000000; if digits look garbled from speech, use the amount they clearly mean), date = target date YYYY-MM-DD worked out from today ("in two years" → same day two years later), ref = one of marriage, house, emergency, car, education, travel, business, retire, custom. Never save a goal as a journal entry.
- A goal to do something on a number of days ("10,000 steps on 300 days this year", "gym 200 days in 2027", "read every day for 100 days") → goal_add with ref = 'habit:' + the matching habit id from the habit lists (or 'habit:new' if none fits), value = number of days, text = short title ("10,000 steps on 300 days"), start = first day to count (YYYY-MM-DD; 'this year' = Jan 1 of this year, 'from today' = today, a named year = Jan 1 of it), date = last day (e.g. Dec 31 of that year). For other actions set start to empty.
All money is Indian rupees (₹): treat '$', 'dollars', 'bucks', 'Rs' and 'rupees' as rupees and never convert currencies ("spent $150 on lunch" → expense value 150). People say "one fifty" for 150 and "two thirty" for 230, and paise are never logged, so an amount like 1.50 or 2.30 means 150 or 230.
Never invent things the user didn't say. If nothing fits, return no actions. reply: one short friendly spoken sentence.
question: if they are clearly logging a spend or payment but left out something you can't guess (usually the amount, e.g. "bought groceries"), add no action for it and ask for it in one short spoken question ("How much was it?"). Don't ask about the payment method. Otherwise leave question empty.
Questions: if they ask something about their own data ("how much did I spend this month?", "how many steps today?", "when is my rent due?", "how am I doing on my goals?"), add no actions and answer in reply in one or two short spoken sentences using only the numbers in the context; if the context doesn't have it, say so briefly. General advice questions get a short, practical answer.
open: if they ask to open, show or go to a part of the app ("open my goals", "show my bills", "take me to settings"), set open to the closest page name; also set it when answering a question that is clearly about one page. Otherwise leave it empty.`,
        content: [{ type: 'text', text: String(input.context || '').slice(0, 20000) + '\n\nWHAT I SAID: ' + String(input.text || '').slice(0, 4000) }],
        schema: obj({ reply: S, question: S, open: { type: 'string', enum: ['', ...APP_PAGES] }, actions: { type: 'array', items: obj({ kind: { type: 'string', enum: LOG_KINDS }, ref: S, value: N, text: S, date: S, start: S, protein: N, carbs: N, fat: N }) } }),
      };
    }
    case 'onb': {
      // Voice onboarding: pull profile details out of one spoken answer. Only what was actually said.
      const FOCUS_KEYS = ['health', 'money', 'grooming', 'goals', 'mind', 'home'];
      return {
        effort: 'low', maxTokens: 2000,
        system: `You help a new user set up Self Streak, an Indian app for habits, health, money and reminders, by voice. They answered one question (English, Hindi or Hinglish; speech-to-text may have small errors). Pull out ONLY what they actually said; leave every other field empty ('' for text, 0 for numbers, [] for lists). They may answer more than was asked: capture all of it.
- first: their first name only, properly capitalised ("main Aditya hoon" → "Aditya"). Never guess.
- age: whole years. city: Indian city name, properly spelled.
- gender: male / female / other only if they said it or used a clearly gendered self-reference; otherwise ''.
- wake, sleep, gym: 24-hour HH:MM. "up by 7" → 07:00, "sleep at 11" or "11 baje sota hoon" → 23:00, "gym in the evening" → 18:30, "morning workout" → 07:00. works_out: "yes" / "no" if they said whether they exercise, else ''.
- focus: which areas they want help with, from ${FOCUS_KEYS.join(', ')} (health = fitness/water/sleep/food, money = budget/bills/spending/saving, grooming = skincare/haircut, goals = targets/plans, mind = journal/mood/meditation, home = birthdays/house/dates). "everything" → all six.
- income: monthly take-home in rupees ("50k" → 50000, "1.2 lakh" → 120000, "15 hazaar" → 15000). Yearly amounts → divide by 12.
- habit: one habit they want to build, as a short title ("Drink 3 L water", "Read 20 minutes", "Meditate"). habit_time: HH:MM if they gave one.
- skip: true if they said skip / don't want to say / later / pass.
- reply: a warm acknowledgement of at most 8 words, no question, e.g. "Nice to meet you, Aditya." or "Got it."`,
        content: [{ type: 'text', text: 'QUESTION: ' + String(input.question || '').slice(0, 300) + '\nANSWER: ' + String(input.text || '').slice(0, 1500) }],
        schema: obj({ first: S, age: N, city: S, gender: { type: 'string', enum: ['', 'male', 'female', 'other'] }, wake: S, sleep: S, gym: S, works_out: { type: 'string', enum: ['', 'yes', 'no'] }, focus: { type: 'array', items: { type: 'string', enum: FOCUS_KEYS } }, income: N, habit: S, habit_time: S, skip: { type: 'boolean' }, reply: S }),
      };
    }
    case 'statement':
      return {
        effort: 'medium', maxTokens: 64000, stream: true,
        system: `You read Indian bank statements for a personal budgeting app. Amounts are in rupees. Return every transaction row, never opening/closing balances or totals. direction "out" = withdrawal/debit, "in" = deposit/credit.
Category rules: salary credits → "Salary (already counted)". Transfers to the user's own accounts, FDs/RDs, sweeps, SIPs, mutual funds, brokers, NPS/PPF → "Transfer / ignore". Credit-card bill payments, rent, electricity, broadband, mobile recharge, LPG, insurance premiums, house tax → "Bill payment". Loan EMIs → "EMI". Refunds, cashback, interest and other credits → "Income". Everything else → the closest category, else "Other".
payee: a short readable name (e.g. "Swiggy", "Rahul Sharma"), never UPI ids or reference numbers.`,
        content: [fileBlock(input), { type: 'text', text: 'Extract every transaction from this statement.' }],
        schema: obj({ bank: S, transactions: { type: 'array', items: obj({ date: { type: 'string', description: 'YYYY-MM-DD' }, description: S, payee: S, amount: N, direction: { type: 'string', enum: ['in', 'out'] }, category: { type: 'string', enum: catEnum } }) } }),
      };
    case 'categorise':
      return {
        effort: 'low', maxTokens: 32000, stream: true,
        system: 'Categorise Indian bank transactions for a budgeting app. Salary → "Salary (already counted)"; own-account transfers, SIPs, investments → "Transfer / ignore"; bills (rent, electricity, recharge, insurance, card bill) → "Bill payment"; loan EMIs → "EMI"; refunds/interest → "Income". payee: short readable name.',
        content: [{ type: 'text', text: 'Each line: index, direction, amount, narration.\n' + strList(input.lines, 400).join('\n') }],
        schema: obj({ items: { type: 'array', items: obj({ i: { type: 'integer' }, category: { type: 'string', enum: catEnum }, payee: S }) } }),
      };
    case 'receipt':
      return {
        effort: 'low', maxTokens: 8000,
        system: `You read photos or PDFs of Indian bills and receipts. kind: 'bill' for any utility/service bill (internet, phone, electricity, gas, water, insurance, rent, subscription, card statement) even if it is already paid; 'receipt' for a one-off purchase (shop, restaurant, online order); else 'other'. already_paid: true if it shows paid / payment received / zero balance, or the user says so. recurring: true for service bills. frequency: from the billing period on the bill (about 1 month → monthly, about 3 months → quarterly, 6 → half-yearly, 12 → yearly); if unclear use monthly for utilities. billing_period: as printed, e.g. '01 Aug–31 Oct 2026'. title: the provider and service only, never a month or year (e.g. 'Airtel Fiber', 'BSES Electricity'). bill_date = bill/invoice date; due_date = pay-by date. Dates as YYYY-MM-DD, empty if absent. Amount in rupees (total payable, or total paid). Known bills the user already tracks: ${strList(input.bills, 40).join(' | ') || 'none'} — set matched_bill to the exact name if this is one of them, else empty.`,
        content: [fileBlock(input), { type: 'text', text: 'Read this bill or receipt.' }],
        schema: docSchema(['bill', 'receipt', 'other'], catEnum),
      };
    case 'snap':
      return {
        effort: 'low', maxTokens: 8000,
        system: `You look at one photo or PDF a user of an Indian life-tracking app snapped and decide what it is: "meal" (food or drink they ate), "bill" (still to be paid: has an amount payable / due date, e.g. electricity, phone, card statement), "receipt" (already paid: shop/restaurant/online order receipt, UPI payment screenshot), "statement" (a bank or card statement with many transactions), or "other". confident=false if you genuinely cannot tell; then put a short friendly question in question. A utility/service bill (internet, phone, electricity, insurance, rent, subscription) is kind 'bill' even if already paid; set doc.already_paid accordingly. Fill meal only for meals (realistic Indian portions, calories and grams of protein, carbs, fat), and doc only for bills and receipts (dates YYYY-MM-DD or empty, amount in rupees; doc.frequency from the billing period: ~1 month monthly, ~3 months quarterly, ~6 half-yearly, ~12 yearly; doc.recurring true for service bills). Known bills: ${strList(input.bills, 40).join(' | ') || 'none'} — set doc.matched_bill to the exact name if it is one of them. For unused sections return empty strings and zeros.`,
        content: [fileBlock(input), { type: 'text', text: 'What is this? ' + String(input.note || '').slice(0, 300) }],
        schema: obj({ kind: { type: 'string', enum: ['meal', 'bill', 'receipt', 'statement', 'other'] }, confident: { type: 'boolean' }, question: S, meal: MEAL, doc: docSchema(['bill', 'receipt', 'other'], catEnum) }),
      };
    case 'meal_photo':
      return {
        effort: 'low', maxTokens: 6000,
        system: 'Estimate the nutrition of the food in this photo for a fitness app used in India. Identify each item and a realistic portion, then estimate total calories and grams of protein, carbs and fat. Be realistic, not optimistic. note: one short tip (e.g. how to add protein).',
        content: [fileBlock(input), { type: 'text', text: 'What did I eat? ' + String(input.note || '').slice(0, 300) }],
        schema: MEAL,
      };
    case 'debtplan': {
      const D = JSON.stringify(input || {}).slice(0, 12000);
      return {
        effort: 'medium', maxTokens: 12000, stream: true,
        system: `You are a careful, kind debt-repayment coach for people in India. You get one person's real numbers as JSON (monthly income, budget, bills, loans with outstanding/EMI/interest, credit cards and pay-later with limit/bill/minimum/interest, savings, emergency fund, and a computed baseline). Build a realistic month-by-month plan to become debt-free as fast as is safe on THEIR income.
Rules:
- Use only the numbers given; never invent loans or income. All money in rupees, whole numbers.
- First protect essentials: rent, food, utilities, existing EMIs and at least card minimums. Never suggest skipping an EMI.
- Keep or build a small emergency buffer (aim 1 month of essentials) before aggressive prepayment, unless card interest is very high.
- Credit cards/pay-later at 30%+ yearly (≈2.5%+/month) are usually cleared first; otherwise compare avalanche (highest rate) vs snowball (smallest balance) and pick what suits them; say why.
- If EMIs exceed ~50% of income or income can't cover essentials + EMIs, say so plainly and give concrete options: talk to the lender about restructuring/tenure extension, balance transfer, consolidating high-interest debt into a cheaper personal loan, selling unused items, or extra income ideas. Mention RBI rules only if relevant (no foreclosure charges on floating-rate individual loans). Never suggest new borrowing to pay EMIs, or illegal/unsafe lending apps.
- budget_cuts: only from their listed budget categories, with realistic cuts.
- If the JSON has life priorities (e.g. marriage savings by a date), balance debt payoff against them: never starve a near-term priority, and say when freed-up EMIs should switch to the priority.
- months: plan for the next 6 months (labels like "Dec 2026"), what to pay on each debt beyond the EMI, and the expected total remaining at month end.
- WRITE VERY LITTLE. People skim on a phone. Never repeat the same fact in two fields (e.g. don't restate the income/EMI gap in summary, warnings and order).
  headline: max 12 words. summary: max 2 short sentences, under 220 characters, and it must add something the headline doesn't.
  debt_free_month: just a month like "Mar 2028", or "After restructuring" — never a sentence.
  strategy_why: one sentence, max 20 words. order[].why: max 12 words. budget_cuts[].how: max 8 words.
  quick_wins: at most 3, each max 12 words, starting with a verb (they are this week's to-dos).
  warnings: at most 3, each max 15 words, only things not already said elsewhere.
  months[].actions[].note: max 6 words or empty.
- Plain, warm words. No jargon without a 3-word explanation. Today is ${new Date().toISOString().slice(0, 10)}.`,
        content: [{ type: 'text', text: 'My numbers:\n' + D }],
        schema: obj({
          headline: S, summary: S, health: { type: 'string', enum: ['good', 'tight', 'stretched', 'critical'] },
          monthly_free: N, extra_per_month: N, strategy: { type: 'string', enum: ['avalanche', 'snowball', 'cards_first', 'stabilise'] }, strategy_why: S,
          debt_free_month: S, interest_saved: N,
          order: { type: 'array', items: obj({ name: S, why: S, target_month: S }) },
          months: { type: 'array', items: obj({ month: S, actions: { type: 'array', items: obj({ name: S, pay: N, note: S }) }, debt_left: N }) },
          budget_cuts: { type: 'array', items: obj({ category: S, cut: N, how: S }) },
          quick_wins: { type: 'array', items: S }, warnings: { type: 'array', items: S },
        }),
      };
    }
    case 'priorityplan': {
      const D = JSON.stringify(input || {}).slice(0, 14000);
      return {
        effort: 'medium', maxTokens: 10000, stream: true,
        system: `You are a practical, warm money coach for people in India. The user has one big life priority (e.g. marriage, house) with a target amount and date, plus their real income, budget, bills, EMIs, credit cards, savings and other priorities as JSON. Tell them honestly whether it is reachable and exactly how.
Rules:
- Use only the numbers given; whole rupees. Never invent income.
- Essentials, EMIs and card minimums always come first. Never suggest skipping an EMI, borrowing to save, or risky/illegal schemes.
- If it is not reachable by the date, say so plainly in one sentence, then give 2–4 concrete options with their monthly amount and when the goal would be reached: e.g. extend the date, lower the target, cut specific budget categories (name them and the amount), redirect EMIs after a loan closes (say which and when), add income, or a mix. Mark one option as recommended by putting it first.
- If they have high-interest card debt, say whether to clear it first and how that changes the date.
- For money needed within 3 years, suggest safe places (recurring deposit, liquid/short-duration debt funds, high-interest savings), not stocks. Mention marriage-specific ideas only if the goal is marriage (e.g. split into must-have vs nice-to-have costs).
- this_month: 2–4 specific actions for this month with amounts.
Today is ${new Date().toISOString().slice(0, 10)}.`,
        content: [{ type: 'text', text: 'My priority and numbers:\n' + D }],
        schema: obj({
          verdict: S, reachable: { type: 'boolean' }, monthly_target: N,
          options: { type: 'array', items: obj({ title: S, detail: S, monthly: N, reach_by: S }) },
          this_month: { type: 'array', items: S }, warnings: { type: 'array', items: S },
        }),
      };
    }
    case 'daysummary': {
      const D = JSON.stringify(input || {}).slice(0, 14000);
      return {
        effort: 'low', maxTokens: 6000,
        system: `You are a warm, honest daily coach for an Indian user of a life-tracking app. You get one day's log as JSON: meals (names, estimated macros), steps, water, sleep, mood, habits done/not done, spending, journal and goals. Write a short review of the day and a plan for tomorrow.
Rules:
- Use only what is in the log. If an area has no data, say it wasn't logged rather than judging it.
- Targets: 10,000 steps, 12 glasses of water (0.25 L each), 7–9 h sleep, and the protein/calorie targets given. Only say a target was hit if the number meets it; quote the real numbers (e.g. '6,200 of 10,000 steps'). A missing or 0 sleep value means not logged.
- Food: compare protein and calories to targets. From the meal names, flag things like fried/oily, very sugary, low fibre, few vegetables or fruit, late heavy dinner. likely_missing: 1–4 essential nutrients that this day's meals were probably low in (e.g. magnesium, calcium, iron, fibre, vitamin B12, vitamin D, omega-3, potassium), each with a one-line why and 2–3 common Indian foods to fix it (e.g. "curd, paneer, ragi"). Leave it empty if nothing was eaten/logged.
- areas: one entry each for Food, Health (steps, water, sleep), Habits, Money, Mind (mood/journal) — and Goals if goals are given. rating one of great, good, okay, needs_attention; summary one sentence with numbers.
- wins/misses: 1–4 short items each. tomorrow: 3–5 specific actions with the area they belong to (e.g. "Add 2 eggs or a bowl of dal at breakfast to reach 110 g protein").
- score 0–100 for the whole day. headline: one encouraging, honest sentence.
- person.gender and person.age (if given) only shape nutrient advice where it genuinely matters (e.g. iron, folate and calcium for women; protein needs by body weight). Don't mention gender otherwise.
- No medical diagnoses. Plain words.`,
        content: [{ type: 'text', text: 'My day:\n' + D }],
        schema: obj({
          headline: S, score: N,
          areas: { type: 'array', items: obj({ area: { type: 'string', enum: ['Food', 'Health', 'Habits', 'Money', 'Mind', 'Goals'] }, rating: { type: 'string', enum: ['great', 'good', 'okay', 'needs_attention'] }, summary: S }) },
          food: obj({ protein_ok: { type: 'boolean' }, notes: { type: 'array', items: S }, likely_missing: { type: 'array', items: obj({ nutrient: S, why: S, foods: S }) } }),
          wins: { type: 'array', items: S }, misses: { type: 'array', items: S },
          tomorrow: { type: 'array', items: obj({ area: { type: 'string', enum: ['Food', 'Health', 'Habits', 'Money', 'Mind', 'Goals'] }, action: S }) },
        }),
      };
    }
    case 'meal_text':
      return {
        effort: 'low', maxTokens: 6000,
        system: 'Estimate the nutrition of a meal described in English, Hindi or Hinglish, using typical Indian home portions unless stated. Return total calories and grams of protein, carbs and fat. note: one short tip.',
        content: [{ type: 'text', text: String(input.text || '').slice(0, 1000) }],
        schema: MEAL,
      };
  }
  return null;
}
async function runAI(env, spec) {
  const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  const params = { model: MODEL, max_tokens: spec.maxTokens, system: spec.system, messages: [{ role: 'user', content: spec.content }], output_config: { effort: spec.effort, format: { type: 'json_schema', schema: spec.schema } } };
  const msg = spec.stream ? await client.messages.stream(params).finalMessage() : await client.messages.create(params);
  if (msg.stop_reason === 'refusal') return { error: 'refused' };
  if (msg.stop_reason === 'max_tokens') return { error: 'too_long' };
  const text = msg.content.filter((b) => b.type === 'text').map((b) => b.text).join('');
  return { result: JSON.parse(text) };
}

/* ---------------- Google sign-in ---------------- */
let googleKeys = { at: 0, keys: [] };
const b64uBytes = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)), (c) => c.charCodeAt(0));
async function verifyGoogleToken(env, jwt) {
  const [h, p, sig] = jwt.split('.');
  if (!h || !p || !sig) throw new Error('bad_jwt');
  const head = JSON.parse(new TextDecoder().decode(b64uBytes(h))), claims = JSON.parse(new TextDecoder().decode(b64uBytes(p)));
  if (Date.now() - googleKeys.at > 3600e3 || !googleKeys.keys.some((k) => k.kid === head.kid)) {
    const r = await fetch('https://www.googleapis.com/oauth2/v3/certs'); googleKeys = { at: Date.now(), keys: (await r.json()).keys || [] };
  }
  const jwk = googleKeys.keys.find((k) => k.kid === head.kid); if (!jwk || head.alg !== 'RS256') throw new Error('unknown_key');
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64uBytes(sig), new TextEncoder().encode(h + '.' + p));
  if (!ok) throw new Error('bad_signature');
  if (!['accounts.google.com', 'https://accounts.google.com'].includes(claims.iss)) throw new Error('bad_issuer');
  // Website (GSI) and Android tokens use the web client ID; the iPhone app's native sign-in uses the iOS client ID.
  if (![env.GOOGLE_CLIENT_ID, env.GOOGLE_IOS_CLIENT_ID].filter(Boolean).includes(claims.aud)) throw new Error('bad_audience');
  if (!(claims.exp * 1000 > Date.now())) throw new Error('expired');
  if (!claims.email || claims.email_verified !== true && claims.email_verified !== 'true') throw new Error('email_not_verified');
  return claims;
}

/* ---------------- Sign in with Apple (iPhone app) ---------------- */
let appleKeys = { at: 0, keys: [] };
async function verifyAppleToken(env, jwt) {
  const [h, p, sig] = String(jwt).split('.');
  if (!h || !p || !sig) throw new Error('bad_jwt');
  const head = JSON.parse(new TextDecoder().decode(b64uBytes(h))), claims = JSON.parse(new TextDecoder().decode(b64uBytes(p)));
  if (Date.now() - appleKeys.at > 3600e3 || !appleKeys.keys.some((k) => k.kid === head.kid)) {
    const r = await fetch('https://appleid.apple.com/auth/keys'); appleKeys = { at: Date.now(), keys: (await r.json()).keys || [] };
  }
  const jwk = appleKeys.keys.find((k) => k.kid === head.kid); if (!jwk || head.alg !== 'RS256') throw new Error('unknown_key');
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  if (!(await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64uBytes(sig), new TextEncoder().encode(h + '.' + p)))) throw new Error('bad_signature');
  if (claims.iss !== 'https://appleid.apple.com') throw new Error('bad_issuer');
  // Native iPhone sign-in tokens are issued to the app's bundle ID.
  if (![env.APPLE_BUNDLE_ID || 'com.selfstreak.app', env.APPLE_SERVICE_ID].filter(Boolean).includes(claims.aud)) throw new Error('bad_audience');
  if (!(claims.exp * 1000 > Date.now())) throw new Error('expired');
  if (!claims.sub) throw new Error('no_subject');
  return claims;
}

/* ---------------- Email (password resets) ---------------- */
// Cloudflare Email Sending if the EMAIL binding exists, otherwise Resend if RESEND_API_KEY is set.
const MAIL_FROM = (env) => env.MAIL_FROM || 'no-reply@selfstreak.com';
const mailReady = (env) => !!(env.EMAIL || env.RESEND_API_KEY);
async function sendMail(env, { to, subject, html, text }) {
  if (env.EMAIL) return env.EMAIL.send({ from: { email: MAIL_FROM(env), name: 'Self Streak' }, to, subject, html, text });
  if (env.RESEND_API_KEY) {
    const r = await fetch('https://api.resend.com/emails', { method: 'POST', headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' }, body: JSON.stringify({ from: `Self Streak <${MAIL_FROM(env)}>`, to: [to], subject, html, text }) });
    if (!r.ok) throw new Error('resend ' + r.status + ' ' + (await r.text()).slice(0, 200));
    return r.json();
  }
  throw new Error('mail_not_configured');
}

/* ---------------- Admin (owner only) ---------------- */
const daysBack = (n) => { const out = []; for (let i = n - 1; i >= 0; i--) out.push(new Date(Date.now() + 5.5 * 3600e3 - i * DAY).toISOString().slice(0, 10)); return out; };
async function admin(req, env, url, p, m, body) {
  const all = async (q, ...a) => (await env.DB.prepare(q).bind(...a).all()).results;
  const one = async (q, ...a) => await env.DB.prepare(q).bind(...a).first();
  const now = Date.now(), d30 = daysBack(30), today = d30[29], since = (d) => now - d * DAY;
  if (p === '/api/admin/stats' && m === 'GET') {
    const users = await all('SELECT plan, trial_ends, paid_until, created, last_seen FROM users');
    const st = (x) => x.plan === 'owner' ? 'owner' : x.paid_until > now ? 'active' : x.trial_ends > now ? 'trial' : 'expired';
    const cnt = { owner: 0, active: 0, trial: 0, expired: 0 }; users.forEach((x) => cnt[st(x)]++);
    const signups = Object.fromEntries(d30.map((d) => [d, 0]));
    users.forEach((x) => { const d = new Date(x.created + 5.5 * 3600e3).toISOString().slice(0, 10); if (d in signups) signups[d]++; });
    const act = await all('SELECT day, COUNT(*) AS n FROM active_days WHERE day >= ? GROUP BY day', d30[0]);
    const ai = await all("SELECT day, SUM(count) AS n, COUNT(*) AS u FROM usage WHERE day >= ? AND day NOT LIKE 'tts-%' AND day NOT LIKE 'stt-%' GROUP BY day", d30[0]);
    const pv = await all('SELECT day, SUM(n) AS n FROM page_views WHERE day >= ? GROUP BY day', d30[0]);
    const uv = await all('SELECT day, COUNT(*) AS n FROM visitors WHERE day >= ? GROUP BY day', d30[0]);
    const pay = await one("SELECT COUNT(*) AS n, COALESCE(SUM(amount),0) AS sum FROM payments WHERE status = 'paid'");
    const pay30 = await one("SELECT COUNT(*) AS n, COALESCE(SUM(amount),0) AS sum FROM payments WHERE status = 'paid' AND paid_at > ?", since(30));
    const recentPay = await all("SELECT p.order_id, p.amount, p.status, p.created, p.paid_at, u.email FROM payments p LEFT JOIN users u ON u.id = p.user_id ORDER BY p.created DESC LIMIT 10");
    const pages = await all('SELECT path, SUM(n) AS n FROM page_views WHERE day >= ? GROUP BY path ORDER BY n DESC LIMIT 12', d30[0]);
    const refs = await all("SELECT ref, SUM(n) AS n FROM page_views WHERE day >= ? AND ref <> '' GROUP BY ref ORDER BY n DESC LIMIT 10", d30[0]);
    const countries = await all("SELECT country, SUM(n) AS n FROM page_views WHERE day >= ? GROUP BY country ORDER BY n DESC LIMIT 8", d30[0]);
    const devices = await all('SELECT device, SUM(n) AS n FROM page_views WHERE day >= ? GROUP BY device ORDER BY n DESC', d30[0]);
    const push = await one('SELECT COUNT(*) AS n, COUNT(DISTINCT user_id) AS u FROM push_subs');
    const topAI = await all("SELECT u.email, SUM(x.count) AS n FROM usage x JOIN users u ON u.id = x.user_id WHERE x.day >= ? AND x.day NOT LIKE 'tts-%' AND x.day NOT LIKE 'stt-%' GROUP BY x.user_id ORDER BY n DESC LIMIT 8", daysBack(7)[0]);
    const map = (rows) => Object.fromEntries(rows.map((r) => [r.day, r.n]));
    const A = map(act), I = map(ai), P = map(pv), V = map(uv);
    const wau = await one('SELECT COUNT(DISTINCT user_id) AS n FROM active_days WHERE day >= ?', daysBack(7)[0]);
    const mau = await one('SELECT COUNT(DISTINCT user_id) AS n FROM active_days WHERE day >= ?', d30[0]);
    return json({
      users: { total: users.length, ...cnt, new7: users.filter((x) => x.created > since(7)).length, new30: users.filter((x) => x.created > since(30)).length,
        dau: A[today] || 0, wau: wau.n, mau: mau.n, online: users.filter((x) => x.last_seen > now - 15 * 60e3).length },
      money: { price: Number(env.PRICE_INR || 199), mrr: cnt.active * Number(env.PRICE_INR || 199), paidTotal: pay.sum, paidCount: pay.n, paid30: pay30.sum, paid30Count: pay30.n, cashfree: cfReady(env) },
      ai: { today: I[today] || 0, d30: d30.reduce((t, d) => t + (I[d] || 0), 0), limit: Number(env.DAILY_AI_LIMIT || 20), top: topAI },
      web: { views30: d30.reduce((t, d) => t + (P[d] || 0), 0), visitors30: d30.reduce((t, d) => t + (V[d] || 0), 0), viewsToday: P[today] || 0, visitorsToday: V[today] || 0, pages, refs, countries, devices },
      push: push, series: { days: d30, signups: d30.map((d) => signups[d]), active: d30.map((d) => A[d] || 0), ai: d30.map((d) => I[d] || 0), views: d30.map((d) => P[d] || 0), visitors: d30.map((d) => V[d] || 0) },
      recentPay,
    });
  }
  if (p === '/api/admin/users' && m === 'GET') {
    const q = '%' + (url.searchParams.get('q') || '').toLowerCase() + '%';
    const rows = await all(`SELECT u.id, u.email, u.name, u.plan, u.trial_ends, u.paid_until, u.created, u.last_seen,
      (SELECT count FROM usage WHERE user_id = u.id AND day = ?) AS ai_today,
      (SELECT COUNT(*) FROM push_subs WHERE user_id = u.id) AS devices,
      (SELECT COUNT(*) FROM active_days WHERE user_id = u.id AND day >= ?) AS active30,
      (SELECT COALESCE(SUM(amount),0) FROM payments WHERE user_id = u.id AND status = 'paid') AS paid
      FROM users u WHERE lower(u.email) LIKE ? OR lower(u.name) LIKE ? ORDER BY u.created DESC LIMIT 200`, istDay(), d30[0], q, q);
    return json({ users: rows.map((x) => ({ ...x, status: x.plan === 'owner' ? 'owner' : x.paid_until > now ? 'active' : x.trial_ends > now ? 'trial' : 'expired' })) });
  }
  if (p === '/api/admin/user' && m === 'POST') {
    const b = await body(), target = await one('SELECT * FROM users WHERE id = ?', String(b.id || ''));
    if (!target) return err(404, 'User not found.');
    if (target.plan === 'owner') return err(400, 'The owner account can’t be changed here.');
    if (b.action === 'extend_trial') await env.DB.prepare('UPDATE users SET trial_ends = ? WHERE id = ?').bind(Math.max(now, target.trial_ends) + 7 * DAY, target.id).run();
    else if (b.action === 'grant_month') await env.DB.prepare("UPDATE users SET paid_until = ?, plan = 'active' WHERE id = ?").bind(Math.max(now, target.paid_until) + 30 * DAY, target.id).run();
    else if (b.action === 'revoke') await env.DB.prepare("UPDATE users SET paid_until = 0, trial_ends = ?, plan = 'trial' WHERE id = ?").bind(now, target.id).run();
    else if (b.action === 'reset_ai') await env.DB.prepare('DELETE FROM usage WHERE user_id = ? AND day = ?').bind(target.id, istDay()).run();
    else if (b.action === 'logout') await env.DB.prepare('DELETE FROM sessions WHERE user_id = ?').bind(target.id).run();
    else if (b.action === 'delete') { try { await env.DB.prepare('DELETE FROM apple_ids WHERE user_id = ?').bind(target.id).run(); } catch (e) {} for (const t of ['sessions', 'user_data', 'usage', 'push_subs', 'push_schedule', 'active_days', 'password_resets', 'game']) await env.DB.prepare(`DELETE FROM ${t} WHERE user_id = ?`).bind(target.id).run(); await env.DB.prepare('DELETE FROM friends WHERE a = ? OR b = ?').bind(target.id, target.id).run(); await env.DB.prepare('DELETE FROM users WHERE id = ?').bind(target.id).run(); }
    else return err(400, 'unknown_action');
    return json({ ok: true });
  }
  return err(404, 'not_found');
}

/* ---------------- Cashfree payments ---------------- */
const cfReady = (env) => !!(env.CASHFREE_APP_ID && env.CASHFREE_SECRET_KEY);
const cfMode = (env) => (env.CASHFREE_ENV === 'sandbox' ? 'sandbox' : 'production');
const cf = (env, path, init = {}) => fetch((cfMode(env) === 'sandbox' ? 'https://sandbox.cashfree.com/pg' : 'https://api.cashfree.com/pg') + path, {
  ...init, headers: { 'content-type': 'application/json', 'x-api-version': '2023-08-01', 'x-client-id': env.CASHFREE_APP_ID, 'x-client-secret': env.CASHFREE_SECRET_KEY },
});
// Ask Cashfree for the order's real status; on PAID extend the plan by a month (once per order).
async function settleOrder(env, orderId) {
  const row = await env.DB.prepare('SELECT * FROM payments WHERE order_id = ?').bind(orderId).first();
  if (!row) return 'unknown';
  if (row.status === 'paid') return 'paid';
  const r = await cf(env, '/orders/' + encodeURIComponent(orderId));
  const o = await r.json().catch(() => ({}));
  const st = String(o.order_status || '').toUpperCase();
  if (st === 'PAID' && Number(o.order_amount) >= row.amount) {
    const claimed = await env.DB.prepare("UPDATE payments SET status = 'paid', paid_at = ? WHERE order_id = ? AND status <> 'paid' RETURNING user_id").bind(Date.now(), orderId).first();
    if (claimed) {
      const u = await env.DB.prepare('SELECT paid_until FROM users WHERE id = ?').bind(claimed.user_id).first();
      const from = Math.max(Date.now(), Number(u?.paid_until) || 0);
      await env.DB.prepare("UPDATE users SET paid_until = ?, plan = CASE WHEN plan = 'owner' THEN plan ELSE 'active' END WHERE id = ?").bind(from + 30 * DAY, claimed.user_id).run();
    }
    return 'paid';
  }
  if (st === 'EXPIRED' || st === 'TERMINATED') await env.DB.prepare('UPDATE payments SET status = ? WHERE order_id = ? AND status <> \'paid\'').bind(st.toLowerCase(), orderId).run();
  return st.toLowerCase() || 'pending';
}

/* ---------------- API router ---------------- */
async function api(req, env, url, ctx) {
  const p = url.pathname, m = req.method;
  if (m !== 'GET') {
    const origin = req.headers.get('origin');
    if (origin && origin !== url.origin) return err(403, 'bad_origin');
  }
  const body = async () => { try { return await req.json(); } catch { return {}; } };

  if (p === '/api/signup' && m === 'POST') {
    const b = await body(), email = String(b.email || '').trim().toLowerCase(), pw = String(b.password || ''), name = String(b.name || '').trim().slice(0, 60);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return err(400, 'Enter a valid email address.');
    if (pw.length < 8) return err(400, 'Use at least 8 characters for your password.');
    if (await env.DB.prepare('SELECT 1 FROM users WHERE email = ?').bind(email).first()) return err(409, 'An account with this email already exists. Log in instead.');
    const first = !(await env.DB.prepare('SELECT 1 FROM users LIMIT 1').first());
    const id = crypto.randomUUID(), salt = randHex(16), now = Date.now();
    await env.DB.prepare('INSERT INTO users (id, email, name, pass_hash, salt, plan, trial_ends, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .bind(id, email, name, await hashPassword(pw, salt), salt, first ? 'owner' : 'trial', now + Number(env.TRIAL_DAYS || 7) * DAY, now).run();
    if (b.ref) { try { await applyReferral(env, id, b.ref); } catch (e) { console.error('ref', e); } }
    const u = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first();
    return json({ ...(await me(env, u)), isNew: true }, 200, { 'set-cookie': await newSession(env, req, id) });
  }
  if (p === '/api/login' && m === 'POST') {
    const b = await body(), email = String(b.email || '').trim().toLowerCase(), pw = String(b.password || '');
    const u = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first();
    if (!u) { await hashPassword(pw, '00'.repeat(16)); return err(401, 'Wrong email or password.'); }
    if (u.locked_until > Date.now()) return err(429, 'Too many attempts. Try again in a few minutes.');
    if (!safeEqual(await hashPassword(pw, u.salt), u.pass_hash)) {
      const fails = u.fail_count + 1;
      await env.DB.prepare('UPDATE users SET fail_count = ?, locked_until = ? WHERE id = ?').bind(fails >= 5 ? 0 : fails, fails >= 5 ? Date.now() + 10 * 60000 : 0, u.id).run();
      return err(401, 'Wrong email or password.');
    }
    await env.DB.prepare('UPDATE users SET fail_count = 0, locked_until = 0 WHERE id = ?').bind(u.id).run();
    return json(await me(env, u), 200, { 'set-cookie': await newSession(env, req, u.id) });
  }
  if (p === '/api/logout' && m === 'POST') {
    const t = cookie(req, 'ss_session');
    const b = await body();
    if (t) {
      const s = await env.DB.prepare('SELECT user_id FROM sessions WHERE token_hash = ?').bind(await sha256(t)).first();
      if (s && b.endpoint) await env.DB.prepare('DELETE FROM push_subs WHERE user_id = ? AND endpoint = ?').bind(s.user_id, String(b.endpoint)).run();
      await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?').bind(await sha256(t)).run();
    }
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(req, '', 0) });
  }

  if (p === '/api/billing/rzp/webhook' && m === 'POST') return rzpWebhook(req, env);
  if (p === '/api/billing/webhook' && m === 'POST') {
    if (!cfReady(env)) return err(404, 'not_found');
    const raw = await req.text(), ts = req.headers.get('x-webhook-timestamp') || '', sig = req.headers.get('x-webhook-signature') || '';
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.CASHFREE_SECRET_KEY), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const mac = btoa(String.fromCharCode(...new Uint8Array(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(ts + raw)))));
    if (!sig || !safeEqual(mac, sig)) return err(401, 'bad_signature');
    let ev = {}; try { ev = JSON.parse(raw); } catch {}
    const orderId = ev?.data?.order?.order_id;
    if (orderId) await settleOrder(env, String(orderId));
    return json({ ok: true });
  }

  if (p === '/api/google' && m === 'POST') {
    // "Continue with Google": verify Google's signed ID token, then log in or create the account.
    if (!env.GOOGLE_CLIENT_ID) return err(501, 'Google sign-in isn’t switched on yet.');
    const b = await body(); let g;
    try { g = await verifyGoogleToken(env, String(b.credential || '')); } catch (e) { console.error('google', e); return err(401, 'Google sign-in failed. Please try again.'); }
    const email = String(g.email || '').toLowerCase();
    let usr = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first(), isNew = false;
    if (!usr) {
      const first = !(await env.DB.prepare('SELECT 1 FROM users LIMIT 1').first());
      const id = crypto.randomUUID(), salt = randHex(16), now = Date.now();
      // Random password the person never sees; they can set one later with "Forgot password".
      await env.DB.prepare('INSERT INTO users (id, email, name, pass_hash, salt, plan, trial_ends, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
        .bind(id, email, String(g.given_name || g.name || '').slice(0, 60), await hashPassword(randHex(24), salt), salt, first ? 'owner' : 'trial', now + Number(env.TRIAL_DAYS || 7) * DAY, now).run();
      if (b.ref) { try { await applyReferral(env, id, b.ref); } catch (e) { console.error('ref', e); } }
      usr = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first(); isNew = true;
    }
    return json({ ...(await me(env, usr)), isNew, name: usr.name }, 200, { 'set-cookie': await newSession(env, req, usr.id) });
  }
  if (p === '/api/apple' && m === 'POST') {
    // "Continue with Apple": verify Apple's signed identity token, then log in, link or create the account.
    // Apple only sends the email (often a private relay address) the first time, so we remember the Apple user ID.
    const b = await body(); let a;
    try { a = await verifyAppleToken(env, b.credential); } catch (e) { console.error('apple', e); return err(401, 'Apple sign-in failed. Please try again.'); }
    await env.DB.prepare('CREATE TABLE IF NOT EXISTS apple_ids (sub TEXT PRIMARY KEY, user_id TEXT NOT NULL, created INTEGER NOT NULL)').run();
    const link = await env.DB.prepare('SELECT user_id FROM apple_ids WHERE sub = ?').bind(a.sub).first();
    const email = String(a.email || '').toLowerCase(), verified = a.email_verified === true || a.email_verified === 'true';
    let usr = link ? await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(link.user_id).first() : null, isNew = false;
    if (!usr && email && verified) usr = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email).first();
    if (!usr) {
      if (!email || !verified) return err(400, 'Apple didn’t share an email. In Settings → Apple ID → Sign in with Apple, remove Self Streak and try again.');
      const first = !(await env.DB.prepare('SELECT 1 FROM users LIMIT 1').first());
      const id = crypto.randomUUID(), salt = randHex(16), now = Date.now();
      await env.DB.prepare('INSERT INTO users (id, email, name, pass_hash, salt, plan, trial_ends, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
        .bind(id, email, String(b.name || '').trim().slice(0, 60), await hashPassword(randHex(24), salt), salt, first ? 'owner' : 'trial', now + Number(env.TRIAL_DAYS || 7) * DAY, now).run();
      if (b.ref) { try { await applyReferral(env, id, b.ref); } catch (e) { console.error('ref', e); } }
      usr = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first(); isNew = true;
    }
    if (!link) await env.DB.prepare('INSERT OR REPLACE INTO apple_ids (sub, user_id, created) VALUES (?, ?, ?)').bind(a.sub, usr.id, Date.now()).run();
    return json({ ...(await me(env, usr)), isNew, name: usr.name }, 200, { 'set-cookie': await newSession(env, req, usr.id) });
  }
  if (p === '/api/config' && m === 'GET') return json({ googleClientId: env.GOOGLE_CLIENT_ID || '', googleIosClientId: env.GOOGLE_IOS_CLIENT_ID || '' });
  if (p === '/api/forgot' && m === 'POST') {
    const b = await body(), email = String(b.email || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return err(400, 'Enter the email you signed up with.');
    if (!mailReady(env)) return err(503, 'Password reset emails aren’t switched on yet. Email adityaps700@gmail.com and we’ll reset it for you.');
    const usr = await env.DB.prepare('SELECT id, name FROM users WHERE email = ?').bind(email).first();
    // Same answer whether or not the account exists, so nobody can probe for emails.
    const okMsg = { ok: true, message: 'If that email has an account, a reset link is on its way. Check spam too. It works for 30 minutes.' };
    if (!usr) { await hashPassword('x', '00'.repeat(16)); return json(okMsg); }
    const recent = await env.DB.prepare('SELECT COUNT(*) AS n FROM password_resets WHERE user_id = ? AND created > ?').bind(usr.id, Date.now() - 3600e3).first();
    if ((recent?.n || 0) >= 3) return json(okMsg);
    const token = randHex(32), now = Date.now();
    await env.DB.prepare('INSERT INTO password_resets (token_hash, user_id, expires, used, created) VALUES (?, ?, ?, 0, ?)').bind(await sha256(token), usr.id, now + 30 * 60e3, now).run();
    const link = `${url.origin}/app#reset=${token}`, hi = usr.name ? `Hi ${usr.name},` : 'Hi,';
    try {
      await sendMail(env, { to: email, subject: 'Reset your Self Streak password',
        text: `${hi}\n\nTap this link to choose a new password (valid for 30 minutes):\n${link}\n\nIf you didn’t ask for this, you can ignore this email. Your password won’t change.\n\n— Self Streak`,
        html: `<div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:480px;margin:auto;padding:24px;color:#18181b"><div style="display:inline-block;background:#d7f64a;color:#10120a;font-weight:800;font-size:20px;width:40px;height:40px;line-height:40px;text-align:center;border-radius:11px">S</div><h2 style="margin:18px 0 8px">Reset your password</h2><p>${hi}</p><p>Tap the button to choose a new password for Self Streak. The link works for 30 minutes.</p><p style="margin:24px 0"><a href="${link}" style="background:#d7f64a;color:#10120a;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:999px;display:inline-block">Choose a new password</a></p><p style="color:#71717a;font-size:13px">If you didn’t ask for this, ignore this email. Your password won’t change.</p></div>` });
    } catch (e) { console.error('mail', e); return err(502, 'Couldn’t send the email right now. Please try again in a minute.'); }
    return json(okMsg);
  }
  if (p === '/api/reset' && m === 'POST') {
    const b = await body(), token = String(b.token || ''), pw = String(b.password || '');
    if (pw.length < 8) return err(400, 'Use at least 8 characters.');
    const row = await env.DB.prepare('SELECT * FROM password_resets WHERE token_hash = ?').bind(await sha256(token)).first();
    if (!row || row.used || row.expires < Date.now()) return err(400, 'This reset link has expired or was already used. Ask for a new one.');
    const salt = randHex(16);
    await env.DB.prepare('UPDATE users SET pass_hash = ?, salt = ?, fail_count = 0, locked_until = 0 WHERE id = ?').bind(await hashPassword(pw, salt), salt, row.user_id).run();
    await env.DB.prepare('UPDATE password_resets SET used = 1 WHERE user_id = ?').bind(row.user_id).run();
    await env.DB.prepare('DELETE FROM sessions WHERE user_id = ?').bind(row.user_id).run();
    const usr = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(row.user_id).first();
    return json(await me(env, usr), 200, { 'set-cookie': await newSession(env, req, usr.id) });
  }

  if (p === '/api/hit' && m === 'POST') {
    // Page-view counter for the public pages. No cookies; visitors counted by a daily one-way hash.
    const ua = req.headers.get('user-agent') || '';
    if (/bot|crawl|spider|slurp|preview|headless|lighthouse|facebookexternalhit|whatsapp/i.test(ua)) return json({ ok: true });
    const b = await body(), day = istDay();
    const path = String(b.p || '/').split('?')[0].slice(0, 80) || '/';
    let ref = ''; try { const r = new URL(String(b.r || '')); ref = /selfstreak\.com|workers\.dev/.test(r.hostname) ? '' : r.hostname.replace(/^www\./, '').slice(0, 60); } catch {}
    const country = String(req.cf?.country || '').slice(0, 2), device = /mobile|iphone|android/i.test(ua) ? 'mobile' : /ipad|tablet/i.test(ua) ? 'tablet' : 'desktop';
    await env.DB.prepare('INSERT INTO page_views (day, path, ref, country, device, n) VALUES (?, ?, ?, ?, ?, 1) ON CONFLICT(day, path, ref, country, device) DO UPDATE SET n = n + 1').bind(day, path, ref, country, device).run();
    const h = (await sha256(day + (req.headers.get('cf-connecting-ip') || '') + ua)).slice(0, 24);
    await env.DB.prepare('INSERT OR IGNORE INTO visitors (day, h) VALUES (?, ?)').bind(day, h).run();
    return json({ ok: true });
  }

  const u = await currentUser(env, req);
  if (!u) return err(401, 'not_signed_in');
  if (p.startsWith('/api/game')) { const r = await gameRoutes(req, env, p, m, body, u); if (r) return r; }
  if (p.startsWith('/api/billing/rzp/')) { const r = await rzpRoutes(req, env, p, m, body, u, url); if (r) return r; }
  if (p.startsWith('/api/billing/store/')) { const r = await storeRoutes(req, env, p, m, body, u); if (r) return r; }
  if (Date.now() - (u.last_seen || 0) > 10 * 60e3) {
    await env.DB.prepare('UPDATE users SET last_seen = ? WHERE id = ?').bind(Date.now(), u.id).run();
    await env.DB.prepare('INSERT OR IGNORE INTO active_days (user_id, day) VALUES (?, ?)').bind(u.id, istDay()).run();
  }

  if (p.startsWith('/api/admin/')) {
    if (u.plan !== 'owner') return err(403, 'forbidden');
    return admin(req, env, url, p, m, body);
  }

  if (p === '/api/me' && m === 'GET') { await storeRefresh(env, u).catch(() => {}); return json(await me(env, u)); }
  if (p === '/api/profile' && m === 'POST') {
    const b = await body();
    await env.DB.prepare('UPDATE users SET name = ? WHERE id = ?').bind(String(b.name || '').slice(0, 60), u.id).run();
    return json({ ok: true });
  }
  if (p === '/api/password' && m === 'POST') {
    const b = await body();
    if (!safeEqual(await hashPassword(String(b.current || ''), u.salt), u.pass_hash)) return err(400, 'Current password is wrong.');
    if (String(b.next || '').length < 8) return err(400, 'Use at least 8 characters.');
    const salt = randHex(16);
    await env.DB.prepare('UPDATE users SET pass_hash = ?, salt = ? WHERE id = ?').bind(await hashPassword(String(b.next), salt), salt, u.id).run();
    await env.DB.prepare('DELETE FROM sessions WHERE user_id = ? AND token_hash <> ?').bind(u.id, await sha256(cookie(req, 'ss_session') || '')).run();
    return json({ ok: true });
  }
  if (p === '/api/account' && m === 'DELETE') {
    for (const t of ['sessions', 'user_data', 'usage', 'push_subs', 'push_schedule', 'active_days', 'password_resets', 'game']) await env.DB.prepare(`DELETE FROM ${t} WHERE user_id = ?`).bind(u.id).run(); await env.DB.prepare('DELETE FROM friends WHERE a = ? OR b = ?').bind(u.id, u.id).run();
    try { await env.DB.prepare('DELETE FROM apple_ids WHERE user_id = ?').bind(u.id).run(); } catch (e) {}
    await env.DB.prepare('DELETE FROM users WHERE id = ?').bind(u.id).run();
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(req, '', 0) });
  }
  if (p === '/api/data') {
    if (m === 'GET') {
      const r = await env.DB.prepare('SELECT json, updated FROM user_data WHERE user_id = ?').bind(u.id).first();
      return json(r ? { data: JSON.parse(r.json), updated: r.updated } : { data: null, updated: 0 });
    }
    if (m === 'PUT') {
      const text = await req.text();
      if (text.length > 1_900_000) return err(413, 'Your data is too large to sync.');
      let b; try { b = JSON.parse(text); } catch { return err(400, 'bad_json'); }
      const updated = Number(b.updated) || Date.now();
      if (b.base != null) {
        const cur = await env.DB.prepare('SELECT json, updated FROM user_data WHERE user_id = ?').bind(u.id).first();
        if (cur && cur.updated > Number(b.base)) return json({ conflict: true, data: JSON.parse(cur.json), updated: cur.updated }, 409);
      }
      await env.DB.prepare('INSERT INTO user_data (user_id, json, updated) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET json = excluded.json, updated = excluded.updated')
        .bind(u.id, JSON.stringify(b.data ?? null), updated).run();
      return json({ ok: true, updated });
    }
  }
  if (p === '/api/ai' && m === 'POST') {
    if (planStatus(u) === 'expired') return err(402, 'Your free trial has ended. Subscribe to keep using AI features.');
    const b = await body(), spec = (() => { try { return buildTask(String(b.task || ''), b.input || {}); } catch { return 'bad_file'; } })();
    if (spec === 'bad_file') return err(400, 'That file type isn’t supported. Use a PDF or a photo (JPG/PNG).');
    if (!spec) return err(400, 'unknown_task');
    const limit = Number(env.DAILY_AI_LIMIT || 100), day = istDay();
    const row = await env.DB.prepare('INSERT INTO usage (user_id, day, count) VALUES (?, ?, 1) ON CONFLICT(user_id, day) DO UPDATE SET count = count + 1 WHERE count < ? RETURNING count').bind(u.id, day, limit).first();
    if (!row) return err(429, `You’ve used all ${limit} AI actions for today. They reset at midnight.`, { used: limit, limit });
    try {
      const out = await runAI(env, spec);
      if (out.error) return err(422, out.error === 'refused' ? 'The AI declined this one.' : 'That was too long to read in one go. Try a shorter statement period.', { used: row.count, limit });
      return json({ result: out.result, used: row.count, limit });
    } catch (e) {
      // Refund only when the request never produced output (overloaded / network / auth); a bad reply still cost tokens.
      console.error('ai', b.task, e?.status || '', String(e?.message || e).slice(0, 300));
      const status = e?.status || 0, upstream = status >= 400 || e?.name === 'APIConnectionError' || /connection|fetch/i.test(String(e?.message || ''));
      if (upstream) await env.DB.prepare('UPDATE usage SET count = MAX(count - 1, 0) WHERE user_id = ? AND day = ?').bind(u.id, day).run();
      return err(502, status === 429 || status === 529 ? 'The AI is busy right now. Try again in a minute.' : 'The AI couldn’t process that. Please try again.', { used: upstream ? row.count - 1 : row.count, limit });
    }
  }
  if (p === '/api/vt' && m === 'POST') {
    const b = await body().catch(() => ({}));
    console.log('voice-timing', JSON.stringify(b).slice(0, 400));
    return json({ ok: true });
  }
  if (p === '/api/stt' && m === 'POST') {
    // Speech-to-text for the assistant mic (Whisper on Workers AI). We record the audio ourselves,
    // so phones don't play their system dictation beep.
    if (!env.AI) return err(501, 'no_stt');
    if (planStatus(u) === 'expired') return err(402, 'trial_ended');
    const buf = await req.arrayBuffer();
    if (!buf.byteLength) return err(400, 'empty');
    if (buf.byteLength > 4_000_000) return err(413, 'Recording too long. Keep it under a minute.');
    const day = 'stt-' + istDay(), cap = Number(env.DAILY_STT_MB || 40) * 1_000_000;
    const row = await env.DB.prepare('INSERT INTO usage (user_id, day, count) VALUES (?, ?, ?) ON CONFLICT(user_id, day) DO UPDATE SET count = count + ? WHERE count + ? <= ? RETURNING count').bind(u.id, day, buf.byteLength, buf.byteLength, buf.byteLength, cap).first();
    if (!row) return err(429, 'Voice limit reached for today. Type instead, or try tomorrow.');
    const ctype = (req.headers.get('content-type') || 'audio/mp4').split(';')[0];
    const t0 = Date.now();
    // Deepgram Nova-3 (fast, Indian English); Whisper is the fallback if it fails.
    let raw = '', engine = 'nova3';
    try {
      const n = await env.AI.run('@cf/deepgram/nova-3', { audio: { body: new Blob([buf], { type: ctype }).stream(), contentType: ctype }, language: 'en-IN', smart_format: true, numerals: true, punctuate: true, keyterm: 'Zomato Swiggy UPI EMI Paytm Blinkit Zepto chai' });
      raw = n?.results?.channels?.[0]?.alternatives?.[0]?.transcript || '';
    } catch (e) { console.error('nova3', String(e?.message || e).slice(0, 200)); }
    let bin = '';
    try {
      const r = raw ? { text: raw } : (engine = 'whisper', await (async () => { const bytes = new Uint8Array(buf); for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
        return env.AI.run('@cf/openai/whisper-large-v3-turbo', { audio: btoa(bin), task: 'transcribe', vad_filter: true, initial_prompt: 'Indian English and Hinglish about habits, steps, water, gym, rupees, bills, EMI, Zomato, Swiggy, UPI.' }); })());
      console.log('stt', engine, Date.now() - t0, 'ms');
      // Money in this app is always rupees: Whisper sometimes writes "150" as "$150" or "150 dollars".
      const text = String(r?.text || '').trim()
        .replace(/\$\s?(\d{1,2})\.(\d0)\b/g, (m, a, b) => '₹' + (Number(a) * 100 + Number(b))) // "one fifty" → $1.50 → ₹150
        .replace(/\$\s?(\d[\d,]*(?:\.\d+)?)/g, '₹$1')
        .replace(/(\d[\d,]*(?:\.\d+)?)\s*(?:US\s*)?(?:dollars?|bucks|USD)\b/gi, '₹$1');
      return json({ text });
    } catch (e) { console.error('stt', e); return err(502, 'Couldn’t understand that. Please try again.'); }
  }
  if (p === '/api/tts' && m === 'POST') {
    // Natural voice for talk-back (Deepgram Aura-2 on Workers AI). Capped per user per day.
    if (!env.AI) return err(501, 'no_tts');
    if (planStatus(u) === 'expired') return err(402, 'trial_ended');
    const b = await body(), text = String(b.text || '').replace(/\s+/g, ' ').trim().slice(0, 600);
    if (!text) return err(400, 'empty');
    const VOICES = ['luna', 'thalia', 'asteria', 'athena', 'aurora', 'orion', 'arcas', 'apollo', 'hermes', 'zeus'];
    const speaker = VOICES.includes(b.voice) ? b.voice : 'luna';
    // Fixed app lines (onboarding questions) are generated once and then served to everyone from Cloudflare's cache.
    const shared = b.shared === true && text.length <= 300, ck = shared ? new Request('https://tts-cache.selfstreak.com/' + speaker + '/' + (await sha256(text))) : null;
    if (ck) { try { const hit = await caches.default.match(ck); if (hit) return new Response(hit.body, { headers: { 'content-type': 'audio/mpeg', 'cache-control': 'private, max-age=86400', 'x-tts-cache': 'hit' } }); } catch (e) {} }
    const day = 'tts-' + istDay(), cap = Number(env.DAILY_TTS_CHARS || 30000);
    const row = await env.DB.prepare('INSERT INTO usage (user_id, day, count) VALUES (?, ?, ?) ON CONFLICT(user_id, day) DO UPDATE SET count = count + ? WHERE count + ? <= ? RETURNING count').bind(u.id, day, text.length, text.length, text.length, cap).first();
    if (!row) return err(429, 'tts_limit');
    try {
      const r = await env.AI.run('@cf/deepgram/aura-2-en', { text, speaker, encoding: 'mp3' }, { returnRawResponse: true });
      const h = new Headers({ 'content-type': 'audio/mpeg', 'cache-control': 'private, max-age=3600' });
      if (ck && r.ok) { const [a, c] = r.body.tee(); ctx?.waitUntil?.(caches.default.put(ck, new Response(c, { headers: { 'content-type': 'audio/mpeg', 'cache-control': 'public, max-age=2592000' } })).catch(() => {})); return new Response(a, { status: 200, headers: h }); }
      return new Response(r.body, { status: r.ok ? 200 : 502, headers: h });
    } catch (e) { console.error('tts', e); return err(502, 'tts_failed'); }
  }
  if (p === '/api/push/subscribe' && m === 'POST') {
    const b = await body();
    if (!/^https:\/\//.test(b.endpoint || '') || !b.keys?.p256dh || !b.keys?.auth) return err(400, 'bad_subscription');
    await env.DB.prepare('INSERT INTO push_subs (endpoint, user_id, p256dh, auth, created) VALUES (?, ?, ?, ?, ?) ON CONFLICT(endpoint) DO UPDATE SET user_id = excluded.user_id, p256dh = excluded.p256dh, auth = excluded.auth')
      .bind(b.endpoint, u.id, b.keys.p256dh, b.keys.auth, Date.now()).run();
    return json({ ok: true });
  }
  if (p === '/api/push/unsubscribe' && m === 'POST') {
    const b = await body();
    await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ? AND user_id = ?').bind(String(b.endpoint || ''), u.id).run();
    return json({ ok: true });
  }
  if (p === '/api/push/schedule' && m === 'PUT') {
    const b = await body(), now = Date.now();
    const items = (Array.isArray(b.items) ? b.items : []).filter((i) => Number(i.at) > now - 3600e3 && Number(i.at) < now + 3 * DAY).slice(0, 300).map((i) => ({
      at: Number(i.at), title: String(i.title || '').slice(0, 120), body: String(i.body || '').slice(0, 400), url: String(i.url || './').slice(0, 200), tag: String(i.tag || '').slice(0, 120),
      actions: (Array.isArray(i.actions) ? i.actions : []).slice(0, 2).map((a) => ({ action: String(a.action).slice(0, 20), title: String(a.title).slice(0, 30) })),
      acts: Object.fromEntries(Object.entries(i.acts || {}).slice(0, 2).map(([k, v]) => [String(k).slice(0, 20), String(v).slice(0, 120)])),
    }));
    await env.DB.prepare('INSERT INTO push_schedule (user_id, items, last_sent, updated) VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET items = excluded.items, updated = excluded.updated')
      .bind(u.id, JSON.stringify(items), now, now).run();
    return json({ ok: true, count: items.length });
  }
  if (p === '/api/push/test' && m === 'POST') {
    const subs = (await env.DB.prepare('SELECT * FROM push_subs WHERE user_id = ?').bind(u.id).all()).results;
    let sent = 0;
    for (const s of subs) { const st = await sendPush(s, { title: 'Push is working 🎉', body: 'Self Streak can now remind you even when the app is closed.', tag: 'push-test', url: './#/notify' }, env); if (st < 300) sent++; else if (st === 404 || st === 410) await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ?').bind(s.endpoint).run(); }
    return json({ ok: true, sent, devices: subs.length });
  }
  if (p === '/api/billing/checkout' && m === 'POST') {
    if (!cfReady(env)) return err(501, 'Online payments are launching soon. We’ll email you as soon as you can subscribe.');
    if (u.plan === 'owner') return err(400, 'You’re the owner. No subscription needed.');
    const b = await body(), phone = String(b.phone || '').replace(/\D/g, '').slice(-10);
    if (!/^[6-9]\d{9}$/.test(phone)) return err(400, 'Enter your 10-digit mobile number. The payment page needs it.');
    const amount = Number(env.PRICE_INR || 199), orderId = 'ss_' + u.id.replace(/-/g, '').slice(0, 12) + '_' + Date.now();
    const r = await cf(env, '/orders', {
      method: 'POST',
      body: JSON.stringify({
        order_id: orderId, order_amount: amount, order_currency: 'INR', order_note: 'Self Streak Plus · 1 month',
        customer_details: { customer_id: u.id.replace(/-/g, '').slice(0, 40), customer_email: u.email, customer_phone: phone, customer_name: (u.name || '').slice(0, 60) || undefined },
        order_meta: { return_url: `${url.origin}/app?order_id={order_id}`, notify_url: `${url.origin}/api/billing/webhook` },
      }),
    });
    const o = await r.json().catch(() => ({}));
    if (!r.ok || !o.payment_session_id) { console.error('cashfree order', r.status, JSON.stringify(o)); return err(502, 'Couldn’t start the payment. Please try again in a minute.'); }
    await env.DB.prepare('INSERT INTO payments (order_id, user_id, amount, status, created) VALUES (?, ?, ?, ?, ?)').bind(orderId, u.id, amount, 'created', Date.now()).run();
    return json({ orderId, paymentSessionId: o.payment_session_id, mode: cfMode(env) });
  }
  if (p === '/api/billing/verify' && m === 'POST') {
    const b = await body(), orderId = String(b.order_id || '');
    const row = await env.DB.prepare('SELECT * FROM payments WHERE order_id = ? AND user_id = ?').bind(orderId, u.id).first();
    if (!row) return err(404, 'Payment not found.');
    const st = await settleOrder(env, orderId);
    const fresh = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(u.id).first();
    return json({ status: st, me: await me(env, fresh) });
  }
  return err(404, 'not_found');
}

/* ---------------- scheduled: send due reminders as push notifications ---------------- */
async function sendDuePushes(env) {
  const now = Date.now();
  // Push reminders are a Plus feature: skip people on the Free plan (past trial/paid end + grace).
  const rows = (await env.DB.prepare(`SELECT s.user_id, s.items, s.last_sent FROM push_schedule s WHERE EXISTS (SELECT 1 FROM push_subs p WHERE p.user_id = s.user_id)
      AND EXISTS (SELECT 1 FROM users u WHERE u.id = s.user_id AND (u.plan = 'owner' OR u.paid_until > ? OR u.trial_ends > ?))`).bind(now - GRACE, now - GRACE).all()).results;
  for (const r of rows) {
    const since = Math.max(Number(r.last_sent) || 0, now - 20 * 60000);
    const due = JSON.parse(r.items).filter((i) => i.at > since && i.at <= now);
    if (!due.length) continue;
    const msg = due.length === 1 ? due[0] : { title: `${due.length} reminders`, body: due.map((i) => '• ' + i.title).join('\n'), tag: due[0].tag, url: due[0].url };
    const subs = (await env.DB.prepare('SELECT * FROM push_subs WHERE user_id = ?').bind(r.user_id).all()).results;
    for (const s of subs) {
      try { const st = await sendPush(s, msg, env); if (st === 404 || st === 410) await env.DB.prepare('DELETE FROM push_subs WHERE endpoint = ?').bind(s.endpoint).run(); } catch (e) { /* try again next run */ }
    }
    await env.DB.prepare('UPDATE push_schedule SET last_sent = ? WHERE user_id = ?').bind(now, r.user_id).run();
  }
  await env.DB.prepare('DELETE FROM sessions WHERE expires < ?').bind(now).run();
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    // Old address and www → the main domain (pages only; the API keeps working everywhere).
    if ((url.hostname.endsWith('.workers.dev') || url.hostname === 'www.selfstreak.com') && !url.pathname.startsWith('/api/') && req.method === 'GET' && url.pathname !== '/sw.js') {
      return Response.redirect('https://selfstreak.com' + url.pathname + url.search, 301);
    }
    // Google Search Console ownership file (served exactly, no redirects).
    if (url.pathname === '/googleed720d5bc99e0297.html') return new Response('google-site-verification: googleed720d5bc99e0297.html', { headers: { 'content-type': 'text/html; charset=utf-8' } });
    if (url.pathname.startsWith('/api/')) {
      try { return await api(req, env, url, ctx); } catch (e) { console.error(e); return err(500, 'Something went wrong. Please try again.'); }
    }
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/app' || url.pathname === '/app/')) {
      const app = url.pathname !== '/' || !!cookie(req, 'ss_session');
      const r = await env.ASSETS.fetch(new Request(new URL(app ? '/' : '/landing', url), req));
      const h = new Headers(r.headers); h.set('cache-control', 'no-cache');
      if (app) return new Response(r.body, { status: r.status, headers: h });
      h.set('x-ss-page', 'landing'); h.set('cache-control', 'no-store');
      return new Response(r.body, { status: r.status, headers: h });
    }
    return env.ASSETS.fetch(req);
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(sendDuePushes(env)); ctx.waitUntil(gameCron(env, mailReady(env) && env.EMAIL_UPDATES === '1' ? sendMail : null).catch((e) => console.error('gameCron', e)));
    // Renewal reminders once a day around 10 am IST (deduped per user/step in the meta table).
    const hm = new Date(Date.now() + 5.5 * 3600e3); const mins = hm.getUTCHours() * 60 + hm.getUTCMinutes();
    if (mins >= 600 && mins < 660) ctx.waitUntil(renewalReminders(env, mailReady(env) && env.EMAIL_UPDATES === '1' ? sendMail : null).catch((e) => console.error('renew', e))); },
};
