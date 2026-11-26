"""Análisis sintéticos para la demo sin conexión de Document Intelligence, Contratos y Fraude.

Formato «suite-analysis»: el resultado con el mismo JSON que devuelve el modelo en cada tab y los
documentos de entrada incrustados. Se escriben como data/demo-offline/<tab>.js (opción A) y como
analisis-offline/analisis-<tab>.json (opción B). Redactados a mano; no son salida del modelo.
"""
import base64, json, mimetypes
from .motor import BASE
from .offline import APP, DATE

DOC = {
 "document_type": "Nómina mensual (recibo individual de salarios)", "document_icon": "🧾",
 "document_tags": ["Nómina", "Datos personales", "Seguridad Social", "Traspaso laboral"],
 "metadata": {"title": "Recibo individual del pago de salarios. Octubre de 2026", "author": "Gestoría Peñalara Nóminas", "date": "2026-10-30", "language": "castellano", "organization": "Norvalia Conectores, S.L.", "pages_estimated": 1},
 "scope": "nómina de octubre de 2026 de la persona E02",
 "summary": ["Nómina de octubre de 2026 de un oficial de segunda de Norvalia Conectores.",
             "Total devengado de 1.650,00 € y líquido de 1.349,97 € tras 300,03 € de deducciones.",
             "Contiene nombre, DNI, IBAN y datos salariales: riesgo alto según el RGPD.",
             "Para el traspaso, conviene contrastar categoría y salario con el contrato de trabajo."],
 "ner": {
  "persons": [{"name": "Julián Ceballos Rueda", "role": "persona trabajadora (E02)", "mentions": 2}, {"name": "Ramiro Tordesillas Vega", "role": "administrador único, firma por la empresa", "mentions": 1}],
  "organizations": [{"name": "Norvalia Conectores, S.L.", "type": "empresa empleadora", "mentions": 3}, {"name": "Gestoría Peñalara Nóminas", "type": "gestoría laboral", "mentions": 1}, {"name": "Tesorería General de la Seguridad Social", "type": "organismo público", "mentions": 1}],
  "locations": [{"name": "Getafe", "type": "ciudad", "mentions": 2}, {"name": "Madrid", "type": "provincia", "mentions": 1}],
  "other": [{"name": "Convenio colectivo de Norvalia Conectores, S.L. 2025-2027", "type": "convenio colectivo", "mentions": 1}, {"name": "28/0000001/00", "type": "código de cuenta de cotización", "mentions": 2}, {"name": "Octubre de 2026", "type": "periodo de liquidación", "mentions": 2}]},
 "iptc_topics": [
  {"code": "09000000", "label": "labour", "label_local": "Trabajo", "path": "Trabajo", "confidence": 96},
  {"code": "20000135", "label": "wages and benefits", "label_local": "Salarios y prestaciones", "path": "Trabajo > Salarios y prestaciones", "confidence": 93},
  {"code": "20000136", "label": "social security", "label_local": "Seguridad Social", "path": "Trabajo > Seguridad Social", "confidence": 84},
  {"code": "20000419", "label": "income tax", "label_local": "Impuesto sobre la renta", "path": "Economía > Fiscalidad > Impuesto sobre la renta", "confidence": 71}],
 "secondary_taxonomy": {"type": "HR-ESCO", "label": "ESCO (ocupaciones y competencias)", "items": [
  {"code": "ISCO 8212", "label": "Electrical equipment assemblers", "label_local": "Montadores de equipos eléctricos", "domain": "ocupación", "confidence": 78},
  {"code": "ISCO 7543", "label": "Product graders and testers", "label_local": "Clasificadores y probadores de productos", "domain": "ocupación relacionada", "confidence": 46}]},
 "pii": {"overall_risk": "HIGH", "risk_description": "La nómina identifica a una persona y contiene su DNI, su cuenta bancaria y sus datos salariales y de cotización. Su tratamiento exige base jurídica, acceso restringido y un contrato de encargo con la gestoría.",
  "items": [
   {"category": "IDENTITY", "severity": "HIGH", "description": "Nombre y apellidos y DNI de la persona trabajadora", "example": "DNI: 7603****T", "gdpr_basis": "art. 6.1.b RGPD (ejecución del contrato)"},
   {"category": "FINANCIAL", "severity": "HIGH", "description": "IBAN de la cuenta de abono de la nómina", "example": "IBAN: ES00 9999 **** **** **** 7202", "gdpr_basis": "art. 6.1.b RGPD"},
   {"category": "EMPLOYMENT", "severity": "MEDIUM", "description": "Categoría, antigüedad, salario y código de empleado", "example": "Oficial de segunda · 23.100 €/año", "gdpr_basis": "art. 6.1.b y 6.1.c RGPD"},
   {"category": "TAX", "severity": "MEDIUM", "description": "Tipo de retención del IRPF, que permite inferir la situación personal y familiar", "example": "IRPF: 10,60 %", "gdpr_basis": "art. 6.1.c RGPD (obligación legal)"},
   {"category": "EMPLOYMENT", "severity": "LOW", "description": "Bases y cotizaciones a la Seguridad Social", "example": "Base CC: 1.925,00 €", "gdpr_basis": "art. 6.1.c RGPD"}]},
 "confidence_scores": {"metadata": 95, "ner": 92, "iptc": 88, "secondary_taxonomy": 74, "pii": 96},
}

