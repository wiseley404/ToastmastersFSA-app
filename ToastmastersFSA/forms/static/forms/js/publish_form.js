document.querySelectorAll(".push-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();
    const urls = btn.dataset.createUrl;

    fetch(`${urls}`)
      .then(response => response.text())
      .then(html => openPopup(html)); 
  });
});