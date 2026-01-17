function initAddOption() {
    const popupForm = document.querySelector('#popup-body form');
    if (!popupForm) return;
    
    const typeSelect = popupForm.querySelector('#id_type');
    const optionsDisplay = popupForm.querySelector('#optionsDisplay');
    const optionsContainer = popupForm.querySelector('#optionsContainer');
    const addOptionBtn = popupForm.querySelector('#addOption');
    
    if (!typeSelect || !optionsDisplay || !optionsContainer || !addOptionBtn) return;

    typeSelect.addEventListener('change', function() {
        const value = this.value;
        if (['select', 'radio', 'checkbox'].includes(value)) {
            optionsDisplay.style.display = 'block';
        } else {
            optionsDisplay.style.display = 'none';
            optionsContainer.innerHTML = '';
        }
    });

    function addOption() {
        const div = document.createElement('div');
        div.style.marginBottom = '5px';
        div.innerHTML = `
            <input type='text' name='options' placeholder='Option' maxlength='50' required>
            <button type='button' class='removebutton'><i class="fas fa-trash"></i></button>
        `;
        optionsContainer.appendChild(div);

        div.querySelector('.removebutton').addEventListener('click', function() {
            div.remove();
        });
    }

    addOptionBtn.addEventListener('click', function() {
        addOption();
    });
}