/*
 * Mersch75 Events-Gate
 *
 * Soft-Lock fuer die Events-Seite (Testphase).
 * Gleiche Logik wie generator-gate.js – haelt Zufallsbesucher fern,
 * kein echter Schutz da Quelltext oeffentlich ist.
 *
 * Passwort: mersch75events
 * TTL: 7 Tage (LocalStorage)
 */
(function () {
    var STORAGE_KEY = 'm75-events-ok';
    var PASSWORD    = 'mersch75events';
    var TTL_MS      = 7 * 24 * 60 * 60 * 1000;
    var TARGET      = 'events.html';

    function isUnlocked() {
        try {
            var raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return false;
            var expiry = parseInt(raw, 10);
            if (!isFinite(expiry)) return false;
            if (Date.now() > expiry) { localStorage.removeItem(STORAGE_KEY); return false; }
            return true;
        } catch (e) { return false; }
    }

    function setUnlocked() {
        try { localStorage.setItem(STORAGE_KEY, String(Date.now() + TTL_MS)); } catch (e) {}
    }

    function buildModal() {
        var existing = document.getElementById('ev-modal');
        if (existing) return existing;

        var overlay = document.createElement('div');
        overlay.id = 'ev-modal';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-labelledby', 'ev-modal-title');
        overlay.hidden = true;
        overlay.style.cssText = [
            'position:fixed;inset:0;z-index:9999',
            'display:flex;align-items:center;justify-content:center',
            'background:rgba(0,0,0,.65);backdrop-filter:blur(4px)'
        ].join(';');

        overlay.innerHTML =
            '<div style="background:#fff;border-radius:16px;padding:2.5rem 2rem;max-width:380px;width:90%;box-shadow:0 24px 64px rgba(0,43,92,.25);font-family:inherit">' +
              '<button type="button" id="ev-modal-close" aria-label="Schliessen" style="float:right;background:none;border:none;font-size:1.5rem;cursor:pointer;color:#666;margin:-1rem -0.5rem 0 0">&times;</button>' +
              '<h2 id="ev-modal-title" style="margin:0 0 .5rem;font-size:1.3rem;color:#002b5c">🔒 Events – Testzugang</h2>' +
              '<p style="margin:0 0 1.25rem;font-size:.9rem;color:#555">Diese Seite befindet sich noch im Testbetrieb. Bitte Passwort eingeben.</p>' +
              '<form id="ev-modal-form" novalidate>' +
                '<label style="display:block;font-size:.8rem;font-weight:700;letter-spacing:.06em;color:#002b5c;margin-bottom:.4rem" for="ev-modal-input">PASSWORT</label>' +
                '<input id="ev-modal-input" type="password" autocomplete="off" autocapitalize="off" spellcheck="false" required ' +
                  'style="width:100%;box-sizing:border-box;padding:.75rem 1rem;border:2px solid #d0d8e4;border-radius:8px;font-size:1rem;outline:none">' +
                '<p id="ev-modal-error" hidden style="color:#c0392b;font-size:.85rem;margin:.5rem 0 0">Passwort falsch – bitte nochmal versuchen.</p>' +
                '<div style="display:flex;gap:.75rem;margin-top:1.25rem">' +
                  '<button type="button" id="ev-modal-cancel" style="flex:1;padding:.75rem;border:2px solid #d0d8e4;border-radius:8px;background:#fff;cursor:pointer;font-size:.95rem">Abbrechen</button>' +
                  '<button type="submit" style="flex:1;padding:.75rem;border:none;border-radius:8px;background:#002b5c;color:#f9d611;font-weight:700;cursor:pointer;font-size:.95rem">Einloggen</button>' +
                '</div>' +
              '</form>' +
            '</div>';

        document.body.appendChild(overlay);

        var form   = document.getElementById('ev-modal-form');
        var input  = document.getElementById('ev-modal-input');
        var err    = document.getElementById('ev-modal-error');
        var cancel = document.getElementById('ev-modal-cancel');
        var close  = document.getElementById('ev-modal-close');

        function dismiss() { overlay.hidden = true; }

        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            if ((input.value || '').trim() === PASSWORD) {
                setUnlocked();
                window.location.href = TARGET;
            } else {
                err.hidden = false;
                input.select();
            }
        });

        cancel.addEventListener('click', dismiss);
        close.addEventListener('click', dismiss);
        overlay.addEventListener('click', function (ev) { if (ev.target === overlay) dismiss(); });
        document.addEventListener('keydown', function (ev) { if (!overlay.hidden && ev.key === 'Escape') dismiss(); });

        return overlay;
    }

    function openModal() {
        var overlay = buildModal();
        var err = document.getElementById('ev-modal-error');
        var input = document.getElementById('ev-modal-input');
        if (err) err.hidden = true;
        if (input) input.value = '';
        overlay.hidden = false;
        if (input) setTimeout(function () { input.focus(); }, 30);
    }

    function interceptLinks() {
        var links = document.querySelectorAll('a[href$="' + TARGET + '"], a[href*="' + TARGET + '?"]');
        for (var i = 0; i < links.length; i++) {
            var a = links[i];
            if (a.dataset.evGated === '1') continue;
            a.dataset.evGated = '1';
            a.addEventListener('click', function (ev) {
                if (isUnlocked()) return;
                ev.preventDefault();
                openModal();
            });
        }
    }

    function handlePageLoad() {
        var path = (window.location.pathname || '').toLowerCase();
        var isEvPage = path.endsWith('/' + TARGET) || path.endsWith(TARGET);

        if (isEvPage) {
            if (!isUnlocked()) {
                window.location.replace('index.html?ev=lock');
            }
            return;
        }

        interceptLinks();
        if (/[?&]ev=lock\b/.test(window.location.search)) {
            openModal();
        }
    }

    window.MerschEventsGate = { isUnlocked: isUnlocked, open: openModal };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', handlePageLoad);
    } else {
        handlePageLoad();
    }
})();
