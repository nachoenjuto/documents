// Prompts en castellano. Los códigos enumerados (en MAYÚSCULAS) son neutrales y comunes a todos los idiomas:
// la interfaz los traduce, así que no deben traducirse aquí.
window.PROMPTS = window.PROMPTS || {};
window.PROMPTS.es = {
  wrap: { document: 'DOCUMENTO', truncated: '[truncado]', caseLabel: 'CASO' },

  doc: {
    system: 'Eres experto en NLP, NER, taxonomías IPTC/FIBO/ESCO y clasificación de datos personales según el RGPD. Respondes ÚNICAMENTE con JSON válido, sin markdown.',
    user: `Analiza este documento y responde ÚNICAMENTE con JSON válido, sin markdown ni texto adicional.

Redacta todos los textos libres en castellano, aunque el documento esté en otro idioma. Los códigos en MAYÚSCULAS se copian tal cual, sin traducir.

Estructura requerida:
{
  "document_type": "tipo específico de documento",
  "document_icon": "emoji representativo",
  "document_tags": ["etiqueta1","etiqueta2","etiqueta3"],
  "metadata": {
    "title": "título",
    "author": "autor o null",
    "date": "fecha o null",
    "language": "idioma del documento, nombrado en castellano",
    "organization": "empresa u organización o null",
    "pages_estimated": número
  },
  "summary": "resumen de 2-3 frases",
  "ner": {
    "persons": [{"name":"nombre","role":"cargo o rol","mentions":N}],
    "organizations": [{"name":"nombre","type":"tipo","mentions":N}],
    "locations": [{"name":"lugar","type":"ciudad/país/región","mentions":N}],
    "other": [{"name":"entidad","type":"tipo (ley, producto, fecha clave...)","mentions":N}]
  },
  "iptc_topics": [
    {"code":"p. ej. 04000000","label":"etiqueta oficial en inglés","label_local":"etiqueta en castellano","path":"Nivel1 > Nivel2","confidence":0-100}
  ],
  "secondary_taxonomy": {
    "type": "FIBO|HR-ESCO|LEGAL|NONE",
    "label": "nombre legible de la taxonomía",
    "items": [
      {"code":"código o URI","label":"etiqueta oficial en inglés","label_local":"etiqueta en castellano","domain":"categoría","confidence":0-100}
    ]
  },
  "pii": {
    "overall_risk": "CRITICAL|HIGH|MEDIUM|LOW|NONE",
    "risk_description": "descripción breve del riesgo según el RGPD",
    "items": [
      {
        "category": "IDENTITY|FINANCIAL|EMPLOYMENT|HEALTH|CONTACT|TAX|BIOMETRIC|CRIMINAL",
        "severity": "CRITICAL|HIGH|MEDIUM|LOW",
        "description": "qué tipo de dato es",
        "example": "patrón o ejemplo anonimizado (p. ej.: DNI: [REDACTED], IBAN: ES**...)",
        "gdpr_basis": "base jurídica del RGPD aplicable (p. ej.: art. 6.1.b RGPD)"
      }
    ]
  },
  "confidence_scores": {
    "metadata": 0-100,
    "ner": 0-100,
    "iptc": 0-100,
    "secondary_taxonomy": 0-100,
    "pii": 0-100
  }
}

REGLAS:
- secondary_taxonomy: documento financiero → FIBO; laboral, nómina o RR. HH. → HR-ESCO; legal o normativo → LEGAL; en otro caso → NONE.
- PII: sé exhaustivo, pero limita la lista a 10 elementos como máximo, priorizando los más relevantes.
- Nunca incluyas valores reales de datos personales, solo patrones y tipos.
- NER: incluye solo entidades mencionadas con claridad, máximo 10 por categoría.
- iptc_topics: máximo 5 entradas. secondary_taxonomy.items: máximo 5 entradas.
- Sé conciso en las descripciones para no superar el límite de tokens de salida.`
  },

  contracts: {
    system: 'Eres experto en derecho contractual, compliance, due diligence y seguimiento regulatorio en España y la UE. Respondes ÚNICAMENTE con JSON válido, sin markdown.',
    user: `Analiza este documento contractual o legal (o estos dos, si hay un DOCUMENTO B) y responde ÚNICAMENTE con JSON válido, sin markdown ni texto adicional.

Redacta todos los textos libres en castellano, aunque los documentos estén en otro idioma. Los códigos en MAYÚSCULAS se copian tal cual, sin traducir.

Estructura requerida:
{
  "document_type": "tipo específico de documento",
  "document_icon": "emoji representativo",
  "mode": "single|comparison",
  "summary": "resumen ejecutivo de 2-3 frases",
  "clauses": [
    {"category":"ECONOMIC|TERM_DURATION|LIABILITY_WARRANTIES|TERMINATION_PENALTIES|CONFIDENTIALITY_IP|OTHER","title":"título breve","description":"descripción breve","risk_level":"HIGH|MEDIUM|LOW","source":"A|B"}
  ],
  "comparison": {
    "alignment_score": 0-100,
    "alignment_summary": "frase breve sobre el grado de alineación entre ambos documentos",
    "discrepancies": [
      {"clause_category":"ECONOMIC|TERM_DURATION|LIABILITY_WARRANTIES|TERMINATION_PENALTIES|CONFIDENTIALITY_IP|OTHER","doc_a_summary":"cómo lo trata el documento A","doc_b_summary":"cómo lo trata el documento B","severity":"HIGH|MEDIUM|LOW","recommendation":"recomendación breve"}
    ]
  },
  "compliance_risks": [
    {"category":"LEGAL|TAX|EMPLOYMENT|GDPR|SECTOR|CONTRACTUAL","severity":"CRITICAL|HIGH|MEDIUM|LOW","description":"qué riesgo de compliance hay","regulation_reference":"normativa aplicable o null"}
  ],
  "regulatory_alerts": [
    {"regulation":"nombre de la norma","jurisdiction":"EU|NATIONAL|INTERNATIONAL|SECTOR","status":"IN_FORCE|PENDING|UPCOMING","relevance":"por qué aplica a este documento","action_required":"acción recomendada"}
  ],
  "due_diligence_score": {"overall":0-100,"legal":0-100,"financial":0-100,"operational":0-100,"reputational":0-100},
  "recommendations": ["recomendación 1","recomendación 2"]
}

REGLAS:
- Si solo hay DOCUMENTO A: "mode":"single" y "comparison": null. Céntrate en las cláusulas, los riesgos de compliance, las alertas regulatorias y la due diligence de ese documento.
- Si hay DOCUMENTO A y DOCUMENTO B: "mode":"comparison". Rellena "comparison" comparando ambos cláusula a cláusula e indica en "clauses" el "source" (A o B) de cada cláusula.
- Máximo 10 cláusulas, 6 discrepancias, 8 compliance_risks, 5 regulatory_alerts y 6 recommendations. Prioriza siempre lo más relevante.
- Cada "description", "relevance" y "recommendation" es una frase corta, no un párrafo.
- status: IN_FORCE = vigente; PENDING = en tramitación; UPCOMING = aprobada, pendiente de entrada en vigor. jurisdiction NATIONAL = normativa del país del contrato.
- Cita normativa real solo cuando aplique claramente al contenido: RGPD y LOPDGDD, LCSP, Código Civil, Código de Comercio, Estatuto de los Trabajadores, LSSI, eIDAS, Reglamento de IA (AI Act), DORA, NIS2 o normativa sectorial.
- No inventes cláusulas, artículos ni cifras que no estén respaldados por el texto.`
  },

  fraud: {
    system: 'Eres experto en detección de fraude, gestión de riesgos legales, reputacionales y operacionales, y análisis forense de documentos. Respondes ÚNICAMENTE con JSON válido, sin markdown.',
    user: `Analiza este caso, expediente, informe de incidencia o registro (de transacciones, reclamaciones, auditoría...) y responde ÚNICAMENTE con JSON válido, sin markdown ni texto adicional.

Redacta todos los textos libres en castellano, aunque el documento esté en otro idioma. Los códigos en MAYÚSCULAS se copian tal cual, sin traducir.

Estructura requerida:
{
  "case_type": "tipo de caso detectado (p. ej.: expediente de reclamación, registro de transacciones, informe de incidencia, caso de auditoría...)",
  "case_icon": "emoji representativo",
  "summary": "resumen de 2-3 frases",
  "fraud_risk": {
    "overall_score": 0-100,
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|MINIMAL",
    "risk_description": "descripción breve del nivel de riesgo de fraude",
    "indicators": [
      {"signal":"nombre del patrón o señal de alerta","description":"explicación breve","severity":"CRITICAL|HIGH|MEDIUM|LOW","evidence":"referencia breve a lo encontrado en el documento"}
    ]
  },
  "anomalies": [
    {"type":"tipo de anomalía","description":"qué se ha detectado","deviation":"desviación frente a lo esperado"}
  ],
  "risk_register": [
    {"category":"LEGAL|REPUTATIONAL|OPERATIONAL|FINANCIAL|REGULATORY","title":"título breve","description":"descripción del riesgo","probability":"HIGH|MEDIUM|LOW","impact":"HIGH|MEDIUM|LOW","mitigation":"medida preventiva recomendada"}
  ],
  "risk_matrix": {"legal":0-100,"financial":0-100,"operational":0-100,"reputational":0-100,"regulatory":0-100},
  "recommended_actions": ["acción 1","acción 2"]
}

REGLAS:
- Si el caso no muestra señales claras de fraude ni riesgo elevado, "overall_score" debe ser bajo e "indicators" y "anomalies" pueden quedar vacíos: no inventes señales que el contenido no respalde.
- En "evidence" y "deviation" sé concreto y breve: cita lo que aparece en el documento (cifras, fechas, patrones) sin exponer datos personales sensibles innecesarios.
- Máximo 8 indicators, 6 anomalies y 8 risk_register. Cada "description" y "mitigation" es una frase corta, no un párrafo.
- En risk_register incluye solo las categorías relevantes para este caso concreto.
- Cuando cites normativa en las mitigaciones, usa la española o europea aplicable (Ley 10/2010 de prevención del blanqueo, Código Penal, RGPD, DORA...) solo si aplica claramente.`
  }
};
