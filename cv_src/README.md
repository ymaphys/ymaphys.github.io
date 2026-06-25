# cv_src — LaTeX sources for the downloadable PDFs

Self-contained build inputs for the PDFs in `../assets/pdf/`. No external dir needed.

- `Ma_Yue_CV{,_EN,_JP}.tex` — CV (中文 / English / 日本語)
- `Ma_Yue_Publications{,_EN,_JP}.tex` — publication list (中文 / English / 日本語)
- `hjstyle.tex` — shared style; JP overrides CJK fonts to Hiragino
- `build.sh` — `xelatex ×2` each, then copies the **served** PDFs (EN + 中文) to `../assets/pdf/`

## Consistency (high priority — see ../CLAUDE.md)
- The Publications `.tex` are **hand-written `\item` lists**. The **web** publication list is generated
  separately by `../tools/build_publications.py` from `../tools/Ma_Yue_papers_only.bib`. **These two
  sources must be kept in step** — same sections, entries and order. The only intended web-vs-PDF
  difference is Belle/Belle II (digest on the page, full list in the PDFs).
- The **Lead-author & major-contributor** section = the **CV's 代表性论文 (9 papers, same order)**.
  If you change one, change the other (and the bib). Okada (TES, PTEP 2016) lives under *Other
  peer-reviewed journal articles*, not the lead section.
- Role wording per language comes from the matching CV (EN/中文/日本語).
- 日本語 PDFs are built but **not** served (downloads taken down); EN + 中文 are copied to `assets/pdf/`.
