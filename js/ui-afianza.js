// Piezas de presentación comunes a los tres tabs originales en index.html.
window.AF = (function () {
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const list = v => (Array.isArray(v) ? v : []).filter(x => x && (typeof x === 'object' || String(x).trim()));
  const ORDER = { critical: 0, high: 1, medium: 2, low: 3 };
  const name = c => t('fraud.sevN.' + c);
  const tag = (c, label) => `<span class="fr-tag ${c}">${esc(label || name(c))}</span>`;
  const empty = m => `<p class="fr-none">${esc(m)}</p>`;
  const bullets = rows => `<ul class="fr-ul">${rows.filter(r => r[1]).map(([k, v]) => `<li><b>${esc(k)}:</b> ${esc(v)}</li>`).join('')}</ul>`;
  const item = (c, title, meta, rows, label) => `<div class="fr-item ${c}"><div class="fr-hd">${tag(c, label)}<b>${esc(title || '—')}</b>${meta ? `<span class="fr-meta">${esc(meta)}</span>` : ''}</div>${bullets(rows)}</div>`;
  const points = s => Array.isArray(s) ? s.map(String).filter(x => x.trim()) : String(s || '').split(/(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑÄÖÜ¿¡])/).filter(x => x.trim());
  const score = v => Math.max(0, Math.min(100, Math.round(Number(v)) || 0));
  const bySev = arr => arr.map((x, i) => ({ ...x, i })).sort((a, b) => ORDER[a.c] - ORDER[b.c] || (b.n || 0) - (a.n || 0) || a.i - b.i);
  const ul = (cls, arr) => `<ul class="${cls}">${arr.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
  const ol = v => { const a = list(v); return a.length ? `<ol class="fr-ol">${a.map(x => `<li>${esc(x)}</li>`).join('')}</ol>` : empty('—'); };
  const row = (label, v, cls) => `<div class="fr-row"><span>${esc(label)}</span><div class="fr-bar"><i class="${cls}" style="width:${v}%"></i></div><b>${v}%</b></div>`;
  function summary(scope, s) {
    const title = `${t('fraud.sumTitle')} ${scope || ''}`;
    return `<h2 class="tr-title" title="${esc(title)}">${esc(title)}</h2>${ul('tr-bullets', points(s))}`;
  }
  function legend(arr, caption) {
    const keys = ['critical', 'high', 'medium', 'low'].filter(k => k !== 'critical' || arr.some(x => x.c === k));
    return `<div class="fr-legend"><span class="tr-lbl">${esc(caption)}</span>${keys.map(k => `<span class="tr-key"><i class="dot ${k.toUpperCase()}"></i>${name(k)} <b>${arr.filter(x => x.c === k).length}</b></span>`).join('')}</div>`;
  }
  // Los <p> originales no admiten listas dentro.
  const toDiv = id => { const o = document.getElementById(id), d = document.createElement('div'); d.id = id; o.replaceWith(d); return d; };
  function show(id, silent) {
    document.getElementById(id).classList.add('show');
    if (!silent) document.getElementById(id).scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  return { esc, list, tag, empty, bullets, item, points, score, bySev, ul, ol, row, summary, legend, toDiv, show };
})();
