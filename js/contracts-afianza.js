// Presentación de Contratos & Compliance para index.html. Sustituye a renderContracts.
(function () {
  const { esc, list, tag, empty, item, score, bySev, ol, row, summary, legend, toDiv, show } = AF;
  toDiv('c-summary-body');
  window.renderContracts = function (d, silent) {
    lastContracts = d;
    $('c-icon').textContent = d.document_icon || '📄';
    $('c-type').textContent = d.document_type || '—';
    const cmp = d.mode === 'comparison' && d.comparison ? d.comparison : null;
    $('c-mode-badge').textContent = t(cmp ? 'contracts.modeComparison' : 'contracts.modeSingle');
    $('c-summary-body').innerHTML = summary(d.scope || d.document_type, d.summary);

    const cl = bySev(list(d.clauses).map(x => ({ ...x, c: sevClass(x.risk_level) })));
    $('c-clauses-body').innerHTML = cl.length ? legend(cl, t('fraud.level')) + cl.map(x => item(x.c, x.title, [tEnum('clause', x.category), x.source ? `${t('contracts.docShort')} ${x.source}` : ''].filter(Boolean).join(' · '), [[t('contracts.says'), x.description]])).join('') : empty(t('contracts.noClauses'));

    $('c-comparison-divider').style.display = cmp ? 'flex' : 'none';
    $('c-comparison-card').style.display = cmp ? 'block' : 'none';
    if (cmp) {
      const v = score(cmp.alignment_score), ds = bySev(list(cmp.discrepancies).map(x => ({ ...x, c: sevClass(x.severity) })));
      $('c-align-val').textContent = v + '%';
      $('c-align-fill').dataset.t = v; $('c-align-fill').style.width = v + '%';
      $('c-comparison-body').innerHTML = (cmp.alignment_summary ? `<p class="fr-lead">${esc(cmp.alignment_summary)}</p>` : '') + (ds.length ? legend(ds, t('fraud.level')) + ds.map(x => `<div class="fr-item ${x.c}"><div class="fr-hd">${tag(x.c)}<b>${esc(tEnum('clause', x.clause_category) || '—')}</b></div>
        <div class="fr-ab"><div><span class="tr-lbl">${t('contracts.documentA')}</span><p>${esc(x.doc_a_summary || '—')}</p></div><div><span class="tr-lbl">${t('contracts.documentB')}</span><p>${esc(x.doc_b_summary || '—')}</p></div></div>
        ${x.recommendation ? AF.bullets([[t('contracts.rec'), x.recommendation]]) : ''}</div>`).join('') : empty(t('contracts.noDiscrepancies')));
    }

    const cr = bySev(list(d.compliance_risks).map(x => ({ ...x, c: sevClass(x.severity) })));
    $('c-compliance-body').innerHTML = cr.length ? legend(cr, t('fraud.level')) + cr.map(x => item(x.c, tEnum('compliance', x.category), '', [[t('fraud.risk'), x.description], [t('contracts.regulation'), x.regulation_reference]])).join('') : empty(t('contracts.noCompliance'));

    // El estado no es criticidad: se ordena por cercanía de la obligación y se muestra su nombre.
    const st = { IN_FORCE: 0, UPCOMING: 1, PENDING: 2 };
    const rg = list(d.regulatory_alerts).slice().sort((a, b) => (st[a.status] ?? 3) - (st[b.status] ?? 3));
    $('c-regulatory-body').innerHTML = rg.map(x => item('info', x.regulation, tEnum('jurisdiction', x.jurisdiction), [[t('contracts.why'), x.relevance], [t('contracts.action'), x.action_required]], tEnum('status', x.status) || '—')).join('') || empty(t('contracts.noRegulatory'));

    const dd = d.due_diligence_score || {};
    $('c-dd-body').innerHTML = ['overall', 'legal', 'financial', 'operational', 'reputational'].map(k => row(t('contracts.dd.' + k), score(dd[k]), 'plain')).join('');
    $('c-recs-body').innerHTML = ol(d.recommendations);
    show('results-c', silent);
  };
})();
