(function initSiteConfig() {
    const existing = window.M75_CONFIG || {};

    window.M75_CONFIG = Object.freeze({
        WEB3FORMS_ENDPOINT: 'https://api.web3forms.com/submit',
        API_BASE: 'https://api.mersch75.lu',
        ...existing
    });
})();
