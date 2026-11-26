// Textos de la pestaña Due Diligence (Tabular Review). Solo castellano: en EN/DE i18next recurre a ES.
Object.assign(window.I18N.es.tabs, { tabular: 'Due Diligence', tabularSub: 'Revisión masiva · Evidencia citada · Excepciones' });
window.I18N.es.tabular = {
  heroTitle: 'Revisa <em>todos</em> los documentos<br>y quédate con las excepciones',
  heroText: 'Extrae los mismos campos de muchos documentos, con cita y página en cada celda, y cruza los resultados para señalar incoherencias.',
  capMulti: 'Revisión masiva', capQuote: 'Evidencia citada', capCross: 'Excepciones', capCsv: 'Exportación CSV',
  template: 'Plantilla', fields: 'Campos a extraer', addField: 'Añadir un campo, p. ej. «¿Hay cláusula de no competencia?»', add: 'Añadir',
  dropTitle: 'Arrastra varios documentos aquí', run: 'Revisar documentos', clear: 'Vaciar lista', export: 'Exportar CSV',
  limit: 'Máximo {{n}} documentos. Se han descartado {{x}}.', empty: 'Añade al menos un campo.', maxFields: 'Máximo {{n}} campos.',
  load: 'Cargar análisis guardado', save: 'Guardar análisis', csvNoAlerts: 'El CSV contiene la tabla, pero no el resumen ni las alertas. Para guardarlo todo, usa «Guardar análisis».',
  savedFrom: 'Análisis guardado: {{name}}{{date}}. No se ha ejecutado ahora.', badFile: 'No se pudo cargar {{name}}: {{message}}', badFormat: 'no tiene el formato de Tabular Review', noFiles: 'Este análisis no incluye los documentos. Cárgalos y lanza la revisión para analizar campos nuevos.',
  noDownload: 'Documento no incluido en el archivo guardado', risk: 'criticidad',
  needKey: 'Introduce la API Key para analizar el campo nuevo.',
  progressNew: 'Analizando el campo nuevo: {{done}} de {{total}}...',
  summaryOne: 'Resumen del análisis de 1 documento', summaryMany: 'Resumen del análisis de {{n}} documentos', alerts: 'Alertas ({{n}})', alertCount: 'Número de alertas',
  legend: 'Criticidad', sevName: { HIGH: 'Alta', MEDIUM: 'Media', LOW: 'Baja' },
  sevHelp: { HIGH: 'Puede afectar a la operación o al encargo', MEDIUM: 'Conviene revisarlo', LOW: 'Informativo' },
  legendQuote: { ok: 'Cita localizada', bad: 'Cita sin localizar', scan: 'Escaneado' },
  literal: 'Texto literal extraído', notLiteral: 'Texto propuesto por el modelo, no comprobado', download: 'Descargar el documento',
  pageN: '{{n}}', pageUnsure: '{{n}} (sin confirmar)', noPage: 'Sin paginación',
  progress: 'Extrayendo {{done}} de {{total}}...', crossing: 'Cruzando documentos...',
  sec: 'Resumen y alertas', table: 'Tabla de revisión', missing: 'No consta', failed: 'Error: {{message}}', document: 'Documento',
  noAlerts: 'No se han detectado excepciones. Revísalo igualmente.', crossFailed: 'No se pudo completar el cruce: {{message}}. La tabla sigue siendo válida.',
  partial: 'Hay documentos con error que no entran en el cruce: {{list}}',
  truncated: 'texto recortado', verified: 'Cita localizada en el documento', unverified: 'Cita no localizada: revisar a mano', noText: 'Documento escaneado: cita no comprobable',
  page: 'Página', confidence: 'Confianza del modelo', action: 'Acción', close: 'Cerrar', usage: '{{in}} tokens de entrada · {{out}} de salida · {{s}} s',
  disclaimer: 'Apoyo a la revisión. Requiere validación profesional.',
  ctxDownload: 'Descargar', ctxOpen: 'Ver en contexto', ctxOnlyPdf: 'Solo disponible para PDF', ctxTitle: 'Documento en contexto', ctxFields: 'Campos extraídos', ctxPage: 'Página {{n}} de {{total}}', ctxShort: 'pág. {{n}}',
  ctxIn: 'Ampliar', ctxOut: 'Reducir', ctxLoading: 'Cargando el documento...', ctxFailed: 'No se pudo abrir el documento: {{message}}',
  ctxNoQuote: 'No se ha podido localizar la cita en el texto. Se muestra la página indicada por el modelo: revísala a mano.', ctxScan: 'Documento escaneado: se muestra la página indicada por el modelo, sin resaltado.', ctxNowhere: 'No se ha podido localizar este dato en el documento: revísalo a mano.',
  editHint: 'Haz clic para editar el campo y su instrucción', editLabel: 'Nombre', editText: 'Criterio o instrucción', editPh: 'p. ej. «solo importes superiores a 30.000 €»',
  mode: { add: 'Complementar', replace: 'Sustituir' }, original: 'Instrucción original: {{ask}}', apply: 'Aplicar', cancel: 'Cancelar', restore: 'Restaurar',
  editedTip: 'Instrucción modificada: {{ask}}', progressEdit: 'Reanalizando «{{label}}»: {{done}} de {{total}}...', editNoFiles: 'Este análisis no incluye los documentos: solo se puede cambiar el nombre.',
  notMet: 'No cumple el criterio', notMetLong: 'El documento no cumple el criterio del revisor. Se muestra el dato real.', outPrefix: 'No cumple el criterio: ',
  conflicts: 'Contradicciones entre documentos ({{n}})', conflictsLead: 'Documentos que establecen cosas incompatibles sobre el mismo asunto. Haz clic en cada documento para ver el dato y su cita.',
  conflictWhy: 'Por qué chocan', conflictImpact: 'Consecuencia', conflictVs: 'frente a',
  sev: { HIGH: 'ALTA', MEDIUM: 'MEDIA', LOW: 'BAJA' }
};
// Fraude & Riesgo en index_afianza.html (ES/EN/DE).
Object.assign(window.I18N.es.fraud, { sumTitle: 'Resumen del análisis de', level: 'Criticidad', levelHelp: 'Criticidad = probabilidad × impacto', signals: 'Indicadores de fraude ({{n}})', noSignals: 'No se han detectado indicadores de fraude.', what: 'Qué ocurre', evidence: 'Evidencia', deviation: 'Desviación', risk: 'Riesgo', sevN: { critical: 'Crítica', high: 'Alta', medium: 'Media', low: 'Baja' } });
Object.assign(window.I18N.en.fraud, { sumTitle: 'Analysis summary:', level: 'Criticality', levelHelp: 'Criticality = probability × impact', signals: 'Fraud indicators ({{n}})', noSignals: 'No fraud indicators detected.', what: 'What happens', evidence: 'Evidence', deviation: 'Deviation', risk: 'Risk', sevN: { critical: 'Critical', high: 'High', medium: 'Medium', low: 'Low' } });
Object.assign(window.I18N.de.fraud, { sumTitle: 'Zusammenfassung der Analyse:', level: 'Kritikalität', levelHelp: 'Kritikalität = Wahrscheinlichkeit × Auswirkung', signals: 'Betrugsindikatoren ({{n}})', noSignals: 'Keine Betrugsindikatoren erkannt.', what: 'Sachverhalt', evidence: 'Beleg', deviation: 'Abweichung', risk: 'Risiko', sevN: { critical: 'Kritisch', high: 'Hoch', medium: 'Mittel', low: 'Niedrig' } });
// Document Intelligence y Contratos en index_afianza.html (ES/EN/DE).
Object.assign(window.I18N.es.contracts, { says: 'Qué dice', why: 'Por qué aplica', rec: 'Recomendación' });
Object.assign(window.I18N.en.contracts, { says: 'What it says', why: 'Why it applies', rec: 'Recommendation' });
Object.assign(window.I18N.de.contracts, { says: 'Inhalt', why: 'Warum relevant', rec: 'Empfehlung' });
Object.assign(window.I18N.es.doc, { datum: 'Qué dato es', example: 'Ejemplo' });
Object.assign(window.I18N.en.doc, { datum: 'What data it is', example: 'Example' });
Object.assign(window.I18N.de.doc, { datum: 'Art der Daten', example: 'Beispiel' });
