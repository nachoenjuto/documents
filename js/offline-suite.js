// Limpiar, cargar y guardar análisis y demo sin conexión en Document Intelligence, Contratos y Fraude.
// Reutiliza las funciones globales de index.html (load, loadCA, loadCB, loadR, render, renderContracts,
// renderFraud) y el cargador de js/demo-offline.js. Formato del archivo: «suite-analysis».
(function () {
  const esc = AF.esc, CASES = window.DEMO_OFFLINE_SUITE || {};
  const TABS = {
    doc: { run: 'btn-run', results: 'results', err: 'err', status: 'status-txt', clear: ['btn-clear'], files: () => [currentFile], last: () => lastDoc,
      show(files, d) { if (files[0]) load(files[0]); render(d); } },
    contracts: { run: 'btn-run-c', results: 'results-c', err: 'err-c', status: 'status-txt-c', clear: ['btn-clear-ca', 'btn-clear-cb'], files: () => [currentFileCA, currentFileCB], last: () => lastContracts,
      show(files, d) { if (files[0]) loadCA(files[0]); if (files[1]) loadCB(files[1]); renderContracts(d); } },
    fraud: { run: 'btn-run-r', results: 'results-r', err: 'err-r', status: 'status-txt-r', clear: ['btn-clear-r'], files: () => [currentFileR], last: () => lastFraud,
      show(files, d) { if (files[0]) loadR(files[0]); renderFraud(d); } }
  };
  const ui = {};

  function setErr(tab, m) { const e = $(TABS[tab].err); e.textContent = m || ''; e.classList.toggle('show', !!m); }
  function banner(tab, saved) {
    ui[tab].saved = saved;
    ui[tab].banner.textContent = saved ? t(saved.synthetic ? 'offline.savedSynthetic' : 'offline.savedFrom', saved) : '';
  }
  // «Guardar análisis» va al pie de los resultados, como en Due Diligence, y solo se ve si hay un resultado.
  function syncSave(tab) { ui[tab].foot.hidden = !(TABS[tab].last() && $(TABS[tab].results).classList.contains('show')); }
  function clear(tab) {
    TABS[tab].clear.forEach(id => $(id).click());
    $(TABS[tab].results).classList.remove('show'); banner(tab, null); setErr(tab, ''); syncSave(tab);
  }
  // El archivo es entrada no fiable: se comprueba el formato y el tab; el contenido lo escapan los renderizadores.
  function apply(tab, d, name) {
    if (!d || d.format !== 'suite-analysis' || typeof d.result !== 'object' || !d.result) throw new Error(t('offline.badFormat'));
    if (d.tab !== tab) throw new Error(t('offline.wrongTab', { tab: t('tabs.' + d.tab) }));
    const files = (Array.isArray(d.files) ? d.files : []).slice(0, 2).map(f => new File([Uint8Array.from(atob(String(f.data || '')), c => c.charCodeAt(0))], String(f.name), { type: String(f.type || '') }));
    clear(tab);
    TABS[tab].show(files, d.result);
    const when = new Date(d.date);
    banner(tab, { name, synthetic: d.synthetic === true, date: isNaN(when) ? '' : ' (' + when.toLocaleString('es-ES') + ')' });
    syncSave(tab);
  }
  async function loadFile(tab, file) {
    try { apply(tab, JSON.parse(await file.text()), file.name); }
    catch (e) { console.error(e); setErr(tab, t('offline.badFile', { name: file.name, message: e.message })); }
  }
  async function loadDemo(tab, key) {
    const c = (CASES[tab] || []).find(x => x.key === key), st = $(TABS[tab].status);
    ui[tab].demo.disabled = true; st.textContent = t('offline.loading', { name: c.label }); st.classList.add('show');
    try { apply(tab, await DemoOffline.fetch(key), c.label); }
    catch (e) { console.error(e); setErr(tab, t('offline.failed', { name: c.label })); }
    finally { ui[tab].demo.disabled = false; ui[tab].demo.value = ''; st.classList.remove('show'); st.textContent = t('common.processing'); }
  }
  const b64 = f => new Promise((ok, ko) => { const r = new FileReader(); r.onload = () => ok(String(r.result).split(',')[1]); r.onerror = ko; r.readAsDataURL(f); });
  async function save(tab) {
    try {
      const files = await Promise.all(TABS[tab].files().filter(Boolean).map(async f => ({ name: f.name, type: f.type, data: await b64(f) })));
      const date = new Date().toISOString();
      const blob = new Blob([JSON.stringify({ format: 'suite-analysis', version: 1, date, tab, files, result: TABS[tab].last() })], { type: 'application/json' });
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `analisis-${tab}-${date.slice(0, 10)}.json`; a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    } catch (e) { console.error(e); setErr(tab, t('common.error', { message: e.message })); }
  }
  function labels(tab) {
    const u = ui[tab];
    u.clear.textContent = t('offline.clear'); u.load.textContent = t('offline.load'); u.save.textContent = t('offline.save');
    u.demo.setAttribute('aria-label', t('offline.demo'));
    u.demo.innerHTML = `<option value="">${esc(t('offline.demo'))}: ${esc(t('offline.pick'))}</option>` + (CASES[tab] || []).map(c => `<option value="${esc(c.key)}">${esc(c.label)}</option>`).join('');
    u.demo.hidden = !(CASES[tab] || []).length;
    if (u.banner.textContent && u.saved) banner(tab, u.saved);
  }

  Object.entries(TABS).forEach(([tab, cfg]) => {
    const row = $(cfg.run).closest('.action-row'), status = $(cfg.status);
    const mk = (tag, cls) => { const e = document.createElement(tag); e.className = cls; if (tag === 'button') e.type = 'button'; status.before(e); return e; };
    const u = ui[tab] = { clear: mk('button', 'tr-btn'), load: mk('button', 'tr-btn'), demo: mk('select', 'tr-btn') };
    u.foot = document.createElement('div'); u.foot.className = 'tr-foot'; u.foot.hidden = true;
    u.save = document.createElement('button'); u.save.type = 'button'; u.save.className = 'tr-btn'; u.save.style.marginLeft = 'auto';
    u.foot.append(u.save); $(cfg.results).append(u.foot);
    u.input = document.createElement('input'); u.input.type = 'file'; u.input.accept = '.json'; u.input.hidden = true; row.append(u.input);
    u.banner = document.createElement('div'); u.banner.className = 'tr-saved'; $(cfg.results).prepend(u.banner);
    u.clear.addEventListener('click', () => clear(tab));
    u.load.addEventListener('click', () => u.input.click());
    u.input.addEventListener('change', () => { const f = u.input.files[0]; u.input.value = ''; if (f) loadFile(tab, f); });
    u.save.addEventListener('click', () => save(tab));
    u.demo.addEventListener('change', () => { if (u.demo.value) loadDemo(tab, u.demo.value); });
    // Un análisis nuevo con el modelo deja de ser el cargado: se quita el aviso.
    $(cfg.run).addEventListener('click', () => banner(tab, null));
    new MutationObserver(() => syncSave(tab)).observe($(cfg.results), { attributes: true, attributeFilter: ['class'] });
    labels(tab); syncSave(tab);
  });
  if (window.i18next && i18next.on) i18next.on('languageChanged', () => Object.keys(TABS).forEach(labels));
})();
