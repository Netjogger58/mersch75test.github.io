(function () {
  'use strict';

  const STORAGE_KEY = 'm75-consent-v1';
  const PREF_KEY = 'm75-consent-preferences';

  const I18N = {
    lb: {
      title: 'Zoustëmmung vu Cookien & Dateveraarbechtung',
      intro: 'Mir benotzen Cookien an ähnlech Technologien, fir d\'Funktionalitéit vun eiser Säit ze garantéieren, Besich ze analyséieren a personaliséiert Inhalter unzebidden. D\'Zoustëmmung ass fräiwëlleg a kann zu aller Zäit iwwer d\'Astellungen zréckgezu ginn.',
      acceptAll: 'Alles akzeptéieren',
      settings: 'Astellungen oder ofleenën',
      save: 'Späicheren',
      back: 'Zeréck',
      essential: 'Noutwendeg',
      analytics: 'Analytik',
      marketing: 'Marketing',
      personalization: 'Personalisatioun',
      cookieInfo: 'Cookien',
      privacy: 'Dateschutz',
      terms: 'AGB',
      imprint: 'Impressum',
      essentialDesc: 'Dës Cookien sinn néideg, fir d\'Säit iwwerhaapt fonctionnéieren ze kënnen.',
      analyticsDesc: 'Hëllefen eis d\'Säitnotzung ze verstoen an anonym Statistiken ze sammelen.',
      marketingDesc: 'Ginn benotzt, fir personaliséiert Reklamm an Offere weiderzeginn.',
      personalizationDesc: 'Erlaben personaliséiert Inhalter a Funktiounen.',
      linkCookies: 'dataprotection.html',
      linkPrivacy: 'dataprotection.html',
      linkTerms: 'terms.html',
      linkImprint: 'impressum.html',
    },
    de: {
      title: 'Einwilligung zu Cookies & Datenverarbeitung',
      intro: 'Wir verwenden Cookies und ähnliche Technologien, um die Funktionalität unserer Website zu gewährleisten, Besuche zu analysieren und personalisierte Inhalte anzubieten. Die Einwilligung ist freiwillig und kann jederzeit in den Einstellungen widerrufen werden.',
      acceptAll: 'Alle akzeptieren',
      settings: 'Einstellungen oder ablehnen',
      save: 'Speichern',
      back: 'Zurück',
      essential: 'Notwendig',
      analytics: 'Analytik',
      marketing: 'Marketing',
      personalization: 'Personalisierung',
      cookieInfo: 'Cookies',
      privacy: 'Datenschutz',
      terms: 'AGB',
      imprint: 'Impressum',
      essentialDesc: 'Diese Cookies sind für den grundlegenden Betrieb der Website erforderlich.',
      analyticsDesc: 'Helfen uns, die Nutzung der Website zu verstehen und anonyme Statistiken zu erfassen.',
      marketingDesc: 'Werden für personalisierte Werbung und Angebote verwendet.',
      personalizationDesc: 'Ermöglichen personalisierte Inhalte und Funktionen.',
      linkCookies: 'dataprotection.html',
      linkPrivacy: 'dataprotection.html',
      linkTerms: 'terms.html',
      linkImprint: 'impressum.html',
    },
    fr: {
      title: 'Consentement aux cookies & traitement des données',
      intro: 'Nous utilisons des cookies et des technologies similaires pour assurer le fonctionnement de notre site, analyser les visites et proposer des contenus personnalisés. Le consentement est libre et peut être retiré à tout moment dans les paramètres.',
      acceptAll: 'Tout accepter',
      settings: 'Paramètres ou refuser',
      save: 'Enregistrer',
      back: 'Retour',
      essential: 'Nécessaire',
      analytics: 'Analytique',
      marketing: 'Marketing',
      personalization: 'Personnalisation',
      cookieInfo: 'Cookies',
      privacy: 'Protection des données',
      terms: 'CGU',
      imprint: 'Mentions légales',
      essentialDesc: 'Ces cookies sont nécessaires au fonctionnement de base du site.',
      analyticsDesc: 'Aident à comprendre l\'utilisation du site et à collecter des statistiques anonymes.',
      marketingDesc: 'Utilisés pour la publicité et les offres personnalisées.',
      personalizationDesc: 'Permettent des contenus et fonctionnalités personnalisés.',
      linkCookies: 'dataprotection.html',
      linkPrivacy: 'dataprotection.html',
      linkTerms: 'terms.html',
      linkImprint: 'impressum.html',
    },
    en: {
      title: 'Cookie & Data Processing Consent',
      intro: 'We use cookies and similar technologies to ensure site functionality, analyse visits, and provide personalised content. Consent is voluntary and can be withdrawn at any time via the settings.',
      acceptAll: 'Accept all',
      settings: 'Settings or decline',
      save: 'Save',
      back: 'Back',
      essential: 'Essential',
      analytics: 'Analytics',
      marketing: 'Marketing',
      personalization: 'Personalisation',
      cookieInfo: 'Cookies',
      privacy: 'Privacy',
      terms: 'Terms',
      imprint: 'Imprint',
      essentialDesc: 'These cookies are necessary for the basic operation of the website.',
      analyticsDesc: 'Help us understand site usage and collect anonymous statistics.',
      marketingDesc: 'Used for personalised advertising and offers.',
      personalizationDesc: 'Enable personalised content and features.',
      linkCookies: 'dataprotection.html',
      linkPrivacy: 'dataprotection.html',
      linkTerms: 'terms.html',
      linkImprint: 'impressum.html',
    },
    pt: {
      title: 'Consentimento de cookies e tratamento de dados',
      intro: 'Utilizamos cookies e tecnologias semelhantes para garantir o funcionamento do site, analisar visitas e oferecer conteúdos personalizados. O consentimento é livre e pode ser retirado a qualquer momento através das definições.',
      acceptAll: 'Aceitar tudo',
      settings: 'Definições ou recusar',
      save: 'Guardar',
      back: 'Voltar',
      essential: 'Necessário',
      analytics: 'Análise',
      marketing: 'Marketing',
      personalization: 'Personalização',
      cookieInfo: 'Cookies',
      privacy: 'Proteção de dados',
      terms: 'Termos',
      imprint: 'Aviso legal',
      essentialDesc: 'Estes cookies são necessários para o funcionamento básico do site.',
      analyticsDesc: 'Ajuda a compreender a utilização do site e a recolher estatísticas anónimas.',
      marketingDesc: 'Utilizados para publicidade e ofertas personalizadas.',
      personalizationDesc: 'Permitem conteúdos e funcionalidades personalizados.',
      linkCookies: 'dataprotection.html',
      linkPrivacy: 'dataprotection.html',
      linkTerms: 'terms.html',
      linkImprint: 'impressum.html',
    },
  };

  function getLang() {
    const stored = (function () {
      try { return localStorage.getItem('site-language'); } catch (e) { return null; }
    })();
    const lang = (stored || document.documentElement.lang || 'lb').toLowerCase().split('-')[0];
    return I18N[lang] ? lang : 'lb';
  }

  function readConsent() {
    try {
      const consent = localStorage.getItem(STORAGE_KEY);
      return consent ? JSON.parse(consent) : null;
    } catch (e) {
      return null;
    }
  }

  function writeConsent(value, preferences) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
      localStorage.setItem(PREF_KEY, JSON.stringify(preferences));
    } catch (e) { /* ignore */ }
  }

  function allowBody() {
    document.documentElement.classList.remove('m75-consent-pending');
  }

  function blockBody() {
    document.documentElement.classList.add('m75-consent-pending');
  }

  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      html.m75-consent-pending, html.m75-consent-pending body {
        overflow: hidden;
      }
      html.m75-consent-pending body > *:not(#m75-consent-overlay) {
        visibility: hidden;
      }
      #m75-consent-overlay {
        position: fixed;
        inset: 0;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: rgba(0,0,0,0.55);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      }
      #m75-consent-card {
        background: #fff;
        color: #222;
        border-radius: 1rem;
        width: min(640px, 100%);
        max-height: 90vh;
        overflow-y: auto;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        padding: 1.75rem;
      }
      #m75-consent-card h2 {
        margin: 0 0 0.75rem;
        font-size: 1.35rem;
        text-align: center;
        color: #111;
      }
      .m75-consent-logo {
        display: block;
        max-width: 140px;
        max-height: 70px;
        margin: 0 auto 1rem;
        object-fit: contain;
      }
      #m75-consent-card p {
        margin: 0 0 1rem;
        font-size: 0.95rem;
        line-height: 1.5;
      }
      .m75-consent-actions {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        margin-bottom: 1rem;
      }
      .m75-consent-actions button {
        border: 0;
        border-radius: 0.6rem;
        padding: 0.85rem 1rem;
        font-size: 1rem;
        cursor: pointer;
        font-weight: 600;
        transition: filter 0.15s ease, transform 0.05s ease;
      }
      .m75-consent-actions button:hover {
        filter: brightness(0.95);
      }
      .m75-consent-actions button:active {
        transform: translateY(1px);
      }
      #m75-btn-accept {
        background: #4a9fd4;
        color: #fff;
      }
      #m75-btn-settings {
        background: #9aa5b1;
        color: #fff;
      }
      #m75-btn-save {
        background: #4a9fd4;
        color: #fff;
      }
      #m75-btn-back {
        background: #e2e8f0;
        color: #334155;
      }
      .m75-consent-links {
        text-align: center;
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.75rem;
      }
      .m75-consent-links a {
        color: #4a9fd4;
        text-decoration: none;
        margin: 0 0.35rem;
      }
      .m75-consent-links a:hover { text-decoration: underline; }
      .m75-consent-categories {
        display: none;
        margin-top: 1rem;
      }
      .m75-consent-categories.open {
        display: block;
      }
      .m75-consent-category {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid #e2e8f0;
      }
      .m75-consent-category:last-child { border-bottom: 0; }
      .m75-consent-category-info strong {
        display: block;
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
      }
      .m75-consent-category-info span {
        font-size: 0.82rem;
        color: #64748b;
      }
      .m75-consent-toggle {
        position: relative;
        width: 46px;
        height: 26px;
        flex-shrink: 0;
      }
      .m75-consent-toggle input {
        opacity: 0;
        width: 0;
        height: 0;
      }
      .m75-consent-toggle-slider {
        position: absolute;
        cursor: pointer;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: #cbd5e1;
        border-radius: 26px;
        transition: .2s;
      }
      .m75-consent-toggle-slider:before {
        position: absolute;
        content: "";
        height: 20px;
        width: 20px;
        left: 3px;
        bottom: 3px;
        background-color: white;
        border-radius: 50%;
        transition: .2s;
      }
      .m75-consent-toggle input:checked + .m75-consent-toggle-slider {
        background-color: #4a9fd4;
      }
      .m75-consent-toggle input:checked + .m75-consent-toggle-slider:before {
        transform: translateX(20px);
      }
      .m75-consent-toggle input:disabled + .m75-consent-toggle-slider {
        opacity: 0.6;
        cursor: not-allowed;
      }
      @media (min-width: 480px) {
        .m75-consent-actions { flex-direction: row; }
        .m75-consent-actions button { flex: 1; }
      }
    `;
    document.head.appendChild(style);
  }

  function createOverlay() {
    const lang = getLang();
    const t = I18N[lang];
    const existing = document.getElementById('m75-consent-overlay');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.id = 'm75-consent-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'm75-consent-title');

    const card = document.createElement('div');
    card.id = 'm75-consent-card';

    const logo = document.createElement('img');
    logo.className = 'm75-consent-logo';
    logo.alt = 'Mersch75';
    logo.src = 'assets/Logo%20Weissen%20Hannergrond%20Mersch%20Applestyle%202026.png';

    const title = document.createElement('h2');
    title.id = 'm75-consent-title';
    title.textContent = t.title;

    const intro = document.createElement('p');
    intro.textContent = t.intro;

    const actions = document.createElement('div');
    actions.className = 'm75-consent-actions';

    const acceptBtn = document.createElement('button');
    acceptBtn.id = 'm75-btn-accept';
    acceptBtn.textContent = t.acceptAll;
    acceptBtn.addEventListener('click', () => {
      writeConsent({ analytics: true, marketing: true, personalization: true, timestamp: Date.now() }, { analytics: true, marketing: true, personalization: true });
      closeOverlay();
    });

    const settingsBtn = document.createElement('button');
    settingsBtn.id = 'm75-btn-settings';
    settingsBtn.textContent = t.settings;
    settingsBtn.addEventListener('click', () => {
      categories.classList.add('open');
      intro.style.display = 'none';
      acceptBtn.style.display = 'none';
      settingsBtn.style.display = 'none';
      saveBtn.style.display = 'block';
      backBtn.style.display = 'block';
    });

    const saveBtn = document.createElement('button');
    saveBtn.id = 'm75-btn-save';
    saveBtn.textContent = t.save;
    saveBtn.style.display = 'none';
    saveBtn.addEventListener('click', () => {
      const analytics = document.getElementById('m75-cat-analytics').checked;
      const marketing = document.getElementById('m75-cat-marketing').checked;
      const personalization = document.getElementById('m75-cat-personalization').checked;
      writeConsent({ analytics, marketing, personalization, timestamp: Date.now() }, { analytics, marketing, personalization });
      closeOverlay();
    });

    const backBtn = document.createElement('button');
    backBtn.id = 'm75-btn-back';
    backBtn.textContent = t.back;
    backBtn.style.display = 'none';
    backBtn.addEventListener('click', () => {
      categories.classList.remove('open');
      intro.style.display = 'block';
      acceptBtn.style.display = 'block';
      settingsBtn.style.display = 'block';
      saveBtn.style.display = 'none';
      backBtn.style.display = 'none';
    });

    actions.append(acceptBtn, settingsBtn, saveBtn, backBtn);

    function makeToggle(id, label, desc, checked, disabled) {
      const wrap = document.createElement('div');
      wrap.className = 'm75-consent-category';
      const info = document.createElement('div');
      info.className = 'm75-consent-category-info';
      const b = document.createElement('strong');
      b.textContent = label;
      const span = document.createElement('span');
      span.textContent = desc;
      info.append(b, span);
      const toggle = document.createElement('label');
      toggle.className = 'm75-consent-toggle';
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.id = id;
      input.checked = checked;
      if (disabled) input.disabled = true;
      const slider = document.createElement('span');
      slider.className = 'm75-consent-toggle-slider';
      toggle.append(input, slider);
      wrap.append(info, toggle);
      return wrap;
    }

    const categories = document.createElement('div');
    categories.className = 'm75-consent-categories';
    categories.append(
      makeToggle('m75-cat-essential', t.essential, t.essentialDesc, true, true),
      makeToggle('m75-cat-analytics', t.analytics, t.analyticsDesc, true, false),
      makeToggle('m75-cat-marketing', t.marketing, t.marketingDesc, false, false),
      makeToggle('m75-cat-personalization', t.personalization, t.personalizationDesc, false, false)
    );

    const links = document.createElement('div');
    links.className = 'm75-consent-links';
    links.innerHTML = [
      `<a href="${t.linkCookies}">${t.cookieInfo}</a>`,
      `<a href="${t.linkPrivacy}">${t.privacy}</a>`,
      `<a href="${t.linkTerms}">${t.terms}</a>`,
      `<a href="${t.linkImprint}">${t.imprint}</a>`,
    ].join(' &bull; ');

    card.append(logo, title, intro, actions, categories, links);
    overlay.appendChild(card);
    document.body.appendChild(overlay);

    function closeOverlay() {
      overlay.remove();
      allowBody();
      document.cookie = 'm75-consent=1; path=/; max-age=31536000; SameSite=Lax';
    }

    return overlay;
  }

  blockBody();
  injectStyles();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    const consent = readConsent();
    if (consent) {
      allowBody();
      return;
    }
    createOverlay();
  }
})();
