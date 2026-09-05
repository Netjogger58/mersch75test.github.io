#!/bin/bash
# Hetzner Snapshot / Backup Strategie für mersch75.lu
#
# Verwendung auf dem Hetzner Server (z.B. als root in /opt/mersch75-backup/):
#   1. cp hetzner-backup.sh /opt/mersch75-backup/
#   2. chmod +x /opt/mersch75-backup/hetzner-backup.sh
#   3. ./hetzner-backup.sh install-cron    # richtet tägliches Backup ein
#
# Was es macht:
#   - Snapshot der mersch75.lu Web-Root (/var/www/mersch75.lu oder ähnlich)
#   - DB-Backup (Vereins-OS SQLite)
#   - Komprimiert alles
#   - Räumt alte Backups auf (>30 Tage)
#   - Optional: rsync auf Hetzner Storage Box (siehe STORAGE_BOX unten)

set -e

# === KONFIGURATION (anpassen) ===
WEB_ROOT="/var/www/mersch75.lu"          # Wo die Live-Site liegt
DB_DIR="/opt/vereins-os"                 # Wo data.db / Sekretariat.db liegen
BACKUP_DIR="/backup/mersch75"            # Lokales Backup-Verzeichnis
RETAIN_DAYS=30                           # Backups älter als X Tage löschen

# Hetzner Storage Box (optional - auskommentieren wenn nicht gewünscht)
# STORAGE_BOX="u123456@u123456.your-storagebox.de"
# STORAGE_BOX_DIR="/backup/mersch75"
# RSYNC_PASS="/root/.storagebox_password"

# === SKRIPT ===
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error_exit() { log "ERROR: $*" >&2; exit 1; }

check_requirements() {
    command -v tar >/dev/null || error_exit "tar nicht installiert"
    command -v gzip >/dev/null || error_exit "gzip nicht installiert"
    [ -d "$WEB_ROOT" ] || error_exit "WEB_ROOT existiert nicht: $WEB_ROOT"
    mkdir -p "$BACKUP_DIR"
}

create_backup() {
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_file="$BACKUP_DIR/mersch75-$timestamp.tar.gz"
    local temp_dir=$(mktemp -d)
    local backup_root="$temp_dir/mersch75-backup-$timestamp"

    log "Erstelle Backup: $backup_file"
    mkdir -p "$backup_root"

    # 1. Web-Root
    if [ -d "$WEB_ROOT" ]; then
        log "  → Web-Root: $WEB_ROOT"
        tar czf "$backup_root/web.tar.gz" -C "$(dirname "$WEB_ROOT")" "$(basename "$WEB_ROOT")" 2>/dev/null || log "  (Warnung: Web-Root tar fehlgeschlagen)"
    fi

    # 2. Datenbanken (SQLite - muss im laufenden Betrieb gesichert werden mit sqlite3 .backup)
    if [ -d "$DB_DIR" ]; then
        log "  → DBs aus: $DB_DIR"
        mkdir -p "$backup_root/db"
        for db in "$DB_DIR"/*.db; do
            [ -f "$db" ] || continue
            local dbname=$(basename "$db")
            log "    → $dbname"
            # .backup ist atomar und sicher im Live-Betrieb
            sqlite3 "$db" ".backup '$backup_root/db/$dbname'" 2>/dev/null || cp "$db" "$backup_root/db/$dbname"
        done
    fi

    # 3. Memberslëscht-Excel (falls auf Server)
    for xlsx in "$WEB_ROOT/docs/GC MEMBERSLESCHT"*.xlsx "$WEB_ROOT/docs/GC MEMBERSLESCHT"*.xlsm; do
        [ -f "$xlsx" ] || continue
        log "  → Excel: $(basename "$xlsx")"
        cp "$xlsx" "$backup_root/"
    done

    # 4. Manifest mit Meta-Info
    cat > "$backup_root/manifest.txt" <<EOF
mersch75.lu Backup
Datum: $timestamp
Hostname: $(hostname)
Git-Commit (lokal): $(cd "$WEB_ROOT" 2>/dev/null && git rev-parse HEAD 2>/dev/null || echo "n/a")
Web-Root: $WEB_ROOT
DB-Verzeichnis: $DB_DIR
EOF

    # 5. Komprimieren
    tar czf "$backup_file" -C "$temp_dir" "mersch75-backup-$timestamp"
    local size=$(du -h "$backup_file" | cut -f1)
    log "  → Fertig: $backup_file ($size)"

    # 6. Storage Box Upload (optional)
    if [ -n "$STORAGE_BOX" ] && [ -f "$RSYNC_PASS" ]; then
        log "  → Upload zu Storage Box..."
        rsync -az --password-file="$RSYNC_PASS" "$backup_file" "${STORAGE_BOX}:${STORAGE_BOX_DIR}/" && \
            log "  → Upload OK" || \
            log "  (Warnung: Storage Box Upload fehlgeschlagen)"
    fi

    # 7. Aufräumen
    rm -rf "$temp_dir"
    cleanup_old_backups

    log "✅ Backup fertig: $backup_file"
}

cleanup_old_backups() {
    local deleted=$(find "$BACKUP_DIR" -name "mersch75-*.tar.gz" -mtime +$RETAIN_DAYS -delete -print | wc -l)
    if [ "$deleted" -gt 0 ]; then
        log "  → $deleted alte Backups gelöscht (>$RETAIN_DAYS Tage)"
    fi
}

install_cron() {
    local script_path=$(readlink -f "$0")
    local cron_line="0 3 * * * $script_path backup >> /var/log/mersch75-backup.log 2>&1"

    log "Installiere Cron-Job: $cron_line"

    # Bestehenden Job entfernen falls vorhanden
    crontab -l 2>/dev/null | grep -v "mersch75-backup" | crontab -

    # Neuen Job hinzufügen
    (crontab -l 2>/dev/null; echo "$cron_line") | crontab -

    log "✅ Cron-Job installiert. Läuft täglich um 03:00."
    log "   Log-Datei: /var/log/mersch75-backup.log"
    log ""
    log "   Aktuelle Crontab:"
    crontab -l | grep mersch75-backup | sed 's/^/   /'
}

show_status() {
    log "=== Backup-Status ==="
    log "Web-Root: $WEB_ROOT $([ -d "$WEB_ROOT" ] && echo "✓" || echo "✗")"
    log "DB-Dir:   $DB_DIR $([ -d "$DB_DIR" ] && echo "✓" || echo "✗")"
    log "Backup-Dir: $BACKUP_DIR"
    log "Speicher-Verbrauch: $(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)"
    log ""
    log "Letzte Backups:"
    ls -lh "$BACKUP_DIR"/mersch75-*.tar.gz 2>/dev/null | tail -5 || log "  (keine)"
}

case "${1:-backup}" in
    backup)
        check_requirements
        create_backup
        ;;
    install-cron)
        install_cron
        ;;
    status)
        show_status
        ;;
    *)
        echo "Verwendung: $0 {backup|install-cron|status}"
        echo ""
        echo "  backup        - Erstellt jetzt ein Backup"
        echo "  install-cron  - Richtet tägliches Backup um 03:00 ein"
        echo "  status        - Zeigt Backup-Status"
        exit 1
        ;;
esac
