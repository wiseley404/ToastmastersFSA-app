document.addEventListener('DOMContentLoaded', function() {
    
    document.addEventListener('click', function(e) {
        const addBtn = e.target.closest('[data-create-url]');
        const editBtn = e.target.closest('[data-edit-url]');
        const deleteBtn = e.target.closest('[data-delete-url]');
        
        const target = addBtn || editBtn || deleteBtn;
        if (!target) return;
        
        e.preventDefault();
        const url = addBtn ? addBtn.dataset.createUrl : 
                    editBtn ? editBtn.dataset.editUrl : 
                    deleteBtn.dataset.deleteUrl;
        
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.querySelector('#popup-body').innerHTML = html;
                document.querySelector('#popup').style.display = 'flex';
            })
            .catch(error => console.error('Erreur fetch:', error));
    });
    
    document.addEventListener('submit', function(e) {
        const form = e.target.closest('form[action*="board"]');
        if (!form) return;
        
        if (form.action.includes('remove')) return;
        
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
                location.reload();
            } else {
                document.querySelector('#popup-body').innerHTML = data.html;
            }
        })
        .catch(error => console.error('Erreur submit:', error));
    });
    
});