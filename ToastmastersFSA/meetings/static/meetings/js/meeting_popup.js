document.addEventListener('DOMContentLoaded', function() {
    
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#create-meeting-btn');
        const editLink = e.target.closest('a[href*="edit_meeting"], a.edit-btn');
        
        const target = btn || editLink;
        if (!target) return;
        
        e.preventDefault();
        const url = btn ? btn.dataset.createUrl : editLink.getAttribute('href');
        
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.querySelector('#popup-body').innerHTML = html;
                document.querySelector('#popup').style.display = 'flex';
                initMeetingForm();
            })
            .catch(error => console.error('Fetch error:', error));
    });
    

    document.addEventListener('submit', function(e) {
        const form = e.target.closest('form[action*="meeting"]');
        
        if (!form) return;
        
        if (form.action.includes('delete')) {
            return;
        }

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
                initMeetingForm();
            }
        })
        .catch(error => console.error('Submit error:', error));
    });
    
});