CON = {
 "document_type": "Contrato de distribución internacional (borrador del distribuidor)", "document_icon": "📑", "mode": "comparison",
 "scope": "borrador de Kestrelby frente a la plantilla de distribución",
 "summary": ["El borrador de Kestrelby cambia las 15 cláusulas propias de la plantilla, casi siempre a favor del distribuidor.",
             "Precio mínimo de reventa y exclusividad territorial amplia: riesgo de competencia.",
             "Norvalia asume responsabilidad ilimitada; la del distribuidor se limita a 50.000 €.",
             "Siete años con prórrogas de cinco, sin desistimiento para Norvalia y con compensación de dos anualidades.",
             "Faltan las cláusulas de protección de datos, auditoría, sostenibilidad e integridad."],
 "clauses": [
  {"category": "OTHER", "title": "Exclusividad también frente a Norvalia", "description": "Exclusiva en un territorio de ocho países, que se amplía con las ventas del distribuidor; Norvalia paga un 8% de lo que venda allí.", "risk_level": "HIGH", "source": "A"},
  {"category": "ECONOMIC", "title": "Precio mínimo de reventa", "description": "Fija un precio mínimo de reventa del 95% de la tarifa y permite suspender suministros si no se respeta.", "risk_level": "HIGH", "source": "A"},
  {"category": "ECONOMIC", "title": "Cliente más favorecido retroactivo", "description": "Mejor precio concedido en Europa, con devolución de la diferencia de los 24 meses anteriores.", "risk_level": "HIGH", "source": "A"},
  {"category": "ECONOMIC", "title": "Pago a 120 días desde la reventa", "description": "Pago a 120 días desde la venta al cliente final, sin intereses durante 60 días y con compensación libre.", "risk_level": "HIGH", "source": "A"},
  {"category": "LIABILITY_WARRANTIES", "title": "Responsabilidad asimétrica", "description": "Norvalia responde sin límite, incluido el lucro cesante; el distribuidor, hasta 50.000 € en total.", "risk_level": "HIGH", "source": "A"},
  {"category": "LIABILITY_WARRANTIES", "title": "Garantía de 60 meses", "description": "Garantía de 60 meses desde la reventa, con reembolso doble a elección del distribuidor.", "risk_level": "MEDIUM", "source": "A"},
  {"category": "TERM_DURATION", "title": "Siete años con prórrogas de cinco", "description": "Vigencia hasta el 30/09/2033; Norvalia necesita 24 meses de preaviso y el distribuidor, 30 días.", "risk_level": "HIGH", "source": "A"},
  {"category": "TERMINATION_PENALTIES", "title": "Compensación por clientela", "description": "Dos anualidades de margen bruto y recompra de existencias a tarifa al terminar, por cualquier causa.", "risk_level": "HIGH", "source": "A"},
  {"category": "CONFIDENTIALITY_IP", "title": "Depósito de planos y fabricación", "description": "Norvalia deposita planos, programas y parámetros, que se liberan al distribuidor al terminar.", "risk_level": "HIGH", "source": "A"},
  {"category": "OTHER", "title": "Cambio de control desde el 25%", "description": "El cambio de control de Norvalia exige consentimiento y da al distribuidor un derecho preferente sobre la línea de negocio.", "risk_level": "HIGH", "source": "A"},
  {"category": "OTHER", "title": "Derecho inglés y arbitraje en Londres", "description": "Excluye las normas españolas de distribución; Norvalia anticipa todas las costas.", "risk_level": "MEDIUM", "source": "A"},
  {"category": "OTHER", "title": "Plantilla: distribución no exclusiva por dos años", "description": "Modelo de la firma: no exclusiva, volúmenes mínimos, responsabilidad limitada a doce meses de compras y ley española.", "risk_level": "LOW", "source": "B"}],
 "comparison": {"alignment_score": 18, "alignment_summary": "El borrador se aparta de la plantilla en todas las cláusulas propias del modelo y suprime cuatro cláusulas generales.",
  "discrepancies": [
   {"clause_category": "OTHER", "doc_a_summary": "Distribución exclusiva, también frente a Norvalia, en ocho países y ampliable", "doc_b_summary": "Distribución no exclusiva en Reino Unido e Irlanda, con venta directa reservada", "severity": "HIGH", "recommendation": "Mantener la no exclusividad o limitarla a Reino Unido e Irlanda con objetivos vinculantes"},
   {"clause_category": "ECONOMIC", "doc_a_summary": "Precio mínimo de reventa y precios fijos durante todo el plazo", "doc_b_summary": "Reventa libre y tarifa revisable una vez al año", "severity": "HIGH", "recommendation": "Eliminar el precio mínimo de reventa: es una restricción especialmente grave de competencia"},
   {"clause_category": "ECONOMIC", "doc_a_summary": "Pago a 120 días desde la reventa, con compensación libre", "doc_b_summary": "Pago a 60 días desde la recepción, sin compensación", "severity": "HIGH", "recommendation": "Volver a 60 días desde la recepción, conforme a la Ley 3/2004"},
   {"clause_category": "LIABILITY_WARRANTIES", "doc_a_summary": "Norvalia sin límite y con lucro cesante; el distribuidor, 50.000 €", "doc_b_summary": "Límite recíproco de doce meses de compras, sin daños indirectos", "severity": "HIGH", "recommendation": "Restablecer el límite recíproco"},
   {"clause_category": "TERM_DURATION", "doc_a_summary": "Siete años y prórrogas de cinco; solo el distribuidor puede desistir", "doc_b_summary": "Dos años; prórroga solo por acuerdo; desistimiento con seis meses", "severity": "HIGH", "recommendation": "Plazo inicial de dos años con desistimiento recíproco"},
   {"clause_category": "TERMINATION_PENALTIES", "doc_a_summary": "Dos anualidades de margen y recompra a tarifa", "doc_b_summary": "Sin compensación por clientela, en lo que permita la ley; recompra opcional", "severity": "HIGH", "recommendation": "Suprimir la compensación pactada"},
   {"clause_category": "CONFIDENTIALITY_IP", "doc_a_summary": "Depósito de planos que se liberan al distribuidor; mejoras propiedad del distribuidor", "doc_b_summary": "Norvalia conserva todos los derechos", "severity": "HIGH", "recommendation": "Eliminar el depósito y la cesión de mejoras"},
   {"clause_category": "OTHER", "doc_a_summary": "Derecho inglés, arbitraje en Londres y costas a cargo de Norvalia", "doc_b_summary": "Ley española y juzgados de Madrid", "severity": "MEDIUM", "recommendation": "Mantener la ley española o, como mínimo, un arbitraje con costas compartidas"},
   {"clause_category": "OTHER", "doc_a_summary": "Sin cláusulas de protección de datos, auditoría, sostenibilidad ni integridad", "doc_b_summary": "Incluye las cuatro", "severity": "MEDIUM", "recommendation": "Reincorporarlas sin cambios"}]},
 "compliance_risks": [
  {"category": "LEGAL", "severity": "CRITICAL", "description": "Fijar un precio mínimo de reventa es una restricción especialmente grave que excluye la exención por categorías.", "regulation_reference": "Reglamento (UE) 2022/720, art. 4.a; art. 101 TFUE"},
  {"category": "LEGAL", "severity": "HIGH", "description": "La exclusividad que impide atender pedidos no solicitados restringe las ventas pasivas.", "regulation_reference": "Reglamento (UE) 2022/720, art. 4.b"},
  {"category": "CONTRACTUAL", "severity": "HIGH", "description": "El aplazamiento a 120 días desde la reventa supera el máximo legal de 60 días.", "regulation_reference": "Ley 3/2004 de medidas contra la morosidad"},
  {"category": "GDPR", "severity": "MEDIUM", "description": "No hay cláusula de protección de datos para los contactos y clientes compartidos.", "regulation_reference": "Reglamento (UE) 2016/679"}],
 "regulatory_alerts": [
  {"regulation": "Reglamento (UE) 2022/720 de acuerdos verticales", "jurisdiction": "EU", "status": "IN_FORCE", "relevance": "El contrato es un acuerdo vertical con exclusividad territorial y precios de reventa.", "action_required": "Revisar con el área de competencia antes de firmar"},
  {"regulation": "Ley 3/2004 de lucha contra la morosidad", "jurisdiction": "NATIONAL", "status": "IN_FORCE", "relevance": "Plazos de pago entre empresas.", "action_required": "Limitar el plazo de pago a 60 días"},
  {"regulation": "Anteproyecto de ley de contratos de distribución", "jurisdiction": "NATIONAL", "status": "PENDING", "relevance": "Podría regular la compensación por clientela y los preavisos.", "action_required": "Seguir su tramitación"}],
 "due_diligence_score": {"overall": 31, "legal": 22, "financial": 35, "operational": 40, "reputational": 55},
 "recommendations": ["Devolver el borrador y negociar sobre la plantilla de la firma.",
                     "Eliminar el precio mínimo de reventa y la restricción de ventas pasivas.",
                     "Restablecer el límite de responsabilidad recíproco y la ley española.",
                     "Reducir el plazo a dos años, con desistimiento recíproco y sin compensación pactada.",
                     "Reincorporar protección de datos, auditoría, sostenibilidad e integridad."],
}

