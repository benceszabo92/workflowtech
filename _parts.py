# -*- coding: utf-8 -*-
"""
Workflow Tech Kft. — többoldalas statikus weboldal generátor.
Külön HTML oldalak, külső images/css/js. Ebből épül a /build kimenet.
Futtatás:  python3 build.py
"""
import json, pickle, unicodedata, html as H, re, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(ROOT, 'build')

spec = json.load(open(os.path.join(ROOT,'data','geppark-specifikaciok.json')))
grants = json.load(open(os.path.join(ROOT,'data','grants.json')))
fm = pickle.load(open(os.path.join(ROOT,'data','filemaps.pkl'),'rb'))
GEP_IMG, WENZEL_IMG, GRANT_IMG = fm['gep'], fm['wenzel'], fm['grants']

# ---------------- KAPCSOLÓK ----------------
SHOW_SZECHENYI = True   # Széchenyi 2020 logó a kezdőlapon (pályázati kötelezettség ~1 évig)
# -------------------------------------------

machines = {m['name']: m for m in spec['groups'][0]['machines']}

def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return ''.join(ch for ch in s if ch.isalnum())
GEP_NORM = {norm(k):v for k,v in GEP_IMG.items()}
def gep_img(name):
    k=norm(name)
    if k in GEP_NORM: return GEP_NORM[k]
    for ik in GEP_NORM:
        if k[:8] in ik or ik[:8] in k: return GEP_NORM[ik]
    return None

def logo(cls='logo'):
    return f'''<svg class="{cls}" viewBox="0 0 360 120" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Workflow Tech">
  <g stroke="#8A97A6" stroke-width="3"><line x1="22" y1="78" x2="44" y2="58"/><line x1="44" y1="58" x2="66" y2="64"/><line x1="66" y1="64" x2="86" y2="40"/></g>
  <circle cx="22" cy="78" r="7" fill="#0B0F14" stroke="#8A97A6" stroke-width="3"/>
  <circle cx="44" cy="58" r="7" fill="#0B0F14" stroke="#8A97A6" stroke-width="3"/>
  <circle cx="66" cy="64" r="7" fill="#0B0F14" stroke="#8A97A6" stroke-width="3"/>
  <circle cx="86" cy="40" r="9" fill="#2563eb"/>
  <text x="110" y="60" font-family="'Plus Jakarta Sans',sans-serif" font-weight="800" font-size="34" letter-spacing="-1.2" fill="#FFFFFF">Workflow</text>
  <text x="112" y="90" font-family="'Plus Jakarta Sans',sans-serif" font-weight="600" font-size="15" letter-spacing="6" fill="#3b82f6">TECH <tspan fill="#8A97A6" letter-spacing="3">KFT.</tspan></text>
</svg>'''

# route -> (filename, label)
PAGES = [
    ('index',        'index.html',        'Kezdőlap'),
    ('workflow-pro', 'workflow-pro.html', 'Workflow Pro'),
    ('workflow-pro-demo', 'workflow-pro-demo.html', 'Workflow Pro – Demó'),
    ('gyartas',      'gyartas.html',      'Gyártás'),
    ('geppark',      'geppark.html',      'Géppark'),
    ('minoseg',      'minoseg.html',      'Minőség'),
    ('referenciak',  'referenciak.html',  'Referenciák'),
    ('rolunk',       'rolunk.html',       'Rólunk'),
    ('kapcsolat',    'kapcsolat.html',    'Kapcsolat'),
]
FILEOF = {r:f for r,f,_ in PAGES}
LABELOF = {r:l for r,r2,l in [(r,f,l) for r,f,l in PAGES]}

# nav (Kapcsolat külön gomb, CAM kihagyva)
NAVLINKS = [('workflow-pro','Workflow Pro'),('gyartas','Gyártás'),('geppark','Géppark'),
            ('minoseg','Minőség'),('referenciak','Referenciák'),('rolunk','Rólunk')]

def nav(active):
    def _acls(r): return ' class="active"' if r==active else ''
    links=''.join(
        f'<a href="{FILEOF[r]}"{_acls(r)}>{H.escape(l)}</a>'
        for r,l in NAVLINKS)
    return f'''<nav class="top"><div class="in"><a href="index.html" aria-label="Workflow Tech">{logo()}</a>
<div class="links" id="navlinks">{links}</div>
<div style="display:flex;align-items:center;gap:10px"><a href="kapcsolat.html" class="cta">Kapcsolat</a><button class="burger" id="burger" aria-label="Menü">☰</button></div></div></nav>'''

def footer():
    return f'''<footer><div class="wrap"><div class="cols">
<div><a href="index.html" aria-label="Workflow Tech">{logo()}</a><p class="ftag">Precíziós fémmegmunkálás és szerszámkészítés Szigetbecsén — vasút-, gépjármű- és repülőgépipari beszállítói minőségben.</p></div>
<div><h4>Cég</h4><a href="gyartas.html">Gyártás</a><a href="geppark.html">Géppark</a><a href="minoseg.html">Minőség</a><a href="referenciak.html">Referenciák</a><a href="rolunk.html">Rólunk</a></div>
<div><h4>Szoftver</h4><a href="workflow-pro.html">Workflow Pro</a><a href="workflow-pro-demo.html">Workflow Pro – élő demó</a><a href="kapcsolat.html">Kapcsolat</a></div>
</div><div class="copy"><span>© 2025 Workflow Tech Kft.</span><span class="mono">ISO 9001:2015 · www.workflowtech.hu</span></div></div></footer>'''

def head(title, desc, extra_css=''):
    return f'''<!DOCTYPE html><html lang="hu"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{H.escape(title)}</title><meta name="description" content="{H.escape(desc)}"><meta name="theme-color" content="#0B0F14">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">{extra_css}</head><body>'''

def page_shell(route, title, desc, body, page_js=''):
    js = '<script src="js/main.js"></script>'
    if page_js:
        js += f'\n<script src="js/{page_js}"></script>'
    html = (head(title, desc) + '\n' + nav(route) + '\n<main>\n' + body +
            '\n</main>\n' + footer() + '\n' + js + '\n</body></html>')
    open(os.path.join(BUILD, FILEOF[route]),'w',encoding='utf-8').write(html)

print("parts loaded")
