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
<div><h3>Tanúsított folyamatok</h3><p>A teljes gyártási folyamatot dokumentált minőségirányítási rendszer fogja össze — az anyagátvételtől a végmérésig. Minden megmunkált alkatrész nyomonkövethető, a kritikus jellemzők méréses jegyzőkönyvvel igazolhatók.</p>
<div class="pills"><span class="pill">Anyagigazolás</span><span class="pill">Méréses jegyzőkönyv</span><span class="pill">Nyomonkövetés</span><span class="pill">SPC</span></div></div></div>
<div class="reveal" style="margin-top:26px"><div class="ey">// A tanúsítványunk</div>
<div class="certrow">
<a class="certbtn" href="images/cert/iso-9001-hu.jpg" target="_blank" rel="noopener" data-cert="images/cert/iso-9001-hu.jpg" data-cap="ISO 9001:2015 tanúsítvány — magyar · FERRCERT, FECR 3806/23"><span class="cb-ic"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></svg></span><span class="cb-t"><b>ISO 9001:2015 tanúsítvány</b><small>magyar · kattints a megtekintéshez</small></span><span class="cb-zoom"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/></svg></span></a>
<a class="certbtn" href="images/cert/iso-9001-en.jpg" target="_blank" rel="noopener" data-cert="images/cert/iso-9001-en.jpg" data-cap="ISO 9001:2015 certificate — English · FERRCERT, FECR 3806/23"><span class="cb-ic"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></svg></span><span class="cb-t"><b>ISO 9001:2015 certificate</b><small>English · click to view</small></span><span class="cb-zoom"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/></svg></span></a>
</div>
<div class="certnote mono">FERRCERT · FECR 3806/23 · érvényes 2026. 12. 26-ig · hatókör: precíziós fémmegmunkálás, prototípus és kisszériás gyártás, összeszerelés.</div>
</div></div></section>
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
<div class="row"><a href="kapcsolat.html" class="btn pri">Ajánlatkérés</a><a href="geppark.html" class="btn sec">A teljes géppark</a></div></div></div></section>
<div class="lightbox" id="lightbox" aria-hidden="true"><div class="lb-backdrop"></div><button class="lb-close" type="button" aria-label="Bezárás">×</button><div class="lb-inner"><img class="lb-img" src="" alt="Tanúsítvány — teljes méret"><div class="lb-cap"></div></div></div>'''
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
    # Ügyfelek / partnerek — valódi logók fehér csempéken, névvel, auto-scroll sáv.
    # Új partner: rakd a logót az images/brand/logos/-ba és vedd fel ide (név, fájl, weboldal).
    REFCLIENTS=[
     ("Siemens Zrt.","siemens.svg","https://www.siemens.com/hu-hu/"),
     ("Siemens Energy Kft.","siemens-energy.svg","https://www.siemens-energy.com/global/en/home.html"),
     ("Knorr-Bremse Hungária Kft.","knorr-bremse.svg","https://rail.knorr-bremse.com/"),
     ("Rolls-Royce","rolls-royce.png","https://www.rolls-royce.com/country-sites/hungary-hu.aspx"),
     ("KUKA Hungária Kft.","kuka.svg","https://www.kuka.com/"),
     ("AVL Hungary Kft.","avl.png","https://www.avl.com/"),
     ("OBO Bettermann Hungary Kft.","obo-bettermann.svg","https://www.obo.hu/"),
     ("Schwarzmüller Kft.","schwarzmuller.png","https://schwarzmueller.com/hu/"),
     ("Harlo Kft.","harlo.png","https://dorzshegesztes.hu/"),
     ("Oncotherm Kft.","oncotherm.svg","https://www.oncotherm.com/"),
     ("HUN-REN Magyar Kutatási Hálózat","hun-ren.png","https://hun-ren.hu/"),
     ("Flame Spray Hungary Kft.","flame-spray.png","https://flamespray.org/"),
     ("Gábos Kft.","gabos.svg","https://gabosplasztik.hu/"),
     ("EXATON Kft.","exaton.svg","https://exaton.hu/"),
     ("SMB Industries Kft.","smb.png","https://smb.at/"),
    ]
    def reftile(name,fn,url):
        return (f'<a class="ref" href="{H.escape(url)}" target="_blank" rel="noopener" title="{H.escape(name)}">'
                f'<span class="ref-logo"><img src="images/brand/logos/{fn}" alt="{H.escape(name)}" loading="lazy"></span>'
                f'<span class="ref-name">{H.escape(name)}</span></a>')
    reftiles=''.join(reftile(*c) for c in REFCLIENTS)
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Referenciák</div>
<h1>Pályázatok és fejlesztések</h1>
<p>Az elmúlt évek európai uniós és hazai pályázatai a gépparkunkat és a mérési képességeinket fejlesztették — közvetlenül a mindennapi gyártásban hasznosulnak.</p></div></header>
<section><div class="wrap"><div class="refwall reveal">
<div class="ch"><span class="ey">// Ügyfeleink</span><h2>Akiknek gyártunk</h2><p>Precíziós alkatrészek és gyártóeszközök — hazai és nemzetközi ipari partnereknek, a vasúttól a repüléstechnikáig.</p></div>
<div class="marquee"><div class="mtrack"><div class="mset">{reftiles}</div><div class="mset dup" aria-hidden="true">{reftiles}</div></div></div>
</div></div></section>
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
<div class="row" style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap"><a href="workflow-pro-demo.html" class="btn pri">Élő demó megtekintése</a><a href="kapcsolat.html" class="btn sec">Bemutatót kérek</a></div></div>
<div class="pro-mock"><div class="bar"><i></i><i></i><i></i></div>
<div class="kpis"><div class="kpi"><div class="l">Gépkihasználtság</div><div class="v ac">87%</div></div><div class="kpi"><div class="l">Aktív munkalap</div><div class="v">24</div></div>
<div class="kpi"><div class="l">Mai gépidő</div><div class="v">142 ó</div></div><div class="kpi"><div class="l">Határidőre</div><div class="v ac">96%</div></div></div>
<div class="barchart">{bars}</div></div>
</div></div></header>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Funkciók</div><h2>Amit egy gyártó nap mint nap használ</h2>
<p>Nem általános ERP — a forgácsolóüzem tényleges folyamataira építve.</p></div><div class="fgrid">{profeats}</div></div></section>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// Folyamat</div><h2>Az ajánlatkéréstől a számlázásig</h2>
<p>Minden lépés egy rendszerben — a partner pedig az ügyfélportálon valós időben követi a saját projektjeit.</p></div>
<div class="steps">
<div class="step reveal"><div class="num">01</div><h4>Ajánlatkérés</h4><p>A partner beküldi az igényt; a tételek — alkatrész és kereskedelmi cikk — a rajzzal és a 3D modellel együtt rögzülnek.</p></div>
<div class="step reveal"><div class="num">02</div><h4>Feldolgozás &amp; kalkuláció</h4><p>A Workflow Pro a technológia, a gépidő és az anyag alapján összeállítja az ajánlati árat.</p></div>
<div class="step reveal"><div class="num">03</div><h4>Kiajánlás dokumentációval</h4><p>A partner az ajánlat mellé minden tétel teljes dokumentációját megkapja: rajz, 3D modell, adatlap.</p></div>
<div class="step reveal"><div class="num">04</div><h4>Ügyfélportál</h4><p>A megrendelő digitálisan, valós időben követi a projektjei és megrendelései állapotát — a kiszállításig.</p></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Nézze meg működés közben</h2><p>Egy működő mintán végigvezetjük az ajánlatkéréstől a kiajánláson át a számlázásig.</p>
<div class="row"><a href="workflow-pro-demo.html" class="btn pri">Élő demó megtekintése</a><a href="kapcsolat.html" class="btn sec">Bemutatót kérek</a></div></div></div></section>'''
    page_shell('workflow-pro','Workflow Pro — gyártásirányítás | Workflow Tech Kft.','Vállalatirányítási rendszer gyártóknak: valós idejű riport, munkalapok, kapacitástervezés, kalkuláció — az ajánlatkéréstől a számlázásig.',body)

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
    stats=[('35','év · 1991 óta'),('20','év CAM-tapasztalat'),('27','megmunkálógép'),('ISO','9001:2015')]
    sg=''.join(f'<div class="stat reveal"><div class="v">{H.escape(v)}</div><div class="l">{H.escape(l)}</div></div>' for v,l in stats)
    VALS=[('Precizitás','Mikronos tűrések, mérhető és dokumentált minőség — nem ígérjük, igazoljuk.',
     '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>'),
     ('Teljes lánc','Esztergálástól a mérésig minden házon belül — gyorsabb átfutás, kevesebb hibalehetőség.',
     '<path d="M4 7h16M4 12h16M4 17h10"/>'),
     ('Saját szoftver','A Workflow Pro-val a saját gyártásunkat is mi optimalizáljuk — és ezt adjuk tovább.',
     '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 20h8M8 9l3 3-3 3"/>'),
     ('Prototípustól sorozatig','Egyedi prototípusoktól a kis- és közepes szériákig — ugyanazzal a mérhető minőséggel.',
     '<path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/>'),
     ('Saját készülékgyártás','A prototípusokhoz és a megrendelői alkatrészekhez a befogó- és mérőkészülékeket is mi készítjük.',
     '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2-2 2.6-2.6z"/>')]
    vl=''.join(f'<div class="vrow reveal"><div class="vi"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ico}</svg></div><div><h4>{H.escape(n)}</h4><p>{H.escape(d)}</p></div></div>' for n,d,ico in VALS)
    MILES=[('1991','Az alapítás','Családi vállalkozásként, Szabó Bt. néven indul a szerszámkészítés.'),
     ('2000','Első CNC','Az első CNC megmunkálóközpont beszerzése — megkezdődik a fordulás a gépi forgácsolás felé.'),
     ('2005','Új üzemcsarnok','450 m²-es saját gyártócsarnokba költözés, bővülő kapacitással.'),
     ('2014','Repülőgépipari belépés','LEADER-pályázatból három új szerszámgép; megkezdődik a repülőgépipari beszállítói munka.'),
     ('2015','10 fős csapat','GINOP-beruházás, a szervezet 10 főre bővül.'),
     ('2016–2017','EU-s gépberuházások','VEKOP és GINOP társfinanszírozású beruházások — modern, 5 tengelyes géppark.'),
     ('2018','Kft. forma','A vállalkozás Szabó Szerszámkészítő Kft. formában működik tovább.'),
     ('2023','Csúcstechnológia','Új DMG MORI eszterga- és megmunkálóközpontok — Ø500 × 1200 mm, 5 tengely, köszörűfunkcióval.'),
     ('2026','Workflow Tech Kft.','A 35 éves gyártói tudás új fejezete: prototípus és kis/közepes széria gyártás, saját fejlesztésű Workflow Pro gyártásirányító rendszerrel.')]
    tl=''.join(f'<div class="tl-row reveal{" now" if i==len(MILES)-1 else ""}"><div class="tl-yr">{H.escape(yr)}</div><h4>{H.escape(t)}</h4><p>{H.escape(d)}</p></div>' for i,(yr,t,d) in enumerate(MILES))
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Rólunk</div>
<h1>35 év — szerszámkészítésből precíziós gyártás</h1>
<p>1991 óta gyártunk egyedi, nagy pontosságú alkatrészeket. Mára a hangsúly a prototípusok, valamint a kis- és közepes szériák precíziós gyártásán van — <strong style="color:var(--t);font-weight:700">20 év CAM-tapasztalattal az egyedi, kis- és közepes széria megmunkálásban</strong>. Ebből a napi gyakorlatból nőtt ki a Workflow Tech Kft. és a saját fejlesztésű gyártásirányító rendszerünk, a Workflow Pro.</p></div></header>
<section style="padding-top:24px"><div class="wrap"><div class="statgrid">{sg}</div></div></section>
<section><div class="wrap"><div class="about"><div class="reveal"><div class="ey">// A történet</div>
<h2 style="font-size:clamp(22px,3vw,30px);font-weight:800;color:var(--t);margin-top:8px">Hogyan lettünk Workflow Tech</h2>
<p>Családi vállalkozásként, szerszámkészítéssel indultunk 1991-ben. Az évek alatt a hangsúly a nagy pontosságú, bonyolult alkatrészek gyors és megbízható legyártására tolódott — ma ebben vagyunk igazán jók, a prototípustól a kis- és közepes szériáig.</p>
<p>Közben felépült egy modern, 5 tengelyes géppark, és kialakult egy gyártási kultúra, amely az ajánlattól a leszámlázásig mindent dokumentál. A prototípusokhoz és a megrendelői alkatrészekhez a befogó- és mérőkészülékeket is házon belül tervezzük és gyártjuk.</p>
<p>A 20 év CAM-tapasztalattal felépített tudást formáltuk szoftverré: így született a <strong style="color:var(--t)">Workflow Pro</strong>, a gyártóknak szánt vállalatirányítási rendszer. A cég neve <strong style="color:var(--t)">Workflow Tech Kft.</strong> lett — mert már nemcsak alkatrészt, hanem folyamatot is szállítunk.</p>
<div class="row" style="margin-top:22px"><a href="geppark.html" class="btn pri">Géppark</a><a href="workflow-pro.html" class="btn sec">Workflow Pro</a></div></div>
<div class="vlist reveal">{vl}</div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="shead reveal"><div class="ey">// Mérföldkövek</div><h2>1991 → ma</h2>
<p>A szerszámkészítéstől a saját fejlesztésű gyártásirányító rendszerig — a fontosabb állomások.</p></div>
<div class="tl">{tl}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Dolgozzunk együtt</h2><p>Akár alkatrész, akár szoftver — keress minket.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Kapcsolat</a></div></div></div></section>'''
    page_shell('rolunk','Rólunk — Workflow Tech Kft.','35 év: 1991 óta precíziós alkatrészgyártás (korábban Szabó Szerszámkészítő Kft.) — prototípus és kis/közepes széria, 20 év CAM-tapasztalat, saját Workflow Pro rendszerrel.',body)

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
<p>Szabó Szerszámkészítőből precíziós gyártóvá alakultunk — prototípusok, valamint kis- és közepes szériák gyártása, 20+ év CAM-tapasztalattal az egyedi megmunkálásban. A darabokhoz a készülékeket is házon belül gyártjuk, és minden folyamatunkat a saját fejlesztésű Workflow Pro rendszerünk fogja össze.</p>
<div class="row" style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap"><a href="geppark.html" class="btn pri">A teljes géppark</a><a href="kapcsolat.html" class="btn sec">Ajánlatkérés</a></div>
</div></header>
<section style="padding-top:24px"><div class="wrap"><div class="pillars">
<a class="pillar reveal" href="gyartas.html"><div class="pi"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg></div>
<h3>Gyártás</h3><p>Esztergálás, marás, szikra- és köszörülés, lézerhegesztés és mérés — a teljes forgácsolási lánc házon belül.</p><span class="more">Képességek →</span></a>
<a class="pillar reveal" href="workflow-pro.html"><div class="pi"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/></svg></div>
<h3>Workflow Pro</h3><p>Vállalatirányítási rendszer gyártóknak: valós idejű riport, munkalapok, kapacitástervezés és kalkuláció.</p><span class="more">A szoftver →</span></a>
</div></div></section>
<section><div class="wrap"><div class="shead reveal"><div class="ey">// A cégről</div><h2>Szerszámkészítőből precíziós gyártó</h2>
<p>A Szabó Szerszámkészítő Kft. évtizedes szerszámkészítő tudására építve jött létre a Workflow Tech Kft. Ma prototípusokat, valamint kis- és közepes szériákat gyártunk — 20+ év CAM-tapasztalattal az egyedi megmunkálásban. A megrendelői alkatrészekhez és prototípusokhoz a befogó- és mérőkészülékeket is házon belül tervezzük és gyártjuk.</p></div>
<div class="fgrid">
<article class="fcard reveal"><div class="fi"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/></svg></div><h3>Prototípustól sorozatig</h3><p>Egyedi prototípusoktól a kis- és közepes szériákig — ugyanazzal a mérhető minőséggel.</p></article>
<article class="fcard reveal"><div class="fi"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2-2 2.6-2.6z"/></svg></div><h3>Saját készülékgyártás</h3><p>A prototípusokhoz és a megrendelői alkatrészekhez a készülékeket is mi tervezzük és gyártjuk.</p></article>
<article class="fcard reveal"><div class="fi"><svg viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 7v5l3 2"/></svg></div><h3>20+ év CAM-tapasztalat</h3><p>Évtizedek egyedi gyártási tudása a komplex geometriák programozásában és megmunkálásában.</p></article>
</div></div></section>
<section><div class="wrap"><div class="shead reveal" style="text-align:center"><div class="ey">// Géppark</div><h2>Élvonalbeli gépek, egy üzemben</h2>
<p style="margin:8px auto 0;max-width:56ch">27 CNC és egyetemes gép — a teljes forgácsolási lánc esztergálástól a mérésig, egy üzemben.</p></div>
<div class="logos">{bl}</div>
<div style="text-align:center;margin-top:24px"><a href="geppark.html" class="btn sec">A teljes géppark →</a></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cta-band reveal"><h2>Megvan a géped hozzá? Mi is.</h2><p>Küldd el a rajzot — visszajelzünk a megmunkálhatóságról és az árról.</p>
<div class="row"><a href="kapcsolat.html" class="btn pri">Ajánlatkérés</a><a href="minoseg.html" class="btn sec">Minőség &amp; mérőszoba</a></div></div></div></section>'''
    page_shell('index','Workflow Tech Kft. — Precíziós fémmegmunkálás & szoftver','Precíziós CNC-forgácsolás és szerszámkészítés Szigetbecsén, ipari beszállítói minőségben, saját Workflow Pro gyártásirányító szoftverrel.',body)

