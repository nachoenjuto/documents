// i18n bootstrap: i18next with resources from locales/*.js and prompts from prompts/*.js.
// Resources are plain scripts (not JSON) so the page also works when opened via file://.
(function () {
  const SUPPORTED = ['es', 'en', 'de'];
  const FALLBACK = 'es';
  const STORAGE_KEY = 'aiucs.lang';

  function pick(l) {
    const base = (l || '').toLowerCase().split('-')[0];
    return SUPPORTED.includes(base) ? base : null;
  }

  function detect() {
    const fromUrl = pick(new URLSearchParams(location.search).get('lang'));
    if (fromUrl) return fromUrl;
    try { const stored = pick(localStorage.getItem(STORAGE_KEY)); if (stored) return stored; } catch (e) { }
    for (const l of navigator.languages || [navigator.language]) { const p = pick(l); if (p) return p; }
    return FALLBACK;
  }

  function store(l) { try { localStorage.setItem(STORAGE_KEY, l); } catch (e) { } }

  const resources = {};
  SUPPORTED.forEach(l => { resources[l] = { translation: (window.I18N || {})[l] || {} }; });

  i18next.init({
    lng: detect(),
    fallbackLng: FALLBACK,
    supportedLngs: SUPPORTED,
    resources,
    interpolation: { escapeValue: false },
    initImmediate: false
  });

  window.t = (key, opts) => i18next.t(key, opts);
  // Enum codes returned by the model are language-neutral; only their labels are translated.
  window.tEnum = (group, code) => code ? i18next.t(`enum.${group}.${String(code).toUpperCase()}`, { defaultValue: String(code) }) : '';
  window.getPrompts = () => (window.PROMPTS || {})[i18next.resolvedLanguage] || window.PROMPTS[FALLBACK];

  function applyTranslations(root) {
    root = root || document;
    root.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    root.querySelectorAll('[data-i18n-html]').forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
    root.querySelectorAll('[data-i18n-placeholder]').forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    root.querySelectorAll('[data-i18n-aria]').forEach(el => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
    root.querySelectorAll('[data-i18n-sub]').forEach(el => { el.dataset.sub = t(el.dataset.i18nSub); });
    document.documentElement.lang = i18next.resolvedLanguage;
    document.title = t('meta.title');
  }

  // ---- Header language menu ----
  function setupMenu() {
    const menu = document.getElementById('lang-menu');
    const btn = document.getElementById('lang-btn');
    const list = document.getElementById('lang-list');
    if (!menu) return;

    const open = v => { menu.classList.toggle('open', v); btn.setAttribute('aria-expanded', String(v)); };
    const refresh = () => {
      const cur = i18next.resolvedLanguage;
      document.getElementById('lang-current').textContent = cur.toUpperCase();
      list.querySelectorAll('[data-lang]').forEach(li => li.setAttribute('aria-selected', String(li.dataset.lang === cur)));
    };

    btn.addEventListener('click', e => { e.stopPropagation(); open(!menu.classList.contains('open')); });
    list.querySelectorAll('[data-lang]').forEach(li => {
      li.addEventListener('click', () => { window.setLanguage(li.dataset.lang); open(false); btn.focus(); });
      li.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); li.click(); } });
    });
    document.addEventListener('click', e => { if (!menu.contains(e.target)) open(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') open(false); });
    i18next.on('languageChanged', refresh);
    refresh();
  }

  window.setLanguage = l => {
    if (!pick(l)) return;
    store(l);
    i18next.changeLanguage(l);
  };

  i18next.on('languageChanged', () => applyTranslations());

  document.addEventListener('DOMContentLoaded', () => { applyTranslations(); setupMenu(); });
})();
