# -*- coding: utf-8 -*-
"""Workflow Tech Kft. — build script. Futtatás: python3 build.py"""
import os, shutil, html as H
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'_parts.py')).read())

# ===== build mappa előkészítése =====
if os.path.isdir(BUILD): shutil.rmtree(BUILD)
os.makedirs(BUILD)
for sub in ['css','js','images']:
    shutil.copytree(os.path.join(ROOT,sub), os.path.join(BUILD,sub))

# ============================================================
#  GÉPPARK
# ============================================================
REMOVE = {'NEUAR CNC-C50','TOS BPH 320A','AVEMAX VH-250VS-SP'}
LIST_ONLY = [('TOS SV18RA','Univerzális csúcseszterga'),('MVE-280','Univerzális csúcseszterga'),
             ('TOS FN-32','Szerszámmarógép'),('KU 250-01','Palástköszörű')]
LIST_ONLY_NAMES = {n for n,_ in LIST_ONLY}
# Sorrend (2 oszlopos rács): 1.sor CTX beta | CMX-70-U · 2.sor MAZAK | T2 · 3.sor VD510 | KAFO CV7-A
CNC_ORDER = ['DMG MOri - CTX beta 1250 TC','DMG MORI CMX-70-U','MAZAK QT200M','DMG MORI T2 V3 PLUS',
 'NCT VD510-S + TJR 5AXIS','NCT KAFO CV7-A','JUNKER GRINDOR SILVER','Eduturn 400 L2',
 'CHARMILLES ROBOFORM 20','EMCO FB-600 MC','NCT EmR-1200D','SODICK VZ300L','Hartford omnis vmc-850s']
EGY_ORDER = ['ECO LASER 2600','ELBO CONTROLLI E346+','PROTH PSGS-80','TOS SN 32/1000','TOS FNGJ-32D',
 'charmilles form 2lc','PALMARY GU42 x 60S','GARANT SU1 CU1','EX4060A']
DISPLAY = {'DMG MOri - CTX beta 1250 TC':'DMG MORI – CTX beta 1250 TC','Hartford omnis vmc-850s':'Hartford Omnis VMC-850S',
 'charmilles form 2lc':'Charmilles Form 2LC','PALMARY GU42 x 60S':'PALMARY GU42×60S'}
def disp(n): return DISPLAY.get(n,n)

def card_html(name):
    m=machines[name]; img=gep_img(name); dn=H.escape(disp(name)); sub=H.escape(m.get('sub',''))
    rows=''.join(f'<div class="srow"><span class="slabel">{H.escape(k.rstrip(":"))}</span><span class="sval mono">{H.escape(v)}</span></div>' for k,v in m.get('specs',[]))
    feats=''
    for f in m.get('feats',[]):
        t=f.lstrip()
        if t.startswith('+'): t=t[1:].strip()
        feats+=f'<div class="feat"><span class="p">+</span><span>{H.escape(t)}</span></div>'
    fb=f'<div class="feats">{feats}</div>' if feats else ''
    if img:
        iw=f'<div class="imgwrap"><img src="{img}" alt="{dn}" loading="lazy"></div>'
    else:
        iw='<div class="imgwrap ph"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.4"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 14l5-4 4 3 4-5 5 6"/></svg></div>'
    return f'<article class="bcard">{iw}<div class="body"><h3>{dn}</h3><div class="sub">{sub}</div><div class="rule"></div><div class="specs">{rows}</div>{fb}</div></article>'

