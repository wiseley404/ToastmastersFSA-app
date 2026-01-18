fetch('/meetings/check-attendance/')
  .then(r => r.json())
  .then(data => {
    if (data.meeting_id) {
      showAttendancePopup(data);
    }
  });

function showAttendancePopup(data) {
  const html = `
    <div class="popup-body">
      <h2>Confirmez votre présence</h2>
      <p>Etes-vous présent(e) à notre reunion actuellement ?</p>
      <button onclick="confirmAttendance(${data.meeting_id}, true)" 
          style="padding: 0.5rem 1rem; border: none; border-radius: 6px;
                cursor: pointer; font-weight: bold;  background-color: #007BFF;>
        Présent(e)
      </button>

      <button onclick="confirmAttendance(${data.meeting_id}, false)" 
          style="padding: 0.5rem 1rem; border: 2px solid #007BFF; border-radius: 6px;
            cursor: pointer; font-weight: bold; background-color: #fff; color: #007BFF;">
        Absent(e)
      </button>
    </div>
  `;
  openPopup(html);
}

function confirmAttendance(meeting_id, is_present) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  fetch(`/meetings/${meeting_id}/confirm-attendance/`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrfToken},
    body: JSON.stringify({is_present})
  })
  .then(() => closePopup());
}