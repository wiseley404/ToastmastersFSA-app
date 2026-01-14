function initEmailScheduledForm() {

    // Contrainte date
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');

    if (startDateInput && endDateInput) {
        function updateDateConstraints() {
            if (startDateInput.value) {
                endDateInput.min = startDateInput.value;
            }
        }

        startDateInput.addEventListener('change', updateDateConstraints);
        updateDateConstraints();
    }

    // Select2 pour emails (mode tags)
    const emailsInput = document.getElementById('id_to_emails');
    if (emailsInput) {
        const container = emailsInput.parentElement;
        const select = document.createElement('select');
        select.id = 'id_to_emails_select';
        select.multiple = true;
        select.style.width = '100%';
        
        if (emailsInput.value) {
            emailsInput.value.split('\n').forEach(email => {
                if (email.trim()) {
                    const option = new Option(email.trim(), email.trim(), true, true);
                    select.appendChild(option);
                }
            });
        }
        
        emailsInput.style.display = 'none';
        container.appendChild(select);
        
        $('#id_to_emails_select').select2({
            tags: true,
            tokenSeparators: [',', ' ', '\n'],
            placeholder: 'Entrez des emails...',
            allowClear: true,
            createTag: function(params) {
                const term = params.term.trim();
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                
                if (term === '' || !emailRegex.test(term)) {
                    return null;
                }
                return {
                    id: term,
                    text: term,
                    newTag: true
                };
            }
        });
        
        $('#id_to_emails_select').closest('form').on('submit', function() {
            const emails = $('#id_to_emails_select').val() || [];
            emailsInput.value = emails.join('\n');
        });
    }

    // Select2 pour profiles
    const profilesSelect = document.getElementById('id_to_profiles');
    if (profilesSelect) {
        $('#id_to_profiles').select2({
            width: '100%',
            placeholder: 'Choisissez des membres...',
            allowClear: true
        });
    }

    // Select2 pour listes
    const listsSelect = document.getElementById('id_to_lists');
    if (listsSelect) {
        $('#id_to_lists').select2({
            width: '100%',
            placeholder: 'Choisissez des listes de diffusion...',
            allowClear: true
        });
    }
}
