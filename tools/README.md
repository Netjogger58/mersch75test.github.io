# mersch75.lu – Backup & CI

## JS-Lint (lokal)

Vor jedem `git push` werden die JS-Syntax in allen HTML-Dateien und `.js`-Dateien geprüft. Wenn ein Fehler gefunden wird, bricht der Push ab.

```bash
node tools/lint-js.cjs          # manueller Check
```

Der `.git/hooks/pre-push` Hook ruft das automatisch vor jedem `git push` auf.

Um den Hook zu umgehen (z.B. wenn du weißt was du tust):
```bash
git push --no-verify
```

## GitHub Actions CI

Bei jedem Push auf `main` läuft automatisch:
- `js-syntax`: prüft alle `<script>`-Blöcke und `.js` Dateien mit `node --check`
- `html-validation`: prüft Klammern-Balance in inline-Scripts

Status: <https://github.com/Netjogger58/mersch75test.github.io/actions>

## Hetzner Backup

Für den Hetzner-Live-Server (nicht GitHub Pages) gibt es ein separates Backup-Skript:

```bash
# 1. Auf Hetzner-Server kopieren
scp tools/hetzner-backup.sh root@<hetzner>:/opt/mersch75-backup/

# 2. Auf dem Server anpassen (Pfade setzen) und ausführbar machen
ssh root@<hetzner>
chmod +x /opt/mersch75-backup/hetzner-backup.sh
nano /opt/mersch75-backup/hetzner-backup.sh   # WEB_ROOT, DB_DIR anpassen

# 3. Test-Backup
/opt/mersch75-backup/hetzner-backup.sh backup

# 4. Cron-Job einrichten (täglich 03:00)
/opt/mersch75-backup/hetzner-backup.sh install-cron

# 5. Status checken
/opt/mersch75-backup/hetzner-backup.sh status
```

**Was gesichert wird:**
- Web-Root (`/var/www/mersch75.lu`) — kompletter HTML/CSS/JS-Stand
- SQLite-Datenbanken (`data.db`, `Sekretariat.db`) — atomar via `.backup`
- Memberslëscht-Excel falls auf Server
- Manifest mit Git-Commit, Datum, Hostname

**Aufbewahrung:** 30 Tage (in `RETAIN_DAYS` änderbar)

**Storage Box (optional):** In der Datei `STORAGE_BOX` und `RSYNC_PASS` einkommentieren und anpassen, dann werden Backups zusätzlich auf eine Hetzner Storage Box geschoben (Off-Site, ~€3.50/Monat).

## Snapshot via Hetzner Cloud Panel

Zusätzlich zum Skript-basieren Backup: im [Hetzner Cloud Console](https://console.hetzner.cloud/) einen **Server-Snapshot** erstellen. Das ist ein komplettes Disk-Image — bei einem großen Problem kann der gesamte Server in Minuten zurückgesetzt werden.

**Empfehlung:** Snapshot **vor jedem größeren Update** manuell erstellen.
