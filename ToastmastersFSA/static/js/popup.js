// static/js/popup.js

function openPopup(htmlContent) {
    document.getElementById("popup-body").innerHTML = htmlContent;
    document.getElementById("popup").style.display = "flex";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

document.addEventListener('DOMContentLoaded', function() {
    
    // Fermer popup en cliquant à l'extérieur (mobile)
    const popupOverlay = document.querySelector('.popup-overlay');
    if (popupOverlay) {
        popupOverlay.addEventListener('click', (e) => {
            if (window.innerWidth <= 767 && e.target === popupOverlay) {
                closePopup();
            }
        });
    }
    
    // Ouvrir le popup (create, edit, delete, show)
    document.addEventListener('click', function(e) {
        const addBtn = e.target.closest('[data-create-url]');
        const editBtn = e.target.closest('[data-edit-url]');
        const deleteBtn = e.target.closest('[data-delete-url]');
        const showBtn = e.target.closest('[data-show-url]');
        
        const target = addBtn || editBtn || deleteBtn || showBtn;
        if (!target) return;
        
        e.preventDefault();
        e.stopImmediatePropagation();  // ← empêche le <a> de naviguer
        
        const url = addBtn ? addBtn.dataset.createUrl : 
                    editBtn ? editBtn.dataset.editUrl : 
                    deleteBtn ? deleteBtn.dataset.deleteUrl :
                    showBtn.dataset.showUrl;
        
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.querySelector('#popup-body').innerHTML = html;
                document.querySelector('#popup').style.display = 'flex';
                initPopupForms();
            })
            .catch(error => console.error('Erreur fetch:', error));
    });
    
    // Soumettre le form en AJAX
    let isSubmitting = false;  // Flag anti-double
    
    document.addEventListener('submit', function(e) {
        const form = e.target.closest('#popup-body form');
        if (!form) return;
        
        if (form.action.includes('delete') || form.action.includes('remove')) return;
        
        if (isSubmitting) return;  // Évite double soumission
        isSubmitting = true;
        
        e.preventDefault();
        e.stopImmediatePropagation();
        
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            isSubmitting = false;
            if (data.success) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url; 
                } else {
                    location.reload();
                }
            } else {
                document.querySelector('#popup-body').innerHTML = data.html;
                initPopupForms();
            }
        })
        .catch(error => {
            isSubmitting = false;
            console.error('Erreur submit:', error);
        });
    });
    
});

function initPopupForms() {
    if (typeof initMeetingForm === 'function') initMeetingForm();
    if (typeof initBoardForm === 'function') initBoardForm();
    if (typeof initSpeechForm === 'function') initSpeechForm();
    if (typeof initEmailListForm === 'function') initEmailListForm();
    if (typeof initAddOption === 'function') initAddOption();
}