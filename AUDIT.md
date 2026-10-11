# Warehouse West launch review

Reviewed the original launch commit `735883a36eeefa2880fec65a3101e0fbda06b0a6` and all 27 tracked files: the README, both HTML documents, inline CSS and JavaScript, header policy, robots rules, app manifest, favicon artwork, six raster icons/social assets, four venue images and ten local font files. The repository originally had one branch, one commit, no open pull requests and no Actions runs. The intended public URL returned HTTP 404 before these changes.

## Architecture

This is a buildless, single-document site with five hash-routed views: Home, Spaces, Events, Book and Info. Its data is configured in `CONFIG`, `SPACES`, `GROUPS` and `EVENTS`. Layouts switch between desktop navigation and a phone tab bar. The three-step booking form posts JSON to FormSubmit and offers a copy/email fallback. There is no server, database, authentication, payment processing or availability system in this repository. No credentials or customer records were found in the tracked source.

## Changes

| Finding | Resolution |
| --- | --- |
| No deployment configuration | Added a GitHub Pages workflow for validated `main` pushes and manual runs; pull requests only validate. |
| Entire source directory described as the live site | Added explicit public-file staging to exclude documentation, scripts and Git metadata. |
| 404 assets and home link targeted the account root | Set a project-relative base for nested missing URLs. |
| Relative social-preview image | Added absolute HTTPS canonical, Open Graph, Twitter and structured-data URLs. |
| Returning to step 3 could bypass an invalid date | Validate forward step navigation and revalidate the date at final submission. |
| Date threshold was frozen when the page loaded | Recompute today's minimum at validation time. |
| Phone validation accepted arbitrarily long digit strings | Require ten US digits with an optional leading 1. |
| Selecting a new space after a result kept the form hidden | Restore the form and hide stale result panels when starting another booking. |
| Programmatic repeated submissions could race | Guard pending submission and mark the form busy. |
| Failed fetch could leave its timeout pending | Always clear the timeout in `finally`. |
| Errors lacked programmatic field relationships | Add required contact fields, error descriptions, invalid-state attributes and focus on final validation failure. |
| Success text claimed verified inbox delivery | Describe submission acceptance and provide phone follow-up. |

## Verification

- Python/Node checks pass for HTML identifiers and field references, local assets, structured data, app manifest, absolute social image URLs and JavaScript syntax.
- The deployment staging script produces 26 public files and excludes source-control and documentation files.
- A local DOM smoke harness executed the complete application script with mocked browser APIs and a mocked FormSubmit endpoint. It passed all five views, four space selections, event filtering, rules switching, date/contact validation, step-navigation validation, submission success/failure, safe fallback rendering, result recovery, duplicate-submit prevention and request-timeout cleanup.
- Raster asset dimensions were inspected: social image 1200×630, touch icon 180×180, app icons 192×192 and 512×512. All referenced local assets are present.
- `git diff --check` passes.

The DOM harness does not verify visual layout, native browser date controls or clipboard behavior. A browser runtime could not be downloaded in this environment, so desktop/phone visual QA remains unverified. No live booking request was sent. FormSubmit activation and actual inbox receipt require the inbox owner's live test. Security response headers in `_headers` are supported by Netlify/Cloudflare Pages and are ignored by GitHub Pages.

## Hosting prerequisite

The Pages workflow requires **Settings → Pages → Source: GitHub Actions**. Creating commits does not enable that repository setting. If the deployment job reports a missing Pages site, enable the source and rerun the workflow. Only a successful deployment and HTTP response at the public URL establish that publication is complete.
