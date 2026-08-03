(function () {
  const STORAGE_KEY = 'vidplex_pending_leads';

  // ---------------- Drawer de galería / video ----------------
  const btnAbrir = document.getElementById('btnAbrirDrawer');
  const btnCerrar = document.getElementById('btnCerrarDrawer');
  const overlay = document.getElementById('overlay');
  const drawer = document.getElementById('drawer');
  const drawerBody = document.getElementById('drawerBody');
  let mediaCargada = false;

  function renderMedia() {
    if (mediaCargada) return;
    mediaCargada = true;
    const media = window.VIDPLEX_MEDIA || [];
    if (media.length === 0) {
      drawerBody.innerHTML = '<div class="media-placeholder">Aún no hay fotos ni video para este vidrio.</div>';
      return;
    }
    drawerBody.innerHTML = media.map(function (m) {
      if (m.tipo === 'video') {
        return '<div class="video-wrap"><iframe src="' + m.url + '" loading="lazy" allowfullscreen></iframe></div>';
      }
      return '<img src="/static/img/' + m.url + '" loading="lazy" alt="Foto del vidrio">';
    }).join('');
  }

  function abrirDrawer() {
    renderMedia(); // solo carga fotos/video cuando el usuario lo pide
    overlay.classList.add('show');
    drawer.classList.add('show');
  }
  function cerrarDrawer() {
    overlay.classList.remove('show');
    drawer.classList.remove('show');
  }
  if (btnAbrir) btnAbrir.addEventListener('click', abrirDrawer);
  if (btnCerrar) btnCerrar.addEventListener('click', cerrarDrawer);
  if (overlay) overlay.addEventListener('click', cerrarDrawer);

  // ---------------- Validación del formulario ----------------
  const form = document.getElementById('leadForm');
  if (!form) return;

  const btn = document.getElementById('submitBtn');
  const avisoOffline = document.getElementById('avisoOffline');

  function validar() {
    let ok = true;

    const nombreEl = document.getElementById('nombre');
    const nombreField = document.getElementById('fName');
    const nombre = nombreEl.value.trim();
    const nombreValido = /^[A-Za-zÀ-ÿ\u00f1\u00d1' ]{4,60}$/.test(nombre) && nombre.split(/\s+/).length >= 2;
    nombreField.classList.toggle('has-err', !nombreValido);
    nombreEl.classList.toggle('err', !nombreValido);
    if (!nombreValido) ok = false;

    const telEl = document.getElementById('telefono');
    const telField = document.getElementById('fPhone');
    const telDigits = telEl.value.replace(/[^0-9]/g, '');
    const telValido = telDigits.length >= 7 && telDigits.length <= 15;
    telField.classList.toggle('has-err', !telValido);
    telEl.classList.toggle('err', !telValido);
    if (!telValido) ok = false;

    const mailEl = document.getElementById('correo');
    const mailField = document.getElementById('fEmail');
    const mailValido = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mailEl.value.trim());
    mailField.classList.toggle('has-err', !mailValido);
    mailEl.classList.toggle('err', !mailValido);
    if (!mailValido) ok = false;

    const autorizoEl = document.getElementById('autorizo');
    const autorizoField = document.getElementById('fAutorizo');
    autorizoField.classList.toggle('has-err', !autorizoEl.checked);
    if (!autorizoEl.checked) ok = false;

    return ok;
  }

  ['nombre', 'telefono', 'correo'].forEach(function (id) {
    document.getElementById(id).addEventListener('input', function () {
      if (document.getElementById(id).classList.contains('err')) validar();
    });
  });
  document.getElementById('autorizo').addEventListener('change', validar);

  function payloadActual() {
    return {
      nombre: document.getElementById('nombre').value.trim(),
      telefono: document.getElementById('telefono').value.trim(),
      correo: document.getElementById('correo').value.trim(),
      tipo_proyecto: document.getElementById('tipoProyecto').value,
      autorizo_datos: document.getElementById('autorizo').checked,
      ref_code: document.getElementById('refCode').value
    };
  }

  function guardarPendiente(payload) {
    const pendientes = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    pendientes.push(payload);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(pendientes));
  }

  async function enviarPendientes() {
    const pendientes = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    if (pendientes.length === 0) return;
    const restantes = [];
    for (const p of pendientes) {
      try {
        const res = await fetch('/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(p)
        });
        if (!res.ok) restantes.push(p);
      } catch (e) {
        restantes.push(p);
      }
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(restantes));
  }

  window.addEventListener('online', enviarPendientes);
  enviarPendientes(); // por si quedó algo pendiente de una visita anterior

  function mostrarExito() {
    document.getElementById('formState').style.display = 'none';
    document.getElementById('successState').classList.add('show');
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!validar()) return;

    btn.disabled = true;
    btn.textContent = 'Enviando…';
    avisoOffline.classList.remove('show');

    const payload = payloadActual();

    try {
      const res = await fetch('/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        mostrarExito();
        return;
      }

      const data = await res.json().catch(function () { return {}; });
      if (data.errores) {
        // el server encontró algo que el cliente no validó bien; recargar mensajes visibles
        btn.disabled = false;
        btn.textContent = 'Quiero mi cotización';
        alert('Revisa los datos ingresados.');
        return;
      }
      throw new Error('respuesta no ok');
    } catch (err) {
      // sin conexión: no perder el dato, se reintenta solo
      guardarPendiente(payload);
      avisoOffline.classList.add('show');
      mostrarExito();
    }
  });
})();
