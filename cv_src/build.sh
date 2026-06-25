#!/bin/bash
# Self-contained build of all CV + Publications PDFs, then copy the SERVED ones
# (English + 中文) into ../assets/pdf/.  Japanese is built but NOT served
# (the JP downloads were taken down from the live site).
set -u
cd "$(dirname "$0")"
for d in Ma_Yue_CV Ma_Yue_CV_EN Ma_Yue_CV_JP Ma_Yue_Publications Ma_Yue_Publications_EN Ma_Yue_Publications_JP; do
  xelatex -interaction=nonstopmode -halt-on-error "$d.tex" >/dev/null 2>&1
  xelatex -interaction=nonstopmode -halt-on-error "$d.tex" >"$d.log" 2>&1
  [ -f "$d.pdf" ] && echo "OK  $d.pdf" || { echo "FAIL $d"; tail -15 "$d.log"; }
done
cp Ma_Yue_CV_EN.pdf Ma_Yue_CV.pdf Ma_Yue_Publications_EN.pdf Ma_Yue_Publications.pdf ../assets/pdf/
rm -f *.aux *.log *.out *.synctex.gz
echo "Copied EN + 中文 CV & Publications PDFs to ../assets/pdf/  (JP not served)"
