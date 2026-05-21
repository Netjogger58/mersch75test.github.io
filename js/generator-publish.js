/*
 * Mersch75 Generator-Publisher
 *
 * Schreibt das aktuelle Matchday-Poster direkt ueber die GitHub Contents API
 * ins Repo. Token + Repo-Settings werden lokal im Browser (localStorage)
 * gehalten — Soft-Lock-Prinzip wie generator-gate.js.
 *
 * Konfiguration:
 *   - localStorage[m75-publish-mode] : 'github' oder 'proxy'
 *   - localStorage[m75-proxy-url]    : HTTPS-Endpoint fuer sicheren Publish
 *   - localStorage[m75-gh-token]  : Personal Access Token (Fine-grained, Scope
 *                                    nur dieses Repo + Contents: Read & Write)
 *   - localStorage[m75-gh-owner]  : GitHub-User/Org    (Default: aus URL geraten)
 *   - localStorage[m75-gh-repo]   : Repo-Name          (Default: aus URL geraten)
 *   - localStorage[m75-gh-branch] : Branch             (Default: main)
 *
 * Hauptdateien:
 *   - Media/Hauptseite/current-matchposter.jpg              (wird ueberschrieben)
 *   - Media/Hauptseite/archive/matchposter-DDMMYY.jpg       (Archiv-Kopie)
 */
