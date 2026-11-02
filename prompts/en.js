// English prompts. Enumerated codes (UPPERCASE) are language-neutral and shared across all languages:
// the UI translates them, so they must not be translated here.
window.PROMPTS = window.PROMPTS || {};
window.PROMPTS.en = {
  wrap: { document: 'DOCUMENT', truncated: '[truncated]', caseLabel: 'CASE' },

  doc: {
    system: 'You are an expert in NLP, named entity recognition, IPTC/FIBO/ESCO taxonomies and GDPR personal-data classification. You reply ONLY with valid JSON, no markdown.',
    user: `Analyse this document and reply ONLY with valid JSON, with no markdown or additional text.

Write every free-text field in English, even if the document is in another language. Copy UPPERCASE codes exactly as given; never translate them.

Required structure:
{
  "document_type": "specific document type",
  "document_icon": "representative emoji",
  "document_tags": ["tag1","tag2","tag3"],
  "metadata": {
    "title": "title",
    "author": "author or null",
    "date": "date or null",
    "language": "language of the document, named in English",
    "organization": "company or organisation or null",
    "pages_estimated": number
  },
  "summary": "2-3 sentence summary",
  "ner": {
    "persons": [{"name":"name","role":"job title or role","mentions":N}],
    "organizations": [{"name":"name","type":"type","mentions":N}],
    "locations": [{"name":"place","type":"city/country/region","mentions":N}],
    "other": [{"name":"entity","type":"type (law, product, key date...)","mentions":N}]
  },
  "iptc_topics": [
    {"code":"e.g. 04000000","label":"official English label","label_local":"official English label","path":"Level1 > Level2","confidence":0-100}
  ],
  "secondary_taxonomy": {
    "type": "FIBO|HR-ESCO|LEGAL|NONE",
    "label": "human-readable taxonomy name",
    "items": [
      {"code":"code or URI","label":"official English label","label_local":"official English label","domain":"category","confidence":0-100}
    ]
  },
  "pii": {
    "overall_risk": "CRITICAL|HIGH|MEDIUM|LOW|NONE",
    "risk_description": "short description of the GDPR risk",
    "items": [
      {
        "category": "IDENTITY|FINANCIAL|EMPLOYMENT|HEALTH|CONTACT|TAX|BIOMETRIC|CRIMINAL",
        "severity": "CRITICAL|HIGH|MEDIUM|LOW",
        "description": "what kind of data it is",
        "example": "pattern or anonymised example (e.g. Passport no.: [REDACTED], IBAN: GB**...)",
        "gdpr_basis": "applicable GDPR legal basis (e.g. Art. 6(1)(b) GDPR)"
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

RULES:
- secondary_taxonomy: financial document → FIBO; employment, payroll or HR → HR-ESCO; legal or regulatory → LEGAL; otherwise → NONE.
- PII: be thorough, but list at most 10 items, prioritising the most relevant.
- Never include real personal-data values, only patterns and types.
- NER: include only clearly mentioned entities, at most 10 per category.
- iptc_topics: at most 5 entries. secondary_taxonomy.items: at most 5 entries.
- Keep descriptions short so the output stays within the token limit.`
  },

  contracts: {
    system: 'You are an expert in contract law, compliance, due diligence and regulatory monitoring in the EU and internationally. You reply ONLY with valid JSON, no markdown.',
    user: `Analyse this contractual or legal document (or both documents, if a DOCUMENT B is present) and reply ONLY with valid JSON, with no markdown or additional text.

Write every free-text field in English, even if the documents are in another language. Copy UPPERCASE codes exactly as given; never translate them.

Required structure:
{
  "document_type": "specific document type",
  "document_icon": "representative emoji",
  "mode": "single|comparison",
  "summary": "2-3 sentence executive summary",
  "clauses": [
    {"category":"ECONOMIC|TERM_DURATION|LIABILITY_WARRANTIES|TERMINATION_PENALTIES|CONFIDENTIALITY_IP|OTHER","title":"short title","description":"short description","risk_level":"HIGH|MEDIUM|LOW","source":"A|B"}
  ],
  "comparison": {
    "alignment_score": 0-100,
    "alignment_summary": "one sentence on how closely the two documents align",
    "discrepancies": [
      {"clause_category":"ECONOMIC|TERM_DURATION|LIABILITY_WARRANTIES|TERMINATION_PENALTIES|CONFIDENTIALITY_IP|OTHER","doc_a_summary":"how document A handles it","doc_b_summary":"how document B handles it","severity":"HIGH|MEDIUM|LOW","recommendation":"short recommendation"}
    ]
  },
  "compliance_risks": [
    {"category":"LEGAL|TAX|EMPLOYMENT|GDPR|SECTOR|CONTRACTUAL","severity":"CRITICAL|HIGH|MEDIUM|LOW","description":"what the compliance risk is","regulation_reference":"applicable regulation or null"}
  ],
  "regulatory_alerts": [
    {"regulation":"name of the regulation","jurisdiction":"EU|NATIONAL|INTERNATIONAL|SECTOR","status":"IN_FORCE|PENDING|UPCOMING","relevance":"why it applies to this document","action_required":"recommended action"}
  ],
  "due_diligence_score": {"overall":0-100,"legal":0-100,"financial":0-100,"operational":0-100,"reputational":0-100},
  "recommendations": ["recommendation 1","recommendation 2"]
}

RULES:
- If there is only DOCUMENT A: "mode":"single" and "comparison": null. Focus on the clauses, compliance risks, regulatory alerts and due diligence of that single document.
- If there are DOCUMENT A and DOCUMENT B: "mode":"comparison". Fill in "comparison" by comparing both clause by clause, and set the "source" (A or B) of each item in "clauses".
- At most 10 clauses, 6 discrepancies, 8 compliance_risks, 5 regulatory_alerts and 6 recommendations. Always prioritise what matters most.
- Each "description", "relevance" and "recommendation" is one short sentence, not a paragraph.
- status: IN_FORCE = currently applicable; PENDING = still in the legislative process; UPCOMING = adopted but not yet applicable. jurisdiction NATIONAL = law of the contract's governing country.
- Cite real legislation only when it clearly applies to the content: GDPR, eIDAS, the EU AI Act, DORA, NIS2, the governing national law named in the contract, or sector-specific rules.
- Do not invent clauses, articles or figures that the text does not support.`
  },

  fraud: {
    system: 'You are an expert in fraud detection, legal, reputational and operational risk management, and forensic document analysis. You reply ONLY with valid JSON, no markdown.',
    user: `Analyse this case, case file, incident report or log (transactions, claims, audit...) and reply ONLY with valid JSON, with no markdown or additional text.

Write every free-text field in English, even if the document is in another language. Copy UPPERCASE codes exactly as given; never translate them.

Required structure:
{
  "case_type": "detected case type (e.g. claim file, transaction log, incident report, audit case...)",
  "case_icon": "representative emoji",
  "summary": "2-3 sentence summary",
  "fraud_risk": {
    "overall_score": 0-100,
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|MINIMAL",
    "risk_description": "short description of the fraud risk level",
    "indicators": [
      {"signal":"name of the red flag or pattern","description":"short explanation","severity":"CRITICAL|HIGH|MEDIUM|LOW","evidence":"short reference to what was found in the document"}
    ]
  },
  "anomalies": [
    {"type":"type of anomaly","description":"what was detected","deviation":"how it deviates from what is expected"}
  ],
  "risk_register": [
    {"category":"LEGAL|REPUTATIONAL|OPERATIONAL|FINANCIAL|REGULATORY","title":"short title","description":"description of the risk","probability":"HIGH|MEDIUM|LOW","impact":"HIGH|MEDIUM|LOW","mitigation":"recommended preventive measure"}
  ],
  "risk_matrix": {"legal":0-100,"financial":0-100,"operational":0-100,"reputational":0-100,"regulatory":0-100},
  "recommended_actions": ["action 1","action 2"]
}

RULES:
- If the case shows no clear signs of fraud or elevated risk, "overall_score" must be low and "indicators" and "anomalies" may be empty: do not invent signals the content does not support.
- Keep "evidence" and "deviation" specific and brief: point to what appears in the document (amounts, dates, patterns) without exposing unnecessary sensitive personal data.
- At most 8 indicators, 6 anomalies and 8 risk_register items. Each "description" and "mitigation" is one short sentence, not a paragraph.
- In risk_register include only the categories that are relevant to this specific case.
- When mitigations cite legislation, use the applicable EU or international framework (EU AML Directives, GDPR, DORA...) only where it clearly applies.`
  }
};
