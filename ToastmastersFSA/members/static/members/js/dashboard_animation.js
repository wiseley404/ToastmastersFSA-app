document.addEventListener('DOMContentLoaded', () => {
    function initSlider(containerSelector, prevBtnId, nextBtnId) {
        const container = document.querySelector(containerSelector);
        if (!container) return;

        const slides = container.querySelectorAll('.slide');
        let current = 0;

        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.classList.toggle('active', i === index);
            });
            current = index;
        }

        function nextSlide() {
            const nextIndex = (current + 1) % slides.length;
            showSlide(nextIndex);
        }

        // auto défilement sans pause
        let slideInterval = setInterval(nextSlide, 3000);

        // boutons
        const prevBtn = document.getElementById(prevBtnId);
        const nextBtn = document.getElementById(nextBtnId);

        if (prevBtn) {
            prevBtn.onclick = () => {
                clearInterval(slideInterval);
                current = (current - 1 + slides.length) % slides.length;
                showSlide(current);
                slideInterval = setInterval(nextSlide, 3000);
            };
        }

        if (nextBtn) {
            nextBtn.onclick = () => {
                clearInterval(slideInterval);
                current = (current + 1) % slides.length;
                showSlide(current);
                slideInterval = setInterval(nextSlide, 3000);
            };
        }
    }

    // init pour chaque section
    initSlider('.derniere-seance-section', 'prev-btn', 'next-btn');
    initSlider('.prochaine-seance-section', 'prev-btn-prochaine', 'next-btn-prochaine');
});
