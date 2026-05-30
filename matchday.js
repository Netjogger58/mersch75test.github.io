(function () {
    const data = window.MERSCH_MATCHDAY_DATA;

    if (!data) {
        return;
    }

    function setText(id, value) {
        const target = document.getElementById(id);

        if (target && typeof value === 'string') {
            target.textContent = value;
        }
    }

    function renderFixtures(items) {
        const list = document.getElementById('fixture-list');

        if (!list) {
            return;
        }

        list.innerHTML = '';

        items.forEach((fixture) => {
            const card = document.createElement('article');
            card.className = 'card fixture-card';

            const top = document.createElement('div');
            top.className = 'fixture-card-top';

            const type = document.createElement('span');
            type.className = 'fixture-kicker';
            type.textContent = fixture.type;

            const team = document.createElement('span');
            team.className = 'score-label';
            team.textContent = fixture.team;

            top.append(type, team);

            const matchup = document.createElement('h3');
            matchup.className = 'fixture-matchup';
            matchup.textContent = fixture.matchup;

            const meta = document.createElement('div');
            meta.className = 'fixture-meta';

            [
                ['Datum', fixture.date],
                ['Zeit', fixture.time],
                ['Ort', fixture.venue]
            ].forEach(([label, value]) => {
                const row = document.createElement('div');
                row.className = 'fixture-meta-row';

                const strong = document.createElement('strong');
                strong.textContent = label;

                const span = document.createElement('span');
                span.textContent = value;

                row.append(strong, span);
                meta.append(row);
            });

            card.append(top, matchup, meta);
            list.append(card);
        });
    }

    function renderNotes(items) {
        const list = document.getElementById('matchday-notes');

        if (!list) {
            return;
        }

        list.innerHTML = '';

        items.forEach((note) => {
            const item = document.createElement('li');
            item.textContent = note;
            list.append(item);
        });
    }

    setText('matchday-week-label', data.weekLabel);
    setText('matchday-title', data.title);
    setText('matchday-subtitle', data.subtitle);
    setText('featured-badge', data.featuredGame.badge);
    setText('featured-competition', data.featuredGame.competition);
    setText('featured-matchup', data.featuredGame.matchup);
    setText('featured-date', data.featuredGame.date);
    setText('featured-time', data.featuredGame.time);
    setText('featured-venue', data.featuredGame.venue);
    setText('featured-note', data.featuredGame.note);
    setText('publish-updated', data.publishInfo.updated);
    setText('publish-owner', data.publishInfo.owner);

    const generatorLinks = document.querySelectorAll('[data-generator-link]');
    generatorLinks.forEach((link) => {
        link.setAttribute('href', data.publishInfo.generatorHref);
    });

    renderFixtures(data.fixtures || []);
    renderNotes(data.notes || []);
})();