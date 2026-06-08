(function () {
    const config = window.Mersch75FeedbackConfig;
    if (!config || document.body.classList.contains('feedback-admin-page')) return;

    const ratingsKey = config.storageKey;
    const votesKey = config.voteStorageKey;
    const values = ['up', 'neutral', 'down'];
    const labels = {
        up: 'Daumen hoch',
        neutral: 'Daumen seitwärts',
        down: 'Daumen runter'
    };
    const icons = {
        up: '👍',
        neutral: '↔️',
        down: '👎'
    };

    function readJson(key, fallback) {
        try {
            return JSON.parse(localStorage.getItem(key)) || fallback;
        } catch (error) {
            return fallback;
        }
    }

    function writeJson(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    }

    function normalizedPath() {
        return window.location.pathname.replace(/\/[^/]*$/, function (match) {
            return match || '/';
        });
    }

    function currentPathWithHash() {
        const path = window.location.pathname || '/';
        return path + (window.location.hash || '');
    }

    function findCategory() {
        const explicit = document.querySelector('[data-feedback-category]');
        if (explicit) {
            const id = explicit.getAttribute('data-feedback-category');
            const match = config.categories.find((category) => category.id === id);
            if (match) return match;
        }

        const pathHash = currentPathWithHash();
        const path = window.location.pathname || '/';
        return config.categories.find((category) => Array.isArray(category.paths) && category.paths.includes(pathHash)) ||
            config.categories.find((category) => Array.isArray(category.paths) && category.paths.includes(path)) ||
            config.categories.find((category) => category.id === 'home');
    }

    function ensureRatingBucket(ratings, category) {
        if (!ratings[category.id]) {
            ratings[category.id] = {
                id: category.id,
                title: category.title,
                group: category.group,
                status: category.status,
                up: 0,
                neutral: 0,
                down: 0,
                total: 0,
                history: []
            };
        }
        ratings[category.id].title = category.title;
        ratings[category.id].group = category.group;
        ratings[category.id].status = category.status;
        return ratings[category.id];
    }

    function renderWidget(category) {
        const widget = document.createElement('aside');
        widget.className = 'feedback-widget';
        widget.setAttribute('aria-label', 'Bewäertung');
        widget.innerHTML = '<strong>Bewäertung</strong><span>' + category.title + '</span><div class="feedback-widget-actions"></div><small></small>';

        const actions = widget.querySelector('.feedback-widget-actions');
        const hint = widget.querySelector('small');
        const votes = readJson(votesKey, {});
        const currentVote = votes[category.id];

        values.forEach((value) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.setAttribute('aria-label', labels[value]);
            button.dataset.feedbackValue = value;
            button.textContent = icons[value];
            button.classList.toggle('is-selected', currentVote === value);
            button.addEventListener('click', () => submitVote(category, value, widget));
            actions.append(button);
        });

        hint.textContent = currentVote ? 'Danke, deine Bewertung ist gespeichert.' : 'Dezent, lokal gespeichert.';
        document.body.append(widget);
    }

    function submitVote(category, value, widget) {
        const ratings = readJson(ratingsKey, {});
        const votes = readJson(votesKey, {});
        const previous = votes[category.id];
        const bucket = ensureRatingBucket(ratings, category);

        if (previous && values.includes(previous) && bucket[previous] > 0) {
            bucket[previous] -= 1;
        }

        bucket[value] += 1;
        bucket.total = bucket.up + bucket.neutral + bucket.down;
        bucket.history.push({
            value: value,
            previous: previous || null,
            page: window.location.pathname,
            hash: window.location.hash || '',
            timestamp: new Date().toISOString()
        });

        votes[category.id] = value;
        writeJson(ratingsKey, ratings);
        writeJson(votesKey, votes);

        widget.querySelectorAll('button').forEach((button) => {
            button.classList.toggle('is-selected', button.dataset.feedbackValue === value);
        });
        widget.querySelector('small').textContent = 'Danke, gespeichert.';
    }

    document.addEventListener('DOMContentLoaded', () => {
        const category = findCategory();
        if (category) renderWidget(category);
    });
}());
