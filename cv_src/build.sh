#!/bin/bash
# Single-source build: regenerate the list bodies + web page from the bib, then
# compile all PDFs and copy the SERVED ones (EN + 中文) into ../assets/pdf/.
# 日本語 is built but NOT served (downloads were taken down from the live site).
set -u
cd "$(dirname "$0")"
echo "[1/3] regenerating pub_body_*.tex + publications.html from the bib …"
python3 ../tools/build_publications.py || { echo "generator failed"; exit 1; }
echo "[2/3] compiling PDFs (xelatex ×2) …"
for d in Ma_Yue_CV Ma_Yue_CV_EN Ma_Yue_CV_JP Ma_Yue_Publications Ma_Yue_Publications_EN Ma_Yue_Publications_JP; do
  xelatex -interaction=nonstopmode -halt-on-error "$d.tex" >/dev/null 2>&1
  xelatex -interaction=nonstopmode -halt-on-error "$d.tex" >"$d.log" 2>&1
  [ -f "$d.pdf" ] && echo "  OK  $d.pdf" || { echo "  FAIL $d"; tail -15 "$d.log"; }
done
echo "[3/3] publishing served PDFs → ../assets/pdf/ …"
cp Ma_Yue_CV_EN.pdf Ma_Yue_CV.pdf Ma_Yue_Publications_EN.pdf Ma_Yue_Publications.pdf ../assets/pdf/
rm -f *.aux *.log *.out *.synctex.gz
echo "Done (EN + 中文 CV & Publications copied; JP built but not served)."