def build_geppark():
    cnc='\n'.join(card_html(n) for n in CNC_ORDER if n not in REMOVE and n not in LIST_ONLY_NAMES)
    egy='\n'.join(card_html(n) for n in EGY_ORDER if n not in REMOVE and n not in LIST_ONLY_NAMES)
    lst=''.join(f'<div class="slrow"><span class="n">{H.escape(n)}</span><span class="ty">{H.escape(t)}</span></div>' for n,t in LIST_ONLY)
    n_total=len([n for n in CNC_ORDER if n not in REMOVE and n not in LIST_ONLY_NAMES])+len([n for n in EGY_ORDER if n not in REMOVE and n not in LIST_ONLY_NAMES])+len(LIST_ONLY)
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Géppark</div>
<h1>{n_total} gép, a teljes forgácsolási lánc</h1>
<p>Esztergálás, marás, szikraforgácsolás, köszörülés és mérés — egy üzemben. Minden gépnél a teljes műszaki adatsor.</p>
<div class="tabbar"><div class="tabs"><button class="tab on" data-pane="cnc">CNC Gépeink</button><button class="tab" data-pane="egy">Egyetemes Gépeink</button></div></div></div></header>
<div class="wrap tabhost">
<section class="tabpane on" id="t-cnc" style="padding-top:0"><div class="bgrid">{cnc}</div></section>
<section class="tabpane" id="t-egy" style="padding-top:0"><div class="bgrid">{egy}</div>
<div class="simplelist"><div class="sl-h">// További egyetemes gépek</div>{lst}</div></section>
<div class="cta-band"><h2>Megvan a géped hozzá? Mi is.</h2><p>Küldd el a rajzot — visszajelzünk a megmunkálhatóságról és az árról.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Ajánlatkérés</a><a href="minoseg.html" class="btn sec">Minőség &amp; mérőszoba</a></div></div></div>'''
    page_shell('geppark','Géppark — Workflow Tech Kft.','27 CNC és egyetemes gép — a teljes forgácsolási lánc egy üzemben, teljes műszaki adatokkal.',body)

# ============================================================
#  MINŐSÉG
# ============================================================
def build_minoseg():
    WSPECS=[('Méréstartomány: X / Y / Z','800 / 1500 / 700 mm'),('Vezérlés','CNC, modelltérben programozható'),
     ('Pontosság (E0, MPE)','0,0015 + L/350 mm'),('Mérőléc felbontás','0,0001 mm — RENISHAW'),
     ('Mérőfej','RENISHAW PH10M PLUS'),('Méréstípus','„5" tengelyes — egy felfogásból')]
    wrows=''.join(f'<div class="srow"><span class="slabel">{H.escape(k)}</span><span class="sval mono">{H.escape(v)}</span></div>' for k,v in WSPECS)
    WFEATS=['Egy felfogásból körbemérés — pozíció- és helyzettűrések egy bázison',
     'Alaksajátosságok (síklapúság, hengeresség, egytengelyűség) közvetlen mérése',
     'Modelltérben programozott mérési ciklusok, ismételhető riportokkal']
    wfeats=''.join(f'<div class="feat"><span class="p">+</span><span>{H.escape(f)}</span></div>' for f in WFEATS)
    wslides=''.join(f'<div class="slide"><img src="{img}" alt="WENZEL LH 87 — {i+1}" loading="lazy"></div>' for i,img in enumerate(WENZEL_IMG))
    wdots=''.join(f'<button class="dot{" on" if i==0 else ""}" data-i="{i}"></button>' for i in range(len(WENZEL_IMG)))
    INDUSTRIES=[('Vasútipar','Biztonságkritikus alkatrészek nyomonkövethető gyártása, teljes körű méréses dokumentációval.',
     '<path d="M7 4h10a2 2 0 0 1 2 2v8a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V6a2 2 0 0 1 2-2Z"/><path d="M5 17l-2 3M19 17l2 3M9 8h6M9 12h6"/>'),
     ('Gépjárműipar','Szűk tűrésű, sorozatgyártott alkatrészek — SPC-szintű ismételhetőség és kapabilitás.',
     '<path d="M3 13l2-5a3 3 0 0 1 2.8-2h8.4A3 3 0 0 1 19 8l2 5"/><path d="M3 13h18v4a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-1H7v1a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-4Z"/><circle cx="7" cy="13.5" r="1"/><circle cx="17" cy="13.5" r="1"/>'),
     ('Repülőgépipar','Magas hozzáadott értékű, certifikált eljárások — anyagigazolás és teljes geometriai ellenőrzés.',
     '<path d="M12 2l3 8 6 3-6 1-1 6-2-4-2 4-1-6-6-1 6-3 3-8Z"/>')]
    icards=''.join(f'''<article class="icard reveal"><div class="iico"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><h3>{H.escape(n)}</h3><p>{H.escape(d)}</p></article>''' for n,d,ico in INDUSTRIES)
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Minőség</div>
<h1>A minőség nálunk mérhető</h1>
<p>ISO 9001:2015 szerint tanúsított minőségirányítás és saját, CNC-vezérlésű mérőszoba — a gyártott geometria minden bázisa egy felfogásból, prémium pontossággal ellenőrizve.</p></div></header>
<section><div class="wrap"><div class="iso reveal">
<div class="isobadge"><div class="b1">ISO</div><div class="b2">9001:2015</div><div class="b3">Tanúsított</div></div>
<div><h3>Tanúsított minőségirányítás</h3><p>A teljes gyártási folyamatot dokumentált minőségirányítási rendszer fogja össze — az anyagátvételtől a végmérésig. Minden megmunkált alkatrész nyomonkövethető, a kritikus jellemzők méréses jegyzőkönyvvel igazolhatók.</p>
<div class="pills"><span class="pill">Anyagigazolás</span><span class="pill">Méréses jegyzőkönyv</span><span class="pill">Nyomonkövetés</span><span class="pill">SPC</span></div></div></div></div></section>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Kiszolgált iparágak</div><h2>Ahol a tűrés nem opció</h2>
<p>Biztonságkritikus és certifikált környezetbe gyártunk — a minőségi elvárások a folyamat minden lépésébe be vannak építve.</p></div>
<div class="igrid">{icards}</div></div></section>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Mérőszoba</div><h2>WENZEL LH 87 koordináta-mérőgép</h2>
<p>Klimatizált mérőszobánk szíve egy nagytérfogatú, CNC-vezérlésű 3D koordináta-mérőgép — a munkadarab egyetlen felfogásból, körbemérve ellenőrizhető.</p></div>
<div class="mroom reveal"><div class="carousel" data-idx="0"><div class="viewport"><div class="track">{wslides}</div></div>
<button class="cbtn prev">‹</button><button class="cbtn next">›</button>
<div class="cmeta"><span class="counter"><span class="cur">1</span> / {len(WENZEL_IMG)}</span><div class="dots">{wdots}</div></div></div>
<div class="mbody"><div class="tag">// 3D koordináta-mérőgép</div><h3>WENZEL LH 87</h3><div class="sub">Nagytérfogatú, CNC-vezérlésű mérőközpont</div>
<div class="rule"></div><div class="specs">{wrows}</div><div class="feats">{wfeats}</div></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Rajz alapján visszaigazolt minőség</h2><p>Küldd el az alkatrész rajzát — visszajelzünk a megmunkálhatóságról, a mérési tervről és az árról.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Ajánlatkérés</a><a href="geppark.html" class="btn sec">A teljes géppark</a></div></div></div></section>'''
    page_shell('minoseg','Minőség & mérőszoba — Workflow Tech Kft.','ISO 9001:2015 minőségirányítás és WENZEL LH 87 mérőszoba — méréses dokumentáció a vasút-, gépjármű- és repülőgépiparnak.',body)

