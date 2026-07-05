# CLAUDE.md — ymaphys.github.io

Yue Ma's personal academic homepage. **Plain hand-written static HTML, no build step.** This is a
GitHub **user page**, so **any push to `main` deploys live within ~1–2 min** — GitHub Pages serves the
files directly (no Jekyll, no Actions).

- **Repo:** `github.com/ymaphys/ymaphys.github.io` · **Live:** https://ymaphys.github.io

## 📌 IMPORTANT rule — docs & "memory" live IN THIS REPO (cross-machine)
The user works on this repo from **several machines**. Machine-local Claude memory
(`~/.claude/projects/…`) does **not** travel — **the repo does**. Every session, on every machine:
1. **This CLAUDE.md is the single durable store** of project knowledge — facts, conventions, runbooks,
   pending tasks, lessons learned. When a session learns something durable, **fold it into CLAUDE.md
   (or `cv_src/README.md` for build details) and commit & push in that same session.** Knowledge left
   only in machine-local memory or in the chat is considered lost.
2. **Machine-local Claude memory is only for** machine-specific state (e.g. whether `gh` is
   authenticated on that Mac) and notes too private for a public repo.
3. The repo is **public** — never commit private information; phrase in-repo notes neutrally.
4. If repo docs and local memory disagree, **the repo docs win** (they are the canonical, newest copy).

## 🚀 Quick reference — common tasks
| Task | Do this |
|------|---------|
| **Add / edit / remove a publication** | Edit `tools/Ma_Yue_papers_only.bib` → `cd cv_src && ./build.sh` → commit & push. (Web page + all PDFs regenerate; section counts & "N total" are automatic.) |
| **Rebuild the PDFs** | `cd cv_src && ./build.sh` (regenerates lists from the bib, compiles, copies EN + 中文 to `assets/pdf/`) |
| **Regenerate the web page only** | `python3 tools/build_publications.py` |
| **Change role wording / a new role** | `ROLES` + `ROLE_L10N` in `tools/build_publications.py` → `./build.sh` |
| **Change a section heading / intro text** | `LANG` table in `tools/build_publications.py` → `./build.sh` |
| **Change a download-button label** | `cv.html` **and** the `<a class="btn">` line in `build_publications.py` (then regenerate) — keep all pages parallel |
| **Edit bio / prose / a page** | the `.html` directly (plain static HTML) |
| **Deploy** | `git add -A && git commit -m "…" && git push origin main` → live in ~1–2 min |
| **Verify live** | open `…/publications.html?v=N` (cache-bust); PDFs: compare `md5` of live vs repo |

> Golden rule: **edit the bib, not the generated lists.** `publications.html` and `cv_src/pub_body_*.tex` are
> generated. The only hand-written publication text is the **CV's `代表性论文`** (keep it = the bib lead section).

## ⚠️ Consistency is a HIGH-PRIORITY rule
Treat the whole site — every HTML page **and** every downloadable PDF, in every language — as one
coherent artifact. A change in one place is not done until its counterparts everywhere are aligned.
Before finishing any edit, check across:
- **Parallel UI:** symmetric/parallel labels and structure. Language links/buttons name only the language
  and match across pages — `English (PDF)` / `中文 (PDF)` (no lopsided "Download CV — English" vs bare "中文").
- **Web ⇄ download PDFs:** `publications.html` and the download PDFs carry the **same sections, entries and
  order** because **both are generated from the one bib** (`build_publications.py`). The **only** intended
  difference is Belle/Belle II — a digest (first `DIGEST_N`) on the page vs the full list in the PDFs.
- **Role / contribution wording:** use the **exact** expressions from the CV, and keep them consistent across
  the CV, the publications page, and the PDFs. **Each language uses its own CV's wording** — EN: "First author /
  First author & corresponding author / Spokesperson & corresponding author / Led the luminosity monitor";
  中文: "第一作者 / 第一作者 & 通讯作者 / 发言人 & 通讯作者 / 主导亮度监测器（PbF₂）研制"; 日本語: "筆頭著者 /
  筆頭著者 & 責任著者 / スポークスパーソン & 責任著者 / 輝度モニターの開発を主導".
- **Notation & tone:** hypernuclei subscript-Λ, formal academic tone, footer/nav — identical everywhere (see *Conventions*).

When in doubt, after any change grep the other pages, the generator, and all language `.tex`/PDFs for the same
string and confirm they agree.

