// Ver en contexto: panel lateral con el PDF, las citas resaltadas y la lista de campos extraídos.
// Depende de los helpers globales de la página: $, t, pdfjsLib. Uso: PdfContext.open(doc, items, key).
(function () {
  const ZOOM = { min: .5, max: 3, step: 1.25 }, MAX_DPR = 2, PAGE_MAX = 900;
  const MARK = { ok: '✓', bad: '!', scan: '?' };
  const dlg = $('ctx'), view = $('ctx-view'), list = $('ctx-list'), note = $('ctx-note');
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  let seq = 0, st = null; // seq descarta cargas de un documento que ya se ha cerrado

  // ---- Localización de citas ----
  // Se ignoran espacios, comillas y guiones: PDF.js parte el texto en fragmentos arbitrarios.
  const SKIP = /[\s«»“”"'’‘\-‐‑­]/g;
  const fold = s => s.normalize('NFKC').toLowerCase().replace(SKIP, '');
  const isWord = c => !!c && /[\p{L}\p{N}]/u.test(c);

  function indexPage(chars, items, p) {
    items.forEach((it, i) => {
      for (let o = 0; o < it.str.length;) {
        const raw = String.fromCodePoint(it.str.codePointAt(o)), f = fold(raw);
        if (f) for (const ch of f.split('')) chars.push({ ch, p, i, o, n: raw.length, sep: chars.sep });
        chars.sep = !f;
        o += raw.length;
      }
      chars.sep = true;
    });
  }
  function locate(quote, page) {
    const q = fold(String(quote || ''));
    if (q.length < 4) return null;
    let best = null;
    for (let at = st.text.indexOf(q); at >= 0; at = st.text.indexOf(q, at + 1)) {
      const a = st.chars[at], prev = st.chars[at - 1], next = st.chars[at + q.length];
      const bounded = (a.sep || !prev || !isWord(prev.ch) || !isWord(a.ch)) && (!next || next.sep || !isWord(next.ch) || !isWord(q[q.length - 1]));
      const score = (a.p + 1 === page ? 2 : 0) + (bounded ? 1 : 0);
      if (!best || score > best.score) best = { at, score };
    }
    return best && st.chars.slice(best.at, best.at + q.length);
  }

  const pen = document.createElement('canvas').getContext('2d');
  // Rectángulos en tanto por uno de la página, para que no dependan del zoom.
  function rects(hit) {
    const runs = [];
    hit.forEach(c => {
      const r = runs[runs.length - 1];
      if (r && r.p === c.p && r.i === c.i) r.to = c.o + c.n; else runs.push({ p: c.p, i: c.i, from: c.o, to: c.o + c.n });
    });
    const out = [];
    runs.forEach(r => {
      const pg = st.pages[r.p], it = pg.items[r.i], vp = pg.vp, [a, b, c, d, x, y] = it.transform;
      pen.font = `100px ${(pg.styles[it.fontName] || {}).fontFamily || 'sans-serif'}`;
      const full = pen.measureText(it.str).width || 1, w = n => pen.measureText(it.str.slice(0, n)).width / full * it.width;
      const len = Math.hypot(a, b) || 1, h = Math.hypot(c, d) || it.height, ux = a / len, uy = b / len;
      const pts = [[w(r.from), -.22 * h], [w(r.to), -.22 * h], [w(r.from), .88 * h], [w(r.to), .88 * h]]
        .map(([s, v]) => vp.convertToViewportPoint(x + ux * s - uy * v, y + uy * s + ux * v));
      const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
      const box = { p: r.p, l: Math.min(...xs) / vp.width, t: Math.min(...ys) / vp.height, r: Math.max(...xs) / vp.width, b: Math.max(...ys) / vp.height };
      const last = out[out.length - 1], bh = box.b - box.t;
      // Une los fragmentos contiguos de una misma línea.
      if (last && last.p === box.p && Math.abs(last.b - box.b) < bh * .3 && box.l >= last.l && (box.l - last.r) * vp.width < bh * vp.height) {
        last.r = Math.max(last.r, box.r); last.t = Math.min(last.t, box.t); last.b = Math.max(last.b, box.b);
      } else out.push(box);
    });
    return out;
  }

  // ---- Páginas ----
  async function paint(pg) {
    if (pg.task || pg.done) return;
    const w = pg.el.clientWidth, vp = pg.page.getViewport({ scale: w / pg.vp.width * Math.min(window.devicePixelRatio || 1, MAX_DPR) });
    pg.canvas.width = vp.width; pg.canvas.height = vp.height;
    const task = pg.task = pg.page.render({ canvasContext: pg.canvas.getContext('2d'), viewport: vp });
    try { await task.promise; if (pg.task === task) pg.done = true; }
    catch (e) { if (e.name !== 'RenderingCancelledException') console.error(e); }
    finally { if (pg.task === task) pg.task = null; }
  }
  function wipe(pg) {
    if (pg.task) { pg.task.cancel(); pg.task = null; }
    pg.done = false;
    // Un lienzo por dibujado: PDF.js no admite dos a la vez sobre el mismo.
    const c = document.createElement('canvas'); c.width = c.height = 0;
    pg.canvas.replaceWith(c); pg.canvas = c;
  }
  function layout() {
    const w = Math.min(PAGE_MAX, Math.max(200, view.clientWidth - 40)) * st.zoom;
    st.pages.forEach(pg => { pg.el.style.width = w + 'px'; pg.el.style.aspectRatio = `${pg.vp.width} / ${pg.vp.height}`; });
  }
  function relayout(zoom) {
    if (!st || !st.ready) return;
    const n = current(), el = st.pages[n].el, f = (view.scrollTop - el.offsetTop) / el.offsetHeight;
    st.zoom = zoom; layout();
    view.scrollTop = el.offsetTop + f * el.offsetHeight;
    st.pages.forEach(pg => { if (pg.task || pg.done) wipe(pg); if (pg.seen) paint(pg); });
    pageLabel();
  }
  function current() {
    const mid = view.scrollTop + view.clientHeight / 2;
    let n = 0;
    st.pages.forEach((pg, i) => { if (pg.el.offsetTop <= mid) n = i; });
    return n;
  }
  function pageLabel() {
    if (!st || !st.ready) return;
    $('ctx-page').textContent = t('tabular.ctxPage', { n: current() + 1, total: st.pages.length });
    $('ctx-out').disabled = st.zoom <= ZOOM.min; $('ctx-in').disabled = st.zoom >= ZOOM.max;
  }

  // ---- Lista de campos ----
  function renderList() {
    list.innerHTML = st.items.map((it, i) => {
      const off = it.value == null;
      const val = it.error ? t('tabular.failed', { message: it.error }) : off ? t('tabular.missing') : it.value;
      return `<button type="button" class="ctx-item r-${it.risk}" data-i="${i}" ${off ? 'disabled' : ''}><span class="ctx-top"><span class="tr-lbl">${esc(it.label)}</span>${!off && it.page != null ? `<span class="ctx-pg">${esc(t('tabular.ctxShort', { n: it.page }))}</span>` : ''}</span>` +
        `<span class="ctx-val">${it.risk !== 'NONE' && !off ? `<i class="dot ${it.risk}" title="${esc(t('tabular.sevName.' + it.risk))}"></i>` : ''}${esc(val)}${MARK[it.check] ? ` <i class="q-${it.check}" title="${esc(t('tabular.legendQuote.' + it.check))}">${MARK[it.check]}</i>` : ''}</span></button>`;
    }).join('');
  }
  function select(i, scroll) {
    const it = st.items[i];
    if (!it || it.value == null) return;
    st.active = i;
    list.querySelectorAll('.ctx-item').forEach((el, n) => { el.classList.toggle('on', n === i); if (n === i) { el.setAttribute('aria-current', 'true'); el.scrollIntoView({ block: 'nearest' }); } else el.removeAttribute('aria-current'); });
    view.querySelectorAll('.ctx-hl').forEach(el => el.classList.toggle('on', +el.dataset.i === i));
    if (!st.ready) return;
    const hl = view.querySelector('.ctx-hl.on'), pg = it.page && st.pages[it.page - 1];
    note.textContent = hl ? '' : t(!pg ? 'tabular.ctxNowhere' : it.check === 'scan' ? 'tabular.ctxScan' : 'tabular.ctxNoQuote');
    if (!scroll) return;
    const box = (hl || (pg && pg.el));
    if (!box) return;
    const v = view.getBoundingClientRect(), b = box.getBoundingClientRect();
    view.scrollTo({
      top: view.scrollTop + b.top - v.top - (hl ? (v.height - b.height) / 2 : 12),
      left: view.scrollLeft + (hl ? b.left + b.width / 2 - v.left - v.width / 2 : 0),
      behavior: scroll === 'smooth' && !matchMedia('(prefers-reduced-motion: reduce)').matches ? 'smooth' : 'auto'
    });
  }

  // ---- Apertura y cierre ----
  async function load(doc, my) {
    if (!pdfjsLib) throw new Error(t('common.pdfLoading'));
    // isEvalSupported: evita la ejecución de código en PDF manipulados (CVE-2024-4367).
    const pdf = await pdfjsLib.getDocument({ data: await doc.file.arrayBuffer(), isEvalSupported: false }).promise;
    if (my !== seq) { pdf.destroy(); return; }
    st.pdf = pdf;
    const chars = [], pages = [];
    chars.sep = true;
    for (let n = 1; n <= pdf.numPages; n++) {
      const page = await pdf.getPage(n), c = await page.getTextContent();
      if (my !== seq) return;
      const items = c.items.filter(x => x.str);
      indexPage(chars, items, n - 1);
      pages.push({ page, items, styles: c.styles, vp: page.getViewport({ scale: 1 }) });
    }
    st.pages = pages; st.chars = chars; st.text = chars.map(c => c.ch).join('');
    view.innerHTML = '';
    pages.forEach((pg, n) => {
      pg.el = document.createElement('div'); pg.el.className = 'ctx-sheet'; pg.el.setAttribute('aria-label', t('tabular.ctxPage', { n: n + 1, total: pages.length }));
      pg.canvas = document.createElement('canvas'); pg.canvas.width = pg.canvas.height = 0;
      pg.el.append(pg.canvas); view.append(pg.el);
    });
    st.items.forEach((it, i) => {
      const hit = it.value != null && it.check === 'ok' ? locate(it.quote, it.page) : null;
      if (!hit) return;
      it.page = hit[0].p + 1;
      rects(hit).forEach(r => {
        const el = document.createElement('div');
        el.className = 'ctx-hl'; el.dataset.i = i; el.title = it.label;
        el.style.cssText = `left:${r.l * 100}%;top:${r.t * 100}%;width:${(r.r - r.l) * 100}%;height:${(r.b - r.t) * 100}%`;
        pages[r.p].el.append(el);
      });
    });
    st.ready = true;
    layout();
    st.io = new IntersectionObserver(es => es.forEach(e => {
      const pg = pages.find(x => x.el === e.target);
      pg.seen = e.isIntersecting;
      if (pg.seen) paint(pg); else wipe(pg);
    }), { root: view, rootMargin: '600px 0px' });
    renderList(); select(st.active, 'jump');
    pages.forEach(pg => st.io.observe(pg.el));
    pageLabel();
    const on = list.querySelector('.ctx-item.on'); if (on) on.focus({ preventScroll: true });
  }
  async function open(doc, items, key) {
    cleanup();
    const my = seq;
    st = { items: items.map(x => ({ ...x })), active: Math.max(0, items.findIndex(x => x.key === key)), zoom: 1, pages: [], ready: false };
    $('ctx-id').textContent = doc.id; $('ctx-name').textContent = doc.name;
    $('ctx-dl').href = doc.url; $('ctx-dl').download = doc.name;
    $('ctx-page').textContent = ''; note.textContent = '';
    view.innerHTML = `<p class="ctx-msg">${esc(t('tabular.ctxLoading'))}</p>`;
    renderList(); if (!dlg.open) dlg.showModal(); select(st.active);
    try { await load(doc, my); }
    catch (e) { if (my === seq) { console.error(e); view.innerHTML = `<p class="ctx-msg tr-warn">${esc(t('tabular.ctxFailed', { message: e.message }))}</p>`; } }
  }
  function cleanup() {
    seq++;
    if (!st) return;
    if (st.io) st.io.disconnect();
    if (st.pdf) st.pdf.destroy();
    st = null; view.innerHTML = ''; list.innerHTML = '';
  }
  // 'close' es asíncrono: si ya se ha abierto otro documento, no hay que limpiarlo.
  dlg.addEventListener('close', () => { if (!dlg.open) cleanup(); });
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
  $('ctx-close').addEventListener('click', () => dlg.close());
  $('ctx-in').addEventListener('click', () => st && relayout(Math.min(ZOOM.max, st.zoom * ZOOM.step)));
  $('ctx-out').addEventListener('click', () => st && relayout(Math.max(ZOOM.min, st.zoom / ZOOM.step)));
  list.addEventListener('click', e => { const b = e.target.closest('.ctx-item'); if (b) select(+b.dataset.i, 'smooth'); });
  view.addEventListener('click', e => { const h = e.target.closest('.ctx-hl'); if (h) select(+h.dataset.i); });
  view.addEventListener('scroll', pageLabel, { passive: true });
  window.addEventListener('resize', () => st && relayout(st.zoom));

  window.PdfContext = { open, supports: r => !!r.file && /\.pdf$/i.test(r.name) };
})();
