Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
Chart.defaults.color = '#888';

// Membres actifs
const membersCtx = document.getElementById('membersChart').getContext('2d');
new Chart(membersCtx, {
    type: 'line',
    data: {
        labels: chartData.membersLabels,
        datasets: [{
            label: 'Membres actifs',
            data: chartData.membersData,
            borderColor: '#007BFF',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#007BFF',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4
        }, {
            label: 'Nouveaux membres',
            data: chartData.newMembersData,
            borderColor: '#28a745',
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0.4,
            pointBackgroundColor: '#28a745',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: '#f0f0f0'
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});

// Taux de présence
const attendanceCtx = document.getElementById('attendanceChart').getContext('2d');
new Chart(attendanceCtx, {
    type: 'line',
    data: {
        labels: chartData.attendanceLabels,
        datasets: [{
            label: 'Taux de présence (%)',
            data: chartData.attendanceData,
            borderColor: '#6f42c1',
            backgroundColor: 'rgba(111, 66, 193, 0.1)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#6f42c1',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: {
                    color: '#f0f0f0'
                },
                ticks: {
                    callback: function(value) {
                        return value + '%';
                    }
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});

// Réunions par mois
const meetingsCtx = document.getElementById('meetingsChart').getContext('2d');
new Chart(meetingsCtx, {
    type: 'bar',
    data: {
        labels: chartData.meetingsLabels,
        datasets: [{
            label: 'Réunions',
            data: chartData.meetingsData,
            backgroundColor: '#28a745',
            borderRadius: 6,
            barThickness: 32
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: '#f0f0f0'
                },
                ticks: {
                    stepSize: 1
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});