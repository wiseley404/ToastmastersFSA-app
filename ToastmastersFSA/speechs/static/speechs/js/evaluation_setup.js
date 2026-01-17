function initEvaluation() {

    const criteriaSelect = $('#criteria-select');
    const membersSelect = $('#members-select');

    // INIT SELECT2
    criteriaSelect.select2({
        width: '100%',
        placeholder: 'Sélectionner des critères...',
        allowClear: true,
        dropdownParent: $('#popup-body')
    });

    membersSelect.select2({
        width: '100%',
        placeholder: 'Sélectionner des membres...',
        allowClear: true,
        dropdownParent: $('#popup-body')
    });

    fetch('/speechs/evaluations/get-all-criteria/')
        .then(r => r.json())
        .then(data => updateCriteriaSelect(data.criteria));

    fetch('/speechs/evaluations/get-all-members/')
        .then(r => r.json())
        .then(data => updateMembersSelect(data.members));

    
    document.addEventListener('change', function(e) {
        if (e.target.id === 'eval-type') {
            console.log('Type changed:', e.target.value);
            if (!e.target.value) {
                fetch('/speechs/evaluations/get-all-criteria/')
                    .then(r => r.json())
                    .then(data => updateCriteriaSelect(data.criteria));
                return;
            }
            
            fetch(`/speechs/evaluations/get-criteria/${e.target.value}/`)
                .then(r => r.json())
                .then(data => updateCriteriaSelect(data.criteria));
        }
        
        if (e.target.id === 'eval-meeting') {
            console.log('Meeting changed:', e.target.value);
            if (!e.target.value) {
                fetch('/speechs/evaluations/get-all-members/')
                    .then(r => r.json())
                    .then(data => updateMembersSelect(data.members));
                return;
            }
            
            fetch(`/speechs/evaluations/get-meeting-members/${e.target.value}/`)
                .then(r => r.json())
                .then(data => updateMembersSelect(data.members));
        }
    });

    document.addEventListener('submit', function(e) {
        if (e.target.id === 'eval-config-form') {
            e.preventDefault();
            
            const meeting = document.getElementById('eval-meeting').value;
            const type = document.getElementById('eval-type').value;
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch('/speechs/evaluations/generate-table/', {
                method: 'POST',
                headers: {'X-CSRFToken': csrfToken,
                          'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    meeting_id: meeting,
                    evaluation_type_id: type,
                    criteria_ids: criteriaSelect.val(),
                    member_ids: membersSelect.val()
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

function updateCriteriaSelect(criteria) {
    const select = $('#criteria-select');
    select.empty();

    criteria.forEach(c => {
        select.append(new Option(c.name, c.id));
    });

    select.trigger('change');
}

function updateMembersSelect(members) {
    const select = $('#members-select');
    select.empty();

    members.forEach(m => {
        select.append(new Option(m.name, m.id));
    });

    select.trigger('change');
}
