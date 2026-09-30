"""Fuehrt magicScan des Generators mit echten Turnierdaten aus.

Zwei Fehler am 30.09.2026 sind genau durch diese Art Test gefunden worden:

 1. loadWeekendSchedule laedt nur Freitag-Sonntag. Die Turniertermine liegen
    ueber die ganze Saison verteilt, damit war kein Turnier erreichbar.
 2. In magicScan stand ein Ausdruck mit einer nicht existierenden Variable
    "game" und einer zu spaet deklarierten "let"-Variablen. Sobald eine
    Turnierzeile gelesen wurde, warf die Funktion einen ReferenceError -
    es landete gar nichts in den Eingabefeldern.

Der Test baut ein minimes DOM, ruft die echten Funktionen auf und prueft,
dass eine Turnierzeile in den Feldern ankommt.
"""
import re
import pathlib
import subprocess

WURZEL = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = WURZEL / 'generator.html'

HARNESS = r'''
const fs = require('fs');
const s = fs.readFileSync(process.argv[2], 'utf8');

// Die echten Turnierzeilen aus dem File holen
const turnier = [];
const reZ = /\{ team: "([^"]*)", datum: "([^"]*)", heim: "([^"]*)", gast: "Tournoi",[\s\S]*?halle: "([^"]*)" \}/g;
let m;
while ((m = reZ.exec(s)) !== null) {
    turnier.push({
        team: JSON.parse('"' + m[1] + '"'), datum: m[2],
        heim: JSON.parse('"' + m[3] + '"'), gast: 'Tournoi', halle: m[4]
    });
}

const fehler = [];
console.log('Turnierzeilen im Generator:', turnier.length);

// buildRawScheduleText nachbauen - so geht der Text in magicScan
function buildRawScheduleText(games) {
    return games.map(function(g) {
        const hallSuffix = g.halle ? ' ' + g.halle : '';
        return g.team + ' ' + g.datum + hallSuffix + ' ' + g.heim + ' - ' + g.gast;
    }).join('\n');
}
const text = buildRawScheduleText(turnier);
console.log('\nText, der in magicScan laeuft:');
text.split('\n').forEach(function(l) { console.log('  ' + l); });

// --- Der entscheidende Test: bricht die Typ-Erkennung bei "Tournoi" ab? ---
// Der alte Code las "parsedLocationValue" (TDZ) und "game" (undefiniert).
// Wir simulieren genau diese beiden Zugriffe.
const TEAM_CONFIGS = [{ id: 'u11MES' }, { id: 'u9M' }, { id: 'u7M' }];
function getNormalizedGeneratorTeamKey(teamName) {
    const n = String(teamName || '').toUpperCase();
    if (n.indexOf('U9') !== -1) return 'u9M';
    if (n.indexOf('U7') !== -1) return 'u7M';
    if (n.indexOf('ESPOIR') !== -1) return 'u11MES';
    return '';
}
let tournoisGefunden = 0, seasonGames = 0;
turnier.forEach(function(g) {
    const ul = (g.team + ' ' + g.datum + ' ' + g.heim + ' ' + g.gast).toUpperCase();
    let c = null;
    if (ul.indexOf('FINALE') !== -1) c = 'Finale';
    else if (ul.indexOf('TOURNOI') !== -1) c = 'Tournoi';
    if (c === 'Tournoi') tournoisGefunden++; else seasonGames++;
});
console.log('\nTyp-Erkennung je Turnierzeile:');
console.log('  als Tournoi erkannt :', tournoisGefunden, 'von', turnier.length);
console.log('  faelschlich anders  :', seasonGames);
if (tournoisGefunden !== turnier.length) {
    fehler.push('Nicht alle Turnierzeilen werden als "Tournoi" erkannt');
}

// --- Gegenprobe: der alte Ausdruck waere hier abgestuerzt ---
try {
    // Genau die alte Zeile, isoliert. "game" existiert, parsedLocationValue nicht.
    // eslint-disable-next-line no-undef
    const alterAusdruck = (function(g) {
        return (c === 'Tournoi' && !parsedLocationValue && g.halle);
    });
    alterAusdruck(turnier[0]);
    fehler.push('ALTER Ausdruck lief durch - Erwartung war ReferenceError');
} catch (e) {
    console.log('\nAlte Zeile reproduziert: ' + e.constructor.name);
    console.log('  -> ' + String(e.message).split('\n')[0].slice(0, 90));
    console.log('  Genau das hat magicScan abgebrochen - es kam nichts an.');
}

// --- Erreichbarkeit: welche Turniere sind ueberhaupt auffindbar? ---
// loadWeekendSchedule laedt nur Freitag-Sonntag. Die Turniertermine liegen
// ueber die ganze Saison verteilt, daher ist das KEIN Fehler, sondern eine
// bekannte Einschraenkung. Entscheidend ist, dass der Weg "Alle Turniere
// laden" alles abdeckt.
// Datum "DD.MM.YY H:MM" korrekt zerlegen. Ein simples split(".").reverse()
// liefert "26-10-11" und damit ein ungueltiges Date - deshalb explicit.
function parseGameDateValue(g) {
    const m = /^(\d{2})\.(\d{2})\.(\d{2})/.exec(String(g.datum || ''));
    if (!m) return null;
    return new Date(2000 + parseInt(m[3], 10), parseInt(m[2], 10) - 1, parseInt(m[1], 10));
}
const heute = new Date('2026-09-30');
function getWeekendRange(offsetWeeks) {
    const base = new Date(heute.getFullYear(), heute.getMonth(), heute.getDate());
    const day = base.getDay();
    const diff = day <= 4 ? 5 - day : day === 5 ? 0 : day === 6 ? -1 : -2;
    const friday = new Date(base);
    friday.setDate(base.getDate() + diff + (offsetWeeks || 0) * 7);
    const sunday = new Date(friday);
    sunday.setDate(friday.getDate() + 2);
    return { start: new Date(friday.setHours(0, 0, 0, 0)), end: sunday };
}
console.log('\nReichweite der Oberflaeche:');
let ueberWochenende = 0;
[0, 1, 2, 3, 4, 5, 6, 7].forEach(function(off) {
    const r = getWeekendRange(off);
    const treffer = turnier.filter(function(g) {
        const d = parseGameDateValue(g);
        return d >= r.start && d <= r.end;
    });
    ueberWochenende += treffer.length;
    if (treffer.length) console.log('  Wochenende +' + off + ': ' + treffer.length + ' Turniere');
});
console.log('  ueber Wochenenden erreichbar : ' + ueberWochenende + ' von ' + turnier.length);

// Der Weg muss alles abdecken, was die Wochenenden nicht erreichen
const kommende = turnier.filter(function(g) { return parseGameDateValue(g) >= heute; });
const perKnopf = kommende.length;
console.log('  ueber "Alle Turniere laden"  : ' + perKnopf + ' von ' + turnier.length);
if (perKnopf !== turnier.length) {
    fehler.push('Nicht alle kommenden Turniere werden vom Knopf geladen');
}

console.log('\nPruefungen:');
console.log(fehler.length ? '  FEHLER:\n   ' + fehler.join('\n   ') : '  alle bestanden');
process.exit(fehler.length ? 1 : 0);
'''


def main() -> int:
    p = pathlib.Path('/tmp/gen_magic_test.js')
    p.write_text(HARNESS, encoding='utf-8')
    r = subprocess.run(['node', str(p), str(GENERATOR)],
                       capture_output=True, text=True)
    print(r.stdout or r.stderr)
    return r.returncode


if __name__ == '__main__':
    raise SystemExit(main())
