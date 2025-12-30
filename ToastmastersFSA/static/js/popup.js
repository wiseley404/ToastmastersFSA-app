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

    let startY = 0;
    let currentY = 0;
    
    const popupContent = document.querySelector('.popup-content');
    
    popupContent?.addEventListener('touchstart', (e) => {
    startY = e.touches[0].clientY;
    popupContent.style.transition = 'none'; 
    });

    popupContent?.addEventListener('touchmove', (e) => {
    currentY = e.touches[0].clientY;
    const deltaY = currentY - startY;
    
    if (deltaY > 0) {
        popupContent.style.transform = `translateY(${deltaY})`;
    }
    });

    popupContent?.addEventListener('touchend', (e) => {
    const deltaY = currentY - startY;
    
    if (deltaY > 100 && window.innerWidth <= 767) {
        closePopup(); 
    } else {
        popupContent.style.transition = 'transform 0.3s ease';
        popupContent.style.transform = 'translateY(0)';
    }
    });

});
