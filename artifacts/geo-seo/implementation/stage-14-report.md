# Stage 14 — Production cutover (blocked)

**Outcome:** `STAGE 14 BLOCKED — PRODUCTION CUTOVER NOT COMPLETE`

No SEO/schema/content/`robots.txt`/benchmark/`before/` changes.

---

## Exact reason

`maltstudio.co` is on **Cloudflare DNS + orange-cloud proxy**, but the **origin behind that proxy is still Netlify**.

Evidence (2026-08-31, public lookups, not repo files):

| Fact | Value |
|---|---|
| Git | `main` / `HEAD` / `origin/main` = `846aaf5`; contains rebuild `c3335d8` |
| Pages project | `malt-site` (GitHub check success for `846aaf5`) |
| Pages production alias | `https://malt-site.pages.dev/hakkimizda/` → rebuild Hakkımızda |
| Unique deploy | `https://75f1c2b9.malt-site.pages.dev` (commit `846aaf5`) |
| Public NS | `michael.ns.cloudflare.com` / `pola.ns.cloudflare.com` |
| Public A (apex + www) | Cloudflare anycast `188.114.96.3` / `188.114.97.3` (proxied) |
| `https://maltstudio.co/` | `server: cloudflare` **and** `cache-status: "Netlify Edge"` + `x-nf-request-id` |
| `/hakkimizda/` on apex | **404** |
| `www` | 301 → `https://maltstudio.co/` (still `x-nf-request-id`) |

Registrar NS is already Cloudflare. The remaining gap is **not** “move nameservers”. It is: the proxied `@`/`www` records still send origin traffic to Netlify, and the Pages **custom domain** `maltstudio.co` is not what the apex is serving.

This environment has **no** `CLOUDFLARE_API_TOKEN`, **no** Wrangler, **no** Netlify CLI. DNS targets behind the proxy cannot be read or rewritten from here. Inventing a CNAME target was not done.

---

## Exact infrastructure action required

In the Cloudflare dashboard (same account as Pages project `malt-site`, account path already used by GitHub: `dash.cloudflare.com/?to=/47c42d8bf8dea65321eb4cdc66502f49/pages/view/malt-site/…`):

1. **Workers & Pages → malt-site → Custom domains → Add** `maltstudio.co`.
2. Let Cloudflare create/replace the apex record so it CNAME-flattens to **`malt-site.pages.dev`** (Pages production), **replacing** the current origin that produces `x-nf-request-id`.
3. Add **`www.maltstudio.co`** the same way (today www 301s to apex; keep that).
4. Wait until SSL is active, then confirm `https://maltstudio.co/hakkimizda/` is **200** and response headers **no longer** include `x-nf-request-id` / `Netlify Edge`.
5. After that is proven: Netlify dashboard → remove the custom domain / stop using this site as origin (DEPLOY-CLOUDFLARE.md Adım 5). Do not delete Netlify first.

Do not edit git `robots.txt` for AI crawlers.

---

## What was verified

- Repository `main` = rebuild.
- Cloudflare Pages **did** deploy `846aaf5`; `malt-site.pages.dev` serves `/hakkimizda/`.
- `maltstudio.co` still Netlify origin; rebuild **not** on the public hostname.
- Collector **not** run to `artifacts/geo-seo/live-stage-14/` (would not measure the public origin as the rebuild).

---

## Repository change

This report file only. No production HTML, schema, DNS files, or `robots.txt` edits.