### 🗺️ Surface map — the SAME content lives in several files; edit ALL of them
Before editing, find every surface the content appears on. Most content is **mirrored**, not single-sourced:
| Content | Surfaces that MUST stay in sync |
|---------|--------------------------------|
| **CV body** (Profile, Leadership/Appointments, **Signature Achievements**, Education, Grants, …) | `cv.html` **(hand-written mirror of the CV PDF)** ⇄ `cv_src/Ma_Yue_CV.tex` + `_EN.tex` + `_JP.tex` (×3) → rebuilt CV PDFs. **`cv.html` is NOT a publications-only page — it mirrors the whole CV.** |
| **Publications list** | `tools/Ma_Yue_papers_only.bib` → (generator) → `publications.html` + `cv_src/pub_body_{en,zh,ja}.tex` → Publications PDFs. Edit the **bib**, never the outputs. |
| **CV `代表性论文` (lead list)** | hand-written in the 3 CV `.tex` — must equal the bib lead section (papers/count/order). |
| **Bio / recent-pubs / role wording / nav / footer** | every `.html` page + the matching `.tex`/PDFs, all languages. |

### ✅ Mandatory pre-finish checklist (do NOT declare done until all pass)
1. **Map first:** grep the changed string/number across `*.html`, `cv_src/*.tex`, `tools/`. A CV-body edit is **not** "CV only" — `cv.html` mirrors it.
2. **Apply to every surface** the grep found, in **every language** (EN / 中文 / 日本語).
3. **Rebuild** (`cd cv_src && ./build.sh`) and **visually inspect** the affected PDFs.
4. **Re-grep** the same string post-edit: every surface must agree (count, order, wording, notation).
5. Only then commit. **Skipping a surface is the #1 recurring mistake in this repo** — e.g. editing the CV body in the 3 `cv_src/*.tex` files but forgetting `cv.html` (or vice-versa). The map+re-grep steps exist to catch exactly that; do not shortcut them.

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
- **Footer:** `© 2026 Yue Ma · Last updated <month year>`. The month lives in **4 places** — `index.html`,
  `cv.html`, `research.html` **and** the footer string in `build_publications.py` (→ `publications.html`);
  bump all four together when publishing a content update.
- **Contact:** email + ORCID only. **INSPIRE is deliberately NOT linked** — the live INSPIRE author profile
  is Belle-only and hides the lead-author work; ORCID is the canonical ID.

## Languages — downloadable PDFs
The CV and publication list ship in **two languages**, in `assets/pdf/`. The **CV** PDFs are linked from both `cv.html` and the Home page (`index.html`); the **Publications** PDFs from `publications.html`. (A Japanese set previously shipped but was taken down — links and `*_JP.pdf` files removed.)

| | English | 中文 (default) |
|--|--|--|
| **CV** | `Ma_Yue_CV_EN.pdf` | `Ma_Yue_CV.pdf` |
| **Publications** | `Ma_Yue_Publications_EN.pdf` | `Ma_Yue_Publications.pdf` |

These PDFs are **built in-repo** from **`cv_src/`** (self-contained — no external dir): `cd cv_src && ./build.sh`
regenerates the lists from the bib, runs `xelatex ×2` on each doc, and copies the served EN + 中文 PDFs into
`assets/pdf/` (日本語 is built but **not** served). The downloadable **Publications PDFs match this site's
Publications page** (both generated from the bib) — Lead-author & major-contributor → Belle / Belle II → Other
→ Proceedings; the only intended web-vs-PDF difference is Belle/Belle II (digest on the page, full list in the PDFs).

> **Single source:** the **web list AND the PDF lists are both generated from the bib** by
> `build_publications.py` (→ `publications.html` + `cv_src/pub_body_{en,zh,ja}.tex`, which the
> `Ma_Yue_Publications*.tex` wrappers `\input`). Edit the bib, not the lists. The **Lead-author &
> major-contributor** section equals the **CV's `代表性论文` (same papers, count, order)** — the CV is the one
> publication list still hand-written, so update it (and the bib) together. (`general_CV/` is superseded by `cv_src/`.)

## Publications page is GENERATED — do not hand-edit
**`tools/build_publications.py`** reads **`tools/Ma_Yue_papers_only.bib`** (128 verified entries, sectioned)
and writes BOTH the web page **and** the PDF list bodies — single source. Edit the bib (or the script), then:

```bash
python3 tools/build_publications.py   # rewrites ../publications.html AND ../cv_src/pub_body_{en,zh,ja}.tex
```

