# Warehouse West Event Collective — website

Static site for Warehouse West, 1397 Hamilton Ave, St. Louis. No build step is needed to host it: every file in this folder is the live site.

## Edit prices, spaces or contact info
Open `index.html` and find `SITE SETTINGS` near the bottom. Prices and descriptions live in `SPACES`; email, phone and Instagram live in `CONFIG`.

## Booking requests
The Book form sends each request to **Warehousewest@icloud.com** through FormSubmit (formsubmit.co).
The first request on the live site sends a one-time **"Activate Form"** email to that inbox. Click it once; every later request arrives directly.
If sending ever fails, visitors see their request ready to copy and email, so nothing is lost.

## Hosting
- **GitHub Pages:** Settings → Pages → Source "Deploy from a branch" → `main` / `(root)`.
- **Netlify / Cloudflare Pages:** connect this repo, no build command, publish directory `/`. `_headers` adds security and caching headers on these hosts.

## Custom domain
Add the domain in your host's settings, then point DNS as the host instructs. For GitHub Pages, put the domain in a file named `CNAME` in this folder.
