// Deutsche Prompts. Die Aufzählungscodes (GROSSBUCHSTABEN) sind sprachneutral und für alle Sprachen gleich:
// die Oberfläche übersetzt sie, daher dürfen sie hier nicht übersetzt werden.
window.PROMPTS = window.PROMPTS || {};
window.PROMPTS.de = {
  wrap: { document: 'DOKUMENT', truncated: '[gekürzt]', caseLabel: 'FALL' },

  doc: {
    system: 'Du bist Experte für NLP, Named Entity Recognition, IPTC-/FIBO-/ESCO-Taxonomien und die Klassifizierung personenbezogener Daten nach DSGVO. Du antwortest AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown.',
    user: `Analysiere dieses Dokument und antworte AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown und ohne zusätzlichen Text.

Verfasse alle Freitextfelder auf Deutsch, auch wenn das Dokument in einer anderen Sprache vorliegt. Codes in GROSSBUCHSTABEN werden unverändert übernommen und nie übersetzt.

Erforderliche Struktur:
{
  "document_type": "konkreter Dokumenttyp",
  "document_icon": "passendes Emoji",
  "document_tags": ["Schlagwort1","Schlagwort2","Schlagwort3"],
  "metadata": {
    "title": "Titel",
    "author": "Autor oder null",
    "date": "Datum oder null",
    "language": "Sprache des Dokuments, auf Deutsch benannt",
    "organization": "Unternehmen oder Organisation oder null",
    "pages_estimated": Zahl
  },
  "summary": "Zusammenfassung in 2-3 Sätzen",
  "ner": {
    "persons": [{"name":"Name","role":"Funktion oder Rolle","mentions":N}],
    "organizations": [{"name":"Name","type":"Art","mentions":N}],
    "locations": [{"name":"Ort","type":"Stadt/Land/Region","mentions":N}],
    "other": [{"name":"Entität","type":"Art (Gesetz, Produkt, Stichtag...)","mentions":N}]
  },
  "iptc_topics": [
    {"code":"z. B. 04000000","label":"offizielle englische Bezeichnung","label_local":"Bezeichnung auf Deutsch","path":"Ebene1 > Ebene2","confidence":0-100}
  ],
  "secondary_taxonomy": {
    "type": "FIBO|HR-ESCO|LEGAL|NONE",
    "label": "lesbarer Name der Taxonomie",
    "items": [
      {"code":"Code oder URI","label":"offizielle englische Bezeichnung","label_local":"Bezeichnung auf Deutsch","domain":"Kategorie","confidence":0-100}
    ]
  },
  "pii": {
    "overall_risk": "CRITICAL|HIGH|MEDIUM|LOW|NONE",
    "risk_description": "kurze Beschreibung des Datenschutzrisikos nach DSGVO",
    "items": [
      {
        "category": "IDENTITY|FINANCIAL|EMPLOYMENT|HEALTH|CONTACT|TAX|BIOMETRIC|CRIMINAL",
        "severity": "CRITICAL|HIGH|MEDIUM|LOW",
        "description": "um welche Art von Daten es sich handelt",
        "example": "Muster oder anonymisiertes Beispiel (z. B. Ausweisnr.: [REDACTED], IBAN: DE**...)",
        "gdpr_basis": "einschlägige Rechtsgrundlage nach DSGVO (z. B. Art. 6 Abs. 1 lit. b DSGVO)"
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

REGELN:
- secondary_taxonomy: Finanzdokument → FIBO; Arbeitsvertrag, Gehaltsabrechnung oder Personalwesen → HR-ESCO; juristisches oder regulatorisches Dokument → LEGAL; sonst → NONE.
- PII: gründlich vorgehen, aber höchstens 10 Einträge auflisten, die relevantesten zuerst.
- Niemals echte personenbezogene Werte ausgeben, nur Muster und Datentypen.
- NER: nur eindeutig erwähnte Entitäten, höchstens 10 pro Kategorie.
- iptc_topics: höchstens 5 Einträge. secondary_taxonomy.items: höchstens 5 Einträge.
- Beschreibungen knapp halten, damit das Token-Limit der Ausgabe nicht überschritten wird.`
  },

  contracts: {
    system: 'Du bist Experte für Vertragsrecht, Compliance, Due Diligence und regulatorisches Monitoring in Deutschland und der EU. Du antwortest AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown.',
    user: `Analysiere dieses Vertrags- oder Rechtsdokument (bzw. beide Dokumente, falls ein DOKUMENT B vorliegt) und antworte AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown und ohne zusätzlichen Text.

Verfasse alle Freitextfelder auf Deutsch, auch wenn die Dokumente in einer anderen Sprache vorliegen. Codes in GROSSBUCHSTABEN werden unverändert übernommen und nie übersetzt.

Erforderliche Struktur:
{
  "document_type": "konkreter Dokumenttyp",
  "document_icon": "passendes Emoji",
  "mode": "single|comparison",
  "summary": "Management Summary in 2-3 Sätzen",
  "clauses": [
    {"category":"ECONOMIC|TERM_DURATION|LIABILITY_WARRANTIES|TERMINATION_PENALTIES|CONFIDENTIALITY_IP|OTHER","title":"kurzer Titel","description":"kurze Beschreibung","risk_level":"HIGH|MEDIUM|LOW","source":"A|B"}
  ],
  "comparison": {
    "alignment_score": 0-100,
    "alignment_summary": "ein Satz zum Grad der Übereinstimmung beider Dokumente",
    "discrepancies": [
      {"clause_category":"ECONOMIC|TERM_DURATION|LIABILITY_WARRANTIES|TERMINATION_PENALTIES|CONFIDENTIALITY_IP|OTHER","doc_a_summary":"Regelung in Dokument A","doc_b_summary":"Regelung in Dokument B","severity":"HIGH|MEDIUM|LOW","recommendation":"kurze Empfehlung"}
    ]
  },
  "compliance_risks": [
    {"category":"LEGAL|TAX|EMPLOYMENT|GDPR|SECTOR|CONTRACTUAL","severity":"CRITICAL|HIGH|MEDIUM|LOW","description":"worin das Compliance-Risiko besteht","regulation_reference":"einschlägige Vorschrift oder null"}
  ],
  "regulatory_alerts": [
    {"regulation":"Bezeichnung der Vorschrift","jurisdiction":"EU|NATIONAL|INTERNATIONAL|SECTOR","status":"IN_FORCE|PENDING|UPCOMING","relevance":"warum sie für dieses Dokument relevant ist","action_required":"empfohlene Maßnahme"}
  ],
  "due_diligence_score": {"overall":0-100,"legal":0-100,"financial":0-100,"operational":0-100,"reputational":0-100},
  "recommendations": ["Empfehlung 1","Empfehlung 2"]
}

REGELN:
- Liegt nur DOKUMENT A vor: "mode":"single" und "comparison": null. Konzentriere dich auf Klauseln, Compliance-Risiken, regulatorische Hinweise und Due Diligence dieses einen Dokuments.
- Liegen DOKUMENT A und DOKUMENT B vor: "mode":"comparison". Fülle "comparison" durch einen Klausel-für-Klausel-Vergleich aus und gib in "clauses" für jede Klausel die "source" (A oder B) an.
- Höchstens 10 Klauseln, 6 Abweichungen, 8 compliance_risks, 5 regulatory_alerts und 6 recommendations. Immer das Relevanteste zuerst.
- Jede "description", "relevance" und "recommendation" ist ein kurzer Satz, kein Absatz.
- status: IN_FORCE = geltendes Recht; PENDING = im Gesetzgebungsverfahren; UPCOMING = verabschiedet, aber noch nicht anwendbar. jurisdiction NATIONAL = Recht des Landes, dem der Vertrag unterliegt.
- Echte Vorschriften nur zitieren, wenn sie eindeutig einschlägig sind: DSGVO und BDSG, BGB (insb. AGB-Recht §§ 305 ff.), HGB, GwG, eIDAS, KI-Verordnung (AI Act), DORA, NIS2 bzw. NIS2UmsuCG oder branchenspezifisches Recht.
- Keine Klauseln, Paragrafen oder Zahlen erfinden, die der Text nicht belegt.`
  },

  fraud: {
    system: 'Du bist Experte für Betrugserkennung, das Management rechtlicher, reputationsbezogener und operativer Risiken sowie forensische Dokumentenanalyse. Du antwortest AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown.',
    user: `Analysiere diesen Fall, diese Fallakte, diesen Vorfallbericht oder dieses Protokoll (Transaktionen, Reklamationen, Prüfung...) und antworte AUSSCHLIESSLICH mit gültigem JSON, ohne Markdown und ohne zusätzlichen Text.

Verfasse alle Freitextfelder auf Deutsch, auch wenn das Dokument in einer anderen Sprache vorliegt. Codes in GROSSBUCHSTABEN werden unverändert übernommen und nie übersetzt.

Erforderliche Struktur:
{
  "case_type": "erkannter Falltyp (z. B. Reklamationsakte, Transaktionsprotokoll, Vorfallbericht, Prüfungsfall...)",
  "case_icon": "passendes Emoji",
  "summary": "Zusammenfassung in 2-3 Sätzen",
  "fraud_risk": {
    "overall_score": 0-100,
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|MINIMAL",
    "risk_description": "kurze Beschreibung des Betrugsrisikos",
    "indicators": [
      {"signal":"Bezeichnung des Warnsignals oder Musters","description":"kurze Erläuterung","severity":"CRITICAL|HIGH|MEDIUM|LOW","evidence":"kurzer Verweis auf die Fundstelle im Dokument"}
    ]
  },
  "anomalies": [
    {"type":"Art der Anomalie","description":"was festgestellt wurde","deviation":"Abweichung vom erwarteten Zustand"}
  ],
  "risk_register": [
    {"category":"LEGAL|REPUTATIONAL|OPERATIONAL|FINANCIAL|REGULATORY","title":"kurzer Titel","description":"Beschreibung des Risikos","probability":"HIGH|MEDIUM|LOW","impact":"HIGH|MEDIUM|LOW","mitigation":"empfohlene Präventivmaßnahme"}
  ],
  "risk_matrix": {"legal":0-100,"financial":0-100,"operational":0-100,"reputational":0-100,"regulatory":0-100},
  "recommended_actions": ["Maßnahme 1","Maßnahme 2"]
}

REGELN:
- Zeigt der Fall keine klaren Betrugsindikatoren oder erhöhten Risiken, muss "overall_score" niedrig sein und "indicators" und "anomalies" dürfen leer bleiben: keine Signale erfinden, die der Inhalt nicht belegt.
- "evidence" und "deviation" konkret und knapp halten: auf Inhalte des Dokuments verweisen (Beträge, Daten, Muster), ohne unnötig sensible personenbezogene Daten offenzulegen.
- Höchstens 8 indicators, 6 anomalies und 8 risk_register-Einträge. Jede "description" und "mitigation" ist ein kurzer Satz, kein Absatz.
- Im risk_register nur die Kategorien aufnehmen, die für diesen konkreten Fall relevant sind.
- Werden in Gegenmaßnahmen Vorschriften genannt, das einschlägige deutsche bzw. EU-Recht verwenden (GwG, StGB, DSGVO, DORA...), aber nur, wenn es eindeutig zutrifft.`
  }
};
