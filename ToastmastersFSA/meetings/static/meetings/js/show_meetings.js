function filterMeetings() {
    const selected = document.getElementById('monthFilter').value;
    document.querySelectorAll('.meeting-card').forEach(card => {
        if (selected === 'all' || card.dataset.month === selected) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

document.getElementById('monthFilter').addEventListener('change', filterMeetings);
window.addEventListener('load', filterMeetings);


//menu-action
document.querySelectorAll('.menu-btn').forEach(btn => {
btn.addEventListener('click', function(e) {
    e.stopPropagation();
    document.querySelectorAll('.menu-dropdown').forEach(d => d.style.display = 'none');
    this.nextElementSibling.style.display = 'block';
});
});

document.addEventListener('click', () => {
    document.querySelectorAll('.menu-dropdown').forEach(d => d.style.display = 'none');
});

// CONFIG 
const itemsPerPage = 10;
const cards = Array.from(document.querySelectorAll('.meeting-card')); 
const btnPrev = document.querySelector('.page-btn.prev');
const btnNext = document.querySelector('.page-btn.next');
const pageCount = document.querySelector('.page-count');

let currentPage = 1;
const totalPages = Math.ceil(cards.length / itemsPerPage);

// Show meetings for actual search
function renderPage() {
    cards.forEach(c => c.style.display = 'none');
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    cards.slice(start, end).forEach(c => {
        c.style.display = 'flex'; 
    });

    pageCount.textContent = currentPage;

    // Btn state
    btnPrev.disabled = (currentPage === 1);
    btnNext.disabled = (currentPage === totalPages);
}

// LISTENERS 
btnPrev.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderPage();
    }
});

btnNext.addEventListener('click', () => {
    if (currentPage < totalPages) {
        currentPage++;
        renderPage();
    }
});

renderPage();
