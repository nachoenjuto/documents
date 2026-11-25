// Ajuste de los tres prompts originales solo para index_afianza.html (castellano): resumen en puntos y alcance breve.
// En EN/DE se mantienen los prompts comunes y la interfaz separa el resumen por frases.
(function () {
  ['doc', 'contracts', 'fraud'].forEach(k => {
    const P = window.PROMPTS.es[k];
    P.user = P.user
      .replace(/"summary": "resumen[^"]*",/, '"scope": "qué se analiza, sintagma de máximo 9 palabras sin punto final",\n  "summary": ["punto breve"],')
      .replace('\nREGLAS:\n', '\nREGLAS:\n- summary: de 3 a 5 puntos, cada uno una frase de 20 palabras como máximo, con cifras cuando las haya, del más al menos importante.\n');
    if (!P.user.includes('"scope"') || !P.user.includes('- summary: de 3')) console.warn('suite-afianza: no se ha podido ajustar el prompt ' + k);
  });
})();
