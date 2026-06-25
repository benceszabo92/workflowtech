# Workflow Tech Kft. — weboldal

Statikus, többoldalas weboldal a Workflow Tech Kft. (precíziós fémmegmunkálás + Workflow Pro szoftver) számára.

## Gyors start

```bash
python3 build.py        # legenerálja a build/ mappát
```

Aztán a `build/` mappa teljes tartalmát töltsd fel a tárhelyre (cPanel → public_html).

## Helyi előnézet

```bash
cd build
python3 -m http.server 8000
# böngésző: http://localhost:8000
```

## Mappák

| Mappa / fájl | Mi az |
|---|---|
| `build.py` | a fő generátor (oldalakat épít a build/-be) |
| `_parts.py` | közös fejléc, lábléc, logó, oldal-sablon |
| `data/` | gépadatok (JSON), pályázatok, képindex |
| `images/` | gépfotók, mérőszoba, pályázati képek, Széchenyi logó |
| `css/style.css` | a teljes stílus (kék arculat) |
| `js/main.js` | menü, galériák, fülek, lightbox |
| `build/` | a legenerált oldal (ezt kell feltölteni) |
| `regi-2016/` | a régi oldal archív helye (üres a repóban) |

Részletes szerkesztési szabályok: lásd `CLAUDE.md`.
