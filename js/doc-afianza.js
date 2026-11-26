// Presentación de Document Intelligence para index.html. Sustituye a render.
(function () {
  const { esc, list, empty, item, points, score, bySev, ul, row, summary, legend, toDiv, show } = AF;
  const sum = toDiv('summary-body'), grid = sum.closest('.g2');
  grid.classList.add('af-stack'); grid.prepend(sum.closest('.card'));
  const ok = v => v && v !== 'null' && v !== 'No detectado';
  const taxo = (arr, meta) => `<ul class="fr-ul fr-taxo">${arr.slice().sort((a, b) => score(b.confidence) - score(a.confidence)).map(x => `<li><b>${esc(x.label_local || x.label_es || x.label)}</b> <span class="fr-pct">${score(x.confidence)}%</span><small>${esc(meta(x).filter(Boolean).join(' · '))}</small></li>`).join('')}</ul>`;

  window.render = function (d, silent) {
    lastDoc = d;
    $('d-icon').textContent = d.document_icon || '📄';
    $('d-type').textContent = d.document_type || '—';
    $('d-tags').innerHTML = list(d.document_tags).slice(0, 4).map(x => `<span class="doc-tag">${esc(x)}</span>`).join('');
    sum.innerHTML = summary(d.scope || d.document_type, d.summary);

    const m = d.metadata || {};
    $('meta-body').innerHTML = [['title', m.title], ['author', m.author], ['date', m.date], ['language', m.language], ['organization', m.organization], ['pages', m.pages_estimated]].filter(x => ok(x[1]))
      .map(([k, v]) => `<div class="meta-row"><span class="mk">${t('doc.field.' + k)}</span><span class="mv">${esc(v)}</span></div>`).join('');

    const ner = d.ner || {};
    const groups = [['persons', 'p', '👤'], ['organizations', 'o', '🏢'], ['locations', 'l', '📍'], ['other', 'x', '🔖']].map(([k, c, i]) => ({ k, c, i, a: list(ner[k]).slice().sort((x, y) => (Number(y.mentions) || 0) - (Number(x.mentions) || 0)) })).filter(g => g.a.length);
    $('ner-body').innerHTML = groups.length ? `<div class="fr-ner">${groups.map(g => `<div><h3 class="fr-sub" style="color:var(--n${g.c})">${g.i} ${t('doc.ner.' + g.k)} (${g.a.length})</h3><ul class="fr-ul">${g.a.map(x => `<li><b>${esc(x.name)}</b>${x.role || x.type ? ` · ${esc(x.role || x.type)}` : ''}${Number(x.mentions) > 1 ? ` <span class="fr-pct">×${Number(x.mentions)}</span>` : ''}</li>`).join('')}</ul></div>`).join('')}</div>` : empty(t('doc.noEntities'));

    const ip = list(d.iptc_topics);
    $('iptc-tags').innerHTML = ip.length ? taxo(ip, x => [x.path, x.code]) : empty(t('common.notApplicable'));
    const sec = d.secondary_taxonomy || {}, si = sec.type && sec.type !== 'NONE' ? list(sec.items) : [];
    $('sec-taxo-title').textContent = si.length && sec.label ? sec.label : t('doc.secondaryTaxonomy');
    $('sec-tags').innerHTML = si.length ? taxo(si, x => [x.domain, x.code]) : empty(t('doc.secondaryNotApplicable'));

    const pii = d.pii || {}, lvl = String(pii.overall_risk || 'NONE').toUpperCase(), cls = sevClass(lvl);
    const pi = bySev(list(pii.items).map(x => ({ ...x, c: sevClass(x.severity) })));
    $('pii-body').innerHTML = (lvl !== 'NONE' ? `<div class="fr-score ${cls}"><div class="fr-score-b"><b>${t('risk.' + cls)}</b>${ul('fr-ul', points(pii.risk_description))}</div></div>` : '') +
      (pi.length ? `<div style="margin-top:16px">${legend(pi, t('fraud.level'))}</div>` + pi.map(x => item(x.c, tEnum('pii', x.category), '', [[t('doc.datum'), x.description], [t('doc.example'), x.example], [t('doc.gdpr'), x.gdpr_basis]])).join('') : empty(t('doc.noPii')));

    const cs = d.confidence_scores || {};
    $('conf-body').innerHTML = [['metadata', t('doc.conf.metadata')], ['ner', t('doc.conf.ner')], ['iptc', t('doc.conf.iptc')], ['secondary_taxonomy', sec.label || t('doc.conf.secondary')], ['pii', t('doc.conf.pii')]].map(([k, l]) => ({ l, v: score(cs[k]) })).sort((a, b) => b.v - a.v).map(x => row(x.l, x.v, 'plain')).join('');
    show('results', silent);
  };
})();
