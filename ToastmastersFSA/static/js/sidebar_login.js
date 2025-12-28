document.addEventListener('DOMContentLoaded', ()=> {
    const sidebar = document.querySelector('.sidebar');
    const navbar  = document.querySelector('.navbar');
    const closeBtn = document.querySelector('.sidebar-close-btn');
    const openBtn  = document.querySelector('.sidebar-open-btn');

        // Desktop screen
    if (window.innerWidth >= 1025) {
        sidebar.classList.remove('close'); 
        document.documentElement.classList.remove('sidebar-closed');
    }
    

    function updateNavbar() {
        if (!navbar) return;
        if (sidebar.classList.contains('close')) {
        navbar.style.left = '40px';
        navbar.style.width = 'calc(100% - 40px)';
        } else {
        navbar.style.left = '230px';
        navbar.style.width = 'calc(100% - 230px)';
        }
    }

    
    function applySavedState() {
        if (!sidebar) return;
        sidebar.style.transition = 'none';
        const saved = localStorage.getItem('sidebarClosed');
        const closed = saved === '1';
        sidebar.classList.toggle('close', closed);
        navbar.style.transition = 'none';

        updateNavbar();

        setTimeout(() => {
        navbar.style.transition = 'left 0.3s ease, width 0.3s ease';
        }, 50);

        requestAnimationFrame(() => { sidebar.style.transition = ''; });
    }


    function setClosed(closed) {
        sidebar.classList.toggle('close', closed);
        localStorage.setItem('sidebarClosed', closed ? '1' : '0');
        updateNavbar();
    }
    closeBtn?.addEventListener('click', (e) => {
        e.preventDefault(); e.stopPropagation();
        setClosed(true);
    });

    openBtn?.addEventListener('click', (e) => {
        e.preventDefault(); e.stopPropagation();
        setClosed(false);
    });

    // Previous state on loading..
    applySavedState();


    const hamburger = document.querySelector('.hamburger');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    function openMobileSidebar() {
        sidebar.classList.add('open');
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
        const sidebarOpenBtn = sidebar.querySelector('.sidebar-open-btn');
        if (sidebarOpenBtn) sidebarOpenBtn.style.display = 'none';
        
        sidebar.querySelector('.sidebar-title').style.display = 'block';
        sidebar.querySelector('.sidebar-close-btn').style.display = 'flex';
    }


    function closeMobileSidebar() {
        sidebar.classList.remove('open');
        overlay.style.display = '';
        document.body.style.overflow = '';
        const sidebarOpenBtn = sidebar.querySelector('.sidebar-open-btn');
        if (sidebarOpenBtn) sidebarOpenBtn.style.display = '';
        
        sidebar.querySelector('.sidebar-title').style.display = '';
        sidebar.querySelector('.sidebar-close-btn').style.display = '';
    }

    // On mobile
    hamburger?.addEventListener('click', () => {
        if (sidebar.classList.contains('open')) closeMobileSidebar();
        else openMobileSidebar();
    });

    overlay?.addEventListener('click', closeMobileSidebar);

    const closeMobileBtn = document.querySelector('.sidebar-close-btn');

    closeMobileBtn?.addEventListener('click', () => {
        closeMobileSidebar();
    });
});