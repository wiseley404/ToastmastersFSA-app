function initMeetingForm() {
    const dateInput = document.getElementById('id_date');
    const startTimeInput = document.getElementById('id_start_time');
    const endTimeInput = document.getElementById('id_end_time');

    if (!dateInput || !startTimeInput || !endTimeInput) return;

    const today = new Date().toLocaleDateString('en-CA');
    const form = dateInput.closest('form');
    const isEdit = form && form.action.includes('edit');

    function getNowTime() {
        const now = new Date();
        return now.toTimeString().slice(0, 5); 
    }

    function updateConstraints() {
        dateInput.min = today;

        if (isEdit) {
            startTimeInput.removeAttribute('min');
        } else {
            if (dateInput.value === today) {
                startTimeInput.min = getNowTime();
            } else {
                startTimeInput.min = '00:00';
            }
        }

        if (startTimeInput.value) {
            endTimeInput.min = startTimeInput.value;
        } else {
            endTimeInput.min = '00:00';
        }
    }

    dateInput.addEventListener('change', updateConstraints);
    startTimeInput.addEventListener('change', updateConstraints);

    updateConstraints(); 
}