FRA = {
 "case_type": "Registro de notas de gasto (tercer trimestre de 2026)", "case_icon": "💳",
 "scope": "notas de gasto del tercer trimestre de 2026",
 "summary": ["119 gastos por 52.632,33 €; 28 muestran señales de riesgo.",
             "Un proveedor sin contrato cobra cinco cargos de 2.900 € repartidos entre cuatro empleados.",
             "Tordalia, vinculada al administrador, factura 11.400 € como consultoría sin justificantes.",
             "EMP-031 concentra importes justo por debajo de 500 € y comidas durante sus vacaciones.",
             "Hay dos autoaprobaciones, un pago en efectivo y un kilometraje imposible."],
 "fraud_risk": {"overall_score": 78, "risk_level": "HIGH", "risk_description": "Varias señales se repiten y se concentran en pocas personas y proveedores. Los patrones de fraccionamiento y autoaprobación indican que los controles de aprobación no funcionan.",
  "indicators": [
   {"signal": "Fraccionamiento entre empleados", "description": "Vía Solana Servicios cobra cinco cargos idénticos de 2.900 € en ocho días, imputados por cuatro personas.", "severity": "CRITICAL", "evidence": "GTO-2026-T3-078, 081, 084, 087 y 093: 14.500 €"},
   {"signal": "Pagos a parte vinculada", "description": "Tordalia, sociedad del administrador único, cobra 3.800 € al mes como consultoría sin justificantes.", "severity": "HIGH", "evidence": "GTO-2026-T3-044, 072 y 119: 11.400 €"},
   {"signal": "Importes justo bajo el umbral", "description": "Seis gastos de EMP-031 entre 496,80 y 499 €, por debajo del límite de 500 €.", "severity": "HIGH", "evidence": "GTO-2026-T3-003, 012, 024, 036, 070 y 091: 2.989,30 €"},
   {"signal": "Autoaprobación", "description": "Dos personas aprueban sus propios gastos, una de ellas un cargo de Vía Solana.", "severity": "HIGH", "evidence": "GTO-2026-T3-049 (Sonia Reyes) y 078 (David Ortega)"},
   {"signal": "Gastos en vacaciones y fin de semana", "description": "Cuatro comidas en un chiringuito durante las vacaciones de la empleada, dos en sábado y dos en domingo.", "severity": "MEDIUM", "evidence": "GTO-2026-T3-053, 054, 063 y 064"},
   {"signal": "Kilometraje imposible", "description": "3.750 km en un día y, la misma fecha, un hotel en Sevilla.", "severity": "MEDIUM", "evidence": "GTO-2026-T3-098: 712,50 €"},
   {"signal": "Pago en efectivo", "description": "1.980 € en efectivo con recibo manuscrito.", "severity": "MEDIUM", "evidence": "GTO-2026-T3-105"},
   {"signal": "Ticket duplicado", "description": "Mismo restaurante e importe con tres días de diferencia, uno marcado como «ticket reenviado».", "severity": "MEDIUM", "evidence": "GTO-2026-T3-020 y 029: 186,40 €"},
   {"signal": "Categoría incoherente", "description": "Compra en una joyería registrada como material de oficina.", "severity": "MEDIUM", "evidence": "GTO-2026-T3-114: 320 €"}]},
 "anomalies": [
  {"type": "Concentración por proveedor", "description": "Vía Solana, Tordalia e Impulso Digital suman 35.900 €, el 68% del gasto del trimestre en solo diez cargos.", "deviation": "El gasto medio del resto es de 154 € por nota"},
  {"type": "Aprobación en el mismo día", "description": "Dos pagos de 5.000 € a Impulso Digital Norte aprobados el mismo día de la solicitud.", "deviation": "Importes redondos por encima del umbral de revisión"},
  {"type": "Concentración por empleado", "description": "EMP-031 acumula 10 comidas y alojamientos por 3.407,30 €, sin identificar al cliente.", "deviation": "Cuatro veces y media más que la siguiente persona (EMP-071, 738,02 €)"}],
 "risk_register": [
  {"category": "FINANCIAL", "title": "Pagos sin contraprestación acreditada", "description": "Vía Solana y Tordalia suman 25.900 € sin contrato, entregables ni justificantes.", "probability": "HIGH", "impact": "HIGH", "mitigation": "Suspender pagos y pedir contratos y entregables"},
  {"category": "REGULATORY", "title": "Operaciones vinculadas no autorizadas", "description": "Los pagos a la sociedad del administrador pueden requerir aprobación de la junta y afectan a covenants bancarios.", "probability": "HIGH", "impact": "HIGH", "mitigation": "Revisión por el órgano de administración y comunicación al banco"},
  {"category": "OPERATIONAL", "title": "Segregación de funciones insuficiente", "description": "Hay autoaprobaciones y aprobaciones en el mismo día sin revisión adicional.", "probability": "HIGH", "impact": "MEDIUM", "mitigation": "Bloquear la autoaprobación en el sistema y exigir un segundo aprobador desde 2.000 €"},
  {"category": "LEGAL", "title": "Gastos personales como gastos de empresa", "description": "Comidas en vacaciones y compras en joyería pueden suponer apropiación indebida.", "probability": "MEDIUM", "impact": "MEDIUM", "mitigation": "Investigación interna con audiencia a la persona afectada"},
  {"category": "REPUTATIONAL", "title": "Hallazgo en una due diligence", "description": "Un comprador detectaría estos patrones en una revisión del gasto.", "probability": "MEDIUM", "impact": "MEDIUM", "mitigation": "Corregir y documentar antes de abrir el data room"}],
 "risk_matrix": {"legal": 58, "financial": 82, "operational": 74, "reputational": 61, "regulatory": 66},
 "recommended_actions": ["Bloquear los pagos a Vía Solana Servicios y pedir contrato y entregables.",
                         "Elevar al órgano de administración los pagos a Tordalia Inversiones.",
                         "Revisar con la persona EMP-031 los gastos bajo umbral y en vacaciones.",
                         "Impedir la autoaprobación y exigir doble firma desde 2.000 €.",
                         "Reclamar justificantes del kilometraje, el pago en efectivo y la joyería."],
}

