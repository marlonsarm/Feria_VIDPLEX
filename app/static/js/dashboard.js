(function () {
  let chart = null;

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function renderTabla(leads) {
    const body = document.getElementById('leadsBody');
    if (leads.length === 0) {
      body.innerHTML = '<tr><td colspan="6" style="padding:14px 6px; color:#9A9A9A;">Aún no hay contactos registrados.</td></tr>';
      return;
    }
    body.innerHTML = leads.map(function (l) {
      return '<tr>' +
        '<td style="padding:9px 6px; border-bottom:1px solid var(--gris-linea);">' + escapeHtml(l.nombre) + '</td>' +
        '<td style="padding:9px 6px; border-bottom:1px solid var(--gris-linea);">' + escapeHtml(l.telefono) + '</td>' +
        '<td style="padding:9px 6px; border-bottom:1px solid var(--gris-linea);">' + escapeHtml(l.correo) + '</td>' +
        '<td style="padding:9px 6px; border-bottom:1px solid var(--gris-linea);">' + escapeHtml(l.tipo_proyecto || '—') + '</td>' +
        '<td style="padding:9px 6px; border-bottom:1px solid var(--gris-linea);">' + escapeHtml(l.productos || '—') + '</td>' +
        '<td style="padding:9px 6px; border-bottom:1px solid var(--gris-linea); white-space:nowrap;">' + escapeHtml(l.fecha_creacion) + '</td>' +
        '</tr>';
    }).join('');
  }

  function renderChart(ranking) {
    const ctx = document.getElementById('rankingChart');
    const labels = ranking.map(function (r) { return r.ref_code; });
    const escaneos = ranking.map(function (r) { return r.escaneos; });
    const leads = ranking.map(function (r) { return r.leads; });

    if (chart) {
      chart.data.labels = labels;
      chart.data.datasets[0].data = escaneos;
      chart.data.datasets[1].data = leads;
      chart.update();
      return;
    }

    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          { label: 'Escaneos', data: escaneos, backgroundColor: 'rgba(154,154,154,0.5)' },
          { label: 'Leads', data: leads, backgroundColor: '#E4572E' }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: { ticks: { color: '#9A9A9A' }, grid: { color: 'rgba(255,255,255,0.08)' } },
          y: { ticks: { color: '#9A9A9A' }, grid: { color: 'rgba(255,255,255,0.08)' }, beginAtZero: true }
        },
        plugins: { legend: { labels: { color: '#FFFFFF' } } }
      }
    });
  }

  async function cargar() {
    try {
      const res = await fetch('/admin/data');
      if (!res.ok) throw new Error('error de red');
      const data = await res.json();
      document.getElementById('totalLeadsHint').textContent = data.total_leads + ' contacto(s) capturados en total';
      var elEscaneosHome = document.getElementById('escaneosHomeValor');
      if (elEscaneosHome) {
        elEscaneosHome.textContent = data.escaneos_home;
      }
      renderTabla(data.leads);
      renderChart(data.ranking);
    } catch (e) {
      document.getElementById('totalLeadsHint').textContent = 'No se pudo cargar la información.';
    }
  }

  document.getElementById('btnRefrescar').addEventListener('click', function (e) {
    e.preventDefault();
    const btn = document.getElementById('btnRefrescar');
    const icono = document.getElementById('iconoRefrescar');
    const texto = document.getElementById('textoRefrescar');

    btn.disabled = true;
    icono.style.transform = 'rotate(360deg)';
    texto.textContent = 'Actualizando...';

    cargar().finally(function () {
      texto.textContent = '¡Actualizado!';
      setTimeout(function () {
        texto.textContent = 'Refrescar ahora';
        icono.style.transform = 'rotate(0deg)';
        btn.disabled = false;
      }, 1200);
    });
  });

  cargar();
  setInterval(cargar, 30000); // se actualiza sola cada 30s
})();

