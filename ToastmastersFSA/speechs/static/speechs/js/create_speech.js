document.querySelectorAll(".action-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();
    const discoursUrl = btn.dataset.createUrl;

    fetch(`${discoursUrl}`)
      .then(response => response.text())
      .then(html => openPopup(html)) 
      .then(() => {
            const popupForm = document.querySelector('.popup-form');
          initRoleSelect(popupForm);
          initFieldVisibility(popupForm);
      });

  });
});

function initRoleSelect (FormElement) {
    const meetingSelect = FormElement.querySelector('#id_reunion');
    const roleSelect = FormElement.querySelector('#id_role');
    const rolesUrl = document.querySelector('.action-btn').dataset.roles;

    meetingSelect.addEventListener('change', function() {
        const meetingId = this.value;
        fetch(`${rolesUrl}?reunion=${meetingId}`)
            .then(response => response.json())
            .then(data => {
                roleSelect.innerHTML = '<option value="">--- Choisir un rôle disponible ---</option>';
                data.roles.forEach(role => {
                    const option = document.createElement('option');
                    option.value = role.id;
                    option.text = role.nom;
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

    function updateVisibility() {
        const roleText = roleSelect.options[roleSelect.selectedIndex].text;
        titleField.style.display = (roleText === "Discours préparé") ? "block" : "none";
        themeField.style.display = (roleText === "Meneur(se) des improvisations") ? "block" : "none";
        highlightWordField.style.display = (roleText === "Grammairien(ne)") ? "block" : "none";
    }

    roleSelect.addEventListener('change', updateVisibility);
    updateVisibility();
}


