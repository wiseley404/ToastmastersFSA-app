function initEmailListForm() {
    const membersSelect = document.getElementById('id_members');
    if (!membersSelect) return;
    
    $('#id_members').select2({
        width: '100%',
        placeholder: 'Rechercher des membres...',
        allowClear: true,
        dropdownParent: $('#popup-body'),
    });
}