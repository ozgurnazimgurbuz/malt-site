# Frozen GEO rubric (Stage 2)

**Do not change scoring rules after BEFORE capture.**

Scale: 0 = absent · 1 = weak · 2 = partial · 3 = adequate · 4 = strong · 5 = excellent.

Score page types, not the original 45/100 composite. Program composite = mean of nine dimensions on the frozen five-URL set: `/`, `/hizmetler/tabela/`, `/bilgi/tabela-cesitleri/`, `/bolgeler/tekirdag/`, `/projeler/ofiso/`.

| Dimension | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| **Entity clarity** | No NAP / no name | Brand name only | NAP in HTML, no schema | LocalBusiness + NAP match | + geo/hours/logo | + GBP/sameAs consistent, no colliding sameAs |
| **Answerability** | No Q/A | Fragments | FAQ or H2 questions, 1-line answers | Direct 2–4 sentence answers | 80–160w self-contained answers | Same + tables/lists AI can lift |
| **Semantic structure** | No H1 | Multiple H1 or skip levels | One H1, messy H2 | H1>H2>H3, lists | Question H2s + process ol | + comparison table |
| **Structured data** | None | Invalid JSON | Thin LocalBusiness | WebSite+Service+Breadcrumb | + FAQPage parity + Article on guides | Full graph, no dangling @id, knowsAbout |
| **Machine readability** | JS-only body | Thin HTML | SSR text | llms.txt + twins | Twins ≈ HTML + llms facts | Bots allowed + twins complete |
| **Entity relationships** | Isolated pages | Links, no schema | Breadcrumbs HTML | BreadcrumbList + provider @id | WebSite hub + Service about business | Person/GBP/Wikidata sameAs |
| **Trust** | No contact | Phone or address | Full NAP | Hours + maps link | Legal page + honest no-fake-metrics | Reviews only if real; Person named |
| **Freshness** | No dates | Copyright only | Sitemap lastmod some | lastmod all + visible güncelleme on guides | Visible dates match lastmod | Changelog / dateModified in Article |
| **Extractability** | Nothing quotable | Cards/fragments | Short definitions | Named-subject paragraphs | 80–160w unique (not EEAT clone) | Project pages citeable case facts |

Scoring rule: integer 0–5 per dimension per URL; report mean. Evidence quotes required. Do not invent external citations.
