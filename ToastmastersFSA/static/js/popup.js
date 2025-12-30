function openPopup(htmlContent) {
  document.getElementById("popup-body").innerHTML = htmlContent;
  document.getElementById("popup").style.display = "flex";
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

document.addEventListener('DOMContentLoaded', () => {
  const popupOverlay = document.querySelector('.popup-overlay');
  
  if (popupOverlay) {
    popupOverlay.addEventListener('click', (e) => {
      
      if (window.innerWidth <= 767 && e.target === popupOverlay) {
        closePopup();
      }
    });
  }
});