# ============================================================
#  WORKFLOW PRO — ÉLŐ DEMÓ (read-only minta ügyfélportál / ERP)
# ============================================================
def build_workflowpro_demo():
    def ft(n): return format(n,',d').replace(',',' ')+' Ft'
    def doc(label):
        return ('<span class="dm-doc" data-lock="Minta — a dokumentum nem nyitható meg.">'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>'
                + H.escape(label) + '</span>')
    inv_total=1270000+1905000+642000; inv_paid=1270000+1905000; inv_due=642000

    # ---------- oldalsáv ----------
    NAV=[('dash','Áttekintő','<path d="M3 13h8V3H3zM13 21h8V11h-8zM13 3v6h8V3zM3 21h8v-6H3z"/>'),
         ('part','Partnerek','<circle cx="9" cy="7" r="4"/><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M22 21v-2a4 4 0 0 0-3-3.87"/>'),
         ('proj','Projektek','<path d="M3 7a2 2 0 0 1 2-2h4l2 2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'),
         ('quote','Ajánlatok','<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/>'),
         ('ship','Szállítólevelek','<rect x="1" y="3" width="15" height="13" rx="1"/><path d="M16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/>'),
         ('inv','Számlák','<path d="M4 2l2 1 2-1 2 1 2-1 2 1 2-1 2 1v18l-2-1-2 1-2-1-2 1-2-1-2 1-2-1z"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
         ('portal','Ügyfélportál','<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>')]
    side=''.join(
        '<button class="dm-nav'+(' on' if i==0 else '')+'" data-view="'+k+'">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+ico+'</svg>'
        + H.escape(lab) + '</button>'
        for i,(k,lab,ico) in enumerate(NAV))

    # ---------- Áttekintő ----------
    dash=f'''<div class="dm-h"><div><h3>Áttekintő</h3><div class="sub">Aximo Precision Kft. · gyártási irányítópult</div></div></div>
<div class="dm-kpis">
<div class="dm-kpi"><div class="l">Aktív projekt</div><div class="v ac">2</div></div>
<div class="dm-kpi"><div class="l">Nyitott ajánlat</div><div class="v">1</div></div>
<div class="dm-kpi"><div class="l">Kiszállítva (hó)</div><div class="v">1</div></div>
<div class="dm-kpi"><div class="l">Kintlévőség</div><div class="v warn">{ft(inv_due)}</div></div>
</div>
<div class="dm-card"><div class="ch"><span>Legutóbbi mozgások</span><button class="dm-btn" data-go="proj">Projektek megnyitása</button></div>
<table class="dm-table"><thead><tr><th>Bizonylat</th><th>Partner</th><th>Esemény</th><th>Állapot</th></tr></thead><tbody>
<tr><td class="mono">SZ-2026-0312</td><td>AeroNova Components Kft.</td><td>Számla kiállítva</td><td><span class="dm-badge warn">Kifizetetlen</span></td></tr>
<tr><td class="mono">SZL-2026-0188</td><td>HidroFlow Kft.</td><td>Szállítólevél lezárva</td><td><span class="dm-badge ok">Kiszállítva</span></td></tr>
<tr><td class="mono">AJ-2026-0042</td><td>HidroFlow Kft.</td><td>Ajánlat kiküldve</td><td><span class="dm-badge info">Kiajánlva</span></td></tr>
<tr><td class="mono">PRJ-2026-021</td><td>AeroNova Components Kft.</td><td>Projekt létrehozva</td><td><span class="dm-badge mut">Tervezés</span></td></tr>
</tbody></table></div>'''

    # ---------- Partnerek ----------
    PARTNERS=[('HidroFlow Kft.','Hidraulika','Kovács Anna','a.kovacs@hidroflow.example',2),
              ('AeroNova Components Kft.','Légtechnika / repülés','Tóth Gergő','g.toth@aeronova.example',1),
              ('Tervgép Zrt.','Általános gépgyártás','Varga Béla','b.varga@tervgep.example',0),
              ('MobilTech Automotive Kft.','Autóipari beszállító','Kiss Réka','r.kiss@mobiltech.example',1)]
    prows=''.join(
        f'<tr><td><b style="color:var(--t);font-weight:600">{H.escape(nm)}</b></td>'
        f'<td>{H.escape(sec)}</td><td>{H.escape(con)}</td><td class="mono">{H.escape(em)}</td>'
        f'<td class="r mono">{ap}</td>'
        '<td class="r"><button class="dm-btn" data-lock="Minta — partneradat csak megtekinthető.">Megnyitás</button></td></tr>'
        for nm,sec,con,em,ap in PARTNERS)
    part=f'''<div class="dm-h"><div><h3>Partnerek</h3><div class="sub">{len(PARTNERS)} aktív partner a mintában</div></div><button class="dm-btn pri" data-lock="Minta — új partner nem rögzíthető.">+ Új partner</button></div>
<div class="dm-card"><table class="dm-table"><thead><tr><th>Partner</th><th>Szektor</th><th>Kapcsolattartó</th><th>E-mail</th><th class="r">Projekt</th><th></th></tr></thead><tbody>{prows}</tbody></table></div>'''

    # ---------- Projektek ----------
    PROJ=[
      {'name':'Hidraulika tömb sorozat','partner':'HidroFlow Kft.','id':'PRJ-2026-018','due':'2026-07-15','resp':'Nagy P.','status':('Gyártásban','info'),
       'items':[('Hidraulika vezérlőtömb','A','HF-2200-BLK','AlMgSi1',50,['HF-2200_r3.pdf','HF-2200.step']),
                ('Csatlakozó karima','A','HF-2200-FLG','1.4301',50,['HF-2200-FLG_r1.pdf','HF-2200-FLG.step']),
                ('O-gyűrű készlet NBR70','K','OR-NBR70-KIT','—',100,[]),
                ('Belső kulcsny. csavar M6×20 A2','K','DIN912-M6x20','A2',400,[])]},
      {'name':'Prototípus befogókészülék','partner':'AeroNova Components Kft.','id':'PRJ-2026-021','due':'2026-07-28','resp':'Szabó B.','status':('Tervezés','mut'),
       'items':[('Befogókészülék alaplap','A','AN-JIG-01','1.2312',1,['AN-JIG-01_r2.pdf','AN-JIG-01.step']),
                ('Pozícionáló pecek','A','AN-JIG-PIN','1.2379 (edzett)',8,['AN-JIG-PIN_r1.pdf','AN-JIG-PIN.step']),
                ('Gyorsszorító CL-200','K','CL-200','—',4,[])]},
    ]
    def proj_card(p):
        name=p['name']; partner=p['partner']; pid=p['id']; due=p['due']; resp=p['resp']
        stl=p['status'][0]; stc=p['status'][1]; items=p['items']; n=len(items); rows=''
        for nm,ty,ck,mat,db,docs in items:
            if ty=='A':
                tag='<span class="dm-tag part">Alkatrész</span>'
                dchips='<div class="dm-docs">'+''.join(doc(d) for d in docs)+'</div>'
            else:
                tag='<span class="dm-tag com">Kereskedelmi</span>'
                dchips='<span style="color:var(--td)">—</span>'
            rows+=(f'<tr><td><b style="color:var(--t);font-weight:600">{H.escape(nm)}</b></td>'
                   f'<td>{tag}</td><td class="mono">{H.escape(ck)}</td><td>{H.escape(mat)}</td>'
                   f'<td class="r mono">{db}</td><td>{dchips}</td></tr>')
        return (f'<div class="dm-card"><div class="ch"><span>{H.escape(name)} · '
                f'<span style="color:var(--tm);font-weight:500">{H.escape(partner)}</span></span>'
                f'<span class="dm-badge {stc}">{H.escape(stl)}</span></div>'
                f'<div class="dm-meta"><div><div class="k">Azonosító</div><div class="v">{H.escape(pid)}</div></div>'
                f'<div><div class="k">Határidő</div><div class="v">{H.escape(due)}</div></div>'
                f'<div><div class="k">Felelős</div><div class="v">{H.escape(resp)}</div></div>'
                f'<div><div class="k">Tételek</div><div class="v">{n}</div></div></div>'
                f'<table class="dm-table"><thead><tr><th>Tétel</th><th>Típus</th><th>Cikkszám</th><th>Anyag</th>'
                f'<th class="r">Db</th><th>Dokumentumok</th></tr></thead><tbody>{rows}</tbody></table></div>')
    proj=('<div class="dm-h"><div><h3>Projektek</h3><div class="sub">Alkatrészek (rajz + 3D modell) és kereskedelmi tételek egy projektben</div></div>'
          '<button class="dm-btn pri" data-lock="Minta — új projekt nem hozható létre.">+ Új projekt</button></div>'
          + ''.join(proj_card(p) for p in PROJ))

    # ---------- Ajánlatok ----------
    Q=[('Hidraulika vezérlőtömb','HF-2200-BLK',50,28500,['rajz','modell','adatlap']),
       ('Csatlakozó karima','HF-2200-FLG',50,7200,['rajz','modell']),
       ('O-gyűrű készlet NBR70','OR-NBR70-KIT',100,180,[]),
       ('Belső kulcsny. csavar M6×20 A2','DIN912-M6x20',400,12,[])]
    qrows=''; net=0
    for nm,ck,qty,unit,docs in Q:
        line=qty*unit; net+=line
        dchips=('<div class="dm-docs">'+''.join(doc(d) for d in docs)+'</div>') if docs else '<span style="color:var(--td)">—</span>'
        qrows+=(f'<tr><td><b style="color:var(--t);font-weight:600">{H.escape(nm)}</b></td>'
                f'<td class="mono">{H.escape(ck)}</td><td class="r mono">{qty}</td>'
                f'<td class="r mono">{ft(unit)}</td><td class="r mono">{ft(line)}</td><td>{dchips}</td></tr>')
    vat=round(net*0.27); gross=net+vat
    quote=f'''<div class="dm-h"><div><h3>Ajánlatok</h3><div class="sub">A partner az ajánlat mellé minden tétel teljes dokumentációját megkapja</div></div><button class="dm-btn pri" data-lock="Minta — új ajánlat nem készíthető.">+ Új ajánlat</button></div>
<div class="dm-card"><div class="ch"><span>AJ-2026-0042 · HidroFlow Kft.</span><span class="dm-badge info">Kiajánlva</span></div>
<div class="dm-meta"><div><div class="k">Kelt</div><div class="v">2026-05-02</div></div><div><div class="k">Érvényes</div><div class="v">2026-06-01</div></div><div><div class="k">Fizetés</div><div class="v">30 nap</div></div><div><div class="k">Projekt</div><div class="v">PRJ-2026-018</div></div></div>
<table class="dm-table"><thead><tr><th>Tétel</th><th>Cikkszám</th><th class="r">Db</th><th class="r">Egységár</th><th class="r">Nettó</th><th>Dokumentumok</th></tr></thead><tbody>{qrows}
<tr class="dm-tot"><td colspan="4" class="r">Nettó összesen</td><td class="r mono">{ft(net)}</td><td></td></tr>
<tr class="dm-tot"><td colspan="4" class="r">ÁFA 27%</td><td class="r mono">{ft(vat)}</td><td></td></tr>
<tr class="dm-tot"><td colspan="4" class="r">Bruttó összesen</td><td class="r mono">{ft(gross)}</td><td></td></tr>
</tbody></table>
<div style="padding:14px 16px;display:flex;gap:10px;flex-wrap:wrap;border-top:1px solid var(--b1)"><button class="dm-btn pri" data-lock="Minta — PDF nem tölthető le.">PDF letöltése</button><button class="dm-btn" data-lock="Minta — az ajánlat nem küldhető el.">Küldés a partnernek</button></div></div>'''

    # ---------- Szállítólevelek ----------
    D=[('HF-2200-BLK','Hidraulika vezérlőtömb',50),('HF-2200-FLG','Csatlakozó karima',50),
       ('OR-NBR70-KIT','O-gyűrű készlet NBR70',100),('DIN912-M6x20','Belső kulcsny. csavar M6×20 A2',400)]
    drows=''.join(f'<tr><td class="mono">{H.escape(ck)}</td><td><b style="color:var(--t);font-weight:600">{H.escape(nm)}</b></td><td class="r mono">{db}</td></tr>' for ck,nm,db in D)
    ship=f'''<div class="dm-h"><div><h3>Szállítólevelek</h3><div class="sub">Kiszállított tételek bizonylata</div></div><button class="dm-btn pri" data-lock="Minta — új szállítólevél nem készíthető.">+ Új szállítólevél</button></div>
<div class="dm-card"><div class="ch"><span>SZL-2026-0188 · HidroFlow Kft.</span><span class="dm-badge ok">Kiszállítva</span></div>
<div class="dm-meta"><div><div class="k">Kelt</div><div class="v">2026-06-12</div></div><div><div class="k">Projekt</div><div class="v">PRJ-2026-018</div></div><div><div class="k">Irány</div><div class="v">Aximo → HidroFlow</div></div></div>
<table class="dm-table"><thead><tr><th>Cikkszám</th><th>Megnevezés</th><th class="r">Kiszállítva</th></tr></thead><tbody>{drows}</tbody></table></div>'''

    # ---------- Számlák ----------
    INV=[('SZ-2026-0298','HidroFlow Kft.','2026-04-30','2026-05-14',1270000,'ok','Fizetve'),
         ('SZ-2026-0301','HidroFlow Kft.','2026-05-20','2026-06-03',1905000,'ok','Fizetve'),
         ('SZ-2026-0312','AeroNova Components Kft.','2026-06-18','2026-07-02',642000,'warn','Kifizetetlen')]
    irows=''.join(
        f'<tr><td class="mono">{H.escape(no)}</td><td>{H.escape(pt)}</td>'
        f'<td class="mono">{H.escape(d1)}</td><td class="mono">{H.escape(d2)}</td>'
        f'<td class="r mono">{ft(amt)}</td><td><span class="dm-badge {bc}">{H.escape(bl)}</span></td>'
        '<td class="r"><button class="dm-btn" data-lock="Minta — a számla csak megtekinthető.">Megtekintés</button></td></tr>'
        for no,pt,d1,d2,amt,bc,bl in INV)
    inv=f'''<div class="dm-h"><div><h3>Számlák</h3><div class="sub">Fizetett és kifizetetlen bizonylatok</div></div><button class="dm-btn pri" data-lock="Minta — új számla nem állítható ki.">+ Új számla</button></div>
<div class="dm-kpis">
<div class="dm-kpi"><div class="l">Kiállítva összesen</div><div class="v">{ft(inv_total)}</div></div>
<div class="dm-kpi"><div class="l">Befolyt</div><div class="v ac">{ft(inv_paid)}</div></div>
<div class="dm-kpi"><div class="l">Kintlévőség</div><div class="v warn">{ft(inv_due)}</div></div>
<div class="dm-kpi"><div class="l">Számla</div><div class="v">3</div></div>
</div>
<div class="dm-card"><table class="dm-table"><thead><tr><th>Számlaszám</th><th>Partner</th><th>Kelt</th><th>Fiz. határidő</th><th class="r">Bruttó</th><th>Állapot</th><th></th></tr></thead><tbody>{irows}</tbody></table></div>'''

    # ---------- Ügyfélportál ----------
    STEPS=[('done','Ajánlat elfogadva','2026-05-02','Az AJ-2026-0042 ajánlatot a megrendelő visszaigazolta.'),
           ('done','Anyagbeszerzés','2026-05-08','AlMgSi1 és 1.4301 alapanyag bevételezve, anyagigazolással.'),
           ('now','Gyártásban','folyamatban','A vezérlőtömb és a karima CNC-megmunkálása zajlik, valós idejű nyomonkövetéssel.'),
           ('todo','Mérés (WENZEL)','tervezett','Méréses jegyzőkönyv a koordináta-mérőgépről, egy felfogásból.'),
           ('todo','Kiszállítás','2026-07-15','Csomagolás és szállítás a megrendelő telephelyére.')]
    tsteps=''
    for st,h4,dt,desc in STEPS:
        mark='✓' if st=='done' else ('●' if st=='now' else '')
        tsteps+=(f'<div class="dm-step {st}"><div class="ds-ico">{mark}</div>'
                 f'<div><h4>{H.escape(h4)}</h4><div class="dt">{H.escape(dt)}</div><p>{H.escape(desc)}</p></div></div>')
    portal=f'''<div class="dm-h"><div><h3>Ügyfélportál</h3><div class="sub">Így látja a megrendelő a saját projektjeit — valós időben, a megosztott dokumentumokkal</div></div><span class="dm-badge info">HidroFlow Kft. nézete</span></div>
<div class="dm-grid2">
<div class="dm-card"><div class="ch"><span>Hidraulika tömb sorozat</span><span class="dm-badge info">Gyártásban</span></div><div style="padding:16px"><div class="dm-time">{tsteps}</div></div></div>
<div>
<div class="dm-card"><div class="ch"><span>Megosztott dokumentumok</span></div><div style="padding:14px 16px;display:flex;flex-direction:column;gap:8px;align-items:flex-start">{doc("HF-2200_r3.pdf — rajz")}{doc("HF-2200.step — 3D modell")}{doc("Meresi_jegyzokonyv.pdf")}</div></div>
<div class="dm-card"><div class="ch"><span>Számla állapota</span></div><table class="dm-table"><tbody>
<tr><td class="mono">SZ-2026-0301</td><td class="r mono">{ft(1905000)}</td><td class="r"><span class="dm-badge ok">Fizetve</span></td></tr>
</tbody></table></div>
</div>
</div>'''

    views=(f'<div class="dm-view on" id="v-dash">{dash}</div>'
           f'<div class="dm-view" id="v-part">{part}</div>'
           f'<div class="dm-view" id="v-proj">{proj}</div>'
           f'<div class="dm-view" id="v-quote">{quote}</div>'
           f'<div class="dm-view" id="v-ship">{ship}</div>'
           f'<div class="dm-view" id="v-inv">{inv}</div>'
           f'<div class="dm-view" id="v-portal">{portal}</div>')
    views=views.replace('<table class="dm-table">','<div class="dm-tw"><table class="dm-table">').replace('</table>','</table></div>')
    body=f'''<header class="hero"><div class="wrap"><div class="ey">// Bemutató</div>
<h1>Workflow Pro — élő demó</h1>
<p>Egy működő bemutató példányon át: ajánlattól a számlázásig, partnerekkel, projektekkel és ügyfélportállal. A demó cég kitalált — <b style="color:var(--t)">Aximo Precision Kft.</b></p></div></header>
<section style="padding-top:8px"><div class="wrap dm-wrap">
<div class="dm-note"><div class="ic">i</div><p><b>Minta környezet.</b> Ez egy bemutató: az adatok kitaláltak, <b>adat nem tölthető fel és nem menthető</b>. A gombok a működést illusztrálják.</p></div>
<div class="dm-frame reveal" id="dmapp">
<aside class="dm-side"><div class="dm-brand"><span class="dot"></span><b>Aximo Precision Kft.</b></div>{side}</aside>
<div class="dm-main"><div class="dm-top"><div class="co"><b>Aximo Precision Kft.</b><span class="dm-pill">Minta</span></div><div class="dm-user"><span>Demó felhasználó</span><span class="dm-av">AP</span></div></div>
<div class="dm-body">{views}</div></div>
</div>
<div style="text-align:center;margin-top:22px"><a href="kapcsolat.html" class="btn pri">Kérek egy bemutatót</a> <a href="workflow-pro.html" class="btn sec">Vissza a Workflow Pro-hoz</a></div>
</div></section>
<div class="dm-toast" id="dm-toast"></div>'''
    page_shell('workflow-pro-demo','Workflow Pro — élő demó | Workflow Tech Kft.','Működő bemutató: partnerek, ajánlat, szállítólevél, fizetett és kifizetetlen számlák, projektek rajzzal és modellel, ügyfélportál. Minta környezet.',body,'demo.js')

# ===== build mind =====
build_index(); build_workflowpro(); build_workflowpro_demo(); build_gyartas(); build_geppark()
build_minoseg(); build_referenciak(); build_rolunk(); build_kapcsolat()
print('Build kész →', BUILD)
print('Oldalak:', ', '.join(f for _,f,_ in PAGES))
