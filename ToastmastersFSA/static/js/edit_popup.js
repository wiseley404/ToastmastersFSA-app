document.querySelectorAll(".edit-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();
    const urls = btn.dataset.editUrl;

    fetch(`${urls}`)
      .then(response => response.text())
      .then(html => openPopup(html)); 
  });
});

