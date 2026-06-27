# Automatikus deploy beállítása (egyszeri)

A `.github/workflows/deploy.yml` minden **main-re kerülő commitnál** (PR-merge is) feltölti a
`build/` mappát a dotroll cPanel `public_html`-jébe (rsync, overlay — nem töröl), majd
**purge-öli a Cloudflare cache-t**. Ehhez az alábbi repo-secret-ek kellenek egyszer.

> A secrets helye: GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**.
> (Vagy `gh secret set NEV` paranccsal — így a value nem kerül be sehova láthatóan.)

## Szükséges secrets

| Secret | Mi ez | Honnan |
|---|---|---|
| `SSH_HOST` | a szerver SSH hostja | cPanel → **SSH Access**, vagy dotroll szerver-hostnév (pl. `sXX.dotroll.com`), vagy `185.33.54.7` |
| `SSH_PORT` | SSH port | általában `22` (dotroll megerősíti) |
| `SSH_USER` | cPanel felhasználó | `egrxtn` |
| `SSH_PRIVATE_KEY` | deploy privát kulcs | a setup során generálva (lásd lent) |
| `CPANEL_DOCROOT` | cél mappa záró perjellel | `/home/egrxtn/public_html/` |
| `CF_API_TOKEN` | Cloudflare token (cache purge) | Cloudflare → My Profile → API Tokens → Create → **Zone › Cache Purge › Purge**, a `workflowtech.hu` zónára |
| `CF_ZONE_ID` | a `workflowtech.hu` Zone ID | Cloudflare → a `workflowtech.hu` Overview oldal, jobb alsó „API” blokk |

`CF_API_TOKEN`/`CF_ZONE_ID` opcionális: ha nincs, a deploy lefut, csak a Cloudflare purge marad ki
(a HTML rögtön frissül, de a css/js akár ~4 óráig cache-elt maradhat, amíg le nem jár).

## 1) SSH deploy-kulcs

A privát kulcsot a setup `SSH_PRIVATE_KEY` secretként már beállította. A hozzá tartozó **publikus
kulcsot engedélyezd a cPanel-ben**:

cPanel → **SSH Access → Manage SSH Keys → Import Key** → illeszd be a publikus kulcsot (csak a `Public Key`
mezőbe) → mentés → a kulcsnál **Manage → Authorize**.

(Ha az SSH hozzáférés nincs engedélyezve a tárhelyen, kérd a dotroll ügyfélszolgálatától, vagy nézd
a cPanel „SSH Access” oldalát. Ha SSH egyáltalán nem elérhető, szólj — átírom a workflow-t FTPS-re,
ahhoz csak FTP user/jelszó kell.)

## 2) A maradék secret-ek beállítása (gh CLI)

```bash
gh secret set SSH_HOST       # pl. 185.33.54.7  (Enter, majd a value)
gh secret set SSH_PORT       # pl. 22
gh secret set CF_API_TOKEN   # a Cloudflare token
gh secret set CF_ZONE_ID     # a workflowtech.hu zone id
```

(A `SSH_USER`, `CPANEL_DOCROOT`, `SSH_PRIVATE_KEY` már beállítva.)

## 3) Teszt

GitHub → **Actions → „Deploy to production (cPanel)” → Run workflow** (a `workflow_dispatch` miatt
kézzel is indítható), vagy egyszerűen mergeelj main-be. A run zöld → kész, onnantól minden merge
automatikusan élesít.

## Megjegyzések

- A rsync **overlay** módban megy (`--delete` nélkül): a `build/`-ben lévő fájlokat felülírja/feltölti,
  de a `public_html` egyéb tartalmát (pl. `regi-2016/`) nem törli. Ha egy oldalt **megszüntetsz**,
  azt a régi fájlt kézzel kell törölni a tárhelyről.
- A `build/` a repóban verziózva van; a deploy pontosan azt tölti fel, ami main-en be van commitolva
  (előtte mindig `python3 build.py` + commit).
