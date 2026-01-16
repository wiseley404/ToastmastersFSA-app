const buttons = document.querySelectorAll('.toggle-text-btn');
const sections = document.querySelectorAll('.section-content');

buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    buttons.forEach(b => b.classList.remove('active'));
    sections.forEach(s => s.style.display = 'none');
    
    // Activate the button clicked
    btn.classList.add('active');
    
    // Show the appropriate section
    const target = btn.getAttribute('data-target');
    document.getElementById(target).style.display = 'block';
    
    // Enlever le "-section" pour l'URL
    const sectionName = target.replace('-section', '');
    const url = new URL(window.location);
    url.searchParams.set('section', sectionName);
    window.history.replaceState({}, '', url);
  });
});