# ============================================================
#  REFERENCIÁK (pályázatok + ügyfelek)
# ============================================================
BADGE={'VEKOP':'#2563eb','GINOP':'#3b82f6','LEADER':'#f97316','Pest megye':'#8A97A6'}
def grant_html(g,imgs,rev):
    col=BADGE.get(g['prog'],'#2563eb')
    slides=''.join(f'<div class="slide"><img src="{img}" alt="{H.escape(g["prog"])} {g["year"]} — {i+1}" loading="lazy"></div>' for i,img in enumerate(imgs))
    dots=''.join(f'<button class="dot{" on" if i==0 else ""}" data-i="{i}"></button>' for i in range(len(imgs)))
    return f'''<div class="grant{' rev' if rev else ''} reveal"><div class="gmedia"><div class="carousel" data-idx="0"><div class="viewport"><div class="track">{slides}</div></div>
<button class="cbtn prev">‹</button><button class="cbtn next">›</button>
<div class="cmeta"><span class="counter"><span class="cur">1</span> / {len(imgs)}</span><div class="dots">{dots}</div></div></div></div>
<div class="gbody"><span class="gbadge" style="background:{col}">{H.escape(g['prog'])}</span>
<div class="gy">{g['year']} · {H.escape(g['title'])}</div><h3>{H.escape(g['title'])}</h3><p>{H.escape(g['text'])}</p></div></div>'''