(function () {
    var KEYS = {
        mode:   'm75-publish-mode',
        proxyUrl: 'm75-proxy-url',
        token:  'm75-gh-token',
        owner:  'm75-gh-owner',
        repo:   'm75-gh-repo',
        branch: 'm75-gh-branch'
    };
    var DEFAULTS = {
        mode: 'github',
        owner:  'netjogger58',
        repo:   'mersch75test.github.io',
        branch: 'main',
        targetPath:         'Media/Hauptseite/current-matchposter.jpg',
        targetPathPortrait: 'Media/Hauptseite/current-matchposter-portrait.jpg'
    };

    function lsGet(k) { try { return localStorage.getItem(k) || ''; } catch (e) { return ''; } }
    function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
    function lsDel(k) { try { localStorage.removeItem(k); } catch (e) {} }

    function getConfig() {
        return {
            mode:   lsGet(KEYS.mode) || DEFAULTS.mode,
            proxyUrl: lsGet(KEYS.proxyUrl),
            token:  lsGet(KEYS.token),
            owner:  lsGet(KEYS.owner)  || DEFAULTS.owner,
            repo:   lsGet(KEYS.repo)   || DEFAULTS.repo,
            branch: lsGet(KEYS.branch) || DEFAULTS.branch
        };
    }

    function setConfig(cfg) {
        if (typeof cfg.mode === 'string') { cfg.mode ? lsSet(KEYS.mode, cfg.mode) : lsDel(KEYS.mode); }
        if (typeof cfg.proxyUrl === 'string') { cfg.proxyUrl ? lsSet(KEYS.proxyUrl, cfg.proxyUrl) : lsDel(KEYS.proxyUrl); }
        if (typeof cfg.token  === 'string') { cfg.token  ? lsSet(KEYS.token,  cfg.token)  : lsDel(KEYS.token); }
        if (typeof cfg.owner  === 'string') { cfg.owner  ? lsSet(KEYS.owner,  cfg.owner)  : lsDel(KEYS.owner); }
        if (typeof cfg.repo   === 'string') { cfg.repo   ? lsSet(KEYS.repo,   cfg.repo)   : lsDel(KEYS.repo); }
        if (typeof cfg.branch === 'string') { cfg.branch ? lsSet(KEYS.branch, cfg.branch) : lsDel(KEYS.branch); }
    }

    function clearAll() {
        lsDel(KEYS.mode); lsDel(KEYS.proxyUrl);
        lsDel(KEYS.token); lsDel(KEYS.owner); lsDel(KEYS.repo); lsDel(KEYS.branch);
    }

    function hasToken() { return !!lsGet(KEYS.token); }
    function hasProxy() { return !!lsGet(KEYS.proxyUrl); }
    function canPublish() {
        var cfg = getConfig();
        return cfg.mode === 'proxy' ? !!cfg.proxyUrl : !!cfg.token;
    }

    function validateProxyUrl(proxyUrl) {
        try {
            var parsed = new URL(proxyUrl);
            if (parsed.protocol !== 'https:') throw new Error('Proxy-URL muss mit https:// beginnen.');
            return parsed.toString();
        } catch (err) {
            throw new Error('Ungueltige Proxy-URL. Bitte eine vollstaendige https-Adresse eintragen.');
        }
    }

    function apiUrl(cfg, path) {
        return 'https://api.github.com/repos/' + encodeURIComponent(cfg.owner)
            + '/' + encodeURIComponent(cfg.repo) + '/contents/'
            + path.split('/').map(encodeURIComponent).join('/');
    }

    function authHeaders(cfg) {
        return {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': 'Bearer ' + cfg.token
        };
    }

    // GET sha (oder null wenn Datei noch nicht existiert)
    function getFileSha(cfg, path) {
        var url = apiUrl(cfg, path) + '?ref=' + encodeURIComponent(cfg.branch);
        return fetch(url, { headers: authHeaders(cfg) }).then(function (r) {
            if (r.status === 404) return null;
            if (!r.ok) return r.text().then(function (t) { throw new Error('GET ' + path + ' (' + r.status + '): ' + t); });
            return r.json().then(function (j) { return j.sha || null; });
        });
    }

    function putFile(cfg, path, base64Content, message, sha) {
        var body = { message: message, content: base64Content, branch: cfg.branch };
        if (sha) body.sha = sha;
        return fetch(apiUrl(cfg, path), {
            method: 'PUT',
            headers: Object.assign({ 'Content-Type': 'application/json' }, authHeaders(cfg)),
            body: JSON.stringify(body)
        }).then(function (r) {
            if (!r.ok) return r.text().then(function (t) { throw new Error('PUT ' + path + ' (' + r.status + '): ' + t); });
            return r.json();
        });
    }

    // GET /user — verifiziert dass Token gueltig ist
    function testToken(cfg) {
        cfg = cfg || getConfig();
        if (!cfg.token) return Promise.reject(new Error('Kein Token gesetzt.'));
        return fetch('https://api.github.com/user', { headers: authHeaders(cfg) }).then(function (r) {
            if (!r.ok) return r.text().then(function (t) { throw new Error('Token-Check fehlgeschlagen (' + r.status + '): ' + t); });
            return r.json();
        }).then(function (user) {
            // Zusaetzlich: Repo-Zugriff pruefen
            return fetch('https://api.github.com/repos/' + cfg.owner + '/' + cfg.repo, { headers: authHeaders(cfg) }).then(function (r2) {
                if (!r2.ok) return r2.text().then(function (t) { throw new Error('Repo-Zugriff verweigert (' + r2.status + '): ' + t); });
                return r2.json();
            }).then(function (repo) {
                return { user: user.login, repo: repo.full_name, private: repo.private };
            });
        });
    }

    function testPublishTarget(cfg) {
        cfg = cfg || getConfig();
        if (cfg.mode === 'proxy') {
            try {
                return Promise.resolve({
                    mode: 'proxy',
                    target: validateProxyUrl(cfg.proxyUrl),
                    note: 'Proxy-Endpoint sieht syntaktisch gueltig aus.'
                });
            } catch (err) {
                return Promise.reject(err);
            }
        }
        return testToken(cfg).then(function(info) {
            info.mode = 'github';
            return info;
        });
    }

    function dataUrlToBase64(dataUrl) {
        var i = String(dataUrl || '').indexOf(',');
        return i >= 0 ? dataUrl.substring(i + 1) : '';
    }

    function dateStamp(date) {
        var d = date || new Date();
        return String(d.getDate()).padStart(2, '0')
            +  String(d.getMonth() + 1).padStart(2, '0')
            +  String(d.getFullYear()).slice(-2);
    }

    function publishViaProxy(cfg, b64L, b64P, ds, onProgress) {
        var proxyUrl = validateProxyUrl(cfg.proxyUrl);
        var notify = function (s) { if (typeof onProgress === 'function') onProgress(s); };
        notify('Proxy: Poster an sicheren Endpoint senden...');
        return fetch(proxyUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                stamp: ds,
                landscapeBase64: b64L,
                portraitBase64: b64P,
                targets: {
                    landscape: DEFAULTS.targetPath,
                    portrait: DEFAULTS.targetPathPortrait,
                    archiveLandscape: 'Media/Hauptseite/archive/matchposter-' + ds + '.jpg',
                    archivePortrait: 'Media/Hauptseite/archive/matchposter-' + ds + '-portrait.jpg'
                }
            })
        }).then(function (r) {
            if (!r.ok) return r.text().then(function (t) { throw new Error('Proxy-Publish fehlgeschlagen (' + r.status + '): ' + t); });
            return r.json().catch(function () { return {}; });
        }).then(function (payload) {
            notify('Proxy: Veroeffentlicht. GitHub Pages baut in ~30s neu.');
            return {
                stamp: ds,
                mode: 'proxy',
                target: DEFAULTS.targetPath,
                targetPortrait: b64P ? DEFAULTS.targetPathPortrait : null,
                response: payload
            };
        });
    }

    // Hauptfunktion: veroeffentlicht das Poster (Landscape) + optional Portrait
    // + Archiv-Kopien.
    // landscapeDataUrl: "data:image/jpeg;base64,..." (Pflicht)
    // portraitDataUrl:  "data:image/jpeg;base64,..." (optional, kann null sein)
    // stamp: optionaler DDMMYY-String fuer Commit-Nachricht + Archiv-Pfad
    // onProgress: function(stepLabel) — UI-Update
    function publishPoster(landscapeDataUrl, portraitDataUrl, stamp, onProgress) {
        var cfg = getConfig();
        var b64L = dataUrlToBase64(landscapeDataUrl);
        if (!b64L) return Promise.reject(new Error('Kein gueltiges Landscape-Bild zum Veroeffentlichen.'));
        var b64P = portraitDataUrl ? dataUrlToBase64(portraitDataUrl) : null;
        var ds = stamp || dateStamp();
        if (cfg.mode === 'proxy') {
            if (!cfg.proxyUrl) return Promise.reject(new Error('Kein Proxy-Endpoint gesetzt. Bitte zuerst in den Generator-Einstellungen eintragen.'));
            return publishViaProxy(cfg, b64L, b64P, ds, onProgress);
        }
        if (!cfg.token) return Promise.reject(new Error('Kein Token gesetzt. Bitte zuerst in den Generator-Einstellungen eintragen.'));
        var archiveL = 'Media/Hauptseite/archive/matchposter-' + ds + '.jpg';
        var archiveP = 'Media/Hauptseite/archive/matchposter-' + ds + '-portrait.jpg';
        var msg = 'Matchposter ' + ds + ' (Generator)';

        var notify = function (s) { if (typeof onProgress === 'function') onProgress(s); };

        notify('Landscape: aktuelle Version pruefen...');
        return getFileSha(cfg, DEFAULTS.targetPath).then(function (sha) {
            notify('Landscape: hochladen...');
            return putFile(cfg, DEFAULTS.targetPath, b64L, msg, sha);
        }).then(function () {
            notify('Landscape: Archiv-Kopie ablegen...');
            return getFileSha(cfg, archiveL).then(function (sha2) {
                return putFile(cfg, archiveL, b64L, msg + ' (Archiv)', sha2);
            }).catch(function (err) { console.warn('Landscape-Archiv uebersprungen:', err); });
        }).then(function () {
            if (!b64P) return null;
            notify('Portrait: aktuelle Version pruefen...');
            return getFileSha(cfg, DEFAULTS.targetPathPortrait).then(function (sha) {
                notify('Portrait: hochladen...');
                return putFile(cfg, DEFAULTS.targetPathPortrait, b64P, msg + ' (Portrait)', sha);
            }).then(function () {
                notify('Portrait: Archiv-Kopie ablegen...');
                return getFileSha(cfg, archiveP).then(function (sha2) {
                    return putFile(cfg, archiveP, b64P, msg + ' (Portrait Archiv)', sha2);
                }).catch(function (err) { console.warn('Portrait-Archiv uebersprungen:', err); });
            });
        }).then(function () {
            notify('Veroeffentlicht. GitHub Pages baut in ~30s neu.');
            return { stamp: ds, target: DEFAULTS.targetPath, targetPortrait: b64P ? DEFAULTS.targetPathPortrait : null };
        });
    }

    window.MerschPublish = {
        getConfig:   getConfig,
        setConfig:   setConfig,
        clearAll:    clearAll,
        hasToken:    hasToken,
        hasProxy:    hasProxy,
        canPublish:  canPublish,
        testToken:   testToken,
        testTarget:  testPublishTarget,
        publish:     publishPoster,
        dateStamp:   dateStamp,
        DEFAULTS:    DEFAULTS
    };
})();
