// Tabular Review: N documentos x M campos, con comprobación de citas y alertas cruzadas.
// Depende de los helpers globales de la página: $, t, b64, parseClaudeJSON.
(function () {
  const CFG = {
    extractModel: 'claude-haiku-4-5-20251001', crossModel: 'claude-haiku-4-5-20251001',
    maxDocs: 20, maxFields: 16, concurrency: 3, maxChars: 120000, maxPages: 100,
    timeoutMs: 120000, retries: 5, exts: ['pdf', 'docx', 'txt'],
    ...(window.TABULAR_CONFIG || {})
  };
  const T = window.TABULAR;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const norm = s => String(s || '').normalize('NFKC').toLowerCase().replace(/[«»“”"'’‘]/g, '').replace(/\s+/g, ' ').trim();
  const level = v => ['HIGH', 'MEDIUM', 'LOW'].includes(v) ? v : 'NONE';

  // Instrucción efectiva de un campo: la original, complementada o sustituida desde la cabecera de la tabla.
  const askOf = f => f.edit ? T.edited(f.ask, f.edit.text, f.edit.mode) : f.ask;
  const prompted = list => list.map(f => ({ ...f, ask: askOf(f) }));

  let files = [], tplKey = 'dd', fields = [], running = false, runFields = [], runTpl = 'dd', rows = [], cross = null, stats = null, saved = null, customN = 0;

  // ---- Configuración ----
  // Los campos propios se conservan al cambiar de plantilla.
  function setTemplate(k) { tplKey = k; fields = [...T.templates[k].fields.map(f => ({ ...f })), ...fields.filter(f => f.custom)]; renderConfig(); }
  function renderConfig() {
    $('tr-templates').innerHTML = Object.entries(T.templates).map(([k, v]) =>
      `<button type="button" class="tr-tpl ${k === tplKey ? 'on' : ''}" data-k="${k}" aria-pressed="${k === tplKey}"><b>${esc(v.label)}</b><small>${esc(v.lob)}</small></button>`).join('');
    $('tr-fields').innerHTML = fields.map((f, i) =>
      `<span class="tr-chip${f.edit ? ' tr-edited' : ''}" title="${esc(askOf(f))}">${esc(f.label)}${f.edit ? ' <i aria-hidden="true">✎</i>' : ''}<button type="button" data-i="${i}" aria-label="Quitar ${esc(f.label)}">×</button></span>`).join('');
    sync();
  }
  function renderFiles() {
    $('tr-files').innerHTML = files.map((f, i) =>
      `<span class="tr-chip"><em>D${i + 1}</em>${esc(f.name)}<button type="button" data-i="${i}" aria-label="Quitar ${esc(f.name)}">×</button></span>`).join('');
    sync();
  }
  function sync() { $('tr-add').disabled = $('tr-load').disabled = $('tr-save').disabled = running; $('btn-run-t').disabled = running || !files.length || !$('api-key').value.trim().startsWith('sk-ant'); }
  function err(m) { $('err-t').textContent = m || ''; $('err-t').classList.toggle('show', !!m); }
  function addFiles(list) {
    if (running) return;
    const ok = [...list].filter(f => CFG.exts.includes(f.name.split('.').pop().toLowerCase()) &&
      !files.some(x => x.name === f.name && x.size === f.size));
    const bad = [...list].some(f => !CFG.exts.includes(f.name.split('.').pop().toLowerCase()));
    const room = CFG.maxDocs - files.length;
    files = files.concat(ok.slice(0, room));
    err(ok.length > room ? t('tabular.limit', { n: CFG.maxDocs, x: ok.length - room }) : bad ? t('common.unsupported') : '');
    renderFiles();
  }
  function addField() {
    const v = $('tr-new').value.trim();
    if (!v || running) return true;
    if (fields.length >= CFG.maxFields) { err(t('tabular.maxFields', { n: CFG.maxFields })); return false; }
    fields.push({ key: 'custom_' + (++customN), label: v.length > 60 ? v.slice(0, 58) + '…' : v, ask: v, custom: true });
    $('tr-new').value = '';
    err(''); renderConfig();
    return true;
  }

  // Con resultados en pantalla, un campo nuevo se analiza al momento, solo esa columna.
  function addAndAnalyze() {
    if (!$('tr-new').value.trim() || running || !addField()) return;
    if (!$('results-t').classList.contains('show') || !rows.some(r => !r.error)) return;
    if (rows.some(r => !r.error && !r.file)) { err(t('tabular.noFiles')); return; }
    if (!$('api-key').value.trim().startsWith('sk-ant')) { err(t('tabular.needKey')); return; }
    const have = new Set(runFields.map(f => f.key));
    analyzeNew(fields.filter(f => f.custom && !have.has(f.key)));
  }

  // ---- Lectura ----
  async function readDoc(file) {
    const ext = file.name.split('.').pop().toLowerCase();
    let pages = [], cut = false;
    if (ext === 'pdf') {
      if (!pdfjsLib) throw new Error(t('common.pdfLoading'));
      const pdf = await pdfjsLib.getDocument({ data: await file.arrayBuffer(), isEvalSupported: false }).promise;
      cut = pdf.numPages > CFG.maxPages;
      for (let i = 1; i <= Math.min(pdf.numPages, CFG.maxPages); i++) {
        const c = await (await pdf.getPage(i)).getTextContent();
        pages.push(c.items.map(x => x.str).join(' '));
      }
    } else if (ext === 'docx') {
      pages = [(await mammoth.extractRawText({ arrayBuffer: await file.arrayBuffer() })).value];
    } else pages = [await file.text()];

    if (pages.join('').trim().length < 80) {
      if (ext !== 'pdf') throw new Error(t('common.extractFailed'));
      return { scanned: true, paged: true, pages: [], cut: false, part: { type: 'document', source: { type: 'base64', media_type: 'application/pdf', data: await b64(file) } } };
    }
    let text = pages.map((p, i) => `[PÁGINA ${i + 1}]\n${p}`).join('\n');
    if (text.length > CFG.maxChars) { text = text.slice(0, CFG.maxChars); cut = true; }
    return { scanned: false, paged: ext === 'pdf', pages, cut, part: { type: 'text', text: `<doc>\n${text}\n</doc>` } };
  }

  // ---- API ----
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  async function call(model, system, content, maxTokens) {
    for (let n = 0; ; n++) {
      const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), CFG.timeoutMs);
      let error, retry = false;
      try {
        const res = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST', signal: ctl.signal,
          headers: { 'Content-Type': 'application/json', 'x-api-key': $('api-key').value.trim(), 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
          body: JSON.stringify({ model, max_tokens: maxTokens, system, messages: [{ role: 'user', content }] })
        });
        if (res.ok) {
          const d = await res.json(), u = d.usage || {};
          stats.in += u.input_tokens || 0; stats.out += u.output_tokens || 0;
          return parseClaudeJSON((d.content || []).map(b => b.text || '').join(''));
        }
        const e = await res.json().catch(() => ({}));
        error = new Error(e.error?.message || `HTTP ${res.status}`);
        retry = res.status === 429 || res.status >= 500;
      } catch (e) {
        error = e.name === 'AbortError' ? new Error('timeout') : e;
        retry = e.name === 'AbortError' || e instanceof TypeError;
      } finally { clearTimeout(timer); }
      if (!retry || n >= CFG.retries) throw error;
      await sleep(Math.min(32000, 2000 * 2 ** n) * (0.75 + Math.random() / 2));
    }
  }

  // La página y la validez de la cita se comprueban contra el texto, no se toman del modelo.
  function checkCell(raw, doc) {
    const c = raw && typeof raw === 'object' ? raw : {};
    const blank = c.value == null || String(c.value).trim() === '';
    if (blank) return { value: null, quote: null, page: null, confidence: null, risk: 'NONE', check: 'none' };
    const q = norm(c.quote);
    let page = Number.isInteger(c.page) ? c.page : null, check = 'bad';
    if (doc.scanned) check = 'scan';
    else if (q.length >= 4) {
      const i = doc.pages.findIndex(p => norm(p).includes(q));
      if (i >= 0) { page = i + 1; check = 'ok'; }
      else if (norm(doc.pages.join(' ')).includes(q)) check = 'ok';
    }
    if (!doc.paged) page = null;
    const conf = Number(c.confidence);
    return { value: String(c.value), quote: c.quote ? String(c.quote) : null, page, confidence: Number.isFinite(conf) ? Math.max(0, Math.min(100, conf)) : null, risk: level(c.risk), check, meets: c.meets === false ? false : undefined };
  }

  async function extractFields(row, list) {
    const doc = await readDoc(row.file);
    row.cut = doc.cut;
    const out = await call(CFG.extractModel, T.extractSystem, [doc.part, { type: 'text', text: T.extract(prompted(list)) }], 6000);
    if (!out || typeof out.fields !== 'object' || !out.fields) throw new Error(t('common.invalidJson', { message: 'fields' }));
    list.forEach(f => { row.cells[f.key] = checkCell(out.fields[f.key], doc); });
  }
  async function extractRow(file, i) {
    const row = { id: 'D' + (i + 1), name: file.name, file, url: URL.createObjectURL(file), cells: {}, error: null, cut: false };
    try { await extractFields(row, runFields); } catch (e) { console.error(row.id, e); row.error = e.message; }
    return row;
  }

  async function pool(n, job) {
    let next = 0;
    const worker = async () => { while (next < n) await job(next++); };
    await Promise.all(Array.from({ length: Math.min(CFG.concurrency, n) }, worker));
  }
  function begin() {
    running = true; err(''); if (saved) saved.live = true; stats = { in: 0, out: 0, t0: Date.now() };
    $('btn-run-t').classList.add('loading'); $('status-txt-t').classList.add('show'); sync();
  }
  function end(message) {
    stats.s = Math.round((Date.now() - stats.t0) / 1000);
    console.info(JSON.stringify({ timestamp: new Date().toISOString(), level: 'INFO', module: 'tabular-review', message, docs: rows.length, input_tokens: stats.in, output_tokens: stats.out, seconds: stats.s }));
  }
  function finish() { running = false; $('btn-run-t').classList.remove('loading'); $('status-txt-t').classList.remove('show'); sync(); }
  function releaseUrls() { rows.forEach(r => r && r.url && URL.revokeObjectURL(r.url)); }

  // Contradicciones: solo las que enfrentan a dos o más documentos de la tabla.
  function cleanConflicts(list, ids) {
    const rank = { HIGH: 0, MEDIUM: 1, LOW: 2 }, s = v => typeof v === 'string' ? v.trim() : '';
    return (Array.isArray(list) ? list : []).filter(c => c && typeof c === 'object').map(c => ({
      severity: level(c.severity) === 'NONE' ? 'MEDIUM' : c.severity, title: s(c.title), why: s(c.why), impact: s(c.impact), action: s(c.action),
      claims: (Array.isArray(c.claims) ? c.claims : []).filter(x => x && typeof x === 'object' && ids.has(x.doc)).slice(0, 6).map(x => ({ doc: x.doc, field: s(x.field), says: s(x.says) }))
    })).filter(c => c.title && new Set(c.claims.map(x => x.doc)).size >= 2).slice(0, 6).sort((a, b) => rank[a.severity] - rank[b.severity]);
  }
  async function crossCheck() {
    const good = rows.filter(r => !r.error);
    cross = null;
    if (!good.length) return;
    $('status-txt-t').textContent = t('tabular.crossing');
    const table = good.map(r => ({ id: r.id, documento: r.name, campos: Object.fromEntries(runFields.map(f => { const c = r.cells[f.key] || {}; return [f.custom ? f.ask : f.label, c.value == null ? null : c.meets === false ? '(no cumple el criterio) ' + c.value : c.value]; })) }));
    try {
      const now = new Date(), today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
      const focus = T.templates[runTpl].cross + T.crossCustom(runFields.filter(f => f.custom)) + T.crossEdited(prompted(runFields.filter(f => f.edit)));
      const out = await call(CFG.crossModel, T.crossSystem, [{ type: 'text', text: `<tabla>\n${JSON.stringify(table)}\n</tabla>\n\n${T.cross(focus, today)}` }], 7000);
      if (!out || !Array.isArray(out.alerts)) throw new Error(t('common.invalidJson', { message: 'alerts' }));
      const ids = new Set(good.map(r => r.id)), rank = { HIGH: 0, MEDIUM: 1, LOW: 2 };
      const summary = (Array.isArray(out.summary) ? out.summary : [out.summary]).filter(x => typeof x === 'string' && x.trim()).slice(0, 6);
      cross = {
        scope: typeof out.scope === 'string' ? out.scope.trim().replace(/\.$/, '') : '', summary,
        alerts: out.alerts.filter(a => a && typeof a === 'object').slice(0, 10).map(a => ({ ...a, severity: level(a.severity) === 'NONE' ? 'LOW' : a.severity, docs: (Array.isArray(a.docs) ? a.docs : []).filter(d => ids.has(d)) }))
      };
      cross.alerts.sort((a, b) => rank[a.severity] - rank[b.severity]);
      cross.conflicts = cleanConflicts(out.conflicts, ids);
    } catch (e) { console.error(e); cross = { error: e.message }; }
  }

  async function run() {
    if (running) return;
    if ($('tr-new').value.trim() && !addField()) return;
    if (!fields.length) { err(t('tabular.empty')); return; }
    begin();
    releaseUrls(); cross = null; rows = []; saved = null;
    runFields = fields.map(f => ({ ...f })); runTpl = tplKey;
    const batch = files.slice();
    let done = 0;
    const tick = () => { $('status-txt-t').textContent = t('tabular.progress', { done, total: batch.length }); };
    $('results-t').classList.remove('show'); tick();
    try {
      await pool(batch.length, async i => { rows[i] = await extractRow(batch[i], i); done++; tick(); });
      await crossCheck();
      end('run_completed'); renderResults(true);
    } catch (e) { console.error(e); err(t('common.error', { message: e.message })); }
    finally { finish(); }
  }

  async function analyzeNew(list) {
    if (!list.length) return;
    runFields = runFields.concat(list.map(f => ({ ...f })));
    await analyzeColumns(list, 'field_added', n => t('tabular.progressNew', n));
    const head = $('tr-table').querySelector('thead tr').lastElementChild;
    const box = head.closest('.tr-scroll'); box.scrollLeft = box.scrollWidth;
    box.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  // Extrae solo las columnas indicadas en cada documento y rehace el cruce; el resto de la tabla no cambia.
  async function analyzeColumns(list, message, label) {
    begin();
    const good = rows.filter(r => !r.error);
    let done = 0;
    const tick = () => { $('status-txt-t').textContent = label({ done, total: good.length }); };
    tick(); renderResults(false);
    $('results-t').classList.add('tr-busy');
    try {
      await pool(good.length, async i => {
        try { await extractFields(good[i], list); }
        catch (e) { console.error(good[i].id, e); list.forEach(f => { good[i].cells[f.key] = { value: null, check: 'none', risk: 'NONE', error: e.message }; }); }
        done++; tick();
      });
      await crossCheck();
      end(message); renderResults(false);
    } catch (e) { console.error(e); err(t('common.error', { message: e.message })); }
    finally { $('results-t').classList.remove('tr-busy'); finish(); }
  }

  // ---- Resultados ----
  const mark = { ok: '✓', bad: '!', scan: '?' };
  function renderLegend() {
    const n = { HIGH: 0, MEDIUM: 0, LOW: 0 };
    if (cross && cross.alerts) cross.alerts.forEach(a => n[a.severity]++);
    $('tr-legend').innerHTML = `<span class="tr-lbl">${t('tabular.legend')}</span>` + ['HIGH', 'MEDIUM', 'LOW'].map(k =>
      `<span class="tr-key" title="${esc(t('tabular.sevHelp.' + k))}"><i class="dot ${k}"></i>${t('tabular.sevName.' + k)}${cross && cross.alerts ? ` <b title="${esc(t('tabular.alertCount'))}">${n[k]}</b>` : ''}</span>`).join('') +
      `<span class="tr-sep"></span>` + ['ok', 'bad', 'scan'].map(k => `<span class="tr-key"><i class="q-${k}">${mark[k]}</i>${t('tabular.legendQuote.' + k)}</span>`).join('');
  }
  function renderResults(scroll) {
    renderLegend();
    $('tr-saved').textContent = saved && !saved.live ? t(saved.synthetic ? 'tabular.savedSynthetic' : 'tabular.savedFrom', saved) : '';
    const failed = rows.filter(r => r.error).map(r => r.id);
    let h = failed.length ? `<p class="tr-warn">${esc(t('tabular.partial', { list: failed.join(', ') }))}</p>` : '';
    if (cross && cross.error) h += `<p class="tr-warn">${esc(t('tabular.crossFailed', { message: cross.error }))}</p>`;
    else if (!cross && saved) h += `<p class="tr-act">${t('tabular.csvNoAlerts')}</p>`;
    else if (cross) {
      const n = rows.length - failed.length, scope = cross.scope || T.templates[runTpl].label;
      const title = `${t(n === 1 ? 'tabular.summaryOne' : 'tabular.summaryMany', { n })}: ${scope}`;
      h += `<h2 class="tr-title" title="${esc(title)}">${esc(title)}</h2>`;
      if (cross.summary.length) h += `<ul class="tr-bullets">${cross.summary.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
      h += `<span class="tr-lbl">${t('tabular.alerts', { n: cross.alerts.length })}</span>`;
      h += cross.alerts.map(a => `<div class="tr-alert ${a.severity}"><div class="tr-alert-hd"><span class="tr-sev">${t('tabular.sev.' + a.severity)}</span><b>${esc(a.title)}</b>${a.docs.map(d => `<button type="button" class="tr-doc" data-doc="${d}">${d}</button>`).join('')}</div><p>${esc(a.description)}</p>${a.action ? `<p class="tr-act">→ ${esc(a.action)}</p>` : ''}</div>`).join('') || `<p class="tr-act">${t('tabular.noAlerts')}</p>`;
    }
    if (cross && cross.conflicts && cross.conflicts.length) h += renderConflicts(cross.conflicts);
    $('tr-alerts').innerHTML = h;
    $('tr-table').innerHTML = `<thead><tr><th scope="col">${t('tabular.document')}</th>${runFields.map(f => f.key === editing ? editorTh(f) : `<th scope="col"${f.edit ? ' class="tr-edited"' : ''}><button type="button" class="tr-th" data-k="${f.key}" title="${esc(f.edit ? t('tabular.editedTip', { ask: askOf(f) }) : askOf(f))}&#10;${esc(t('tabular.editHint'))}">${esc(f.label)}${f.edit ? ' <i aria-hidden="true">✎</i>' : ''}</button></th>`).join('')}</tr></thead><tbody>` +
      rows.map(r => `<tr id="tr-row-${r.id}"><th scope="row"><em>${r.id}</em>${esc(r.name)}${r.cut ? `<small class="tr-warn">${t('tabular.truncated')}</small>` : ''}</th>` +
        (r.error ? `<td colspan="${runFields.length}" class="tr-warn">${esc(t('tabular.failed', { message: r.error }))}</td>` :
          runFields.map(f => {
            const c = r.cells[f.key];
            if (!c) return '<td class="tr-miss">…</td>';
            if (c.error) return `<td class="tr-warn">${esc(t('tabular.failed', { message: c.error }))}</td>`;
            if (c.value != null && c.meets === false) return `<td class="tr-out"><button type="button" class="tr-cell" data-r="${r.id}" data-f="${f.key}" title="${esc(c.value)}">${t('tabular.notMet')} <i class="q-${c.check}">${mark[c.check]}</i></button></td>`;
            return c.value == null ? `<td class="tr-miss">${t('tabular.missing')}</td>` :
              `<td class="r-${c.risk}"><button type="button" class="tr-cell" data-r="${r.id}" data-f="${f.key}">${esc(c.value)} <i class="q-${c.check}">${mark[c.check]}</i></button></td>`;
          }).join('')) + '</tr>').join('') + '</tbody>';
    $('tr-usage').textContent = saved && saved.synthetic && !saved.live ? '' : t('tabular.usage', { in: stats.in, out: stats.out, s: stats.s });
    $('results-t').classList.add('show');
    if (scroll) $('results-t').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function renderConflicts(list) {
    const fieldOf = name => runFields.find(f => f.label === name || f.ask === name);
    return `<div class="tr-confs"><span class="tr-lbl">${t('tabular.conflicts', { n: list.length })}</span><p class="tr-act">${t('tabular.conflictsLead')}</p>` + list.map(c => {
      const claims = c.claims.map(x => {
        const r = rows.find(y => y.id === x.doc), f = fieldOf(x.field), cell = f && r && r.cells[f.key];
        const open = cell && cell.value != null ? ` data-r="${x.doc}" data-f="${f.key}"` : ` data-doc="${x.doc}"`;
        return `<button type="button" class="tr-claim"${open}><span class="tr-claim-hd"><em>${x.doc}</em>${esc(r ? r.name : '')}</span>${x.field ? `<span class="tr-lbl">${esc(x.field)}</span>` : ''}<span class="tr-says">${esc(x.says)}</span></button>`;
      }).join(`<span class="tr-vs" aria-label="${esc(t('tabular.conflictVs'))}">≠</span>`);
      return `<div class="tr-alert tr-conf ${c.severity}"><div class="tr-alert-hd"><span class="tr-sev">${t('tabular.sev.' + c.severity)}</span><b>${esc(c.title)}</b></div>
        <div class="tr-claims">${claims}</div>
        ${c.why ? `<p><b>${t('tabular.conflictWhy')}:</b> ${esc(c.why)}</p>` : ''}${c.impact ? `<p><b>${t('tabular.conflictImpact')}:</b> ${esc(c.impact)}</p>` : ''}${c.action ? `<p class="tr-act">→ ${esc(c.action)}</p>` : ''}</div>`;
    }).join('') + '</div>';
  }
  function docActions(r, key) {
    const can = PdfContext.supports(r);
    return `<b class="tr-name">${esc(r.name)}</b><div class="tr-acts"><a class="tr-btn" href="${r.url}" download="${esc(r.name)}" title="${esc(t('tabular.download'))}"><span aria-hidden="true">⤓</span> ${t('tabular.ctxDownload')}</a>
      <button type="button" class="tr-btn" id="tr-ctx" data-r="${r.id}" data-f="${key}" ${can ? '' : 'disabled'}><span aria-hidden="true">◫</span> ${t('tabular.ctxOpen')}</button>${can ? '' : `<small>${t('tabular.ctxOnlyPdf')}</small>`}</div>`;
  }
  function openContext(rid, key) {
    const r = rows.find(x => x.id === rid);
    $('tr-dlg').close();
    PdfContext.open(r, runFields.map(f => ({ value: null, check: 'none', risk: 'NONE', ...r.cells[f.key], key: f.key, label: f.label })), key);
  }
  function openCell(rid, key) {
    const r = rows.find(x => x.id === rid), c = r.cells[key], f = runFields.find(x => x.key === key);
    const lbl = { ok: 'verified', bad: 'unverified', scan: 'noText' }[c.check];
    const page = c.page == null ? t('tabular.noPage') : c.check === 'ok' ? t('tabular.pageN', { n: c.page }) : t('tabular.pageUnsure', { n: c.page });
    $('tr-dlg-body').innerHTML = `
      <div class="tr-dlg-hd"><div><span class="tr-lbl">${t('tabular.document')} ${r.id}</span>
        ${r.url ? `${docActions(r, key)}` : `<b>${esc(r.name)}</b><small>${t('tabular.noDownload')}</small>`}</div>
        <div class="tr-page"><span class="tr-lbl">${t('tabular.page')}</span><b>${esc(page)}</b></div></div>
      <span class="tr-lbl">${esc(askOf(f))}</span><h3>${esc(f.label)}</h3>
      ${c.meets === false ? `<p class="tr-warn">${t('tabular.notMetLong')}</p>` : ''}
      <p class="tr-val">${c.risk !== 'NONE' ? `<i class="dot ${c.risk}" title="${esc(t('tabular.sevName.' + c.risk))}"></i>` : ''}${esc(c.value)}</p>
      ${c.quote ? `<span class="tr-lbl">${t(c.check === 'ok' ? 'tabular.literal' : 'tabular.notLiteral')}</span><blockquote class="b-${c.check}">${esc(c.quote)}</blockquote>` : ''}
      <p class="q-${c.check}">${mark[c.check]} ${t('tabular.' + lbl)}</p>
      <small>${t('tabular.confidence')}: ${c.confidence == null ? '—' : c.confidence + '%'}</small>`;
    $('tr-dlg').showModal();
  }
  // ---- Edición de un campo desde la cabecera de la tabla ----
  let editing = null;
  const hasDocs = () => rows.every(r => r.error || r.file);
  const hasKey = () => $('api-key').value.trim().startsWith('sk-ant');
  function formErr(form, m) { let p = form.querySelector('.tr-ed-err'); if (!p) { p = document.createElement('small'); p.className = 'tr-warn tr-ed-err'; p.setAttribute('role', 'alert'); form.querySelector('.tr-ed-acts').before(p); } p.textContent = m; }
  // Ejemplo de criterio propio de cada columna; los campos añadidos usan uno genérico.
  function phOf(f) {
    const base = T.templates[runTpl].fields.find(x => x.key === f.key || x.label === ((f.orig && f.orig.label) || f.label));
    return f.ph || (base && base.ph) || t('tabular.editPh');
  }
  function editorTh(f) {
    const e = f.edit || { text: '', mode: 'add' }, docs = hasDocs();
    return `<th scope="col" class="tr-editing"><form class="tr-ed" data-k="${f.key}" aria-label="${esc(t('tabular.editHint'))}">
      <label class="tr-lbl">${t('tabular.editLabel')}<input name="label" maxlength="60" value="${esc(f.label)}"></label>
      <label class="tr-lbl">${t('tabular.editText')}<textarea name="text" rows="3" maxlength="500" placeholder="${esc(phOf(f))}" ${docs ? '' : 'disabled'}>${esc(e.text)}</textarea></label>
      <div class="tr-ed-mode" role="radiogroup">${['add', 'replace'].map(m => `<label><input type="radio" name="mode" value="${m}" ${e.mode === m ? 'checked' : ''} ${docs ? '' : 'disabled'}> ${t('tabular.mode.' + m)}</label>`).join('')}</div>
      <small>${esc(t('tabular.original', { ask: f.ask }))}</small>${docs ? '' : `<small class="tr-warn">${t('tabular.editNoFiles')}</small>`}
      <div class="tr-ed-acts"><button type="submit" class="tr-btn tr-primary">${t('tabular.apply')}</button><button type="button" class="tr-btn" data-act="cancel">${t('tabular.cancel')}</button>${f.edit ? `<button type="button" class="tr-btn" data-act="restore">${t('tabular.restore')}</button>` : ''}</div></form></th>`;
  }
  function openEditor(key) {
    if (running) return;
    editing = key; renderResults(false);
    const form = $('tr-table').querySelector('.tr-ed');
    form.closest('th').scrollIntoView({ block: 'nearest', inline: 'nearest' });
    const ta = form.elements.text; (ta.disabled ? form.elements.label : ta).focus();
  }
  function closeEditor() {
    const key = editing; editing = null; renderResults(false);
    const b = $('tr-table').querySelector(`.tr-th[data-k="${key}"]`); if (b) b.focus();
  }
  // Los cambios se copian también a la lista de campos, para que un nuevo lanzamiento los use.
  function setField(key, props) {
    [runFields.find(f => f.key === key), fields.find(f => f.key === key)].forEach(f => { if (f) Object.assign(f, props); });
    renderConfig();
  }
  async function applyEdit(form) {
    const f = runFields.find(x => x.key === form.dataset.k);
    const label = form.elements.label.value.trim() || f.label, text = form.elements.text.value.trim(), mode = form.elements.mode.value === 'replace' ? 'replace' : 'add';
    const edit = text ? { text, mode } : null;
    const changed = JSON.stringify(edit) !== JSON.stringify(f.edit || null);
    if (changed && !hasDocs()) { formErr(form, t('tabular.editNoFiles')); return; }
    if (changed && !hasKey()) { formErr(form, t('tabular.needKey')); return; }
    err('');
    const orig = f.orig || { label: f.label };
    if (!changed) { setField(f.key, { label, orig: label === orig.label && !f.edit ? undefined : orig }); closeEditor(); return; }
    if (!edit && f.snap) { setField(f.key, { label }); restoreColumn(f.key); return; }
    // Se guardan los valores originales la primera vez, para poder restaurarlos sin volver a extraer.
    if (!f.snap && !f.edit) f.snap = Object.fromEntries(rows.map(r => [r.id, r.cells[f.key]]));
    setField(f.key, { label, edit: edit || undefined, orig: edit ? orig : undefined });
    editing = null;
    await analyzeColumns([f], 'field_edited', n => t('tabular.progressEdit', { ...n, label }));
  }
  async function restoreColumn(key) {
    const f = runFields.find(x => x.key === key);
    editing = null;
    const label = (f.orig || f).label;
    if (!f.snap && !hasKey()) { formErr($('tr-table').querySelector('.tr-ed'), t('tabular.needKey')); editing = key; return; }
    if (!f.snap) { setField(key, { label, edit: undefined, orig: undefined }); await analyzeColumns([f], 'field_restored', n => t('tabular.progressEdit', { ...n, label })); return; }
    rows.forEach(r => { if (r.id in f.snap) r.cells[key] = f.snap[r.id]; });
    setField(key, { label, edit: undefined, orig: undefined, snap: undefined });
    // Los valores vuelven sin llamar al modelo; el cruce se rehace si hay API key.
    if (hasKey()) {
      begin(); renderResults(false); $('results-t').classList.add('tr-busy');
      try { await crossCheck(); end('field_restored'); } finally { $('results-t').classList.remove('tr-busy'); finish(); }
    }
    renderResults(false);
  }

  function exportCsv() {
    // Prefijo ' contra inyección de fórmulas en Excel.
    const q = v => { let s = String(v ?? ''); if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; return '"' + s.replace(/"/g, '""') + '"'; };
    const head = ['ID', t('tabular.document'), ...runFields.flatMap(f => [f.label, f.label + ' (cita)', f.label + ' (página)', f.label + ' (cita comprobada)', f.label + ' (criticidad)', f.label + ' (confianza)'])];
    const yes = { ok: 'sí', bad: 'no', scan: 'no comprobable', none: '' };
    const body = rows.map(r => [r.id, r.name, ...(r.error ? [t('tabular.failed', { message: r.error })] : runFields.flatMap(f => { const c = r.cells[f.key] || {}; return [c.error ? t('tabular.failed', { message: c.error }) : c.value != null && c.meets === false ? t('tabular.outPrefix') + c.value : c.value ?? t('tabular.missing'), c.quote, c.page, yes[c.check] ?? '', c.risk && c.risk !== 'NONE' ? t('tabular.sevName.' + c.risk) : '', c.confidence]; }))]);
    download(new Blob(['\ufeff' + [head, ...body].map(x => x.map(q).join(';')).join('\r\n')], { type: 'text/csv;charset=utf-8' }), `tabular-review-${runTpl}.csv`);
  }
  function download(blob, name) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }

  // ---- Guardar y cargar análisis (uso sin modelo o sin internet) ----
  async function saveSession() {
    try {
      const docs = await Promise.all(rows.map(async r => ({ id: r.id, name: r.name, error: r.error, cut: r.cut, cells: r.cells, type: r.file ? r.file.type : '', data: r.file ? await b64(r.file) : null })));
      const date = new Date().toISOString();
      download(new Blob([JSON.stringify({ format: 'tabular-review', version: 1, date: (saved && !saved.live && saved.iso) || date, template: runTpl, ...(saved && saved.synthetic ? { synthetic: true } : {}), fields: runFields.map(({ snap, ...f }) => f), rows: docs, cross, stats })], { type: 'application/json' }), `analisis-${runTpl}-${date.slice(0, 10)}.json`);
    } catch (e) { console.error(e); err(t('common.error', { message: e.message })); }
  }
  // El archivo es entrada no fiable: se validan los valores que acaban en HTML o en clases.
  const CHECKS = ['ok', 'bad', 'scan', 'none'];
  const num = (v, max) => { const n = v === null || v === '' || v === undefined ? NaN : Number(v); return Number.isFinite(n) && n >= 0 && n <= max ? n : null; };
  const txt = v => (v == null || v === '' ? null : String(v));
  function cleanCell(c) {
    c = c && typeof c === 'object' ? c : {};
    const value = txt(c.value);
    return { value, quote: txt(c.quote), page: num(c.page, 100000), confidence: num(c.confidence, 100), risk: level(c.risk), check: value === null ? 'none' : CHECKS.includes(c.check) ? c.check : 'bad', error: txt(c.error) || undefined, meets: c.meets === false ? false : undefined };
  }
  const bad = () => new Error(t('tabular.badFormat'));
  function cleanEdit(f) {
    const e = f.edit && typeof f.edit === 'object' && typeof f.edit.text === 'string' && f.edit.text.trim() ? { text: f.edit.text.trim().slice(0, 500), mode: f.edit.mode === 'replace' ? 'replace' : 'add' } : null;
    return e ? { edit: e, orig: { label: String((f.orig && f.orig.label) || f.label || f.key) } } : {};
  }
  function parseSession(text) {
    const d = typeof text === 'string' ? JSON.parse(text) : text;
    if (d.format !== 'tabular-review' || !Array.isArray(d.fields) || !Array.isArray(d.rows) || !d.rows.length) throw bad();
    const flds = d.fields.filter(f => f && typeof f.key === 'string').map(f => ({ key: f.key.replace(/\W/g, '_'), src: f.key, label: String(f.label || f.key), ask: String(f.ask || f.label || ''), custom: !!f.custom, ...cleanEdit(f) }));
    if (!flds.length) throw bad();
    const out = d.rows.map((r, i) => {
      let file = null;
      if (typeof r.data === 'string') file = new File([Uint8Array.from(atob(r.data), c => c.charCodeAt(0))], String(r.name), { type: r.type === 'application/pdf' ? r.type : 'application/octet-stream' });
      return { id: 'D' + (i + 1), name: String(r.name), file, error: txt(r.error), cut: !!r.cut, cells: Object.fromEntries(flds.map(f => [f.key, cleanCell((r.cells || {})[f.src])])) };
    });
    const ids = new Set(out.map(r => r.id));
    let cr = null;
    if (d.cross && d.cross.error) cr = { error: String(d.cross.error) };
    else if (d.cross && Array.isArray(d.cross.alerts)) cr = {
      scope: String(d.cross.scope || ''), summary: (Array.isArray(d.cross.summary) ? d.cross.summary : []).map(String),
      alerts: d.cross.alerts.filter(a => a && typeof a === 'object').map(a => ({ ...a, severity: level(a.severity) === 'NONE' ? 'LOW' : a.severity, docs: (Array.isArray(a.docs) ? a.docs : []).filter(x => ids.has(x)) })),
      conflicts: cleanConflicts(d.cross.conflicts, ids)
    };
    const s = d.stats || {}, when = new Date(d.date);
    return { tpl: T.templates[d.template] ? d.template : 'dd', fields: flds, rows: out, cross: cr, stats: { in: num(s.in, 1e9) || 0, out: num(s.out, 1e9) || 0, s: num(s.s, 1e6) || 0 }, iso: d.date, date: isNaN(when) ? '' : ' (' + when.toLocaleString('es-ES') + ')', synthetic: d.synthetic === true };
  }
  function parseCsvRows(s) {
    s = s.replace(/^\ufeff/, '');
    const first = s.split(/\r?\n/, 1)[0], sep = (first.match(/;/g) || []).length >= (first.match(/,/g) || []).length ? ';' : ',';
    const out = []; let row = [], cell = '', inQ = false;
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (inQ) { if (c === '"') { if (s[i + 1] === '"') { cell += '"'; i++; } else inQ = false; } else cell += c; }
      else if (c === '"') inQ = true;
      else if (c === sep) { row.push(cell); cell = ''; }
      else if (c === '\n') { row.push(cell); out.push(row); row = []; cell = ''; }
      else if (c !== '\r') cell += c;
    }
    if (cell || row.length) { row.push(cell); out.push(row); }
    return out.filter(r => r.some(x => x.trim())).map(r => r.map(x => x.replace(/^'(?=[=+\-@])/, '')));
  }
  function parseCsv(text, name) {
    const [head, ...body] = parseCsvRows(text);
    if (!head || head[0] !== 'ID' || !body.length) throw bad();
    const at = n => head.indexOf(n), flds = [];
    head.forEach((h, i) => { if (i > 1 && head[i + 1] === h + ' (cita)') flds.push({ key: 'c' + i, label: h, ask: h, i, page: i + 2, chk: i + 3, risk: head[i + 4] === h + ' (criticidad)' ? i + 4 : -1, conf: head[i + 5] === h + ' (confianza)' ? i + 5 : -1 }); });
    if (!flds.length || at('ID') !== 0) throw bad();
    const risks = Object.fromEntries(['HIGH', 'MEDIUM', 'LOW'].map(k => [t('tabular.sevName.' + k), k])), checks = { 'sí': 'ok', 'no': 'bad', 'no comprobable': 'scan' };
    const out = body.map((r, i) => {
      const failed = /^Error: /.test(r[2] || '') && r.slice(3).every(x => !x);
      return { id: 'D' + (i + 1), name: r[1] || '', file: null, cut: false, error: failed ? r[2].slice(7) : null, cells: Object.fromEntries(flds.map(f => {
        const v = r[f.i];
        const out = (v || '').startsWith(t('tabular.outPrefix'));
        return [f.key, cleanCell(/^Error: /.test(v || '') ? { error: v.slice(7) } : { meets: out ? false : undefined, value: v === t('tabular.missing') ? null : out ? v.slice(t('tabular.outPrefix').length) : v, quote: r[f.i + 1], page: r[f.page], check: checks[r[f.chk]], risk: risks[r[f.risk]], confidence: r[f.conf] })];
      })) };
    });
    const m = Object.keys(T.templates).find(k => name.includes(k));
    return { tpl: m || 'dd', fields: flds.map(f => ({ key: f.key, label: f.label, ask: f.ask })), rows: out, cross: null, stats: { in: 0, out: 0, s: 0 }, date: '' };
  }
  async function loadSaved(file) {
    try {
      const buf = await file.arrayBuffer();
      let text;
      // Excel puede volver a guardar el CSV en Windows-1252.
      try { text = new TextDecoder('utf-8', { fatal: true }).decode(buf); } catch (e) { text = new TextDecoder('windows-1252').decode(buf); }
      show(/\.json$/i.test(file.name) ? parseSession(text) : parseCsv(text, file.name), file.name);
    } catch (e) { console.error(e); err(t('tabular.badFile', { name: file.name, message: e.message })); }
  }
  // Pinta un análisis cargado (archivo guardado o demo sin conexión) sin llamar al modelo.
  function show(d, name) {
    releaseUrls();
    rows = d.rows.map(r => ({ ...r, url: r.file ? URL.createObjectURL(r.file) : null }));
    runFields = d.fields; runTpl = d.tpl; cross = d.cross; stats = d.stats;
    saved = { name, date: d.date, iso: d.iso, live: false, synthetic: !!d.synthetic };
    files = rows.every(r => r.file) ? rows.map(r => r.file) : [];
    customN = Math.max(customN, ...d.fields.map(f => +(/^custom_(\d+)$/.exec(f.key) || [0, 0])[1]));
    tplKey = d.tpl;
    fields = files.length ? d.fields.map(f => ({ ...f })) : T.templates[tplKey].fields.map(f => ({ ...f }));
    err(''); renderConfig(); renderFiles(); renderResults(true);
  }
  // Demo sin conexión (js/demo-offline.js): recibe el análisis ya cargado en memoria.
  window.TabularReview = {
    busy: () => running,
    loadSession(data, name) {
      if (running) return false;
      try { show(parseSession(data), name); return true; }
      catch (e) { console.error(e); err(t('tabular.badFile', { name, message: e.message })); return false; }
    }
  };

  // ---- Eventos ----
  const dz = $('drop-zone-t');
  dz.addEventListener('click', () => $('file-input-t').click());
  dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('over'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('over'));
  dz.addEventListener('drop', e => { e.preventDefault(); dz.classList.remove('over'); addFiles(e.dataTransfer.files); });
  $('file-input-t').addEventListener('click', e => e.stopPropagation());
  $('file-input-t').addEventListener('change', e => { addFiles(e.target.files); e.target.value = ''; });
  $('tr-templates').addEventListener('click', e => { const b = e.target.closest('[data-k]'); if (b && !running) setTemplate(b.dataset.k); });
  $('tr-fields').addEventListener('click', e => { if (e.target.dataset.i != null && !running) { fields.splice(+e.target.dataset.i, 1); renderConfig(); } });
  $('tr-files').addEventListener('click', e => { if (e.target.dataset.i != null && !running) { files.splice(+e.target.dataset.i, 1); renderFiles(); } });
  $('tr-add').addEventListener('click', addAndAnalyze);
  $('tr-new').addEventListener('keydown', e => { if (e.key === 'Enter') addAndAnalyze(); });
  $('tr-clear').addEventListener('click', () => { if (running) return; releaseUrls(); files = []; rows = []; cross = null; saved = null; $('results-t').classList.remove('show'); err(''); renderFiles(); });
  $('btn-run-t').addEventListener('click', run);
  $('tr-export').addEventListener('click', exportCsv);
  $('tr-save').addEventListener('click', saveSession);
  $('tr-load').addEventListener('click', () => { if (!running) $('tr-load-input').click(); });
  $('tr-load-input').addEventListener('change', e => { const f = e.target.files[0]; e.target.value = ''; if (f && !running) loadSaved(f); });
  $('api-key').addEventListener('input', sync);
  $('tr-table').addEventListener('click', e => {
    const b = e.target.closest('.tr-cell'); if (b) { openCell(b.dataset.r, b.dataset.f); return; }
    const h = e.target.closest('.tr-th'); if (h) { openEditor(h.dataset.k); return; }
    const a = e.target.closest('.tr-ed [data-act]'); if (a) a.dataset.act === 'restore' ? restoreColumn(editing) : closeEditor();
  });
  $('tr-table').addEventListener('submit', e => { e.preventDefault(); applyEdit(e.target); });
  $('tr-table').addEventListener('keydown', e => {
    const form = e.target.closest('.tr-ed'); if (!form) return;
    if (e.key === 'Escape') { e.preventDefault(); closeEditor(); }
    else if (e.key === 'Enter' && !e.shiftKey && e.target.tagName === 'TEXTAREA') { e.preventDefault(); form.requestSubmit(); }
  });
  $('tr-alerts').addEventListener('click', e => {
    const c = e.target.closest('.tr-claim[data-r]'); if (c) { openCell(c.dataset.r, c.dataset.f); return; }
    const d = (e.target.closest('[data-doc]') || {}).dataset?.doc; if (!d) return;
    const row = $('tr-row-' + d); row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    row.classList.add('hit'); setTimeout(() => row.classList.remove('hit'), 2000);
  });
  $('tr-close').addEventListener('click', () => $('tr-dlg').close());
  $('tr-dlg').addEventListener('click', e => {
    const c = e.target.closest('#tr-ctx');
    if (c) openContext(c.dataset.r, c.dataset.f);
  });
  setTemplate('dd'); renderFiles();
})();
