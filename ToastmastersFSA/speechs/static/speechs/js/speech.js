function initSpeechForm() {
    const popupForm = document.querySelector('#popup-body form');
    if (!popupForm) return;
    
    initRoleSelect(popupForm);
    initFieldVisibility(popupForm);
}

function initRoleSelect(FormElement) {
    const meetingSelect = FormElement.querySelector('#id_meeting');
    const roleSelect = FormElement.querySelector('#id_role');
    const actionBtn = document.querySelector('[data-roles]');
    
    if (!meetingSelect || !roleSelect || !actionBtn) return;
    
    const rolesUrl = actionBtn.dataset.roles;

    meetingSelect.addEventListener('change', function() {
        const meetingId = this.value;
        fetch(`${rolesUrl}?meeting=${meetingId}`)
            .then(response => response.json())
            .then(data => {
                roleSelect.innerHTML = '<option value="">Choisir un rôle disponible</option>';
                data.roles.forEach(role => {
                    const option = document.createElement('option');
                    option.value = role.id;
                    option.text = role.title;
                    roleSelect.add(option);
                });
            });
    });
}

function initFieldVisibility(form) {
    const roleSelect = form.querySelector('#id_role');
    const titleField = form.querySelector('#title-field');
    const themeField = form.querySelector('#theme-field');
    const highlightWordField = form.querySelector('#highlight_word-field');

    if (!roleSelect) return;

    function updateVisibility() {
        const roleText = roleSelect.options[roleSelect.selectedIndex]?.text || '';
        if (titleField) titleField.style.display = (roleText === "Discours préparé") ? "block" : "none";
        if (themeField) themeField.style.display = (roleText === "Meneur(se) des improvisations") ? "block" : "none";
        if (highlightWordField) highlightWordField.style.display = (roleText === "Grammairien(ne)") ? "block" : "none";
    }

    roleSelect.addEventListener('change', updateVisibility);
    updateVisibility();
}