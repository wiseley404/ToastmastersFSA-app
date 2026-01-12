function initEvaluation() {
    console.log('Init evaluation');
    
    fetch('/speechs/evaluations/get-all-criteria/')
        .then(r => r.json())
        .then(data => displayCriteria(data.criteria))
        .catch(err => console.error('Criteria error:', err));

    fetch('/speechs/evaluations/get-all-members/')
        .then(r => r.json())
        .then(data => displayMembers(data.members))
        .catch(err => console.error('Members error:', err));
    
    // Délégation d'événements
    document.addEventListener('change', function(e) {
        if (e.target.id === 'eval-type') {
            console.log('Type changed:', e.target.value);
            if (!e.target.value) {
                // Réinitialise avec TOUS les critères
                fetch('/speechs/evaluations/get-all-criteria/')
                    .then(r => r.json())
                    .then(data => displayCriteria(data.criteria));
                return;
            }
            
            fetch(`/speechs/evaluations/get-criteria/${e.target.value}/`)
                .then(r => r.json())
                .then(data => displayCriteria(data.criteria));
        }
        
        if (e.target.id === 'eval-meeting') {
            console.log('Meeting changed:', e.target.value);
            if (!e.target.value) {
                // Réinitialise avec TOUS les membres
                fetch('/speechs/evaluations/get-all-members/')
                    .then(r => r.json())
                    .then(data => displayMembers(data.members));
                return;
            }
            
            fetch(`/speechs/evaluations/get-meeting-members/${e.target.value}/`)
                .then(r => r.json())
                .then(data => displayMembers(data.members));
        }
    });

    document.addEventListener('submit', function(e) {
        if (e.target.id === 'eval-config-form') {
            e.preventDefault();
            
            const criteria = Array.from(document.querySelectorAll('input[name="criteria"]:checked')).map(c => c.value);
            const members = Array.from(document.querySelectorAll('input[name="members"]:checked')).map(m => m.value);
            const meeting = document.getElementById('eval-meeting').value;
            const type = document.getElementById('eval-type').value;
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch('/speechs/evaluations/generate-table/', {
                method: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                body: JSON.stringify({
                    meeting_id: meeting,
                    evaluation_type_id: type,
                    criteria_ids: criteria,
                    member_ids: members
                })
            })
            .then(r => r.json())
            .then(data => {
                closePopup();
                location.reload();
            });
        }
    });
    
}

function displayCriteria(criteria) {
    const list = document.getElementById('criteria-list');
    if (!list) return;
    list.innerHTML = '';
    criteria.forEach(c => {
        list.innerHTML += `<label><input type="checkbox" name="criteria" value="${c.id}"> ${c.name}</label><br>`;
    });
}

function displayMembers(members) {
    const list = document.getElementById('members-list');
    if (!list) return;
    list.innerHTML = '';
    members.forEach(m => {
        list.innerHTML += `<label><input type="checkbox" name="members" value="${m.id}"> ${m.name}</label><br>`;
    });
}