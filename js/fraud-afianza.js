// Presentación de Fraude & Riesgo para index.html. Sustituye a renderFraud de la página.
(function () {
  const { esc, list, empty, bullets, item, points, score, bySev, ul, ol, row, summary, legend, toDiv, show } = AF;
  const W = { critical: 3, high: 3, medium: 2, low: 1 };
  // Criticidad del riesgo: probabilidad × impacto (1-9).
  function rate(r) {
    const p = W[sevClass(r.probability)], m = W[sevClass(r.impact)], n = p * m;
    return { n: n + m / 10, c: n >= 6 ? 'high' : n >= 3 ? 'medium' : 'low' };
  }
  const band = v => v >= 75 ? 'high' : v >= 40 ? 'medium' : 'low';
  toDiv('r-summary-body');

  window.renderFraud = function (d, silent) {
    lastFraud = d;
    $('r-icon').textContent = d.case_icon || '📄';
    $('r-type').textContent = d.case_type || '—';
    $('r-summary-body').innerHTML = summary(d.scope || d.case_type, d.summary);

    const fr = d.fraud_risk || {}, cls = sevClass(fr.risk_level || 'MINIMAL'), total = score(fr.overall_score);
    $('r-score-banner').innerHTML = `<div class="fr-score ${cls}"><div class="fr-num">${total}<small>/ 100</small></div><div class="fr-score-b"><b>${t('risk.' + cls)}</b><div class="fr-bar"><i class="${cls}" style="width:${total}%"></i></div>${ul('fr-ul', points(fr.risk_description))}</div></div>`;
    const inds = bySev(list(fr.indicators).map(x => ({ ...x, c: sevClass(x.severity) })));
    $('r-indicators-body').innerHTML = `<h3 class="fr-sub">${t('fraud.signals', { n: inds.length })}</h3>` + (inds.map(x => item(x.c, x.signal, '', [[t('fraud.what'), x.description], [t('fraud.evidence'), x.evidence]])).join('') || empty(t('fraud.noSignals')));

    $('r-anomalies-body').innerHTML = list(d.anomalies).map(a => `<div class="fr-item"><div class="fr-hd"><b>⚠ ${esc(a.type || t('fraud.anomaly'))}</b></div>${bullets([[t('fraud.what'), a.description], [t('fraud.deviation'), a.deviation]])}</div>`).join('') || empty(t('fraud.noAnomalies'));

    const reg = bySev(list(d.risk_register).map(x => ({ ...x, ...rate(x) })));
    $('r-register-body').innerHTML = reg.length ? legend(reg, t('fraud.levelHelp')) + reg.map(x => item(x.c, x.title, tEnum('riskCat', x.category), [[t('fraud.risk'), x.description], [t('fraud.probability'), tEnum('level', x.probability)], [t('fraud.impact'), tEnum('level', x.impact)], [t('fraud.mitigation'), x.mitigation]])).join('') : empty(t('fraud.noRisks'));

    const mx = d.risk_matrix || {};
    $('r-matrix-body').innerHTML = ['legal', 'financial', 'operational', 'reputational', 'regulatory'].map(k => ({ k, v: score(mx[k]) })).sort((a, b) => b.v - a.v).map(({ k, v }) => row(t('fraud.matrix.' + k), v, band(v))).join('');
    $('r-actions-body').innerHTML = ol(d.recommended_actions);
    show('results-r', silent);
  };
})();
