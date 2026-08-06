(function initializeContactForm() {
    const form = document.getElementById('contactForm');
    const submitButton = document.getElementById('contactSubmitBtn');
    const successBox = document.getElementById('contactSuccess');
    const errorBox = document.getElementById('contactError');
    const resetButton = document.getElementById('contactResetBtn');
    const buttonDefaultHtml = submitButton ? submitButton.innerHTML : '';
    const web3FormsEndpoint = window.M75_CONFIG && window.M75_CONFIG.WEB3FORMS_ENDPOINT;

    if (!form || !submitButton || !successBox || !errorBox) {
        return;
    }

    if (!web3FormsEndpoint) {
        throw new Error('Konfigurationsfehler: WEB3FORMS_ENDPOINT fehlt.');
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';

        const formData = new FormData(form);
        const subjectUser = String(formData.get('subject_user') || '').trim();
        const firstname = String(formData.get('firstname') || '').trim();
        const lastname = String(formData.get('lastname') || '').trim();
        const fullName = [firstname, lastname].filter(Boolean).join(' ');

        formData.set('name', fullName);
        formData.set('subject', '[Mersch75 Contact] ' + subjectUser + ' - ' + fullName);

        try {
            const response = await fetch(web3FormsEndpoint, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (!data.success) {
                throw new Error('Send failed');
            }

            form.style.display = 'none';
            successBox.style.display = 'block';
            errorBox.style.display = 'none';
        } catch (error) {
            errorBox.style.display = 'block';
            submitButton.disabled = false;
            submitButton.innerHTML = buttonDefaultHtml;
        }
    });

    if (resetButton) {
        resetButton.addEventListener('click', () => {
            form.reset();
            form.style.display = 'block';
            successBox.style.display = 'none';
            errorBox.style.display = 'none';
            submitButton.disabled = false;
            submitButton.innerHTML = buttonDefaultHtml;
        });
    }
})();
