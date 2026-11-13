# SEO log

- 2026-11-13: Synced the live site's code to GitHub on branch `live-site-sync`. Before this, the blog, the EMI pages, llms.txt and the worker changes were only in an uncommitted local copy.
- 2026-11-13: www, http and workers.dev copies of every page, plus /landing, now 301 to https://selfstreak.com (`src/worker.js`, `wrangler.jsonc` run_worker_first). Before this, only the homepage redirected.
- 2026-11-13: Fixed pricing FAQs that said there is no free plan on /habit-tracker, /credit-card-bill-reminder and /calorie-protein-tracker (the code has a free plan, `src/worker.js:47`).
- 2026-11-13: Surfaced the free plan on /habit-tracker (meta description) and /expense-tracker (new FAQ and FAQ schema).
