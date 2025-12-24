document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('progressionChart').getContext('2d');
    const labels = window.dashboardData.labels;
    const data = {
        labels: labels,
        datasets: [
        {
            label: 'Pertinence',
            data: window.dashboardData.dataPertinence,
            borderColor: 'rgba(37, 99, 235, 1)',
            backgroundColor: 'rgba(37, 99, 235, 0.2)',
            fill: false,
            tension: 0.3,
        },
        {
            label: 'G. du temps',
            data: window.dashboardData.dataTemps,
            borderColor: 'rgba(16, 185, 129, 1)',
            backgroundColor: 'rgba(16, 185, 129, 0.2)',
            fill: false,
            tension: 0.3,
        },
        {
            label: 'Eloquence',
            data: window.dashboardData.dataEloquence,
            borderColor: 'rgba(220, 38, 38, 1)',
            backgroundColor: 'rgba(220, 38, 38, 0.2)',
            fill: false,
            tension: 0.3,
        },
        {
            label: 'Structure',
            data: window.dashboardData.dataStructure,
            borderColor: 'rgba(234, 179, 8, 1)',
            backgroundColor: 'rgba(234, 179, 8, 0.2)',
            fill: false,
            tension: 0.3,
        },
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
        responsive: true,
        interaction: { mode: 'index', intersect: false },
        stacked: false,
        plugins: { legend: { position: 'top' }},
        scales: { y: { beginAtZero: true, max: 100 }}
        }
    };

    new Chart(ctx, config);
});
