// Sustituto mínimo de i18next para arrancar sin internet. Solo actúa si la CDN no ha cargado.
(function () {
  if (window.i18next) return;
  let cfg = {}, cur = 'es';
  const subs = [];
  const look = (l, k) => k.split('.').reduce((o, p) => (o == null ? o : o[p]), (cfg.resources[l] || {}).translation);
  window.i18next = {
    get resolvedLanguage() { return cur; },
    init(c) { cfg = c; cur = c.lng || c.fallbackLng; },
    on(ev, fn) { if (ev === 'languageChanged') subs.push(fn); },
    changeLanguage(l) { cur = l; subs.forEach(f => f(l)); },
    t(k, o = {}) {
      const v = look(cur, k) ?? look(cfg.fallbackLng, k) ?? o.defaultValue ?? k;
      return typeof v === 'string' ? v.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, n) => o[n] ?? '') : k;
    }
  };
})();
