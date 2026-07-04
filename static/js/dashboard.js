document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('activityChart');
  if (!ctx) return;
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Certificates', 'Verifications'],
      datasets: [{
        label: 'Overview',
        data: [window.dashboardData.certificates, window.dashboardData.verifications],
        backgroundColor: ['#0b4f8a', '#1d8ce0']
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });
});
