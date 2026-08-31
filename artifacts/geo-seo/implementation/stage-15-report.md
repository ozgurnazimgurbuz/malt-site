# Stage 15 — Cloudflare Pages custom domain cutover (blocked)

**Outcome:** `STAGE 15 BLOCKED — NETLIFY ORIGIN STILL ACTIVE`

No application, SEO, schema, sitemap, `robots.txt`, benchmark, or content changes.

---

## Why this environment cannot finish the cutover

- `CLOUDFLARE_API_TOKEN` / Wrangler: **absent**
- Cursor browser MCP to `dash.cloudflare.com`: **not available** (provider did not register)
- Dashboard URL was opened for Özgür; attaching domains requires a logged-in Cloudflare session and DNS confirm clicks

Public origin at check time (2026-08-31): `/hakkimizda/` still **404** with `x-nf-request-id` and `cache-status: "Netlify Edge"`.

Pages production alias already serves the rebuild (`malt-site.pages.dev`).

---

## Exact dashboard action (remaining blocker)

1. Open [Pages → malt-site](https://dash.cloudflare.com/47c42d8bf8dea65321eb4cdc66502f49/pages/view/malt-site)
2. **Custom domains** → **Set up a custom domain** (or **Add domain**)
3. Add **`maltstudio.co`**
4. Confirm Cloudflare’s DNS change: apex CNAME-flatten to **`malt-site.pages.dev`** (this **replaces** the current Netlify origin behind the orange cloud)
5. Repeat for **`www.maltstudio.co`** (keep www → apex)
6. Wait until SSL shows **Active**
7. Then verify `https://maltstudio.co/hakkimizda/` = **200** and headers **without** `x-nf-request-id` / `Netlify Edge`

Do not edit git `robots.txt`. After public domain is Pages, Netlify can drop this custom domain.

---

## Not run

Live SEO HTML suite, collector → `artifacts/geo-seo/live-stage-15/` — public domain is still Netlify.
