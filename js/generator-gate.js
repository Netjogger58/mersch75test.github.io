/*
 * Mersch75 Generator-Gate
 *
 * Soft-Lock fuer die interne Generator-App. Reicht NICHT als echter Schutz
 * (Quelltext ist oeffentlich einsehbar), haelt aber Zufallsbesucher fern.
 *
 * Funktionsweise:
 *  - Auf normalen Seiten: faengt Klicks auf Links zu generator.html ab und
 *    zeigt ein Passwort-Modal. Bei richtigem Passwort wird ein Eintrag im
 *    LocalStorage gesetzt (7 Tage gueltig) und zum Generator weitergeleitet.
 *  - Auf generator.html selbst: prueft beim Laden, ob LocalStorage gueltig ist.
 *    Wenn nicht, Redirect zur Startseite mit ?gen=lock (oeffnet dort das Modal).
 *  - "Eingeloggt"-Status legt body.dataset.genUnlocked = "1" frei -> CSS kann
 *    z.B. einen Edit-Button auf der Homepage einblenden.
 */
(function () {
    var STORAGE_KEY = 'm75-gen-ok';
    var PASSWORD = 'mersch75';
    var TTL_MS = 7 * 24 * 60 * 60 * 1000;
    var TARGET = 'generator.html';

    function isUnlocked() {
        try {
            var raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return false;
            var expiry = parseInt(raw, 10);
            if (!isFinite(expiry)) return false;
            if (Date.now() > expiry) {
                localStorage.removeItem(STORAGE_KEY);
                return false;
            }
            return true;
        } catch (e) {
            return false;
        }
    }

    function setUnlocked() {
        try { localStorage.setItem(STORAGE_KEY, String(Date.now() + TTL_MS)); } catch (e) {}
        markBody();
    }

    function clearUnlock() {
        try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
        if (document.body) delete document.body.dataset.genUnlocked;
    }

    function markBody() {
        if (document.body && isUnlocked()) {
            document.body.dataset.genUnlocked = '1';
        }
    }

    function buildModal() {
        var existing = document.getElementById('gen-modal');
        if (existing) return existing;
        var overlay = document.createElement('div');
        overlay.id = 'gen-modal';
        overlay.className = 'gen-modal';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-labelledby', 'gen-modal-title');
        overlay.hidden = true;
        overlay.innerHTML = ''
            + '<div class="gen-modal-card">'
            +   '<button type="button" class="gen-modal-close" aria-label="Schliessen">&times;</button>'
            +   '<h2 id="gen-modal-title">Generator-Zugang</h2>'
            +   '<p class="gen-modal-lead">Interner Bereich fuer den Matchday-Poster-Generator. Bitte Passwort eingeben.</p>'
            +   '<form class="gen-modal-form" novalidate>'
            +     '<label class="gen-modal-label" for="gen-modal-input">Passwort</label>'
            +     '<input id="gen-modal-input" class="gen-modal-input" type="password" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" required>'
            +     '<p class="gen-modal-error" hidden>Passwort falsch.</p>'
            +     '<div class="gen-modal-actions">'
            +       '<button type="button" class="gen-modal-cancel">Abbrechen</button>'
            +       '<button type="submit" class="gen-modal-submit">Einloggen</button>'
            +     '</div>'
            +   '</form>'
            + '</div>';
        document.body.appendChild(overlay);

        var form = overlay.querySelector('.gen-modal-form');
        var input = overlay.querySelector('.gen-modal-input');
        var err = overlay.querySelector('.gen-modal-error');
        var cancel = overlay.querySelector('.gen-modal-cancel');
        var close = overlay.querySelector('.gen-modal-close');

        function dismiss() { closeModal(); }

        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            if ((input.value || '').trim() === PASSWORD) {
                setUnlocked();
                var next = overlay.dataset.nextHref || TARGET;
                window.location.href = next;
            } else {
                err.hidden = false;
                input.select();
            }
        });
        cancel.addEventListener('click', dismiss);
        close.addEventListener('click', dismiss);
        overlay.addEventListener('click', function (ev) { if (ev.target === overlay) dismiss(); });
        document.addEventListener('keydown', function (ev) {
            if (!overlay.hidden && ev.key === 'Escape') dismiss();
        });
        return overlay;
    }

    function openModal(nextHref) {
        var overlay = buildModal();
        overlay.dataset.nextHref = nextHref || TARGET;
        var err = overlay.querySelector('.gen-modal-error');
        var input = overlay.querySelector('.gen-modal-input');
        if (err) err.hidden = true;
        if (input) input.value = '';
        overlay.hidden = false;
        if (input) setTimeout(function () { input.focus(); }, 30);
    }

    function closeModal() {
        var overlay = document.getElementById('gen-modal');
        if (overlay) overlay.hidden = true;
    }

    function interceptLinks() {
        var links = document.querySelectorAll('a[href$="' + TARGET + '"], a[href*="' + TARGET + '?"]');
        for (var i = 0; i < links.length; i++) {
            var a = links[i];
            if (a.dataset.genGated === '1') continue;
            a.dataset.genGated = '1';
            a.classList.add('has-gen-lock');
            a.addEventListener('click', function (ev) {
                if (isUnlocked()) return;
                ev.preventDefault();
                openModal(this.getAttribute('href'));
            });
        }
    }

    function handlePageLoad() {
        markBody();

        var path = (window.location.pathname || '').toLowerCase();
        var isGenPage = path.endsWith('/' + TARGET) || path.endsWith(TARGET);

        if (isGenPage) {
            if (!isUnlocked()) {
                window.location.replace('index.html?gen=lock');
            }
            return;
        }

        interceptLinks();
        if (/[?&]gen=lock\b/.test(window.location.search)) {
            openModal(TARGET);
        }
    }

    window.MerschGate = {
        isUnlocked: isUnlocked,
        open: openModal,
        close: closeModal,
        clear: clearUnlock
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', handlePageLoad);
    } else {
        handlePageLoad();
    }
})();