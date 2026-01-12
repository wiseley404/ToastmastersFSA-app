document.addEventListener('click', function(e) {
    if (e.target.classList.contains('show-btn')) {
        e.preventDefault();
        const url = e.target.dataset.showUrl;
        
        fetch(url)
            .then(r => r.text())
            .then(html => openPopup(html));
    }
});