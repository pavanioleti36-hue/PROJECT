// Forest Fire Detection System - Main JavaScript

// ── Sidebar Toggle (Mobile) ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
        document.addEventListener('click', function (e) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }

    // ── Active sidebar link ──
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            link.classList.add('active');
        }
    });

    // ── Auto-dismiss alerts ──
    setTimeout(() => {
        document.querySelectorAll('.alert.auto-dismiss').forEach(el => {
            const bsAlert = new bootstrap.Alert(el);
            if (bsAlert) bsAlert.close();
        });
    }, 5000);

    // ── Tooltips ──
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // ── Confirm delete ──
    document.querySelectorAll('.btn-confirm-delete').forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});

// ── Dashboard Charts ──────────────────────────────────────────────
function initDashboardCharts(chartData) {
    // Risk distribution pie chart
    const riskCtx = document.getElementById('riskChart');
    if (riskCtx && chartData.riskCounts) {
        new Chart(riskCtx, {
            type: 'doughnut',
            data: {
                labels: ['Low', 'Medium', 'High', 'Critical'],
                datasets: [{
                    data: [
                        chartData.riskCounts.low || 0,
                        chartData.riskCounts.medium || 0,
                        chartData.riskCounts.high || 0,
                        chartData.riskCounts.critical || 0,
                    ],
                    backgroundColor: ['#28a745', '#ffc107', '#fd7e14', '#dc3545'],
                    borderWidth: 2,
                    borderColor: '#fff',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { padding: 15, font: { size: 12 } } },
                    tooltip: {
                        callbacks: {
                            label: ctx => ` ${ctx.label}: ${ctx.raw} readings`
                        }
                    }
                },
                cutout: '65%',
            }
        });
    }

    // Sensor readings line chart (last 7 days)
    const timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx && chartData.timeline) {
        new Chart(timelineCtx, {
            type: 'bar',
            data: {
                labels: chartData.timeline.labels,
                datasets: [{
                    label: 'Sensor Readings',
                    data: chartData.timeline.data,
                    backgroundColor: 'rgba(45, 90, 39, 0.7)',
                    borderColor: '#2d5a27',
                    borderWidth: 1,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// ── Sensor Live Chart ─────────────────────────────────────────────
function initSensorChart(apiUrl) {
    const ctx = document.getElementById('sensorLiveChart');
    if (!ctx) return;

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220,53,69,0.1)',
                    tension: 0.3,
                    fill: true,
                    yAxisID: 'y',
                },
                {
                    label: 'Humidity (%)',
                    data: [],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13,110,253,0.1)',
                    tension: 0.3,
                    fill: true,
                    yAxisID: 'y',
                },
                {
                    label: 'Smoke (ppm)',
                    data: [],
                    borderColor: '#6c757d',
                    backgroundColor: 'rgba(108,117,125,0.1)',
                    tension: 0.3,
                    fill: false,
                    yAxisID: 'y2',
                },
                {
                    label: 'Risk Score',
                    data: [],
                    borderColor: '#fd7e14',
                    backgroundColor: 'rgba(253,126,20,0.15)',
                    tension: 0.3,
                    fill: true,
                    yAxisID: 'y',
                },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: { type: 'linear', display: true, position: 'left', min: 0, max: 100, title: { display: true, text: 'Value' } },
                y2: { type: 'linear', display: true, position: 'right', min: 0, title: { display: true, text: 'Smoke (ppm)' }, grid: { drawOnChartArea: false } },
                x: { ticks: { maxTicksLimit: 10 }, grid: { display: false } }
            },
            plugins: { legend: { position: 'top' } },
            animation: { duration: 300 }
        }
    });

    function loadData() {
        fetch(apiUrl)
            .then(r => r.json())
            .then(data => {
                chart.data.labels = data.labels;
                chart.data.datasets[0].data = data.temperature;
                chart.data.datasets[1].data = data.humidity;
                chart.data.datasets[2].data = data.smoke;
                chart.data.datasets[3].data = data.risk_score;
                chart.update();
            })
            .catch(err => console.warn('Chart data error:', err));
    }

    loadData();
    setInterval(loadData, 30000); // Refresh every 30 seconds
}

// ── Map initialisation (Leaflet) ───────────────────────────────────
function initFireMap(areas, incidents) {
    const mapEl = document.getElementById('fireMap');
    if (!mapEl) return;

    // Center on India by default
    const map = L.map('fireMap').setView([20.5937, 78.9629], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 18,
    }).addTo(map);

    // Forest area markers (green)
    areas.forEach(area => {
        if (area.lat && area.lng) {
            const marker = L.circleMarker([area.lat, area.lng], {
                radius: 10, color: '#2d5a27', fillColor: '#5a9e4e', fillOpacity: 0.8, weight: 2
            }).addTo(map);
            marker.bindPopup(`<strong>${area.name}</strong><br>${area.forest}<br><span class="badge bg-secondary">${area.zone_type}</span>`);
        }
    });

    // Fire incident markers (red)
    incidents.forEach(inc => {
        if (inc.lat && inc.lng) {
            const icon = L.divIcon({
                className: '',
                html: '<span style="font-size:1.4rem;">🔥</span>',
                iconAnchor: [12, 12]
            });
            const marker = L.marker([inc.lat, inc.lng], { icon }).addTo(map);
            marker.bindPopup(`<strong>${inc.title}</strong><br>Severity: ${inc.severity}<br>Status: ${inc.status}`);
        }
    });
}

// ── Number animation on dashboard ─────────────────────────────────
function animateNumbers() {
    document.querySelectorAll('.stat-value[data-target]').forEach(el => {
        const target = parseInt(el.dataset.target, 10);
        if (isNaN(target)) return;
        let current = 0;
        const step = Math.ceil(target / 30);
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current.toLocaleString();
            if (current >= target) clearInterval(timer);
        }, 30);
    });
}

document.addEventListener('DOMContentLoaded', animateNumbers);