Emitted structure: **Lead-author & major-contributor (10)** (role-tagged via the `ROLES` map; **these 10, in
this order, = the CV's `代表性论文`**; each entry also shows its experiment, e.g. J-PARC E73 / OLYMPUS, from
the bib `collaboration` field) → **Belle / Belle II** (digest: first `DIGEST_N`=15 of 78 on the page; the
full set lives in the PDF) → **Other journals (13)** → **Proceedings (27)**. For HTML the script cleans titles
to Unicode; for LaTeX it `\input`s the bib title with bare math macros `\ensuremath`-wrapped (`lx_title`) and
text-arrows mapped to math arrows. Tunables: `DIGEST_N`, `ROLES`/`ROLE_L10N` (role wording), `LANG` (per-language
headings/intro). The bib section order drives both outputs — reorder/move entries in the **bib** to realign
(e.g. Okada/TES sits in *Other journals*, not lead, to keep the lead section = the CV's 10).

## ➕ Adding / updating a publication — ONE source
**The bib `tools/Ma_Yue_papers_only.bib` is the single source for BOTH the web page and the PDF lists.**
`build_publications.py` generates `publications.html` **and** `cv_src/pub_body_{en,zh,ja}.tex` (the LaTeX
bodies the three `Ma_Yue_Publications*.tex` wrappers `\input`). Section counts and the "N total" intro are
all computed from the bib — nothing to bump by hand.

**A. Every new paper — just edit the bib, then rebuild:**
1. **`tools/Ma_Yue_papers_only.bib`** — add the entry under the right `% SECTION` marker
   (Belle / lead / other / proceedings) at the correct spot (**bib order = list order**; reverse-chronological
   within Belle/Other/Proceedings). For a lead/major paper, set its `collaboration` field (shown as the
   experiment tag) and `% [YEAR] … — role` comment.
   **Accepted / in-press paper:** give it `journal`, `year` and `note = "in press"` — no `volume`/`pages`/`doi`
   yet. Web + PDFs render `…, in press (YEAR)`; the web title stays **unlinked** until a `doi`/`eprint` exists.
   When published, fill in `doi`/`volume`/`pages`, drop the `note`, rebuild. *(Currently applies to
   `Ma:2026muSR`, the NIM-A μSR paper — complete its metadata when NIM-A publishes it, and at the same
   time re-verify the quoted "~30%" figure-of-merit gain in the CVs/`cv.html`/`research.html` against the
   final published text.)*
2. **Rebuild everything:** `cd cv_src && ./build.sh` — regenerates the web + the 3 PDF bodies from the bib,
   compiles all PDFs, and copies the served EN + 中文 PDFs to `assets/pdf/`. (Or just
   `python3 tools/build_publications.py` to refresh the web + bodies without compiling.)
3. **Verify** & commit; check live with a cache-buster.

**B. If it's a lead-author / `代表性论文` highlight** (NOT auto — keep these in step with the bib lead section):
- **Role badge:** if the paper needs a role tag, add a `(title-substring, "Role")` to the **`ROLES`** map in
  `build_publications.py`; if it's a NEW role phrase, add its EN/中文/日本語 wording to **`ROLE_L10N`**.
- **The CV** (`cv_src/Ma_Yue_CV{,_EN,_JP}.tex`, `代表性论文`) is hand-written and **must equal the bib lead
  section** (same papers, count, order). Update it to match.
- Optionally feature it in **`index.html` → "Selected recent publications"** (hand-curated ~5 newest, hardcoded).

**C. Belle/Belle II paper:** only **A** (no role tag). The page shows a `DIGEST_N`-of-N digest; the PDFs the full list.

> **Do NOT hand-edit** `publications.html` or `cv_src/pub_body_*.tex` or the list sections of the wrappers —
> they are generated. Edit the **bib** (and for headings/role wording, the `LANG`/`ROLE_L10N` tables in
> `build_publications.py`). The only hand-written publication text left is the **CV's `代表性论文`** and
> **index.html recent-pubs**.

Self-contained: everything builds from this repo (`cv_src/` + `tools/`); only a TeX Live install is needed
(`hjstyle.tex` falls back to bundled XCharter/Fandol fonts). `general_CV/` is the old workspace, superseded.

## Update / deploy
```bash
git add -A && git commit -m "…" && git push origin main
```
Deploy lags ~1–2 min and the CDN may briefly serve the old copy — verify the live site with a
cache-busting query, e.g. `https://ymaphys.github.io/publications.html?v=2`.

**If the "pages build and deployment" run fails at the `deploy` step** with the generic *"Deployment
failed, try again later"* (build job green, deploy red ~10 s in): the content on `main` is fine — it's a
transient GitHub-side error (githubstatus.com may still show "operational"). Retrigger with an empty commit
(`git commit --allow-empty -m "Retrigger Pages deploy" && git push`) or re-run from the Actions UI /
`gh run rerun <id>`; if it fails repeatedly, wait a few minutes between attempts (2026-07-06: two straight
failures, the third push deployed). The site keeps serving the previous version meanwhile, so nothing is
broken publicly. Note: `gh run rerun` on the managed Pages workflow can leave a zombie run stuck in
"queued" that GitHub can't cancel — ignore it; any newer push supersedes it.

## Don't
- Don't leave durable project knowledge only in machine-local Claude memory or the chat — fold it into
  CLAUDE.md and push (see the 📌 rule at the top).
- Don't commit `.history/` (VS Code local history — gitignored).
- Don't hand-edit `publications.html` or `cv_src/pub_body_*.tex` or the wrappers' list sections — regenerate from the bib.
- Don't add the INSPIRE link.

## Revert
Pre-enrichment snapshot: git tag **`pre-cv-enrich-20260625`** (+ a tarball backup beside the repo).
`git reset --hard pre-cv-enrich-20260625` to roll back.
