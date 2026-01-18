// Image slider
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    if (slides[index]) {
        slides[index].classList.add('active');
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

// Change slide every 5 seconds
if (slides.length > 0) {
    setInterval(nextSlide, 5000);
}

// Scroll to top on page load
window.addEventListener('load', () => {
    window.scrollTo(0, 0);
    const formSection = document.querySelector('.form-section');
    if (formSection) {
        formSection.scrollTop = 0;
    }
});