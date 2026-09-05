# Custom Agents für mersch75.lu – Anleitung

> **Erstellt:** 2026-09-05
> **Was es ist:** Custom Agents sind spezialisierte AI-Assistenten in Kilo, die du mit `@agent-name` aufrufst. Sie haben einen festen System-Prompt + Workflow und sind perfekt für **wiederkehrende Aufgaben**.

---

## 📁 Wo Agents leben

| Scope | Pfad | Wann verwenden |
|---|---|---|
| **Global** | `~/.config/kilo/agent/*.md` | Auf allen Projekten verfügbar (z.B. dein persönlicher "Responsive-Audit") |
| **Pro Projekt** | `.kilo/agent/*.md` | Nur in diesem Projekt (z.B. "Memberslëscht-Sync" nur im mersch75-Repo) |

**Goldene Regel:**
- Persönliche Workflows (Git-Hygiene, Responsive-Checks) → **global**
- Projektspezifisches (Memberslëscht, Karussell-CSS) → **pro Projekt**

Aktuell haben wir:
```
mersch75.lu:   .kilo/agent/    ← leer
Vereins-OS:    .kilo/agent/    ← leer
~/.config/kilo/agent/          ← leer
```

---

## 📄 Datei-Format

Jeder Agent ist eine **Markdown-Datei mit YAML-Frontmatter**:

```yaml
---
description: Was dieser Agent tut (wird im @-Menü angezeigt)
mode: primary   # primary = direkt wählbar | subagent = nur via Task-Tool
model: anthropic/claude-sonnet-4.5   # optional: anderes Model
steps: 25      # max Iterationen (default 25)
hidden: false  # aus @-Menü verstecken (nur subagent)
color: "#FF5733"  # Farbe im UI
---

# System Prompt (das was der Agent "weiß")

Du bist ein Experte für [X]. Wenn der User dich aufruft:

1. Schritt 1
2. Schritt 2
3. Schritt 3
```

**Datei = Agent-Name:** `mersch75-karussell.md` → aufrufbar als `@mersch75-karussell`

---

## 🚀 Quick-Start: Dein erster Agent in 3 Minuten

### Beispiel 1: Globaler "Responsive-Audit" Agent

```bash
mkdir -p ~/.config/kilo/agent
```

Datei `~/.config/kilo/agent/responsive-audit.md`:

```yaml
---
description: Audit einer HTML-Seite auf Mobile/Tablet-Probleme
mode: primary
color: "#4CAF50"
---

Du bist ein Responsive-Design-Auditor für die mersch75.lu Webseite.

Wenn der User dich aufruft, prüfe folgende Datei (oder die angegebene):

1. **Viewport-Meta**: Muss `<meta name="viewport" content="width=device-width, initial-scale=1.0">` haben
2. **Hardcoded Sizes**:
   - `grep -n 'width: [0-9]\{3,\}px' DATEI`
   - `grep -n 'min-width: [0-9]\{3,\}px' DATEI`
   - `grep -n 'font-size: [0-9]\{2,\}px' DATEI`
3. **Touch-Targets** (in <button>/<a>): sollten mind. 44x44px sein
4. **Tote Links**: `<a href="#">` oder `javascript:void(0)`
5. **Fehlende Alt-Texte**: `<img>` ohne `alt=`

Gib am Ende aus:
- ✓ Was passt
- ⚠ Konkrete Zeilen mit Problemen (Datei:Zeile)
- Priorisierung: 🔴 kritisch / 🟠 bald / 🟡 nice-to-have

**Workflow:**
1. Lies die Datei mit `read`
2. Führe die grep-Befehle aus
3. Erstelle eine Bullet-Liste mit Befunden
4. Schlage konkrete Fixes vor
```

**Aufruf:** `@responsive-audit contact.html` oder im Chat einfach "check contact.html responsive"

---

### Beispiel 2: Projektspezifischer "Memberslëscht-Sync" Agent

Datei `.kilo/agent/memberslescht-sync.md` (im mersch75-Repo):