def build_referenciak():
    cards=''.join(grant_html(g,GRANT_IMG[i],i%2==1) for i,g in enumerate(grants))
    # Ügyfelek — betűtípussal modellezett wordmarkok. Valódi logóra cseréld a .wm-et:
    #   <img class="logoimg" src="images/brand/siemens.svg" alt="Siemens">
    def wm(inner,title): return f'<div class="clogo" title="{H.escape(title)}"><span class="wm">{inner}</span></div>'
    siemens = wm('<span style="color:#009999;font-weight:600;letter-spacing:-.5px">siemens</span>','Siemens')
    siemens_e = wm('<span style="color:#009999;font-weight:600;letter-spacing:-.5px">siemens</span><span style="color:#009999;font-weight:400;letter-spacing:-.3px"> energy</span>','Siemens Energy Kft.')
    knorr = wm('<span style="display:inline-flex;flex-direction:column;line-height:.92;color:#00427f;font-weight:800;letter-spacing:.5px"><span style="font-size:.92em">KNORR</span><span style="font-size:.66em;letter-spacing:1.5px">BREMSE</span></span>','Knorr-Bremse Hungária Kft.')
    rolls = wm('<span style="display:inline-flex;flex-direction:column;line-height:.95;color:#00498F;font-weight:600;letter-spacing:2px;text-align:center"><span style="font-size:.78em">ROLLS</span><span style="font-size:.78em">ROYCE</span></span>','Rolls-Royce')
    harlo = wm('<span style="color:#1b3a5b;font-weight:800;letter-spacing:1px">HARLO</span><span style="color:#8A97A6;font-weight:600;letter-spacing:.5px"> Kft.</span>','Harlo Kft.')
    logos = siemens+siemens_e+knorr+rolls+harlo
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Referenciák</div>
<h1>Pályázatok és fejlesztések</h1>
<p>Az elmúlt évek európai uniós és hazai pályázatai a gépparkunkat és a mérési képességeinket fejlesztették — közvetlenül a mindennapi gyártásban hasznosulnak.</p></div></header>
<section><div class="wrap"><div class="clients reveal"><div class="ch"><span class="ey">// Ügyfeleink</span></div><div class="logorow">{logos}</div></div></div></section>
<section style="padding-top:24px"><div class="wrap">{cards}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Precíziós gyártás, mérhető minőséggel</h2><p>A fejlesztéseink eredménye a mindennapi gyártásban is ott van.</p>
<div class="row"><a href="geppark.html" class="btn pri">A teljes géppark</a><a href="minoseg.html" class="btn sec">Minőség &amp; mérőszoba</a></div></div></div></section>'''
    page_shell('referenciak','Referenciák & pályázatok — Workflow Tech Kft.','VEKOP, GINOP, LEADER és Pest megyei pályázataink, valamint partnereink.',body)

# ============================================================
#  WORKFLOW PRO
# ============================================================
def build_workflowpro():
    PROFEAT=[('Valós idejű gyártásriport','Gépidő, kihasználtság és állásidő egy képernyőn — a műhely pillanatnyi állapota mindig látszik.',
     '<path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/>'),
     ('Munkalapok és nyomonkövetés','Minden munka a rajztól a kiszállításig követhető — ki, mikor, melyik gépen dolgozott rajta.',
     '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
     ('Kapacitás és tervezés','Gépek terhelése előre látható; a határidők reálisan ígérhetők és tarthatók.',
     '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>'),
     ('Anyag- és technológiafelismerés','A modellből kiindulva azonosítja az anyagot és a megmunkálási igényt — kevesebb kézi adminisztráció.',
     '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M12 12l9-5M12 12v10M12 12L3 7"/>'),
     ('Költségkalkuláció','Gépidő, anyag és technológia alapján gyors, megbízható ajánlati ár.',
     '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.5h4a1.5 1.5 0 0 1 0 3h-3a1.5 1.5 0 0 0 0 3h4"/>'),
     ('Gyártóknak szabva','Kifejezetten forgácsoló- és szerszámkészítő üzemek folyamataira tervezve.',
     '<path d="M12 2a4 4 0 0 1 4 4 4 4 0 0 1-1 2.6L21 14l-2 2-5.4-5.4A4 4 0 0 1 11 12a4 4 0 0 1-1-7.9"/><path d="M6 14l-3 3 2 2 3-3"/>')]
    profeats=''.join(f'''<article class="fcard reveal"><div class="fi"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><h3>{H.escape(n)}</h3><p>{H.escape(d)}</p></article>''' for n,d,ico in PROFEAT)
    bars=''.join(f'<span style="height:{h}%"></span>' for h in [40,62,55,78,70,92,84])
    body=f'''<header class="hero"><div class="wrap"><div class="pro-hero">
