#!/usr/bin/env python3
# Generate homepage publications.html: Lead-author (role-tagged) -> Belle (digest) -> Other -> Proceedings.
import re, html, os
_HERE = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(_HERE, "Ma_Yue_papers_only.bib")
OUT = os.path.join(_HERE, "..", "publications.html")
DIGEST_N = 15

GREEK={'alpha':'α','beta':'β','gamma':'γ','delta':'δ','epsilon':'ε','varepsilon':'ε','zeta':'ζ','eta':'η','theta':'θ','vartheta':'ϑ','iota':'ι','kappa':'κ','lambda':'λ','mu':'μ','nu':'ν','xi':'ξ','omicron':'ο','pi':'π','varpi':'ϖ','rho':'ρ','varrho':'ϱ','sigma':'σ','varsigma':'ς','tau':'τ','upsilon':'υ','phi':'φ','varphi':'φ','chi':'χ','psi':'ψ','omega':'ω','Gamma':'Γ','Delta':'Δ','Theta':'Θ','Lambda':'Λ','Xi':'Ξ','Pi':'Π','Sigma':'Σ','Upsilon':'Υ','Phi':'Φ','Psi':'Ψ','Omega':'Ω'}
SYM={'ell':'ℓ','to':'→','rightarrow':'→','longrightarrow':'→','leftarrow':'←','textrightarrow':'→','textleftarrow':'←','leftrightarrow':'↔','Rightarrow':'⇒','pm':'±','mp':'∓','times':'×','cdot':'·','approx':'≈','sim':'∼','simeq':'≃','neq':'≠','ne':'≠','leq':'≤','le':'≤','geq':'≥','ge':'≥','ll':'≪','gg':'≫','prime':'′','dagger':'†','dag':'†','infty':'∞','partial':'∂','equiv':'≡','propto':'∝','hbar':'ℏ','perp':'⊥','parallel':'∥','rangle':'⟩','langle':'⟨','ast':'*','star':'*','textendash':'–','textemdash':'—','textasciitilde':' ','textdegree':'°','textbullet':'•','textasciimacron':'̅'}
DROP={'ensuremath','text','textrm','textit','textbf','textnormal','mathrm','mathit','mathbf','mathcal','mathbb','mathnormal','mbox','rm','it','bf','left','right','displaystyle','scriptstyle','operatorname','boldsymbol','bm','nonumber','protect'}
ACCENT={'overline':'̅','widehat':'̂','widetilde':'̃','bar':'̅','hat':'̂','tilde':'̃','vec':'⃗','dot':'̇'}
SUP={**{d:c for d,c in zip('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')},'+':'⁺','-':'⁻','−':'⁻','=':'⁼','(':'⁽',')':'⁾','n':'ⁿ','i':'ⁱ'}
SUB={**{d:c for d,c in zip('0123456789','₀₁₂₃₄₅₆₇₈₉')},'+':'₊','-':'₋','−':'₋','=':'₌','(':'₍',')':'₎'}
def macro_repl(m):
    n=m.group(1); return GREEK.get(n) or SYM.get(n) or ('' if n in DROP else '')
def do_accents(s):
    A='|'.join(ACCENT)
    s=re.sub(r'\\('+A+r')\s*\{(\\[A-Za-z]+)\}',lambda m:m.group(2)+ACCENT[m.group(1)],s)
    pat=re.compile(r'\\('+A+r')\s*\{([^{}\\]*)\}'); prev=None
    while prev!=s:
        prev=s; s=pat.sub(lambda m:(''.join(c+ACCENT[m.group(1)] for c in m.group(2)) if m.group(2) else ACCENT[m.group(1)]),s)
    s=re.sub(r'\\('+A+r')(\\[A-Za-z]+)',lambda m:m.group(2)+ACCENT[m.group(1)],s)
    s=re.sub(r'\\('+A+r')\s*([^\s\\{}])',lambda m:m.group(2)+ACCENT[m.group(1)],s)
    return s