TABS = {
 "doc": ("Nómina de octubre (E02)", DOC, ["traspaso-laboral_large/E02-nomina-octubre-2026.pdf"]),
 "contracts": ("Distribución: borrador frente a plantilla", CON, ["contratos_large/contrato-recibido-kestrelby.pdf", "contratos_large/plantilla-distribucion.pdf"]),
 "fraud": ("Notas de gasto del T3 2026", FRA, ["fraude_large/notas-gasto-2026-t3.csv"]),
}


def generar():
    b = BASE / "analisis-offline"; j = APP / "data" / "demo-offline"; b.mkdir(exist_ok=True); j.mkdir(parents=True, exist_ok=True); idx = {}
    for tab, (label, result, files) in TABS.items():
        fs = [{"name": p.split("/")[-1], "type": mimetypes.guess_type(p)[0] or "application/octet-stream", "data": base64.b64encode((BASE / p).read_bytes()).decode()} for p in files]
        d = {"format": "suite-analysis", "version": 1, "synthetic": True, "date": DATE, "tab": tab, "label": label, "files": fs, "result": result}
        txt = json.dumps(d, ensure_ascii=False)
        (b / f"analisis-{tab}.json").write_text(txt, encoding="utf-8")
        (j / f"{tab}.js").write_text(f"// Datos sintéticos de demostración (generador_large/offline_suite.py). No editar a mano.\nwindow.DemoOffline && window.DemoOffline.ready({json.dumps(tab)}, {txt});\n", encoding="utf-8")
        idx[tab] = [{"key": tab, "label": label, "docs": len(fs)}]
    (j / "suite-index.js").write_text("// Casos sin conexión de los tabs Document Intelligence, Contratos y Fraude. Generado por generador_large/offline_suite.py.\nwindow.DEMO_OFFLINE_SUITE = " + json.dumps(idx, ensure_ascii=False) + ";\n", encoding="utf-8")
