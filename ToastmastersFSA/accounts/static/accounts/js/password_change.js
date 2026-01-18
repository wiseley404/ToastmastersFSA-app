function initPasswordChangeForm() {
    const form = document.querySelector('#popup-body form[action*="password_change"]');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                closePopup();
                // Optionnel: reload la page ou rediriger
                window.location.href = data.redirect_url || window.location.href;
            } else {
                // Afficher les erreurs dans le popup
                let errorHtml = '<div style="color: red; margin-bottom: 10px;">';
                for (let field in data.errors) {
                    errorHtml += `<p>${data.errors[field]}</p>`;
                }
                errorHtml += '</div>';
                form.insertAdjacentHTML('afterbegin', errorHtml);
            }
        })
        .catch(error => console.error('Erreur:', error));
    });
}