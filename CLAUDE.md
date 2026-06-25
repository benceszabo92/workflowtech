# Workflow Tech Kft. — weboldal (Claude Code útmutató)

Ez a Workflow Tech Kft. (korábban Szabó Szerszámkészítő Kft.) precíziós fémmegmunkáló
cég weboldala. Statikus, többoldalas oldal, amit egy Python-generátor épít.

## Hogyan épül az oldal

- A **forrás** a `build.py` + `_parts.py` + a `data/` és `images/`, `css/`, `js/` mappák.
- A **kész oldal** a `build/` mappába generálódik: ezt kell a tárhelyre (cPanel `public_html`) feltölteni.
- Build futtatása:
  ```bash
  python3 build.py
  ```
  Ez törli és újragenerálja a `build/` mappát (HTML-ek), és bemásolja a `css/`, `js/`, `images/` tartalmát.

**FONTOS:** ne a `build/`-ben szerkessz kézzel — azt a build felülírja. A tartalmat a
`build.py`-ban (szövegek, gépek, árak) és a `css/style.css` + `js/main.js` fájlokban módosítsd,
majd futtasd újra a buildet.

## Oldalszerkezet (8 oldal)

`index.html` (Kezdőlap), `workflow-pro.html`, `gyartas.html`, `geppark.html`,
`minoseg.html`, `referenciak.html`, `rolunk.html`, `kapcsolat.html`.

A közös fejléc/lábléc/`<head>` a `_parts.py`-ban van (`nav()`, `footer()`, `head()`, `page_shell()`).
Az egyes oldalak tartalmát a `build.py` `build_*()` függvényei állítják elő.

## Arculat (KÉK identitás) — ezt tartsd meg

Design tokenek a `css/style.css` tetején (`:root`):
- háttér `--bg:#0B0F14`, panel `--s1:#121821`, vonal `--b1:#1E2A38`
- szöveg `--t:#F4F6F9` / `--tb:#C7D0DC` / `--tm:#8A97A6`
- **fő kék** `--ac:#2563eb`, világosabb `--ac2:#3b82f6`, sötétebb `--ac3:#1d4ed8`
- betűk: **Plus Jakarta Sans** (cím/szöveg) + **JetBrains Mono** (műszaki adatok)
- logó: node-flow SVG (3 szürke gyűrű + 1 kék végpont), `_parts.py` → `logo()`

## Tartalmi szabályok

- **A Workflow CAM-et NEM reklámozzuk** — ne kerüljön be a menübe vagy promóba.
- A menü (NAVLINKS a `_parts.py`-ban): Workflow Pro, Gyártás, Géppark, Minőség, Referenciák, Rólunk.
  A Kapcsolat külön gomb.
- Ajánlatkérő űrlap mezősorrend: **darabszám → cikkszám → megnevezés**.
- Hangnem: magyar, tömör, szakmai.

## Géppark — kategorizálás (`build.py` tetején)

A gépadatok: `data/geppark-specifikaciok.json`. A `build.py` ezeket csoportosítja:

- **REMOVE** (a cégnek nincs ilyen, ne jelenjen meg): NEUAR CNC-C50, TOS BPH 320A, AVEMAX VH-250VS-SP
- **LIST_ONLY** (létezik, de régi/nincs fotó — csak listában, nagy kártya nélkül):
  TOS SV18RA, MVE-280, TOS FN-32, KU 250-01
- **CNC nagy kártyák** (13): a `CNC_ORDER` lista sorrendjében
- **Egyetemes nagy kártyák** (9): az `EGY_ORDER` lista sorrendjében
- Néhány gép megjelenített neve a `DISPLAY` dict-ben van felülírva (helyes írásmód).

Új gép felvétele: tedd a JSON-ba, majd a megfelelő `CNC_ORDER` / `EGY_ORDER` listába
(vagy `LIST_ONLY`-ba), és rakd a fotóját az `images/gepek/`-be a gép nevéből képzett
fájlnévvel (a `gep_img()` normalizálva keresi meg).

## Képek

- `images/gepek/` — gépfotók (a kártyákhoz, lightboxszal nagyíthatók)
- `images/wenzel/` — WENZEL LH 87 mérőszoba galéria (Minőség oldal)
- `images/grants/` — pályázati képek (Referenciák; fájlnév: `<program>-<év>-N.jpg`)
- `images/brand/szechenyi.png` — Széchenyi 2020 logó (lásd lent)

A pályázati képek sorrendje a `data/filemaps.pkl`-ben van indexelve (a `grants.json`
sorrendjéhez igazítva).

## Széchenyi 2020 logó (pályázati kötelezettség)

- A kezdőlap jobb alsó sarkában fixen, görgetés nélkül látszik; kattintásra a Referenciák oldalra visz.
- Kapcsoló a `build.py` tetején: `SHOW_SZECHENYI = True`.
  Kb. 1 évig kell fenn lennie. Levételhez állítsd `False`-ra és futtasd újra a buildet.
- A logófájl: `images/brand/szechenyi.png` (hivatalos „Kedvezményezetti infoblokk, alsó változat, ERFA”).

## Ügyfél-logók (Referenciák)

A partnerlogók jelenleg **betűtípussal modellezett wordmarkok** (Siemens, Siemens Energy,
Knorr-Bremse, Rolls-Royce, Harlo) — nem a hivatalos logók. Ha valódi logó kerül elő,
az adott `.wm` elemet cseréld `<img class="logoimg" src="images/brand/xxx.svg" alt="…">`-re a
`build_referenciak()`-ben. (Jogi felelősség: a védjegyek használatát a tulajdonos engedélyezze.)

## Deploy (feltöltés)

A `build/` mappa **teljes tartalmát** kell a cPanel `public_html`-jébe másolni
(index.html + a többi .html + css/ + js/ + images/). A `regi-2016/` a régi oldal archív helye —
azt nem ez a projekt kezeli.
