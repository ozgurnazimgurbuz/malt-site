# Stage 16 — Cloudflare AI crawler allow (live check)

**Dashboard change:** succeeded (managed `robots.txt` prepend gone).  
**TECHSEO-001 collector row:** still **FAIL** (false positive in the check, not a live Disallow).

No application / SEO / schema / content / git `robots.txt` / benchmark / `before/` edits.

---

## Live `https://maltstudio.co/robots.txt`

Fetched 2026-08-31. **594 bytes.** `# BEGIN Cloudflare Managed content` is **absent**.

Served file matches git `robots.txt`:

- `User-agent: *` / `Allow: /`
- `Disallow: /admin/` and `Disallow: /proje/`
- **No** `User-agent: GPTBot|ClaudeBot|Google-Extended` + `Disallow: /`

Those three names appear only in a **comment** at the bottom of the git file.

---

## Collector

```
python3 scripts/seo/collect.py --out artifacts/geo-seo/live-stage-16 --phase AFTER
```

```
AFTER captured SHA=76be213 urls=35 geo_mean=3.222 fails=4
```

| | Stage 15 live | Stage 16 live |
|---|---|---|
| GEO mean | 3.133 | **3.222** |
| `/` | 3.222 | 3.222 |
| tabela | 3.000 | 3.111 |
| guide | 3.778 | 3.889 |
| Tekirdağ | 3.111 | 3.222 |
| ofiso | 2.556 | 2.667 |

GEO rose because `live_bots_blocked_agents` is now **`[]`** (strict `User-agent: … Disallow: /` in `main()`). Machine-readability is no longer penalized for a live AI Disallow.

---

## Is TECHSEO-001 resolved?

**Externally (Cloudflare):** yes. Live file no longer injects AI `Disallow: /`.

**Collector `live_robots_blocks_ai`:** still FAIL. Check is:

```
ua in live_robots and "Disallow: /" in live_robots
```

Git comments contain `GPTBot` / `ClaudeBot` / `Google-Extended`, and `Disallow: /admin/` contains the substring `Disallow: /`. That is not an actual crawler block.

This stage did **not** change `collect.py` or git `robots.txt` (Stage 16 forbids both).

Remaining real fails: TECHSEO-005 (GSC token), CONTENT-001, GEO-002. Unscored: GBP, LinkedIn.

---

BEFORE **2.333** → AFTER **3.133** → LIVE-15 **3.133** → LIVE-16 **3.222 / 5**
