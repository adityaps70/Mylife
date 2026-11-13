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
