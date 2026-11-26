"""Análisis sintéticos para la demo sin conexión del tab Due Diligence.

Genera, por caso, el mismo formato que «Guardar análisis» (format: tabular-review) con los PDF incrustados:
- Demo docs/clientes/afianza/analisis-offline/<caso>.json  → opción B: «Cargar análisis guardado».
- data/demo-offline/<caso>.js                               → opción A: selector «Demo sin conexión».
Los valores, citas y páginas salen de REF (comprobados contra el texto del PDF); el informe, las alertas
y los conflictos están redactados a mano. Son datos de demostración, no salida del modelo.
"""
import base64, hashlib, json, re, unicodedata
from pathlib import Path
import pymupdf
from . import dd, laboral, seguros, subvenciones
from .motor import BASE

APP = BASE.parents[2]  # raíz de la app (documents/)
DATE = "2026-11-26T09:00:00.000Z"
FIELDS = {
    "dd": [("contraparte", "Contraparte"), ("objeto", "Objeto"), ("importe", "Importe"), ("vencimiento", "Vencimiento"), ("renovacion", "Renovación"), ("cambio_control", "Cambio de control"), ("exclusividad", "Exclusividad"), ("penalizacion", "Penalizaciones"), ("garantias", "Garantías y covenants"), ("ley_fuero", "Ley y fuero")],
    "seguros": [("aseguradora", "Aseguradora"), ("ramo", "Ramo"), ("coberturas", "Coberturas"), ("limite", "Límite"), ("franquicia", "Franquicia"), ("exclusiones", "Exclusiones"), ("territorio", "Territorio"), ("vencimiento", "Vencimiento"), ("prima", "Prima")],
    "laboral": [("persona", "Código empleado"), ("tipo_doc", "Tipo"), ("categoria", "Categoría"), ("modalidad", "Modalidad y fin"), ("jornada", "Jornada"), ("salario", "Salario bruto anual"), ("antiguedad", "Antigüedad"), ("convenio", "Convenio"), ("ccc", "CCC")],
    "subvenciones": [("tipo_doc", "Tipo"), ("proveedor", "Proveedor"), ("numero", "Número"), ("fecha", "Fecha"), ("base", "Base"), ("iva", "IVA"), ("importe_imputado", "Imputado"), ("pago", "Pago"), ("concepto", "Concepto"), ("condiciones", "Reglas de la convocatoria")],
}
A = lambda sev, title, desc, docs, action: dict(severity=sev, title=title, description=desc, docs=docs, action=action)
C = lambda sev, title, claims, why, impact, action: dict(severity=sev, title=title, claims=[dict(doc=d, field=f, says=s) for d, f, s in claims], why=why, impact=impact, action=action)

