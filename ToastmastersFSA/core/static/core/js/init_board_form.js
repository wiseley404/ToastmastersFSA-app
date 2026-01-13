function initBoardForm() {
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');

    if (!startDateInput || !endDateInput) return;

    function updateConstraints() {
        if (startDateInput.value) {
            endDateInput.min = startDateInput.value;
        }
    }

    startDateInput.addEventListener('change', updateConstraints);
    updateConstraints();
}