def supsub(s):
    f=lambda c,M:(''.join(M[x] for x in c) if c and all(x in M for x in c) else c)
    s=re.sub(r'\^\{([^{}]*)\}',lambda m:f(m.group(1),SUP),s); s=re.sub(r'_\{([^{}]*)\}',lambda m:f(m.group(1),SUB),s)
    s=re.sub(r'\^(\S)',lambda m:f(m.group(1),SUP),s); s=re.sub(r'_(\S)',lambda m:f(m.group(1),SUB),s); return s
def clean(t):
    s=t
    for a,b in [('\\%','%'),('\\&','&'),('\\_','_'),('\\#','#'),('\\$','$')]: s=s.replace(a,b)
    s=re.sub(r'\\[,;:! ]',' ',s); s=s.replace('~',' ')
    s=re.sub(r'\\sqrt\s*\{([^{}]*)\}',lambda m:'√'+m.group(1),s); s=re.sub(r'\\sqrt(?![A-Za-z])','√',s)
    s=do_accents(s); s=re.sub(r'\\([A-Za-z]+)',macro_repl,s); s=s.replace('\\\\',' '); s=supsub(s)
    s=s.replace('$','').replace('{','').replace('}','')
    s=re.sub(r'\s+',' ',s).strip(); s=re.sub(r'\s+([,.;:])',r'\1',s); return s

# hypernucleus notation: mass-number + Λ + element -> MathJax ^{n}_{Λ}element (Λ subscripted)
SUPN={'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9'}
def hyper(t):
    def rep(m):
        mass=''.join(SUPN.get(c,c) for c in m.group(1))
        return '\\(^{'+mass+'}_{\\Lambda}\\mathrm{'+m.group(2)+'}\\)'
    return re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹0-9]+(?:,[⁰¹²³⁴⁵⁶⁷⁸⁹0-9]+)?)Λ([A-Z][a-z]?)', rep, t)

# ---- parse bib into sections ----
raw=open(BIB,encoding='utf-8').read()
def field(block,name):
    m=re.search(r'\b'+name+r'\s*=\s*"([^"]*)"',block); return m.group(1) if m else ''
entries=[]; cur_section=1; last_rc=None; buf=None; sec_here=1; rc=None
for ln in raw.split('\n'):
    if ln.startswith('% LEAD'): cur_section=2
    elif ln.startswith('% OTHER PEER'): cur_section=3
    elif ln.startswith('% CONFERENCE PROCEEDINGS'): cur_section=4
    if re.match(r'%\s*\[\d{4}\]',ln): last_rc=ln.lstrip('% ').strip()
    if ln.startswith('@article'): buf=ln; sec_here=cur_section; rc=last_rc
    elif buf is not None:
        buf+='\n'+ln
        if ln.strip()=='}':
            b=buf; entries.append(dict(section=sec_here,role=rc,title=clean(field(b,'title')),
                author=field(b,'author'),collab=field(b,'collaboration'),journal=field(b,'journal'),
                volume=field(b,'volume'),pages=field(b,'pages'),year=field(b,'year'),doi=field(b,'doi'),eprint=field(b,'eprint')))
            buf=None; last_rc=None
from collections import Counter
print("parsed",len(entries),"by section",dict(sorted(Counter(e['section'] for e in entries).items())))

def first_author(a):
    a=a.split(' and ')[0].strip()
    if ',' in a:
        last,first=[x.strip() for x in a.split(',',1)]; return f"{first} {last}"
    return a
def authors_fmt(e):
    if e['section']==1: return "Belle / Belle II Collaboration"
    fa=first_author(e['author']); return fa+" et al." if (' and ' in e['author'] or 'others' in e['author']) else fa
def venue(e):
    if e['journal']:
        v=e['journal']
        if e['volume']: v+=' '+e['volume']
        if e['pages']: v+=', '+e['pages']
        if e['year']: v+=f" ({e['year']})"
        return v
    if e['eprint']: return f"arXiv:{e['eprint']}"+(f" ({e['year']})" if e['year'] else "")
    return e['year'] or ''
