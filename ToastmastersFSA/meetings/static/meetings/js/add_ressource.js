document.querySelectorAll(".action-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();

    fetch(`add/`)
      .then(response => response.text())
      .then(html => openPopup(html)); 
  });
});
