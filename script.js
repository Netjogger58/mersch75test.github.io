const yearTarget = document.querySelector('#current-year');

function initializeSiteMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');

    if (!navToggle || !siteNav) {
        return;
    }

    const labelDefault = 'Menü';
    const desiredOrder = [
        'matchcenter.html',
        'matchday.html',
        'training.html',
        'news.html',
        'join.html',
        'inside.html',
        'gallery.html',
        'community.html',
        'links.html',
        'contact.html'
    ];
    const primaryLinks = new Set([
        'matchcenter.html',
        'matchday.html',
        'training.html',
        'news.html',
        'join.html',
        'inside.html'
    ]);

    const currentLinks = Array.from(siteNav.querySelectorAll('a'));
    const linkMap = new Map(
        currentLinks.map((link) => [link.getAttribute('href'), link])
    );
    const orderedLinks = desiredOrder
        .map((href) => linkMap.get(href))
        .filter(Boolean);
    const fallbackLinks = currentLinks.filter((link) => !desiredOrder.includes(link.getAttribute('href')));
    const allLinks = [...orderedLinks, ...fallbackLinks];

    const intro = document.createElement('div');
    intro.className = 'site-menu-intro';
    intro.innerHTML = [
        '<p class="site-menu-kicker">Navigation</p>',
        '<h2>Alles Wichtegt fir Mersch75 op enger Plaz.</h2>',
        '<p>Matchday, Matchcenter, Training a Club-Liewen ginn hei wéi an engem richtege Menü-Hub gebündelt, amplaz als klassesch Header-Leescht.</p>'
    ].join('');

    const primaryGroup = document.createElement('div');
    primaryGroup.className = 'site-menu-primary';

    const secondaryGroup = document.createElement('div');
    secondaryGroup.className = 'site-menu-secondary';

    allLinks.forEach((link) => {
        const href = link.getAttribute('href');
        const targetGroup = primaryLinks.has(href) ? primaryGroup : secondaryGroup;
        targetGroup.append(link);
    });

    const footer = document.createElement('div');
    footer.className = 'site-menu-footer';
    footer.innerHTML = [
        '<a class="site-menu-cta" href="matchday.html">',
        '<span>Live Fokus</span>',
        '<strong>Aktueller Spieltag</strong>',
        '</a>',
        '<a class="site-menu-cta" href="join.html">',
        '<span>Club</span>',
        '<strong>Mitmachen & Kontakt</strong>',
        '</a>'
    ].join('');

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'site-menu-close';
    closeButton.setAttribute('aria-label', 'Menü schließen');
    closeButton.textContent = 'X';

    const shell = document.createElement('div');
    shell.className = 'site-menu-shell';
    shell.append(closeButton, intro, primaryGroup, secondaryGroup, footer);

    siteNav.innerHTML = '';
    siteNav.append(shell);
    document.body.append(siteNav);

    const backdrop = document.createElement('button');
    backdrop.type = 'button';
    backdrop.className = 'site-menu-backdrop';
    backdrop.setAttribute('aria-label', 'Menü schließen');
    document.body.append(backdrop);

    const closeMenu = () => {
        document.body.classList.remove('menu-open');
        siteNav.classList.remove('is-open');
        backdrop.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = labelDefault;
    };

    const openMenu = () => {
        document.body.classList.add('menu-open');
        siteNav.classList.add('is-open');
        backdrop.classList.add('is-open');
        navToggle.setAttribute('aria-expanded', 'true');
    };

    navToggle.textContent = labelDefault;
    navToggle.addEventListener('click', () => {
        if (siteNav.classList.contains('is-open')) {
            closeMenu();
            return;
        }

        openMenu();
    });

    backdrop.addEventListener('click', closeMenu);
    closeButton.addEventListener('click', closeMenu);
    siteNav.addEventListener('click', (event) => {
        if (event.target instanceof HTMLAnchorElement) {
            closeMenu();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && siteNav.classList.contains('is-open')) {
            closeMenu();
        }
    });
}

initializeSiteMenu();

if (yearTarget) {
    yearTarget.textContent = new Date().getFullYear();
}