#!/bin/bash

# In das Verzeichnis wechseln, in dem das Skript liegt
cd "$(dirname "$0")"

# Lokalen Stand aktualisieren
git pull origin main

# Alle Änderungen (neue, geänderte, gelöschte Dateien) stagen
git add -A

# Commit mit Zeitstempel erstellen
COMMIT_MSG="KI-Update $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

# Änderungen zu GitHub pushen
git push origin main

