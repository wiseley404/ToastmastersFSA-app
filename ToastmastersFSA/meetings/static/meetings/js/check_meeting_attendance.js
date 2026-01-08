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
      <p>Etes-vous present a la reunion d'aujourd'hui: ${data.date} ?</p>
      <button onclick="confirmAttendance(${data.meeting_id}, true)">Présent</button>
      <button onclick="confirmAttendance(${data.meeting_id}, false)">Absent</button>
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