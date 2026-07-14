#!/usr/bin/env node
// flh-archive.mjs — FLH Spillplang + Tabellen vun handball4all.de eroflueden a lokal sécheren.
//
// Notzung:
//   node tools/flh-archive.mjs                     # Standard: Saison 2627
//   node tools/flh-archive.mjs --season 2526        # aner Saison
//   node tools/flh-archive.mjs --force              # iwwerschreift bestoende Fichier
//
// Effekt:
//   - Eroflueden all FLH-Donnéeën (gemäss js/flh-live-sync.js)
//   - Späicheren an data/flh-archive-<season>.json
//   - D'Websäit kann den Archiv lueden, falls d'FLH net méi accessible ass
//
import { writeFile, mkdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const API_BASE = 'https://spo.handball4all.de/service/if_g_json.php';
const ORG_ID = '95';
const PERIOD_BY_SEASON = {
  '2627': '137',
  '2526': '133',
};

const REQUESTS = [
  { key: 's1', cl: '153713', label: 'MÄNNER 1 (H-PRO)' },
  { key: 'fe', cl: '152653', label: 'FRAUEN (D-PRO)' },
  { key: 'u15', cl: '156341', label: 'JUGEND: U15G' },
  { key: 'u15fin', cl: '162361', label: 'JUGEND: U15G' },
  { key: 'u13pe', cl: '152106', label: 'JUGEND: U13M-PE' },
  { key: 'u11el', cl: '152529', label: 'JUGEND: U11 Elite', replaces: ['JUGEND: U11 Elite', 'JUGEND: U11M-EL', 'JUGEND: U11M-EPF5-10'] },
  { key: 'u11elpf', cl: '158596', label: 'JUGEND: U11 Elite', replaces: ['JUGEND: U11 Elite', 'JUGEND: U11M-EL', 'JUGEND: U11M-EPF5-10'] },
  { key: 'u11es', cl: '153409', label: 'JUGEND: U11 Espoirs', replaces: ['JUGEND: U11 Espoirs', 'JUGEND: U11M-ES'], allowCommentMatch: true },
  { key: 'u9', cl: '151356', label: 'JUGEND: U9M', allowCommentMatch: true },
  { key: 'u7', cl: '152096', label: 'JUGEND: U7M', allowCommentMatch: true }
];

function parseArgs(argv) {
  const opts = { season: '2627', force: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--season') opts.season = argv[++i];
    else if (a === '--force') opts.force = true;
  }
  return opts;
}

function trimValue(value) {
  return String(value == null ? '' : value).trim();
}

function getSboLink(rawValue) {
  const raw = trimValue(rawValue);
  const numericId = parseInt(raw, 10);
  if (!raw || !isFinite(numericId) || numericId <= 0) return '';
  return 'https://spo.handball4all.de/misc/sboPublicReports.php?sGID=' + raw;
}

function extractGames(block) {
  if (!block) return [];
  if (Array.isArray(block)) return block;
  if (Array.isArray(block.games)) return block.games;
  if (Array.isArray(block.rows)) return block.rows;
  return [];
}

function dedupeGames(games) {
  const seen = new Set();
  const unique = [];
  for (const game of games) {
    const key = [
      trimValue(game.nr),
      trimValue(game.sbo),
      trimValue(game.datum),
      trimValue(game.heim),
      trimValue(game.gast),
      trimValue(game.team)
    ].join('|');
    if (seen.has(key)) continue;
    seen.add(key);
    unique.push(game);
  }
  return unique;
}

function normalizeClubName(value) {
  return trimValue(value)
    .toUpperCase()
    .replace(/HBC\s+SCHIFFL(ANGE|\.)?/g, 'HBC SCHIFFLANGE')
    .replace(/HB\s+PETANGE/g, 'HB PETANGE')
    .replace(/BIELES\/P[ÉE]TANGE/g, 'BIELES PETANGE')
    .replace(/[^A-Z0-9]+/g, ' ')
    .trim();
}

function buildMergeKey(game) {
  if (!game) return '';
  const raw = trimValue(game.sboLive) || trimValue(game.sbo);
  const sgid = raw.match(/sGID=(\d+)/);
  if (sgid) return 'sbo|' + sgid[1];
  const number = trimValue(game.nr);
  if (number) return 'nr|' + number;
  return [
    'fallback',
    trimValue(game.team),
    trimValue(game.datum),
    normalizeClubName(game.heim),
    normalizeClubName(game.gast)
  ].join('|');
}

function mergeGameDetails(baseGame, incomingGame) {
  const base = baseGame || {};
  const incoming = incomingGame || {};
  const merged = Object.assign({}, base);
  const fields = ['team', 'rtl', 'yt'];
  for (const field of fields) {
    const incomingValue = trimValue(incoming[field]);
    const baseValue = trimValue(base[field]);
    if (incomingValue && !baseValue) merged[field] = incoming[field];
  }
  for (const field of ['datum', 'heim', 'gast', 'nr', 'halle', 'score', 'bem', 'sbo', 'sboLive']) {
    if (trimValue(incoming[field])) {
      if (field === 'sbo' || field === 'sboLive') {
        if (!trimValue(merged[field])) merged[field] = incoming[field];
      } else {
        merged[field] = incoming[field];
      }
    }
  }
  if (!trimValue(merged.rtl) && trimValue(incoming.rtl)) merged.rtl = incoming.rtl;
  if (!trimValue(merged.yt) && trimValue(incoming.yt)) merged.yt = incoming.yt;
  return merged;
}

function mapScore(game) {
  const homeGoals = trimValue(game.gHomeGoals);
  const guestGoals = trimValue(game.gGuestGoals);
  if (homeGoals === '' || guestGoals === '') return '';
  return homeGoals + ':' + guestGoals;
}

function mapComment(game) {
  const comment = trimValue(game.gComment);
  if (comment && comment !== '-') return comment;
  const groupText = trimValue(game.gGroupsortTxt);
  return groupText && groupText !== '-' ? groupText : '';
}

function hasClubReference(text) {
  const upperText = trimValue(text).toUpperCase();
  return upperText.indexOf('MERSCH') !== -1 || upperText.indexOf('M75') !== -1;
}

function isRelevantGame(config, game) {
  const directText = [trimValue(game.gHomeTeam), trimValue(game.gGuestTeam)].join(' ');
  if (hasClubReference(directText)) return true;
  if (!config || !config.allowCommentMatch) return false;
  const metaText = [trimValue(game.gComment), trimValue(game.gGroupsortTxt)].join(' ');
  return hasClubReference(metaText);
}

function mapGame(config, rawGame) {
  return {
    team: config.label,
    datum: [trimValue(rawGame.gDate), trimValue(rawGame.gTime)].filter(Boolean).join(' '),
    heim: trimValue(rawGame.gHomeTeam),
    gast: trimValue(rawGame.gGuestTeam),
    score: mapScore(rawGame),
    bem: mapComment(rawGame),
    sbo: getSboLink(rawGame.sGID),
    rtl: '',
    nr: trimValue(rawGame.gNo),
    halle: trimValue(rawGame.gGymnasiumNo)
  };
}

function parseLuxDateTime(value) {
  const parts = trimValue(value).split(' ');
  const dateParts = (parts[0] || '').split('.');
  if (dateParts.length !== 3) return null;
  let year = parseInt(dateParts[2], 10);
  if (year < 100) year += 2000;
  return new Date(year, parseInt(dateParts[1], 10) - 1, parseInt(dateParts[0], 10));
}

function isExcludedLiveGame(config, game) {
  if (!config || config.key !== 'u11el') return false;
  const date = parseLuxDateTime(game && game.datum);
  if (!date) return false;
  return date > new Date(2026, 5, 7, 23, 59, 59);
}

function buildUrl(config, periodId) {
  const params = new URLSearchParams({
    cmd: 'ps',
    og: ORG_ID,
    p: periodId,
    cl: config.cl,
    ca: '1',
    _: String(Date.now())
  });
  return API_BASE + '?' + params.toString();
}

async function fetchCompetitionGames(config, periodId) {
  const response = await fetch(buildUrl(config, periodId), { cache: 'no-store' });
  if (!response.ok) throw new Error('FLH ' + config.label + ' HTTP ' + response.status);
  const payload = await response.json();
  const content = payload && payload[0] && payload[0].content ? payload[0].content : null;
  if (!content) return { games: [], standings: [] };

  const combined = extractGames(content.actualGames).concat(extractGames(content.futureGames));
  const games = dedupeGames(
    combined
      .filter(game => isRelevantGame(config, game))
      .map(game => mapGame(config, game))
      .filter(game => !isExcludedLiveGame(config, game))
      .filter(game => game.datum && game.heim)
  );
  const standings = extractGames(content.score).map(mapStandingRow).filter(row => row.team);
  return { games: games, standings: standings };
}

function mapStandingRow(row) {
  const num = (v) => { const n = parseInt(trimValue(v), 10); return isNaN(n) ? 0 : n; };
  const plus = num(row.pointsPlus);
  const minus = num(row.pointsMinus);
  const points = (plus || minus) ? (plus + ':' + minus) : '';
  return {
    place: trimValue(row.tabScore) || trimValue(row.place) || trimValue(row.pl),
    team: trimValue(row.tabTeamname) || trimValue(row.gTeam) || trimValue(row.gName),
    played: num(row.numPlayedGames),
    won: num(row.numWonGames),
    drawn: num(row.numEqualGames),
    lost: num(row.numLostGames),
    goalsFor: num(row.numGoalsShot),
    goalsAgainst: num(row.numGoalsGot),
    pointsPlus: plus,
    pointsMinus: minus,
    points: points
  };
}

async function fetchAllGames(periodId) {
  const results = await Promise.allSettled(REQUESTS.map(async config => {
    const data = await fetchCompetitionGames(config, periodId);
    return { config, games: data.games, standings: data.standings };
  }));

  const mergedGames = [];
  const replaceLabels = new Set();
  const standingsByLabel = {};
  const errors = [];

  for (const result of results) {
    if (result.status === 'fulfilled') {
      const value = result.value;
      if (value.games.length) {
        mergedGames.push(...value.games);
        replaceLabels.add(value.config.label);
        const replaces = value.config.replaces || [];
        for (const r of replaces) replaceLabels.add(r);
      }
      if (value.standings && value.standings.length) {
        standingsByLabel[value.config.label] = value.standings;
      }
    } else {
      errors.push(result.reason && result.reason.message ? result.reason.message : String(result.reason));
    }
  }

  return {
    games: dedupeGames(mergedGames),
    replaceLabels: Array.from(replaceLabels),
    standingsByLabel,
    errors
  };
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const periodId = PERIOD_BY_SEASON[opts.season] || opts.season;
  const outDir = path.resolve(ROOT, 'data');
  const outPath = path.resolve(outDir, `flh-archive-${opts.season}.json`);
  await mkdir(outDir, { recursive: true });

  if (!opts.force && existsSync(outPath)) {
    console.log(`> Archiv existéiert schonn: ${path.relative(ROOT, outPath)}`);
    console.log('> Benotz --force fir nei erofzelueden.');
    return;
  }

  console.log(`> Eroflueden FLH-Donnéeën fir Saison ${opts.season} (Period ${periodId})...`);
  const data = await fetchAllGames(periodId);

  const archive = {
    season: opts.season,
    periodId,
    fetchedAt: new Date().toISOString(),
    source: API_BASE,
    games: data.games,
    replaceLabels: data.replaceLabels,
    standingsByLabel: data.standingsByLabel,
    errors: data.errors
  };

  await writeFile(outPath, JSON.stringify(archive, null, 2) + '\n', 'utf8');
  console.log(`> Fäerdeg: ${data.games.length} Matcher, ${Object.keys(data.standingsByLabel).length} Tabellen.`);
  console.log(`> Archiv: ${path.relative(ROOT, outPath)}`);
  if (data.errors.length) {
    console.warn(`> Feeler bei ${data.errors.length} Request(s):`);
    for (const e of data.errors) console.warn(`  • ${e}`);
  }
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
