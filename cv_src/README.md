# cv_src — LaTeX sources for the downloadable PDFs

Self-contained build inputs for the PDFs in `../assets/pdf/`. No external dir needed.

- `Ma_Yue_CV{,_EN,_JP}.tex` — CV (中文 / English / 日本語), **hand-written**
- `Ma_Yue_Publications{,_EN,_JP}.tex` — thin wrappers (preamble + banner) that `\input` the generated body
- `pub_body_{en,zh,ja}.tex` — **GENERATED** publication-list bodies (do not edit; see header)
- `hjstyle.tex` — shared style; portable fonts (XCharter + Songti/Fandol; JP → Hiragino)
- `build.sh` — regenerates lists from the bib, `xelatex ×2` each, copies served PDFs (EN + 中文) to `../assets/pdf/`

## Single source / consistency (high priority — see ../CLAUDE.md)
- **The publication list has ONE source: `../tools/Ma_Yue_papers_only.bib`.** `../tools/build_publications.py`
  generates BOTH `../publications.html` and `pub_body_{en,zh,ja}.tex` from it. To add/change a paper, **edit the
  bib and run `./build.sh`** (or the generator). The only intended web-vs-PDF difference is Belle/Belle II
  (digest on the page, full list in the PDFs).
- The **Lead-author & major-contributor** section = the **CV's 代表性论文 (same papers, count, order)**. The CV
  (`Ma_Yue_CV*.tex`) is the one publication list still hand-written — keep it equal to the bib lead section.
  Okada (TES, PTEP 2016) lives under *Other peer-reviewed journal articles*, not the lead section.
- Role wording lives in the generator (`ROLES` → `ROLE_L10N`, per language); section headings/intro in `LANG`.
- **In-press papers:** bib `note = "in press"` (with `journal`+`year`, no volume/pages/doi) renders
  `…, in press (YEAR)` in both the web list and the PDF bodies; fill the DOI/volume/pages and drop the
  `note` once published (pending for `Ma:2026muSR`, NIM-A).
- 日本語 PDFs are built but **not** served (downloads taken down); EN + 中文 are copied to `assets/pdf/`.