CROSS = {
 "dd": dict(scope="contratos comerciales, financieros y societarios de Norvalia Conectores", summary=[
    "La única planta productiva queda sin contrato el 31/12/2026, sin derecho de prórroga.",
    "Un cambio de control activa a la vez el banco, el arrendador, Delta y la Dirección General.",
    "La exclusividad de Borealtia sobre NX-200 y NX-300 choca con el suministro directo a Delta.",
    "El cliente principal, 4,2 M€ al año, vence el 28/02/2027 tras la adenda, sin derecho preferente.",
    "Tordalia, vinculada al administrador, factura 180.000 € al año sin entregables y supera el límite del préstamo."],
  alerts=[
    A("HIGH", "La planta de Getafe se queda sin contrato en 5 semanas", "El arrendamiento de la única planta productiva vence el 31/12/2026, sin prórroga ni tácita reconducción. El retraso en la entrega cuesta 2.200 € al día y perder la planta es causa de vencimiento anticipado del préstamo.", ["D5", "D4"], "Negociar una prórroga antes del cierre y fijarla como condición suspensiva"),
    A("HIGH", "Cambio de control con cuatro efectos simultáneos", "Delta puede resolver con 30 días de preaviso (4,2 M€/año), el banco exigir la amortización total desde el 30% del capital, el arrendador debe consentir y AD-01 puede salir con 290.000 €.", ["D1", "D4", "D5", "D7"], "Obtener consentimientos y renuncias antes del cierre"),
    A("HIGH", "Exclusividad incompatible con el suministro a Delta", "Borealtia tiene la exclusividad de NX-200 y, desde la carta de 2025, de NX-300 en España y Portugal, también frente a ventas directas. Norvalia vende ambas gamas a Delta. La penalización es de 350.000 € por gama y año o fracción.", ["D2", "D10", "D1", "D9"], "Cuantificar la contingencia y pedir una renuncia expresa de Borealtia"),
    A("HIGH", "El cliente principal vence antes de lo que dice el contrato", "La adenda adelanta el vencimiento de Delta del 31/03/2027 al 28/02/2027, sin prórroga tácita y sin derecho preferente en la nueva selección de proveedores.", ["D9", "D1"], "Ajustar el plan de negocio y la valoración a la pérdida posible de Delta"),
    A("HIGH", "Contrato con parte vinculada sin contenido verificable", "Tordalia, propiedad al 100% del administrador único, factura 180.000 € al año sin horas ni entregables. Norvalia solo puede resolver con 18 meses de preaviso y el contrato obliga a los sucesores.", ["D8"], "Exigir su resolución antes del cierre y normalizar el EBITDA"),
    A("HIGH", "Pagos a la parte vinculada por encima del límite del préstamo", "El préstamo limita a 50.000 € anuales los pagos a vinculadas fuera del curso ordinario; Tordalia cobra 180.000 €. Puede ser causa de vencimiento anticipado.", ["D4", "D8"], "Revisar con el banco si hay incumplimiento y pedir dispensa"),
    A("MEDIUM", "Covenant de deuda con poco margen", "La deuda financiera neta es 2,9 veces el EBITDA de 2025 frente a un máximo de 3,0. Una caída del EBITDA de unos 83.000 € rompería la ratio.", ["D4"], "Proyectar la ratio con el plan de negocio posterior a la compra"),
    A("MEDIUM", "Compromiso mínimo de compra con penalización", "Lincera exige 900.000 € al año; a 30/09/2026 faltaban 389.000 €. Si no se compra más, la penalización del 40% sería de hasta 155.600 €.", ["D3"], "Verificar las compras del cuarto trimestre y provisionar la diferencia"),
    A("MEDIUM", "Penalizaciones de Delta endurecidas", "La adenda sube el retraso al 1,5% diario con un máximo del 20% y permite reducir volúmenes hasta un 40% si el cumplimiento baja del 95%. En el primer semestre de 2025 fue del 94,1%.", ["D9"], "Revisar el cumplimiento de entregas de 2026"),
    A("LOW", "Contratos sin ley ni fuero", "La licencia del ERP y el contrato con Tordalia no fijan ley aplicable ni jurisdicción.", ["D6", "D8"], "Incluirlo en las manifestaciones del contrato de compraventa")],
  conflicts=[
    C("HIGH", "Exclusividad de Borealtia frente a la venta directa a Delta", [("D2", "Exclusividad", "Exclusividad de NX-200 en España y Portugal, también frente a ventas directas de Norvalia"), ("D10", "Exclusividad", "La exclusividad se extiende a NX-300, también frente a ventas directas"), ("D1", "Objeto", "Suministro en España de conectores NX-200 y NX-300 a Delta")], "Norvalia vende directamente a Delta las dos gamas que ha dado en exclusiva a Borealtia en el mismo territorio.", "Hasta 700.000 € por año o fracción, acumulables, mientras dure el suministro.", "Obtener una renuncia o carve-out firmado por Borealtia antes del cierre"),
    C("HIGH", "La adenda cambia el vencimiento del contrato con Delta", [("D1", "Vencimiento", "El contrato vence el 31 de marzo de 2027"), ("D9", "Vencimiento", "Vence el 28 de febrero de 2027")], "La adenda posterior prevalece y adelanta un mes el fin del contrato del cliente principal.", "Un mes menos de ingresos de 4,2 M€ anuales y sin derecho preferente para renovar.", "Usar la fecha de la adenda en la valoración"),
    C("MEDIUM", "Pagos a Tordalia frente a la restricción del préstamo", [("D4", "Garantías y covenants", "Pagos a vinculadas limitados a 50.000 euros anuales"), ("D8", "Importe", "180.000 euros anuales fijos, sin detalle de horas ni entregables")], "El préstamo prohíbe pagos a vinculadas de esa cuantía sin consentimiento del banco.", "Posible vencimiento anticipado de 1,75 M€ pendientes.", "Pedir confirmación al banco o dispensa formal")]),
 "seguros": dict(scope="pólizas de seguro de Norvalia Conectores", summary=[
    "El D&O vence el 15/12/2026 sin prórroga y excluye actos tras un cambio de control.",
    "La RC de producto está contratada dos veces por 600.000 € y no cubre México.",
    "Daños materiales tiene infraseguro: 3,1 M€ asegurados frente a 5,4 M€ declarados.",
    "La póliza cyber excluye el ransomware porque el cliente declara MFA parcial."],
  alerts=[
    A("HIGH", "El seguro de directivos vence en plena venta", "El D&O vence el 15/12/2026 sin prórroga automática, sin periodo de descubrimiento y excluye las reclamaciones por actos posteriores a un cambio de control.", ["D3"], "Negociar ya la renovación con periodo de descubrimiento de 6 años"),
    A("HIGH", "Infraseguro en daños materiales", "El contenido está asegurado por 3.100.000 € y el propio tomador declara 5.400.000 €. Con la regla proporcional, un siniestro se indemnizaría al 57,4%.", ["D5"], "Ajustar las sumas aseguradas antes del 31/01/2027"),
    A("HIGH", "Ransomware excluido por la propia declaración del cliente", "La póliza exige MFA en todos los accesos remotos y el cuestionario declara MFA parcial: planta y mantenimiento sin MFA.", ["D4"], "Implantar MFA total y comunicarlo a la aseguradora"),
    A("HIGH", "Ventas en México sin cobertura de producto", "El tomador declara 1.350.000 € anuales en México; ambas pólizas cubren solo la Unión Europea.", ["D1", "D2"], "Pedir suplemento de ámbito o póliza local"),
    A("MEDIUM", "RC de producto contratada dos veces", "La RC general incluye producto con sublímite de 600.000 € y hay una póliza específica por el mismo importe. En la específica se declara no tener otra cobertura.", ["D1", "D2"], "Corregir la declaración y revisar el programa; no prometer el ahorro de 9.800 €"),
    A("MEDIUM", "Límite cyber bajo para el tamaño de la empresa", "El límite agregado es de 250.000 € con una facturación de 18,6 M€ y pérdida de beneficios incluida en el mismo límite.", ["D4"], "Estudiar un límite acorde a un paro de planta de varios días"),
    A("MEDIUM", "Trasladar la planta suspende la cobertura", "Daños materiales asegura la nave de Getafe; un traslado exige aceptación previa y la cobertura queda suspendida hasta entonces.", ["D5"], "Coordinar con la aseguradora cualquier traslado ligado al fin del arrendamiento"),
    A("LOW", "Utillajes de clientes sin cubrir", "Los utillajes de terceros en depósito (198.200 €) están excluidos en RC y en daños materiales.", ["D1", "D5"], "Incluirlos mediante suplemento")],
  conflicts=[
    C("MEDIUM", "Declaración incoherente sobre otras coberturas de producto", [("D2", "Coberturas", "Declara no tener contratada otra cobertura de producto"), ("D1", "Coberturas", "RC general con producto y sublímite de 600.000 euros")], "El cuestionario de la póliza específica niega una cobertura que existe en la RC general.", "Riesgo de reducción de la indemnización por declaración inexacta.", "Comunicar la concurrencia a las dos aseguradoras"),
    C("HIGH", "Valor declarado frente a suma asegurada", [("D5", "Límite", "Contenido asegurado por 3.100.000 euros frente a 5.400.000 declarados")], "", "", "")]),
 "laboral": dict(scope="contratos y nóminas de octubre de la plantilla traspasada", summary=[
    "De siete personas, dos cuadran (E01 y E07) y cinco tienen diferencias que revisar.",
    "E03 sigue en nómina con un contrato temporal vencido el 30/06/2026.",
    "E06 cobra la jornada completa pese a una reducción de jornada vigente desde septiembre.",
    "E04 está por debajo del mínimo de convenio y E05 cotiza con otro código de cuenta."],
  alerts=[
    A("HIGH", "Contrato temporal vencido con nómina en curso", "E03 tenía un contrato temporal hasta el 30/06/2026 y sigue cobrando en octubre. Según el convenio, la relación pasa a ser indefinida. Además, el contrato es de 30 h y la nómina, de 40 h.", ["D6", "D7", "D1"], "Regularizar como indefinido y revisar la jornada real"),
    A("HIGH", "Reducción de jornada no aplicada", "E06 tiene reducción a 30 h y 21.000 € desde el 01/09/2026, pero la nómina de octubre liquida 40 h y 28.000 €.", ["D12", "D13"], "Corregir la nómina y regularizar septiembre y octubre"),
    A("HIGH", "Categoría y salario inferiores al contrato", "E02 tiene contrato de oficial de primera con 26.400 €; la nómina le aplica oficial de segunda y 23.100 €. Diferencia de 3.300 € al año.", ["D4", "D5"], "Confirmar la categoría real y cuantificar atrasos"),
    A("HIGH", "Salario por debajo del convenio", "E04 cobra 20.400 € como especialista; el mínimo del convenio para 2026 es de 21.300 €.", ["D8", "D9", "D1"], "Actualizar el salario y abonar la diferencia de 900 €"),
    A("MEDIUM", "Código de cuenta de cotización distinto", "El contrato de E05 indica la CCC 28/0000001/00 y la nómina cotiza por la 45/0000002/00.", ["D10", "D11"], "Verificar el alta en la Seguridad Social"),
    A("MEDIUM", "Antigüedad distinta en contrato y nómina", "E03 figura con antigüedad del 01/01/2025 en el contrato y del 01/07/2025 en la nómina.", ["D6", "D7"], "Fijar la antigüedad correcta: afecta a la indemnización"),
    A("LOW", "Sin diferencias en E01 y E07", "Contrato y nómina coinciden en categoría, jornada, salario, antigüedad, convenio y cotización.", ["D2", "D3", "D14", "D15"], "Ninguna")],
  conflicts=[
    C("HIGH", "E02: contrato y nómina no coinciden", [("D4", "Categoría", "Oficial de primera"), ("D5", "Categoría", "Oficial de segunda"), ("D4", "Salario bruto anual", "26.400 euros"), ("D5", "Salario bruto anual", "23.100 euros, en 14 pagas")], "La nómina aplica una categoría y un salario inferiores a los pactados.", "3.300 € anuales de posible reclamación por persona.", "Revisar el historial de nóminas de los últimos 12 meses"),
    C("HIGH", "E06: la nómina ignora la reducción de jornada", [("D12", "Jornada", "30 horas semanales desde el 01/09/2026"), ("D13", "Jornada", "40 horas semanales")], "El acuerdo de reducción no se ha trasladado a la nómina.", "Pago en exceso de unos 500 € al mes y cotización incorrecta.", "Aplicar la reducción y regularizar"),
    C("MEDIUM", "E05: dos códigos de cotización", [("D10", "CCC", "28/0000001/00"), ("D11", "CCC", "45/0000002/00")], "La persona cotiza por un código distinto del de su contrato.", "Posibles diferencias de tarifa de accidentes y requerimientos.", "Confirmar con la TGSS")]),
 "subvenciones": dict(scope="cuenta justificativa de la ayuda INNOVA del proyecto NX-500", summary=[
    "De 229.400 € imputados, 112.640 € incumplen alguna regla de las bases.",
    "Hay una factura duplicada, otra con IVA y otra pagada en efectivo.",
    "Dos facturas del mismo molde se fraccionan para no pedir tres ofertas.",
    "Personal propio imputa 1.900 horas frente a un máximo de 1.720."],
  alerts=[
    A("HIGH", "Factura imputada dos veces", "La factura F-118 de Sensores Hayedal (24.000 €) aparece en los expedientes 01 y 06. Las bases prohíben imputar una factura más de una vez.", ["D2", "D7", "D1"], "Retirar el expediente 06"),
    A("HIGH", "Gasto vinculado sin autorización", "Tordalia, vinculada al administrador único, factura 15.000 € de gestión. Las bases exigen autorización previa y la resolución dice que no se pidió.", ["D6", "D1", "D15"], "Excluir el gasto o justificar condiciones de mercado"),
    A("HIGH", "Contrato fraccionado para evitar tres ofertas", "Moldes Acebeda emite dos facturas de 14.500 € en días consecutivos para el mismo molde y el mismo pedido PC-25-0611. Juntas suman 29.000 € y superan el umbral de 15.000 €.", ["D9", "D10", "D1"], "Aportar tres ofertas o excluir los 29.000 €"),
    A("HIGH", "Pago fuera de plazo", "El software de simulación (18.000 €) se pagó el 15/04/2026; la fecha límite era el 31/03/2026.", ["D8", "D1"], "Excluir el gasto"),
    A("HIGH", "Factura fuera del periodo elegible", "Los ensayos (12.500 €) se facturaron el 14/01/2026, aunque el servicio se prestó en diciembre de 2025.", ["D4", "D1"], "Excluir el gasto"),
    A("MEDIUM", "IVA imputado", "Ingeniería Pinarea: base de 30.000 € e imputación de 36.300 €. El IVA recuperable no es subvencionable.", ["D3", "D1"], "Reducir la imputación en 6.300 €"),
    A("MEDIUM", "Pago en efectivo", "El pequeño material (2.800 €) se pagó por caja; las bases solo admiten transferencia.", ["D5", "D1"], "Excluir el gasto"),
    A("MEDIUM", "Horas de personal por encima del máximo", "Se imputan 1.900 horas de una persona; el máximo es de 1.720 al año. El exceso es de 180 horas, 5.040 €.", ["D11", "D1"], "Reducir la imputación a 1.720 horas"),
    A("LOW", "Gastos sin incidencias", "Los expedientes 01, 11, 12 y 13 cumplen las reglas revisadas.", ["D2", "D12", "D13", "D14"], "Ninguna")],
  conflicts=[
    C("HIGH", "La misma factura en dos expedientes", [("D2", "Número", "F-118"), ("D7", "Número", "F-118")], "Las dos fichas imputan la misma factura con distinto concepto.", "24.000 € de posible reintegro.", "Retirar la segunda imputación"),
    C("HIGH", "Dos facturas para un mismo pedido", [("D9", "Concepto", "Molde prototipo, primera parte. Pedido PC-25-0611"), ("D10", "Concepto", "Molde prototipo, segunda parte. Pedido PC-25-0611")], "Un único pedido se factura en dos partes por debajo de 15.000 €.", "29.000 € en riesgo por fraccionamiento.", "Aportar ofertas o excluir"),
    C("MEDIUM", "Contratación vinculada sin autorización", [("D6", "Proveedor", "Tordalia Inversiones, S.L., vinculada al administrador único"), ("D15", "Reglas de la convocatoria", "Sin autorización para partes vinculadas")], "La resolución confirma que no se pidió la autorización que exige el artículo 10.", "15.000 € no subvencionables.", "Excluir el gasto")]),
}
# El conflicto de un solo documento no es válido en la app: se quita.
CROSS["seguros"]["conflicts"] = CROSS["seguros"]["conflicts"][:1]
CASOS = {"dd": dd, "seguros": seguros, "laboral": laboral, "subvenciones": subvenciones}
LABEL = {"dd": "Contratos mercantiles", "seguros": "Seguros", "laboral": "Traspaso laboral", "subvenciones": "Subvenciones"}
# Instrucción («ask») de cada campo, leída de la plantilla de la app.
_TPL = (APP / "prompts" / "tabular.js").read_text(encoding="utf-8")
fold = lambda s: re.sub(r"[\s«»“”\"'’‘\-‐‑­]", "", unicodedata.normalize("NFKC", s).lower())


