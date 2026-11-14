# Self Streak (selfstreak.com)

## Deploying: read this first
- Deploy only with `npm run deploy`. Never run `wrangler deploy` directly.
- Before deploying: `git pull origin main`, then commit your changes. The deploy refuses to run if this copy is behind GitHub main or has uncommitted changes in src/, public/, scripts/, schema.sql, wrangler.jsonc or package.json, because deploying an out-of-date copy deletes pages from the live site (this happened on 14 Nov 2026).
- After deploying, the script commits the service-worker bump and pushes to GitHub main automatically.
- A daily SEO autopilot (scheduled task) also commits to GitHub main and deploys. Always pull before starting new work.

## Marketing pages are generated
Edit the Python sources in scripts/ (build-pages.py, build_seo.py, blog_posts.py, build_compare.py, build_hi.py), then run `python3 scripts/build-pages.py`. Don't hand-edit generated HTML in public/ (landing.html and the legal pages are the exceptions). Details: seo/AUTOPILOT.md.
