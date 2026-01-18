// Tab switching (pour authentication.html seulement)
const tabs = document.querySelectorAll('.auth-tab');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;
        
        // Redirect to appropriate URL
        if (targetTab === 'login') {
            window.location.href = "/accounts/login/";
        } else if (targetTab === 'signup') {
            window.location.href = "/accounts/signup/";
        }
    });
});