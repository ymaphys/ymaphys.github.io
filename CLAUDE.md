# CLAUDE.md — ymaphys.github.io

Yue Ma's personal academic homepage. **Plain hand-written static HTML, no build step.** This is a
GitHub **user page**, so **any push to `main` deploys live within ~1–2 min** — GitHub Pages serves the
files directly (no Jekyll, no Actions).

- **Repo:** `github.com/ymaphys/ymaphys.github.io` · **Live:** https://ymaphys.github.io

## Structure
| Path | What |
|------|------|
| `index.html` | Home — bio, research interests, selected recent publications, a phase-space code snippet |
| `cv.html` | CV (HTML, mirrors the PDF) + multi-language CV download buttons |
| `research.html` | Research directions + detector development |
| `publications.html` | **Generated** (see below) — Selected + grouped full list + multi-language PDF downloads |
| `assets/css/style.css` | All styling. Key classes: `.btn`, `.role-tag`, `.pub-title`, `.pub-meta`, `.pub-note`, `.count`, `.publication-list`, `.cv-entry`, `.cv-date`, `.subtitle` |
| `assets/js/script.js` | Minor JS |
| `assets/pdf/` | The downloadable PDFs (see *Languages*) |
| `tools/` | The Publications generator + its data — **not** part of the rendered site |

## Conventions
- **Tone:** professional / formal academic (earlier playful copy was removed — keep it out).
- **Math & particle notation:** MathJax (tex-svg) is loaded on every page; use `\( … \)` for inline math.
  **Hypernuclei must use a subscript Λ/Σ**, e.g. `\(^{4}_{\Lambda}\mathrm{H}\)` → ⁴ΛH. Plain isotopes
  (³He, ⁴He) stay as Unicode superscripts; other symbols (Λπ, K̄N, π⁺, B⁰) are fine as Unicode.
- **Nav** is duplicated in each page's `<header>` — keep the four links and `class="active"` on the current page.
- **Footer:** `© 2026 Yue Ma · Last updated <month year>`.
- **Contact:** email + ORCID only. **INSPIRE is deliberately NOT linked** — the live INSPIRE author profile
  is Belle-only and hides the lead-author work; ORCID is the canonical ID.

## Languages — downloadable PDFs
The CV and publication list ship in **three languages**, in `assets/pdf/`, linked from `cv.html` and `publications.html`:

| | English | 中文 (default) | 日本語 |
|--|--|--|--|
| **CV** | `Ma_Yue_CV_EN.pdf` | `Ma_Yue_CV.pdf` | `Ma_Yue_CV_JP.pdf` |
| **Publications** | `Ma_Yue_Publications_EN.pdf` | `Ma_Yue_Publications.pdf` | `Ma_Yue_Publications_JP.pdf` |

These PDFs are **built outside this repo** from LaTeX in the maintainer's CV workspace
(`general_CV/Ma_Yue_CV{,_EN,_JP}.tex` and `Ma_Yue_Publications{,_EN,_JP}.tex`, `xelatex ×2`) and copied
into `assets/pdf/`. The Japanese docs override the CJK font to Hiragino Mincho/Sans. When the CV/pubs
change, rebuild those PDFs and re-copy them here.

## Publications page is GENERATED — do not hand-edit
`publications.html` is produced by **`tools/build_publications.py`** from **`tools/Ma_Yue_papers_only.bib`**
(127 verified entries, sectioned). To change it, edit the bib or the script and regenerate:

```bash
python3 tools/build_publications.py      # rewrites ../publications.html  (no deps beyond Python 3)
```

Emitted structure: **Selected** (curated, role-tagged) → **Lead-author / J-PARC / OLYMPUS (10)** →
**Belle / Belle II** (digest: first `DIGEST_N`=15 of 78 on the page; the full set lives in the PDF) →
**Other journals (12)** → **Proceedings (27)**. The script cleans LaTeX titles to plain Unicode and
converts hypernuclei to MathJax. Tunables near the top: `DIGEST_N`, `SELECTED`. Keep
`tools/Ma_Yue_papers_only.bib` in sync with the master bib in the CV workspace.

## Update / deploy
```bash
git add -A && git commit -m "…" && git push origin main
```
Deploy lags ~1–2 min and the CDN may briefly serve the old copy — verify the live site with a
cache-busting query, e.g. `https://ymaphys.github.io/publications.html?v=2`.

## Don't
- Don't commit `.history/` (VS Code local history — gitignored).
- Don't hand-edit `publications.html` — regenerate it.
- Don't add the INSPIRE link.

## Revert
Pre-enrichment snapshot: git tag **`pre-cv-enrich-20260625`** (+ a tarball backup beside the repo).
`git reset --hard pre-cv-enrich-20260625` to roll back.
