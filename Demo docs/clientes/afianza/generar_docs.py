# /// script
# requires-python = ">=3.10"
# dependencies = ["reportlab"]
# ///
"""Genera los PDF ficticios de la demo. Uso: uv run generar_docs.py"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

BASE = Path(__file__).parent
S = getSampleStyleSheet()
S["BodyText"].leading = 15
N = "Norvalia Ficticia, S.L."
LEY = ("Ley y fuero", "El contrato se rige por la ley española. Las partes se someten a los juzgados y tribunales de Madrid.")
CONF = ("Confidencialidad", "Las partes mantendrán en secreto la información recibida durante la vigencia y los tres años siguientes a su terminación.")
DATOS = ("Protección de datos", "Las partes tratarán los datos de contacto de los firmantes con la única finalidad de gestionar la relación contractual.")


def pie(c, d):
    c.setFont("Helvetica", 7)
    c.drawString(57, 28, "Documento ficticio creado para una demostración. Sin valor legal.")
    c.drawRightString(540, 28, f"Página {d.page}")


def pdf(carpeta, nombre, titulo, intro, clausulas, corte=4):
    ruta = BASE / carpeta
    ruta.mkdir(exist_ok=True)
    f = [Paragraph(titulo, S["Title"]), Spacer(1, 8), Paragraph(intro, S["BodyText"]), Spacer(1, 8)]
    for i, (t, x) in enumerate(clausulas, 1):
        if corte and i == corte + 1:
            f.append(PageBreak())
        f += [Paragraph(f"{i}. {t}", S["Heading3"]), Paragraph(x, S["BodyText"])]
    SimpleDocTemplate(str(ruta / f"{nombre}.pdf"), pagesize=A4, title=titulo, author="Demo").build(f, pie, pie)


def dd():
    d = "due-diligence"
    pdf(d, "01-suministro-delta", "CONTRATO DE SUMINISTRO", f"Firmado el 1 de abril de 2024 entre {N} (el Proveedor) y Automoción Delta Ficticia, S.A. (el Cliente).", [
        ("Objeto", "Suministro en España de conectores de la gama NX-200 y NX-300 para líneas de montaje."),
        ("Precio", "El volumen anual estimado es de 4.200.000 euros, IVA no incluido. Los precios se revisan cada enero."),
        ("Duración", "El contrato vence el 31 de marzo de 2027. No cabe prórroga tácita; cualquier prórroga requiere acuerdo escrito."),
        ("Calidad", "El Proveedor responde de los defectos durante 24 meses desde la entrega."),
        ("Cambio de control", "Si cambia el control, directo o indirecto, del Proveedor, el Cliente podrá resolver el contrato sin penalización con un preaviso de 30 días."),
        ("Penalizaciones", "El retraso en la entrega devenga un 1% del pedido por día, con un máximo del 15% del pedido."), CONF, LEY])
    pdf(d, "02-distribucion-boreal", "CONTRATO DE DISTRIBUCIÓN", f"Firmado el 15 de enero de 2023 entre {N} y Energía Boreal Ficticia, S.A. (el Distribuidor).", [
        ("Objeto", "Distribución de conectores de la gama NX-200 en España y Portugal."),
        ("Precio", "Las compras anuales del Distribuidor ascienden a 2.100.000 euros."),
        ("Duración", "Vigente hasta el 14 de enero de 2028, con prórrogas automáticas de un año salvo preaviso de seis meses."),
        ("Pedidos", "Los pedidos se confirman en un plazo de cinco días hábiles."),
        ("Exclusividad", "Norvalia concede al Distribuidor la exclusividad de venta de la gama NX-200 en España y Portugal, también frente a ventas directas de Norvalia."),
        ("Penalización", "El incumplimiento de la exclusividad obliga a Norvalia a pagar 350.000 euros por cada año o fracción."), CONF, LEY])
    pdf(d, "03-compra-acero-lince", "CONTRATO MARCO DE COMPRA", f"Firmado el 10 de junio de 2025 entre Aceros Lince Ficticios, S.L. (el Vendedor) y {N} (el Comprador).", [
        ("Objeto", "Compra de fleje de acero para conectores."),
        ("Compromiso mínimo", "El Comprador adquirirá al menos 900.000 euros por año natural."),
        ("Duración", "Vence el 9 de junio de 2028, sin prórroga automática."),
        ("Entregas", "Las entregas se realizan en la planta de Getafe en quince días."),
        ("Penalización", "Si no se alcanza el mínimo, el Comprador abonará el 40% de la diferencia."),
        ("Cesión", "El contrato no puede cederse sin consentimiento escrito de la otra parte."), LEY])
    pdf(d, "04-prestamo-banco", "CONTRATO DE PRÉSTAMO", f"Firmado el 20 de mayo de 2022 entre Banco Ejemplo Ficticio, S.A. (el Banco) y {N} (el Prestatario).", [
        ("Principal", "El Banco concede un préstamo de 3.500.000 euros para financiar la ampliación de la planta."),
        ("Interés", "Euríbor a 12 meses más 2,25%."),
        ("Vencimiento", "El préstamo vence el 20 de mayo de 2029, con amortización trimestral."),
        ("Información", "El Prestatario entrega cuentas auditadas antes del 30 de junio de cada año."),
        ("Covenant", "La deuda financiera neta no superará 3,0 veces el EBITDA. El certificado de cierre de 2025 recoge una ratio de 2,9 veces."),
        ("Cambio de control", "Un cambio de control no autorizado permite al Banco exigir la amortización anticipada total."),
        ("Garantías", "Prenda sobre el 100% de las participaciones del Prestatario e hipoteca sobre la maquinaria."), LEY])
    pdf(d, "05-arrendamiento-nave", "CONTRATO DE ARRENDAMIENTO", f"Firmado el 1 de enero de 2017 entre Inmuebles Sauce Ficticios, S.L. (el Arrendador) y {N} (el Arrendatario).", [
        ("Objeto", "Arrendamiento de la nave industrial de Getafe, única planta productiva del Arrendatario."),
        ("Renta", "La renta es de 264.000 euros anuales, más IVA."),
        ("Duración", "El arrendamiento vence el 31 de diciembre de 2026. No existe derecho de prórroga a favor del Arrendatario."),
        ("Uso", "El inmueble se destina a fabricación y almacén."),
        ("Cesión y cambio de control", "El cambio de control del Arrendatario se considera cesión y exige el consentimiento previo del Arrendador."),
        ("Garantía", "El Arrendatario entrega aval bancario por 132.000 euros."), LEY])
    pdf(d, "06-licencia-erp", "CONTRATO DE LICENCIA DE SOFTWARE", f"Firmado el 3 de octubre de 2024 entre Programas Olmo Ficticios, S.L. (el Licenciante) y {N} (el Licenciatario).", [
        ("Objeto", "Licencia de uso del ERP de producción para 120 usuarios."),
        ("Precio", "La cuota anual es de 78.000 euros."),
        ("Duración", "Vence el 2 de octubre de 2027, con prórroga anual automática salvo preaviso de 90 días."),
        ("Soporte", "Soporte en días laborables de 9:00 a 18:00."),
        ("Intransferibilidad", "La licencia es intransferible, también en fusiones o escisiones, salvo pago de una nueva cuota de alta de 60.000 euros."), DATOS])
    pdf(d, "07-alta-direccion", "CONTRATO DE ALTA DIRECCIÓN", f"Firmado el 1 de septiembre de 2021 entre {N} y la persona que ocupa la Dirección General (código AD-01).", [
        ("Objeto", "Prestación de servicios de Dirección General."),
        ("Retribución", "La retribución fija es de 145.000 euros brutos anuales."),
        ("Duración", "Contrato indefinido."),
        ("Dedicación", "Dedicación plena y exclusiva."),
        ("Cambio de control", "Si cambia el control de la sociedad, AD-01 podrá extinguir el contrato y percibir una indemnización de 24 meses de retribución fija."),
        ("No competencia", "Doce meses tras la extinción, compensados con el 50% de la retribución fija."), LEY])
    pdf(d, "08-servicios-tordo", "CONTRATO DE SERVICIOS DE GESTIÓN", f"Encabezado: 2 de febrero de 2023. Entre Inversiones Tordo Ficticias, S.L. (el Prestador) y {N}.", [
        ("Objeto", "Servicios generales de asesoramiento y gestión, según necesidades."),
        ("Precio", "Importe fijo de 180.000 euros anuales, sin detalle de horas ni entregables."),
        ("Duración", "Indefinida. Norvalia solo puede resolver con un preaviso de 18 meses."),
        ("Vinculación", "El Prestador está participado al 100% por quien ejerce de administrador único de Norvalia."),
        ("Indemnización", "La resolución sin preaviso obliga a pagar las cuotas pendientes del periodo de preaviso."),
        ("Firma", "Firmado en Madrid el 2 de febrero de 2024, con efectos desde la fecha del encabezado.")])


def seguros():
    def pol(nombre, ramo, cia, num, cob, lim, fran, exc, terr, venc, prima):
        pdf("seguros", nombre, f"PÓLIZA DE {ramo.upper()}", f"Aseguradora: {cia}. Póliza: {num}. Tomador: {N}.", [
            ("Coberturas", cob), ("Límite", lim), ("Franquicia", fran), ("Ámbito territorial", terr),
            ("Exclusiones", exc), ("Vigencia", venc), ("Prima", prima)])
    pol("01-rc-general", "Responsabilidad Civil General", "Seguros Alfa Ficticios", "RC-0001", "Explotación, patronal y RC de producto con un sublímite de 600.000 euros.", "1.500.000 euros por siniestro y anualidad.", "3.000 euros por siniestro.", "Se excluyen los daños por productos exportados fuera de la Unión Europea y la retirada de producto.", "Unión Europea.", "Vence el 30 de junio de 2027, con prórroga anual.", "Prima total anual: 14.200 euros.")
    pol("02-rc-producto", "Responsabilidad Civil de Producto", "Seguros Beta Ficticios", "RP-0002", "RC de producto por daños a terceros.", "600.000 euros por siniestro y anualidad.", "6.000 euros por siniestro.", "Se excluyen la retirada de producto y las reclamaciones en EE. UU. y Canadá.", "Unión Europea. Las ventas declaradas en México quedan fuera del ámbito.", "Vence el 31 de marzo de 2027.", "Prima total anual: 9.800 euros.")
    pol("03-do", "Responsabilidad de Administradores y Directivos (D&amp;O)", "Seguros Alfa Ficticios", "DO-0003", "Gastos de defensa y responsabilidad de administradores.", "1.000.000 euros por anualidad.", "Sin franquicia para personas físicas.", "Se excluyen las reclamaciones por actos posteriores a un cambio de control. No se contrata periodo de descubrimiento posterior.", "Todo el mundo, salvo EE. UU. y Canadá.", "Vence el 15 de diciembre de 2026, sin prórroga automática.", "Prima total anual: 5.400 euros.")
    pol("04-cyber", "Ciberriesgos", "Seguros Gamma Ficticios", "CY-0004", "Respuesta a incidentes, pérdida de beneficios y responsabilidad por datos personales.", "250.000 euros por anualidad. La facturación anual declarada es de 18.600.000 euros.", "72 horas de carencia en pérdida de beneficios.", "Se excluye el ransomware si no hay autenticación multifactor en todos los accesos remotos. En el cuestionario, el tomador declara autenticación multifactor parcial.", "Todo el mundo.", "Vence el 28 de febrero de 2027.", "Prima total anual: 7.100 euros.")


def laboral():
    ccc = "Código de cuenta de cotización ficticio: 28/0000001/00."
    conv = "Convenio colectivo ficticio del sector de conectores."
    datos = [
        ("E01", "Técnico/a de calidad", "Técnico/a de calidad", "Indefinido", "40 horas semanales", "40 horas semanales", "27.500", "27.500", "1 de marzo de 2020", "1 de marzo de 2020"),
        ("E02", "Oficial de primera", "Oficial de segunda", "Indefinido", "40 horas semanales", "40 horas semanales", "26.400", "23.100", "15 de mayo de 2018", "15 de mayo de 2018"),
        ("E03", "Administrativo/a", "Administrativo/a", "Temporal hasta el 30 de junio de 2026", "30 horas semanales", "40 horas semanales", "18.900", "18.900", "1 de enero de 2025", "1 de julio de 2025"),
    ]
    for c, g1, g2, mod, j1, j2, s1, s2, a1, a2 in datos:
        pdf("traspaso-laboral", f"{c}-contrato", "CONTRATO DE TRABAJO", f"Empresa: {N}. Código de empleado: {c}.", [
            ("Categoría", g1 + "."), ("Modalidad", mod + "."), ("Jornada", j1 + "."), ("Salario", f"Salario bruto anual de {s1} euros."),
            ("Antigüedad", f"Fecha de antigüedad: {a1}."), ("Convenio", conv), ("Cotización", ccc)], 0)
        pdf("traspaso-laboral", f"{c}-nomina-octubre-2026", "NÓMINA DE OCTUBRE DE 2026", f"Empresa: {N}. Código de empleado: {c}.", [
            ("Categoría", g2 + "."), ("Jornada", j2 + "."), ("Salario", f"Salario bruto anual de {s2} euros, en 14 pagas."),
            ("Antigüedad", f"Fecha de antigüedad: {a2}."), ("Convenio", conv), ("Cotización", ccc)], 0)


def subvenciones():
    d = "subvenciones"
    pdf(d, "00-bases", "BASES REGULADORAS", "Convocatoria ficticia de ayudas a la innovación INNOVA-DEMO.", [
        ("Periodo elegible", "Son elegibles los gastos facturados entre el 1 de enero y el 31 de diciembre de 2025 y pagados antes del 31 de marzo de 2026."),
        ("IVA", "El IVA recuperable no es subvencionable."), ("Pago", "Solo se admite transferencia bancaria. No se admiten pagos en efectivo."),
        ("Partes vinculadas", "La contratación con partes vinculadas exige autorización previa."),
        ("Doble imputación", "Una misma factura solo puede imputarse una vez.")], 0)
    for n, p, num, f, b, iva, imp, pago, con in [
        ("01-sensores", "Sensores Haya Ficticios, S.L.", "F-118", "12 de marzo de 2025", "24.000", "5.040", "24.000", "Transferencia de 10 de abril de 2025", "Sensores para el prototipo del proyecto."),
        ("02-ingenieria", "Ingeniería Pino Ficticia, S.L.", "2025-77", "20 de mayo de 2025", "30.000", "6.300", "36.300", "Transferencia de 18 de junio de 2025", "Diseño del prototipo del proyecto."),
        ("03-ensayos", "Ensayos Roble Ficticios, S.L.", "R-009", "14 de enero de 2026", "12.500", "2.625", "12.500", "Transferencia de 2 de febrero de 2026", "Ensayos del prototipo del proyecto."),
        ("04-material", "Material Fresno Ficticio, S.L.", "A-451", "8 de septiembre de 2025", "2.800", "588", "2.800", "Efectivo el 8 de septiembre de 2025", "Pequeño material para el prototipo."),
        ("05-gestion-tordo", "Inversiones Tordo Ficticias, S.L.", "T-12", "30 de junio de 2025", "15.000", "3.150", "15.000", "Transferencia de 15 de julio de 2025", "Gestión del proyecto. Empresa vinculada al administrador del beneficiario. No consta autorización previa."),
        ("06-sensores-bis", "Sensores Haya Ficticios, S.L.", "F-118", "12 de marzo de 2025", "24.000", "5.040", "24.000", "Transferencia de 10 de abril de 2025", "Sensores para el prototipo del proyecto. Segunda imputación.")]:
        pdf(d, n, f"FACTURA {num}", f"Proveedor: {p} Cliente: {N}", [
            ("Fecha", f"Fecha de emisión: {f}."), ("Concepto", con), ("Importes", f"Base imponible: {b} euros. IVA: {iva} euros."),
            ("Pago", pago + "."), ("Imputación", f"Importe imputado al proyecto: {imp} euros.")], 0)


if __name__ == "__main__":
    for g in (dd, seguros, laboral, subvenciones):
        g()