<div><div class="pro-badge"><span style="width:6px;height:6px;border-radius:50%;background:#3b82f6;display:inline-block"></span> Workflow Pro · ERP gyártóknak</div>
<h1 style="margin-top:14px">A műhely, egyetlen képernyőn</h1>
<p>A Workflow Pro a forgácsoló- és szerszámkészítő üzemek vállalatirányítási rendszere: valós idejű gyártásriport, munkalapok, kapacitástervezés és kalkuláció — egy helyen.</p>
<div class="row" style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap"><a href="https://workflowpro.hu" target="_blank" rel="noopener" class="btn pri">workflowpro.hu</a><a href="kapcsolat.html" class="btn sec">Bemutatót kérek</a></div></div>
<div class="pro-mock"><div class="bar"><i></i><i></i><i></i></div>
<div class="kpis"><div class="kpi"><div class="l">Gépkihasználtság</div><div class="v ac">87%</div></div><div class="kpi"><div class="l">Aktív munkalap</div><div class="v">24</div></div>
<div class="kpi"><div class="l">Mai gépidő</div><div class="v">142 ó</div></div><div class="kpi"><div class="l">Határidőre</div><div class="v ac">96%</div></div></div>
<div class="barchart">{bars}</div></div>
</div></div></header>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Funkciók</div><h2>Amit egy gyártó nap mint nap használ</h2>
<p>Nem általános ERP — a forgácsolóüzem tényleges folyamataira építve.</p></div><div class="fgrid">{profeats}</div></div></section>
<section><div class="wrap"><div class="shead reveal" style="text-align:center"><div class="ey">// Árazás</div><h2>Egyszerű, kiszámítható</h2></div>
<div class="price reveal"><div class="amt">199 €<span> / hó</span></div>
<ul><li>Korlátlan munkalap és gép</li><li>Valós idejű riportok</li><li>Kapacitástervezés</li><li>Költségkalkuláció</li><li>Folyamatos frissítések</li></ul>
<div style="margin-top:26px"><a href="https://workflowpro.hu" target="_blank" rel="noopener" class="btn pri">Részletek a workflowpro.hu-n</a></div></div></div></section>'''
    page_shell('workflow-pro','Workflow Pro — gyártásirányítás | Workflow Tech Kft.','Vállalatirányítási rendszer gyártóknak: valós idejű riport, munkalapok, kapacitástervezés, kalkuláció. 199 €/hó.',body)

# ============================================================
#  GYÁRTÁS
# ============================================================
def build_gyartas():
    CAPS=[('Esztergálás','5-tengelyes eszterga-maró központok, ellenorsó és meghajtott szerszám — komplett alkatrész egy felfogásból.',
     '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/>'),
     ('Marás','3- és 5-tengelyes megmunkálóközpontok, nagysebességű marással — bonyolult geometriák pontosan.',
     '<path d="M12 2v6M12 8l-4 4 4 8 4-8z"/><path d="M8 12h8"/>'),
     ('Szikraforgácsolás','Huzal- és tömbszikra C-tengellyel, startlyukfúró — kemény anyagok és éles belső kontúrok.',
     '<path d="M13 2L4 13h6l-1 9 9-13h-6z"/>'),
     ('Köszörülés','Furat-, palást- és síkköszörülés — felületi minőség és mikronos méretpontosság.',
     '<circle cx="12" cy="12" r="8"/><path d="M12 4v3M12 17v3M4 12h3M17 12h3"/>'),
     ('Lézerhegesztés','Házon belüli szerszámjavítás és precíz hegesztés — gyors átfutás, kevesebb selejt.',
     '<path d="M12 2v8M9 10h6l-3 12z"/>'),
     ('Szerszámbemérés','Digitális szerszámbemérő és klimatizált mérőszoba — minden adat a gyártás előtt rendben.',
     '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M7 18v3M17 18v3M7 9l3 3-3 3"/>')]
    caps=''.join(f'''<article class="cap reveal"><div class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><h3>{H.escape(n)}</h3><p>{H.escape(d)}</p></article>''' for n,d,ico in CAPS)
    STEPS=[('01','Rajz & ajánlat','Beküldöd a modellt vagy rajzot; visszajelzünk a megmunkálhatóságról és az árról.'),
     ('02','Tervezés','Technológia, szerszámozás és mérési terv összeállítása — a Workflow Pro támogatásával.'),
     ('03','Gyártás','CNC megmunkálás a teljes gépparkon, folyamatos nyomonkövetéssel.'),
     ('04','Mérés & kiszállítás','Méréses jegyzőkönyv a WENZEL mérőszobából, majd csomagolás és szállítás.')]
    steps=''.join(f'<div class="step reveal"><div class="num">{n}</div><h4>{H.escape(t)}</h4><p>{H.escape(d)}</p></div>' for n,t,d in STEPS)
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Gyártás</div>
<h1>Komplett forgácsolás egy üzemben</h1>
<p>Esztergálástól a köszörülésig, a méréstől a szerszámjavításig — minden lépés házon belül, ipari beszállítói minőségben.</p>
<div class="row"><a href="geppark.html" class="btn pri">A teljes géppark</a><a href="kapcsolat.html" class="btn sec">Ajánlatkérés</a></div></div></header>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Képességek</div><h2>Amit megcsinálunk</h2>
<p>A teljes forgácsolási lánc egy helyen — nincs külső beszállító, nincs felesleges átfutás.</p></div><div class="cap-grid">{caps}</div></div></section>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Folyamat</div><h2>A rajztól a kész alkatrészig</h2></div><div class="steps">{steps}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Kezdjük a rajzoddal</h2><p>Küldd el — visszajelzünk a megmunkálhatóságról, a határidőről és az árról.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Ajánlatkérés</a></div></div></div></section>'''
    page_shell('gyartas','Gyártás — Workflow Tech Kft.','Komplett CNC-forgácsolás: esztergálás, marás, szikra, köszörülés, lézerhegesztés és mérés egy üzemben.',body)

