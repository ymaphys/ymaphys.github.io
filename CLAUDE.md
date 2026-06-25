# CLAUDE.md — ymaphys.github.io

Yue Ma's personal academic homepage. **Plain hand-written static HTML, no build step.** This is a
GitHub **user page**, so **any push to `main` deploys live within ~1–2 min** — GitHub Pages serves the
files directly (no Jekyll, no Actions).

- **Repo:** `github.com/ymaphys/ymaphys.github.io` · **Live:** https://ymaphys.github.io

## ⚠️ Consistency is a HIGH-PRIORITY rule
Treat the whole site — every HTML page **and** every downloadable PDF, in every language — as one
coherent artifact. A change in one place is not done until its counterparts everywhere are aligned.
Before finishing any edit, check across:
- **Parallel UI:** symmetric/parallel labels and structure. Language links/buttons name only the language
  and match across pages — `English (PDF)` / `中文 (PDF)` (no lopsided "Download CV — English" vs bare "中文").
- **Web ⇄ download PDFs:** `publications.html` and the download PDFs carry the **same sections, entries and
  order**. The **only** intended difference is Belle/Belle II — a digest (first `DIGEST_N`) on the page vs the
  full list in the PDFs. (The web is generated from the bib; the PDFs are built from the LaTeX workspace — keep both in step.)
- **Role / contribution wording:** use the **exact** expressions from the CV, and keep them consistent across
  the CV, the publications page, and the PDFs. **Each language uses its own CV's wording** — EN: "First author /
  Spokesperson & corresponding author / Led the luminosity monitor"; 中文: "第一作者 / 发言人 & 通讯作者 /
  主导亮度监测器（PbF₂）研制"; 日本語: "筆頭著者 / スポークスパーソン & 責任著者 / 輝度モニターの開発を主導".
- **Notation & tone:** hypernuclei subscript-Λ, formal academic tone, footer/nav — identical everywhere (see *Conventions*).

When in doubt, after any change grep the other pages, the generator, and all language `.tex`/PDFs for the same
string and confirm they agree.

## Structure
| Path | What |
|------|------|
| `index.html` | Home — bio, research interests, selected recent publications, a phase-space code snippet |
| `cv.html` | CV (HTML, mirrors the PDF) + multi-language CV download buttons |
| `research.html` | Research directions + detector development |
| `publications.html` | **Generated** (see below) — role-tagged grouped full list + multi-language PDF downloads |
| `assets/css/style.css` | All styling. Key classes: `.btn`, `.role-tag`, `.pub-title`, `.pub-meta`, `.pub-note`, `.count`, `.publication-list`, `.cv-entry`, `.cv-date`, `.subtitle` |
| `assets/js/script.js` | Minor JS |
| `assets/pdf/` | The downloadable PDFs (see *Languages*) |
| `tools/` | The Publications generator (`build_publications.py`) + its bib data — **not** part of the rendered site |
| `cv_src/` | **Self-contained LaTeX sources** for the downloadable PDFs (CV ×3, Publications ×3, `hjstyle.tex`, `build.sh`) — **not** rendered. See `cv_src/README.md` |

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
The CV and publication list ship in **two languages**, in `assets/pdf/`. The **CV** PDFs are linked from both `cv.html` and the Home page (`index.html`); the **Publications** PDFs from `publications.html`. (A Japanese set previously shipped but was taken down — links and `*_JP.pdf` files removed.)

| | English | 中文 (default) |
|--|--|--|
| **CV** | `Ma_Yue_CV_EN.pdf` | `Ma_Yue_CV.pdf` |
| **Publications** | `Ma_Yue_Publications_EN.pdf` | `Ma_Yue_Publications.pdf` |

These PDFs are **built in-repo** from the LaTeX sources in **`cv_src/`** (self-contained — no external dir):
`cd cv_src && ./build.sh` runs `xelatex ×2` on each doc and copies the served EN + 中文 PDFs into
`assets/pdf/` (日本語 is built but **not** served). When the CV/pubs change, edit `cv_src/*.tex`, rebuild,
and re-run the web generator if the bib changed. The downloadable **Publications PDFs match this site's
Publications page** — Lead-author & major-contributor → Belle / Belle II → Other → Proceedings; the only
intended web-vs-PDF difference is Belle/Belle II (digest on the page, full list in the PDFs).

> The Publications `.tex` are **hand-written `\item` lists**; the **web** list is generated from the **bib**.
> They are two sources of the same data — **keep them in step** (same sections, entries, order). The
> **Lead-author & major-contributor** section equals the **CV's `代表性论文` (9 papers, same order)** —
> if the CV changes, change the pub list + bib to match. (`general_CV/` is the maintainer's old workspace,
> now superseded by `cv_src/`.)

## Publications page is GENERATED — do not hand-edit
`publications.html` is produced by **`tools/build_publications.py`** from **`tools/Ma_Yue_papers_only.bib`**
(127 verified entries, sectioned). To change it, edit the bib or the script and regenerate:

```bash
python3 tools/build_publications.py      # rewrites ../publications.html  (no deps beyond Python 3)
```

Emitted structure: **Lead-author & major-contributor (9)** (role-tagged via the `ROLES` map; **these 9, in
this order, = the CV's `代表性论文`**; each entry also shows its experiment, e.g. J-PARC E73 / OLYMPUS, from
the bib `collaboration` field) → **Belle / Belle II** (digest: first `DIGEST_N`=15 of 78 on the page; the
full set lives in the PDF) → **Other journals (13)** → **Proceedings (27)**. The script cleans LaTeX titles
to plain Unicode and converts hypernuclei to MathJax. Tunables near the top: `DIGEST_N`, `ROLES`. The bib
section order drives the page order, so reorder/move entries in the bib (and mirror in `cv_src/*.tex`) to
realign — e.g. Okada (TES, PTEP 2016) sits in *Other journals*, not the lead section, to keep the lead
section equal to the CV's 9.

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
