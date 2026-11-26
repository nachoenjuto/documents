// Demo sin conexión del tab Due Diligence: carga en memoria un análisis sintético (tabla, informe,
// riesgos, conflictos y PDF) desde data/demo-offline/<caso>.js, sin modelo ni red.
// Se usa <script> y no fetch para que funcione también abriendo index.html con doble clic (file://).
// Los datos se generan con «uv run generar_docs_large.py offline» (Demo docs/clientes/afianza).
(function () {
  const DIR = 'data/demo-offline/', sel = $('tr-demo'), cache = {}, wait = {};
  const cases = window.DEMO_OFFLINE_CASES || [];
  const label = k => (cases.find(c => c.key === k) || { label: k }).label;

  window.DemoOffline = {
    // Lo llama cada data/demo-offline/<caso>.js al cargarse.
    ready(key, data) { cache[key] = data; (wait[key] || []).forEach(f => f.ok(data)); delete wait[key]; },
    fetch: key => fetchCase(key)
  };
  function fetchCase(key) {
    if (cache[key]) return Promise.resolve(cache[key]);
    return new Promise((ok, ko) => {
      (wait[key] = wait[key] || []).push({ ok, ko });
      if (wait[key].length > 1) return;
      const s = document.createElement('script');
      s.src = DIR + encodeURIComponent(key) + '.js';
      s.onerror = () => { (wait[key] || []).forEach(f => f.ko(new Error(s.src))); delete wait[key]; s.remove(); };
      document.body.appendChild(s);
    });
  }
  async function load(key) {
    const st = $('status-txt-t'), name = label(key);
    if (!window.TabularReview || TabularReview.busy()) return;
    sel.disabled = true; st.textContent = t('tabular.offlineLoading', { name }); st.classList.add('show');
    try { await fetchCase(key); TabularReview.loadSession(cache[key], name); }
    catch (e) { console.error(e); $('err-t').textContent = t('tabular.offlineFailed', { name }); $('err-t').classList.add('show'); }
    finally { sel.disabled = false; sel.value = ''; st.classList.remove('show'); }
  }
  function render() {
    sel.innerHTML = `<option value="">${t('tabular.offline')}: ${t('tabular.offlinePick')}</option>` +
      cases.map(c => `<option value="${c.key}">${c.label} · ${c.docs} PDF</option>`).join('');
    sel.hidden = !cases.length;
  }
  sel.addEventListener('change', () => { if (sel.value) load(sel.value); });
  render();
  if (window.i18next && i18next.on) i18next.on('languageChanged', render);
})();