```yaml
---
description: Synchronisiert eine neue Memberslëscht-CSV → DBs + xlsm
mode: primary
color: "#002f65"
steps: 30
---

Du bist der Memberslëscht-Sync-Agent für mersch75.lu / Vereins-OS.

Wenn der User eine neue CSV-Datei nennt (z.B. `CascadeProjects/docs/GC MEMBERSLESCHT 2026-2027.csv`):

## 1. Backup
```bash
cd /Users/netjogger58/CascadeProjects/Vereins-OS
cp docs/GC\ MEMBERSLESCHT\ 2026-2027.xlsm docs/GC\ MEMBERSLESCHT\ 2026-2027.xlsm.bak.before-csv-$(date +%Y%m%d-%H%M%S)
cp data.db data.db.bak.before-csv-sync-$(date +%Y%m%d-%H%M%S)
cp Sekretariat.db Sekretariat.db.bak.before-csv-sync-$(date +%Y%m%d-%H%M%S)
```

## 2. Dry-Run
```bash
cd /Users/netjogger58/CascadeProjects/Vereins-OS/.kilo/worktrees/hot-restaurant
python3 scripts/import_memberslescht_full.py "<CSV-PFAD>" --report reports/memberslescht-csv-dry-run.json
```

## 3. Fehlende Card-IDs generieren
Falls `Missing card_id: N > 0`:
- Verwende join.html Alphabet: `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`
- Generiere 8 Zeichen mit `python3 -c "import secrets; print(''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(8)))"`
- Prüfe via SQLite dass die ID unique ist in beiden DBs
- Schreibe die ID zurück in die CSV (Spalte Card-ID)

## 4. xlsm aktualisieren
- Streitz oder andere fehlende Card-IDs in `Membres 2026_2027!Dxxx` schreiben
- Medico-Sheet aus CSV befüllen (header-based mapping)

## 5. Apply auf DBs
```bash
python3 scripts/import_memberslescht_full.py "<CSV-PFAD>" --apply --db /Users/netjogger58/CascadeProjects/Vereins-OS/data.db
python3 scripts/import_memberslescht_full.py "<CSV-PFAD>" --apply --db /Users/netjogger58/CascadeProjects/Vereins-OS/Sekretariat.db
```

## 6. Lint + Commit + Push
```bash
cd /Users/netjogger58/CascadeProjects/mersch75test.github.io
node tools/lint-js.cjs
cd /Users/netjogger58/CascadeProjects/Vereins-OS
git add -A
git commit -m "Sync Memberslëscht YYYY-MM-DD → data.db & Sekretariat.db"
git push
```

## Wichtig
- NIEMALS xlsm/CSV/DB ohne Backup ändern
- IMMER erst Dry-Run, dann fragen ob apply
- Card-ID-Generierung muss gegen ALLE bestehenden IDs unique sein
- Streitz & andere Officiels ohne Card-ID sind Spezialfall (manuell)
```

**Aufruf:** `@memberslescht-sync` oder im Chat "sync die neue Memberslëscht CSV"

---

## 🎯 Wann Agents helfen und wann nicht

### ✅ Use-Cases für Agents

| Pattern | Beispiel | Spart |
|---|---|---|
| **Immer gleiche Sequenz** | CSV → Backup → Sync → Test → Push | ~30 Min/Monat |
| **Komplexes Domain-Wissen** | "Wo ist die Karussell-CSS-Logik?" | ~10 Min pro Frage |
| **Wiederkehrende Audits** | Responsive-Check bei jeder neuen Seite | ~20 Min pro Seite |
| **Setup-Wissen** | "Wie deploye ich zu Hetzner?" | bei jedem neuen Teammitglied |

### ❌ Nicht für Agents geeignet

- Einmalige Bugs
- Komplett neue Features (zu wenig Kontext)
- Schnelle Fragen ("Wo ist Datei X?")
- Wenn du eh live mit mir arbeitest (ein Agent ist halt auch nur ich)

---

## 🛠️ Praxis-Tipps

### 1. Klein anfangen
Schreib **einen** Agent für dein dringendstes Problem. Nicht 5 auf einmal.

### 2. Workflow mit Beispielen dokumentieren
Statt "ändere das Karussell" lieber:
```yaml
Beispiel-Aufruf: "Family-Friends Slide wird überdeckt"
→ Liest index.html Zeile 223
→ Sieht .news-slide-family-friends
→ Liest styles.css Zeile 997
→ Unterscheidet: Bild ist POSTER (nicht Hintergrund)
→ Fix: ersetzt events-background mit Handballfeld, fügt events-poster-image hinzu
```

### 3. Im Agent nur das Wesentliche
- ✅ "Wann immer der User X sagt, mach Y"
- ❌ "Du bist ein freundlicher, hilfsbereiter Assistent der..."

### 4. Agent testen mit echtem Use-Case
Nach dem Erstellen: einmal manuell durchspielen ob der Agent den Use-Case auch wirklich abdeckt.

### 5. Versioniere Agents
Agents sind Markdown-Dateien. Pack sie in Git:
- Pro Agent → 1 Datei
- Im `.kilo/agent/` Ordner
- Bei größeren Änderungen: Changelog im File-Header

---

## 📋 Empfehlung für mersch75.lu

| Agent | Scope | Priorität | Aufwand |
|---|---|---|---|
| **memberslescht-sync** | Pro Projekt (Vereins-OS + mersch75) | 🔴 hoch | 15 Min |
| **responsive-audit** | Global (auch für andere Projekte) | 🟠 mittel | 10 Min |
| **carouel-fixer** | Pro Projekt (mersch75) | 🟡 nice | 10 Min |
| **i18n-checker** | Pro Projekt (mersch75) | 🟡 nice | 5 Min |

**Mein Tipp:** Fang mit **memberslescht-sync** an — das ist der Use-Case den du am häufigsten hast (alle paar Wochen neue CSV vom Sekretariat).

---

## 🧪 Ersten Agent jetzt erstellen

Sag mir Bescheid welchen Agent ich bauen soll. Ich kann:
1. Die Datei erstellen
2. Mit Dummy-Daten testen ob sie funktioniert
3. Committen

Oder du willst es selbst versuchen? Dann kopier einfach das Template oben, ändere die description + den Body, speichere in `.kilo/agent/name.md`, und lad Kilo neu (oder starte neue Session).
