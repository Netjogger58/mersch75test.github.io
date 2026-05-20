(function() {
    const API_BASE = 'https://spo.handball4all.de/service/if_g_json.php';
    const ORG_ID = '95';
    const CURRENT_PERIOD_ID = '137';
    const REQUESTS = [
        { key: 's1', cl: '153713', label: 'HERREN 1 (H-PRO)' },
        { key: 'fe', cl: '152653', label: 'FRAUEN (D-PRO)' },
        { key: 'u15', cl: '156341', label: 'JUGEND: U15G' },
        { key: 'u13pe', cl: '152106', label: 'JUGEND: U13M-PE' },
        { key: 'u11el', cl: '152529', label: 'JUGEND: U11 Elite', replaces: ['JUGEND: U11 Elite', 'JUGEND: U11M-EL', 'JUGEND: U11M-EPF5-10'] },
        { key: 'u11es', cl: '153409', label: 'JUGEND: U11 Espoirs', replaces: ['JUGEND: U11 Espoirs', 'JUGEND: U11M-ES'], allowCommentMatch: true },
        { key: 'u9', cl: '151356', label: 'JUGEND: U9M', allowCommentMatch: true },
        { key: 'u7', cl: '152096', label: 'JUGEND: U7M', allowCommentMatch: true }
    ];

    function buildUrl(config) {
        const params = new URLSearchParams({
            cmd: 'ps',
            og: ORG_ID,
            p: CURRENT_PERIOD_ID,
            cl: config.cl,
            ca: '1',
            _: String(Date.now())
        });
        return API_BASE + '?' + params.toString();
    }

    function trimValue(value) {
        return String(value == null ? '' : value).trim();
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
        for (let index = 0; index < games.length; index++) {
            const game = games[index];
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

        const sbo = trimValue(game.sbo);
        if (sbo) return 'sbo|' + sbo;

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

        for (let index = 0; index < fields.length; index++) {
            const field = fields[index];
            const incomingValue = trimValue(incoming[field]);
            const baseValue = trimValue(base[field]);
            if (incomingValue && !baseValue) {
                merged[field] = incoming[field];
            }
        }

        if (trimValue(incoming.datum)) merged.datum = incoming.datum;
        if (trimValue(incoming.heim)) merged.heim = incoming.heim;
        if (trimValue(incoming.gast)) merged.gast = incoming.gast;
        if (trimValue(incoming.nr)) merged.nr = incoming.nr;
        if (trimValue(incoming.halle)) merged.halle = incoming.halle;
        if (trimValue(incoming.score)) merged.score = incoming.score;
        if (trimValue(incoming.bem)) merged.bem = incoming.bem;
        if (trimValue(incoming.sbo)) merged.sbo = incoming.sbo;
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
        const directText = [
            trimValue(game.gHomeTeam),
            trimValue(game.gGuestTeam)
        ].join(' ');

        if (hasClubReference(directText)) return true;
        if (!config || !config.allowCommentMatch) return false;

        const metaText = [
            trimValue(game.gComment),
            trimValue(game.gGroupsortTxt)
        ].join(' ');

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
            sbo: trimValue(rawGame.sGID) ? 'https://spo.handball4all.de/misc/sboPublicReports.php?sGID=' + trimValue(rawGame.sGID) : '',
            rtl: '',
            nr: trimValue(rawGame.gNo),
            halle: trimValue(rawGame.gGymnasiumNo)
        };
    }

    async function fetchCompetitionGames(config) {
        const response = await fetch(buildUrl(config), { cache: 'no-store' });
        if (!response.ok) throw new Error('FLH ' + config.label + ' HTTP ' + response.status);
        const payload = await response.json();
        const content = payload && payload[0] && payload[0].content ? payload[0].content : null;
        if (!content) return [];

        const combined = extractGames(content.actualGames).concat(extractGames(content.futureGames));
        return dedupeGames(
            combined
                .filter(function(game) { return isRelevantGame(config, game); })
                .map(function(game) { return mapGame(config, game); })
                .filter(function(game) { return game.datum && game.heim; })
        );
    }

    async function fetchAllGames(progressCallback) {
        const results = await Promise.allSettled(REQUESTS.map(async function(config) {
            if (typeof progressCallback === 'function') progressCallback('Aktualisiere FLH-Daten: ' + config.label + '...');
            const games = await fetchCompetitionGames(config);
            return { config: config, games: games };
        }));

        const mergedGames = [];
        const replaceLabels = new Set();
        const errors = [];

        for (let index = 0; index < results.length; index++) {
            const result = results[index];
            if (result.status === 'fulfilled') {
                const value = result.value;
                if (value.games.length) {
                    mergedGames.push.apply(mergedGames, value.games);
                    replaceLabels.add(value.config.label);
                    const replaces = value.config.replaces || [];
                    for (let replaceIndex = 0; replaceIndex < replaces.length; replaceIndex++) {
                        replaceLabels.add(replaces[replaceIndex]);
                    }
                }
            } else {
                errors.push(result.reason && result.reason.message ? result.reason.message : String(result.reason));
            }
        }

        return {
            games: dedupeGames(mergedGames),
            replaceLabels: Array.from(replaceLabels),
            errors: errors
        };
    }

    function mergeLiveSeasonGames(staticGames, livePayload) {
        const liveGames = livePayload && Array.isArray(livePayload.games) ? livePayload.games : [];
        const preservedGames = Array.isArray(staticGames) ? staticGames : [];

        const mergedByKey = new Map();
        preservedGames.concat(liveGames).forEach(function(game) {
            const key = buildMergeKey(game);
            if (!key) return;
            if (!mergedByKey.has(key)) {
                mergedByKey.set(key, Object.assign({}, game));
                return;
            }
            mergedByKey.set(key, mergeGameDetails(mergedByKey.get(key), game));
        });

        return Array.from(mergedByKey.values());
    }

    window.MerschFlhSync = {
        fetchAllGames: fetchAllGames,
        mergeLiveSeasonGames: mergeLiveSeasonGames
    };
})();