def ask(tpl, key):
    blk = _TPL[_TPL.index(f"    {tpl}: {{"):]
    return re.search(r"key: '" + key + r"', label: '[^']*', ask: '([^']*)'", blk).group(1)


def caso(k):
    m = CASOS[k]
    if not m.REF: m.generar()
    carpeta = BASE / m.DIR; files = sorted(m.REF); rows = []
    for i, fn in enumerate(files):
        raw = (carpeta / fn).read_bytes(); pages = [fold(p.get_text()) for p in pymupdf.open(stream=raw)]
        cells = {}
        for key, label in FIELDS[k]:
            v = m.REF[fn].get(key)
            if not v: cells[key] = {"value": None, "quote": None, "page": None, "confidence": None, "risk": "NONE", "check": "none"}; continue
            pg = next((n for n, t in enumerate(pages, 1) if fold(v[1]) in t), None)
            if pg is None: raise SystemExit(f"Cita no encontrada: {fn} {key}")
            conf = 80 + int(hashlib.md5(f"{fn}{key}".encode()).hexdigest(), 16) % 18 - (6 if v[2] == "HIGH" else 0)
            cells[key] = {"value": v[0], "quote": v[1], "page": pg, "confidence": conf, "risk": v[2], "check": "ok"}
        rows.append({"id": f"D{i+1}", "name": fn, "error": None, "cut": False, "cells": cells, "type": "application/pdf", "data": base64.b64encode(raw).decode()})
    ids = {r["id"] for r in rows}
    for a in CROSS[k]["alerts"]: assert set(a["docs"]) <= ids, (k, a["title"])
    for c in CROSS[k]["conflicts"]: assert {x["doc"] for x in c["claims"]} <= ids and len({x["doc"] for x in c["claims"]}) >= 2, c["title"]
    return {"format": "tabular-review", "version": 1, "synthetic": True, "date": DATE, "template": k, "fields": [{"key": a, "label": b, "ask": ask(k, a)} for a, b in FIELDS[k]], "rows": rows, "cross": CROSS[k], "stats": {"in": 0, "out": 0, "s": 0}}


def generar():
    b = BASE / "analisis-offline"; j = APP / "data" / "demo-offline"; b.mkdir(exist_ok=True); j.mkdir(parents=True, exist_ok=True); idx = []
    for k in CASOS:
        d = caso(k); txt = json.dumps(d, ensure_ascii=False)
        (b / f"analisis-{k}.json").write_text(txt, encoding="utf-8")
        (j / f"{k}.js").write_text(f"// Datos sintéticos de demostración (generador_large/offline.py). No editar a mano.\nwindow.DemoOffline && window.DemoOffline.ready({json.dumps(k)}, {txt});\n", encoding="utf-8")
        idx.append({"key": k, "label": LABEL[k], "docs": len(d["rows"])})
    (j / "index.js").write_text("// Índice de casos sin conexión. Generado por generador_large/offline.py.\nwindow.DEMO_OFFLINE_CASES = " + json.dumps(idx, ensure_ascii=False) + ";\n", encoding="utf-8")