# ============================================================
#  RÓLUNK
# ============================================================
def build_rolunk():
    stats=[('30+','év tapasztalat'),('27','gép'),('ISO','9001:2015'),('3','iparág')]
    sg=''.join(f'<div class="stat reveal"><div class="v">{H.escape(v)}</div><div class="l">{H.escape(l)}</div></div>' for v,l in stats)
    VALS=[('Precizitás','Mikronos tűrések, mérhető és dokumentált minőség — nem ígérjük, igazoljuk.',
     '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>'),
     ('Teljes lánc','Esztergálástól a mérésig minden házon belül — gyorsabb átfutás, kevesebb hibalehetőség.',
     '<path d="M4 7h16M4 12h16M4 17h10"/>'),
     ('Saját szoftver','A Workflow Pro-val a saját gyártásunkat is mi optimalizáljuk — és ezt adjuk tovább.',
     '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 20h8M8 9l3 3-3 3"/>')]
    vl=''.join(f'<div class="vrow reveal"><div class="vi"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><div><h4>{H.escape(n)}</h4><p>{H.escape(d)}</p></div></div>' for n,d,ico in VALS)
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Rólunk</div>
<h1>Szerszámkészítésből precíziós gyártás és szoftver</h1>
<p>A Workflow Tech Kft. (korábban Szabó Szerszámkészítő Kft.) Szigetbecsén működő precíziós fémmegmunkáló üzem — mára saját fejlesztésű vállalatirányítási szoftverrel, a Workflow Pro-val.</p></div></header>
<section style="padding-top:24px"><div class="wrap"><div class="statgrid">{sg}</div></div></section>
<section><div class="wrap"><div class="about"><div class="reveal"><div class="ey">// A cég</div>
<h2 style="font-size:clamp(22px,3vw,30px);font-weight:800;color:var(--t);margin-top:8px">Évtizedek tapasztalata, mai eszközökkel</h2>
<p>Folyamatos géppark-fejlesztéssel és minőségirányítással építettük fel azt a képességet, amivel vasút-, gépjármű- és repülőgépipari beszállítóként is megfelelünk. A gyártás mellett a saját üzemünk működtetéséből nőtt ki a Workflow Pro — a gyártóknak szánt vállalatirányítási rendszer.</p>
<div class="row" style="margin-top:22px"><a href="geppark.html" class="btn pri">Géppark</a><a href="workflow-pro.html" class="btn sec">Workflow Pro</a></div></div>
<div class="vlist reveal">{vl}</div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Dolgozzunk együtt</h2><p>Akár alkatrész, akár szoftver — keress minket.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Kapcsolat</a></div></div></div></section>'''
    page_shell('rolunk','Rólunk — Workflow Tech Kft.','Szigetbecsei precíziós fémmegmunkáló üzem (korábban Szabó Szerszámkészítő Kft.) saját Workflow Pro szoftverrel.',body)

# ============================================================
#  KAPCSOLAT
# ============================================================
def build_kapcsolat():
    KITEMS=[('E-mail','info@workflowtech.hu','<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
     ('Telefon','+36 …','<path d="M5 4h4l2 5-3 2a11 11 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>'),
     ('Cím','Szigetbecse','<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/>'),
     ('Web','www.workflowtech.hu','<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>')]
    ki=''.join(f'<div class="kitem"><div class="ki"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><div><div class="l">{H.escape(l)}</div><div class="v">{H.escape(v)}</div></div></div>' for l,v,ico in KITEMS)
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Kapcsolat</div>
<h1>Beszéljük meg a projektet</h1>
<p>Küldd el a rajzot vagy írj pár sort arról, mire van szükséged — visszajelzünk a megmunkálhatóságról, a határidőről és az árról.</p></div></header>
<section style="padding-top:24px"><div class="wrap"><div class="kgrid">
<div class="kcard"><h3>Elérhetőség</h3>{ki}</div>
<div class="kcard"><h3>Ajánlatkérés</h3>
<div class="field"><label>Név</label><input type="text" placeholder="Teljes név"></div>
<div class="field"><label>E-mail</label><input type="email" placeholder="nev@ceg.hu"></div>
<div class="field"><label>Üzenet / rajz leírása</label><textarea placeholder="Mit szeretnél gyártatni? Darabszám, anyag, határidő…"></textarea></div>
<button class="btn pri" type="button" onclick="alert('Ez egy bemutató űrlap — a végleges oldalon lesz élesítve.')">Üzenet küldése</button>
<div class="formnote">Ez egy bemutató űrlap; a feldolgozás a live oldalon kerül bekötésre.</div></div>
</div></div></section>'''
    page_shell('kapcsolat','Kapcsolat — Workflow Tech Kft.','Ajánlatkérés és elérhetőség — Workflow Tech Kft., Szigetbecse.',body)

