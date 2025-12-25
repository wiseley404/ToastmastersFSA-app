document.querySelectorAll(".delete-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();
    const urls = btn.dataset.deleteUrl;

    fetch(`${urls}`)
      .then(response => response.text())
      .then(html => openPopup(html)); 
  });
});
