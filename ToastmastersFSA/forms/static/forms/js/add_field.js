document.querySelectorAll(".add-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();
    const urls = btn.dataset.createUrl;

    fetch(`${urls}`)
      .then(response => response.text())
      .then(html => openPopup(html)) 
      .then(() => {
            const popupForm = document.querySelector('.popup-form');
          initAddOption(popupForm);
      });
  });
});


function initAddOption(element) {
        const typeSelect = element.querySelector('#id_type')
        const optionsDisplay = element.querySelector('#optionsDisplay')
        const optionsContainer = element.querySelector('#optionsContainer')
        const option = element.querySelector('#addOption')

        typeSelect.addEventListener('change', function(){
            const value = this.value;
            if (['select', 'radio', 'checkbox'].includes(value)){
                optionsDisplay.style.display = 'block';
            }else{
                optionsDisplay.style.display = 'none';
                optionsContainer.innerHTML = '';
            }
        });

        function addOption(){
            const div = document.createElement('div')
            div.style.marginBottom = '5px';
            div.innerHTML = `
                <input type='text' name='options' placeholder='Option' maxlenght='50' required>
                <button type='button' class='removebutton'><i class="fas fa-trash"></i></button>
            `;
            optionsContainer.appendChild(div);

            div.querySelector('.removebutton').addEventListener('click', function(){
                div.remove();
            });
        }

        option.addEventListener('click', function(){
            addOption();
        });
}