# ============================================================
#  KEZDŐLAP
# ============================================================
def build_index():
    sz=''
    if SHOW_SZECHENYI:
        sz=('''<div class="szechenyi"><a href="referenciak.html" title="Széchenyi 2020 — Pályázataink" aria-label="Széchenyi 2020 pályázati logó">
<img src="images/brand/szechenyi.png" alt="Széchenyi 2020 — Európai Regionális Fejlesztési Alap — Befektetés a jövőbe">
</a></div>''')
    brands=['DMG MORI','MAZAK','JUNKER','SODICK','CHARMILLES','RENISHAW','WENZEL','HARTFORD']
    bl=''.join(f'<span>{b}</span>' for b in brands)
    body=f'''{sz}
<header class="home-hero"><div class="wrap">
<div class="ey">// Precíziós fémmegmunkálás &amp; szoftver</div>
<h1 style="margin-top:14px">Precíziós gyártás,<br><span class="ac">mérhető</span> minőséggel</h1>
<p>Szerszámkészítés és komplett CNC-forgácsolás egy üzemben, vasút-, gépjármű- és repülőgépipari beszállítói minőségben — saját fejlesztésű gyártásirányító szoftverrel, a Workflow Pro-val.</p>
<div class="row" style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap"><a href="geppark.html" class="btn pri">A teljes géppark</a><a href="kapcsolat.html" class="btn sec">Ajánlatkérés</a></div>
</div></header>
<section style="padding-top:24px"><div class="wrap"><div class="pillars">
<a class="pillar reveal" href="gyartas.html"><div class="pi"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg></div>
<h3>Gyártás</h3><p>Esztergálás, marás, szikra- és köszörülés, lézerhegesztés és mérés — a teljes forgácsolási lánc házon belül.</p><span class="more">Képességek →</span></a>
<a class="pillar reveal" href="workflow-pro.html"><div class="pi"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/></svg></div>
<h3>Workflow Pro</h3><p>Vállalatirányítási rendszer gyártóknak: valós idejű riport, munkalapok, kapacitástervezés és kalkuláció.</p><span class="more">A szoftver →</span></a>
</div></div></section>
<section><div class="wrap"><div class="shead reveal" style="text-align:center"><div class="ey">// Géppark</div><h2>Élvonalbeli gépek, egy üzemben</h2></div>
<div class="logos">{bl}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Megvan a géped hozzá? Mi is.</h2><p>Küldd el a rajzot — visszajelzünk a megmunkálhatóságról és az árról.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Ajánlatkérés</a><a href="minoseg.html" class="btn sec">Minőség &amp; mérőszoba</a></div></div></div></section>'''
    page_shell('index','Workflow Tech Kft. — Precíziós fémmegmunkálás & szoftver','Precíziós CNC-forgácsolás és szerszámkészítés Szigetbecsén, ipari beszállítói minőségben, saját Workflow Pro gyártásirányító szoftverrel.',body)

# ===== build mind =====
build_index(); build_workflowpro(); build_gyartas(); build_geppark()
build_minoseg(); build_referenciak(); build_rolunk(); build_kapcsolat()
print('Build kész →', BUILD)
print('Oldalak:', ', '.join(f for _,f,_ in PAGES))