def link(e):
    if e['doi']: return "https://doi.org/"+e['doi']
    if e['eprint']: return "https://arxiv.org/abs/"+e['eprint']
    return None
def esc(s): return html.escape(s,quote=True)
def render_entry(e, role=None, show_collab=False):
    t=esc(hyper(e['title'])); a=esc(authors_fmt(e)); v=esc(venue(e)); u=link(e)
    tt=f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' if u else t
    badge=f' <span class="role-tag">{role}</span>' if role else ''
    collab=f' &middot; {esc(e["collab"])}' if show_collab and e['collab'] else ''
    return f'      <li>\n        <span class="pub-title">{tt}</span>{badge}<br>\n        <span class="pub-meta">{a} &middot; {v}{collab}</span>\n      </li>'

# Role badges for the Lead-author & major-contributor section (sec 2), matched by title substring.
ROLES=[("First Observation of Λπ","First author"),
 ("Precise lifetime measurement of","Spokesperson &amp; corresponding author"),
 ("reaction cross section and evaluation of hypertriton","Spokesperson"),
 ("spectroscopy study of ¹¹","First author"),
 ("nuclear bound state, observed","Founding member &middot; major author"),
 ("Observation of a K̅NN bound state","Major contributor"),
 ("kaonic-helium isotopes","Major contributor"),
 ("Hard two-photon contribution","Led the luminosity monitor"),
 ("level structure by","Second author"),
 ("First application of superconducting","Major contributor")]
def role_for(e):
    for sub,r in ROLES:
        if sub.lower() in e['title'].lower(): return r
    return None

NAV='''  <header>
    <nav>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="cv.html">CV</a></li>
        <li><a href="research.html">Research</a></li>
        <li><a href="publications.html" class="active">Publications</a></li>
      </ul>
    </nav>
  </header>'''
MATHJAX='''  <script>
    MathJax = { tex: { inlineMath: [['$','$'],['\\\\(','\\\\)']] }, svg: { fontCache: 'global' } };
  </script>
  <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>'''

parts=[f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Publications &mdash; Yue Ma</title>
  <link rel="stylesheet" href="assets/css/style.css">
{MATHJAX}
</head>
<body>
{NAV}
  <main>
    <h1>Publications</h1>
    <p>
      Complete record of {len(entries)} publications. In hadron-physics collaborations author names are
      listed alphabetically; first-author, corresponding-author and spokesperson roles are noted below where
      they apply. The full formatted list (all {len(entries)}, including every Belle / Belle II paper) is available as a PDF:
    </p>
    <p class="links">
      <a class="btn" href="assets/pdf/Ma_Yue_Publications_EN.pdf">&#8681; Full list &mdash; English (PDF)</a>
      <a class="btn" href="assets/pdf/Ma_Yue_Publications.pdf">&#8681; 中文 (PDF)</a>
    </p>
''']

GROUPS=[(2,"Lead-author &amp; major-contributor",""),
        (1,"Belle / Belle II Collaboration",""),
        (3,"Other peer-reviewed journal articles",""),
        (4,"Conference proceedings","")]
for sec,title,note in GROUPS:
    allents=[e for e in entries if e['section']==sec]
    n=len(allents)
    shown=allents[:DIGEST_N] if sec==1 else allents
    if sec==1:
        note=f'A representative selection &mdash; showing {len(shown)} of {n}. The complete set of {n} Belle / Belle II collaboration papers is in the PDF above.'
    note_html=f'\n    <p class="pub-note">{note}</p>' if note else ''
    body="\n".join(render_entry(e, role_for(e) if sec==2 else None, show_collab=(sec==2)) for e in shown)
    parts.append(f'''    <h2>{title} <span class="count">({n})</span></h2>{note_html}
    <ul class="publication-list">
{body}
    </ul>
''')
parts.append('''  </main>
  <footer>
    <p>&copy; 2026 Yue Ma &middot; Last updated June 2026</p>
  </footer>
</body>
</html>
''')
open(OUT,'w',encoding='utf-8').write("\n".join(parts))
print("wrote",OUT)
