# Warehouse West Event Collective

Static venue website for Warehouse West, 1397 Hamilton Ave, St. Louis. HTML, CSS and JavaScript live in `index.html`; images, fonts and app icons are self-hosted. No framework, database or package installation is required.

**Publication URL:** https://knr315.github.io/warehouse-west-site/ (available after Pages deployment succeeds).

## Publish on GitHub Pages

1. Open [Settings → Pages](https://github.com/KNR315/warehouse-west-site/settings/pages).
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Open [Actions → Validate and publish website](https://github.com/KNR315/warehouse-west-site/actions/workflows/pages.yml), select **Run workflow**, and run it on `main`. Future pushes to `main` validate and publish automatically. Pull requests validate without deploying.
4. Confirm both `validate` and `deploy` are green, then open the publication URL.

The workflow checks HTML field references, local assets, metadata, the app manifest and JavaScript syntax. It stages an explicit list of public site files in `_site/`; README files, scripts and Git metadata are excluded. If `Configure Pages` reports that the site is missing, complete step 2 and rerun the failed workflow.

## Local checks and preview

Requires Python 3 and Node.js for checks; serving the website only requires Python 3.

```sh
python3 scripts/check-site.py
python3 scripts/build-site.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. Check Home, Spaces, Events, Book and Info at desktop and phone widths. The 404 page's base path targets the GitHub project URL; test its links there after publication.

## Edit venue details

**Venue phone:** 314-276-2959 (call or text). Keep `CONFIG.phone`, structured-data `telephone`, and the JavaScript-disabled fallback in `index.html` aligned with this number.

Find `SITE SETTINGS` near the bottom of `index.html`. `SPACES` contains rates, descriptions and features. `CONFIG` contains the booking inbox, delivery endpoint, phone and Instagram. Update both `bookingEmail` and `endpoint` when changing the inbox. Keep head metadata, structured data, visible address and FAQ text consistent with changed venue details.

## Booking delivery

The three-step form sends requests to **Warehousewest@icloud.com** through **FormSubmit**. Contact fields and date are validated before sending. If sending fails or times out, the request remains available on the page to copy or open in an email app. Navigation to another space restores the form after a submission result.

The inbox owner must click FormSubmit's one-time **Activate Form** email on the first live submission. A successful API response means the service accepted the request; it does not prove the email arrived. Confirm activation and receipt with a real booking test before relying on delivery. Automated verification must mock the endpoint and never send customer or test data to the live inbox.

Booking requests are not stored in this repository or a site database. FormSubmit processes the submitted contact details. The form is an inquiry, not a reservation or payment. There is no live availability calendar, admin dashboard or payment backend.

## Other hosts and custom domains

Netlify and Cloudflare Pages can serve `_site/` without a framework build. Run `python3 scripts/build-site.py` as the build command and use `_site` as the publish directory. `_headers` adds security and caching headers on those hosts; GitHub Pages ignores it.

Before changing the public hostname or path, update canonical, `og:url`, social image URLs and structured data in `index.html`, plus the `<base>` path in `404.html` (use `/` for a root-domain deployment). For a GitHub Pages custom domain, configure the domain in Pages settings, follow GitHub's DNS instructions and add `CNAME` to the repository root. The staging script includes it when present.

See [AUDIT.md](AUDIT.md) for the launch review and verification limits.
