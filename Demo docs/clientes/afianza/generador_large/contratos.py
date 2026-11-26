"""Contrato de distribución recibido frente a la plantilla de la firma (pestaña Contratos)."""
from .comun import ADM, AUD, COMP, CONF, CONT, FM, GEN, INT, LEY, NOT, NV, REP, RGPD, SOST, cola, nv, parte
from .motor import est, eur, pdf

DIR = "contratos_large"
DIST = "Kestrelby Components Ltd."

# Cada cláusula: (título, [texto de plantilla], [texto del contrato recibido] o None si es idéntica)
C = [
 ("Definiciones", ["Productos: los conectores de la gama NX-200 relacionados en el Anexo 1, con las modificaciones que las partes acuerden por escrito.", "Territorio: los países relacionados en el Anexo 2.", "Canal: los fabricantes, integradores y mayoristas establecidos en el Territorio.", "Año Contractual: cada periodo de doce meses desde la fecha de entrada en vigor.", "Control: la titularidad de la mayoría de los derechos de voto o la facultad de designar a la mayoría del órgano de administración."],
  ["Productos: los conectores de las gamas NX-200 y NX-300, así como cualquier producto futuro que Norvalia fabrique o comercialice, aunque no figure en el Anexo 1.", "Territorio: los países relacionados en el Anexo 2 y cualquier otro en el que el Distribuidor realice ventas durante dos trimestres consecutivos.", "Canal: cualquier cliente público o privado, sin limitación.", "Año Contractual: cada año natural.", "Control: la titularidad, directa o indirecta, de una participación igual o superior al 25% de los derechos de voto."]),
 ("Nombramiento", ["Norvalia nombra al Distribuidor como distribuidor no exclusivo de los Productos en el Territorio.", "Norvalia se reserva la venta directa y el nombramiento de otros distribuidores.", "El Distribuidor actúa en nombre y por cuenta propios y no podrá obligar a Norvalia."],
  ["Norvalia nombra al Distribuidor como distribuidor exclusivo de los Productos en el Territorio, también frente a las ventas directas de Norvalia.", "Norvalia no atenderá pedidos, aun no solicitados, de clientes del Territorio y los remitirá al Distribuidor, que percibirá un 8% de las ventas que Norvalia realice pese a ello.", "El Distribuidor actúa en nombre y por cuenta propios y podrá nombrar subdistribuidores sin autorización."]),
 ("Obligaciones del Distribuidor", ["Promover las ventas, mantener personal técnico formado y prestar atención previa y posterior a la venta.", "Mantener existencias equivalentes a tres meses de ventas previstas.", "Entregar informes trimestrales de ventas, existencias y previsión.", "Cumplir la normativa del Territorio y obtener las autorizaciones necesarias."],
  ["Promover las ventas con esfuerzos razonables, según su criterio comercial.", "Mantener existencias en depósito, propiedad de Norvalia, equivalentes a tres meses de ventas. El riesgo permanece en Norvalia hasta la venta al cliente final.", "Entregar un informe anual de ventas agregadas, sin identificación de clientes.", "Norvalia obtendrá y costeará las autorizaciones y certificaciones del Territorio."]),
 ("Objetivos de compra", ["El Distribuidor adquirirá en cada Año Contractual los volúmenes mínimos del Anexo 3.", "Si no alcanza el 80% del mínimo durante dos años consecutivos, Norvalia podrá resolver el contrato.", "El incumplimiento no genera penalización económica."],
  ["Los volúmenes del Anexo 3 son objetivos orientativos y no vinculantes.", "Norvalia no podrá resolver ni reducir la exclusividad por no alcanzarse los objetivos.", "Si Norvalia sirve menos del 95% de los pedidos en plazo, abonará una penalización de 40 euros por cada unidad no servida, sin límite."]),
 ("Precios", ["Los precios son los de la tarifa vigente, con los descuentos del Anexo 4.", "Norvalia podrá revisar la tarifa una vez al año con sesenta días de preaviso.", "El Distribuidor fija libremente sus precios de reventa."],
  ["Los precios quedan fijados durante todo el plazo inicial, sin revisión por coste de materias primas.", "Cláusula de cliente más favorecido: Norvalia aplicará al Distribuidor el mejor precio que conceda a cualquier cliente en Europa y le devolverá la diferencia de los veinticuatro meses anteriores.", "El Distribuidor no venderá por debajo del precio mínimo de reventa que figura en el Anexo 4. El incumplimiento permitirá suspender los suministros."]),
 ("Pago", ["Las facturas se pagarán por transferencia a sesenta días desde la recepción de la mercancía.", "La demora devengará el interés de la Ley 3/2004.", "No cabe retención ni compensación sin acuerdo previo."],
  ["Las facturas se pagarán a ciento veinte días desde la venta al cliente final.", "No se devengarán intereses de demora durante los primeros sesenta días de retraso.", "El Distribuidor podrá compensar cualquier importe que considere adeudado por Norvalia o por sociedades de su grupo."]),
 ("Pedidos y entregas", ["Los pedidos se confirman en cinco días hábiles. Las entregas se realizan FCA Getafe (Incoterms 2020).", "El plazo ordinario es de veinte días hábiles.", "El Distribuidor comunicará los defectos aparentes en diez días."],
  ["Los pedidos se entienden aceptados por su mera remisión. Las entregas se realizan DDP almacén del Distribuidor (Incoterms 2020).", "El plazo máximo es de diez días hábiles. Su incumplimiento permite adquirir productos sustitutivos a costa de Norvalia.", "El Distribuidor podrá comunicar defectos en cualquier momento de la vida útil del producto."]),
 ("Marcas y publicidad", ["El Distribuidor usará las marcas conforme al manual de Norvalia y con aprobación previa de los materiales.", "No registrará marcas, denominaciones ni dominios confundibles.", "Cesará en su uso a la terminación."],
  ["El Distribuidor podrá usar y adaptar las marcas sin aprobación previa.", "El Distribuidor podrá registrar a su nombre dominios y denominaciones que incluyan las marcas en el Territorio.", "Podrá seguir usándolas hasta veinticuatro meses después de la terminación."]),
 ("Garantía de producto", ["Norvalia garantiza los Productos durante veinticuatro meses desde la entrega.", "La garantía comprende reparación, sustitución o abono, a elección de Norvalia.", "Se excluyen el uso indebido y las modificaciones de terceros."],
  ["Norvalia garantiza los Productos durante sesenta meses desde la venta al cliente final.", "La garantía comprende, a elección del Distribuidor, sustitución, reembolso doble o costes de terceros.", "Norvalia organizará y costeará cualquier retirada de producto que el Distribuidor estime conveniente."]),
 ("Responsabilidad", ["Salvo dolo o culpa grave, la responsabilidad anual de cada parte se limita al importe de las compras de los doce meses anteriores.", "Se excluyen el lucro cesante y los daños indirectos.", "Cada parte mantendrá un seguro de responsabilidad civil de 1.000.000 euros."],
  ["La responsabilidad del Distribuidor se limita a 50.000 euros por todo el contrato. La responsabilidad de Norvalia no tiene límite.", "Norvalia responderá del lucro cesante, los daños indirectos y las penalizaciones que los clientes impongan al Distribuidor.", "Norvalia mantendrá un seguro de responsabilidad civil de 5.000.000 euros, con cobertura mundial y el Distribuidor como asegurado adicional."]),
 ("Propiedad industrial", ["Norvalia conserva la titularidad de todos los derechos sobre los Productos.", "El Distribuidor comunicará las infracciones que conozca. Norvalia decidirá las acciones."],
  ["Las mejoras sugeridas por el Distribuidor y sus derivados serán propiedad del Distribuidor, que concederá a Norvalia una licencia revocable.", "Norvalia depositará ante un tercero los planos, programas y parámetros de fabricación, que se liberarán al Distribuidor en caso de terminación por cualquier causa."]),
 ("No competencia", ["Durante la vigencia, el Distribuidor informará de los productos competidores que distribuya.", "No existe obligación de no competencia tras la terminación."],
  ["Norvalia no fabricará para terceros productos destinados al Territorio durante la vigencia y los tres años posteriores.", "Ninguna de las partes contratará empleados de la otra durante la vigencia y los tres años posteriores. Norvalia abonará 100.000 euros por cada infracción."]),
 ("Duración", ["El contrato tiene una duración de dos años desde su firma.", "Cabe prórroga por años sucesivos solo mediante acuerdo escrito."],
  ["El contrato tiene una duración inicial de siete años, hasta el 30 de septiembre de 2033.", "Se prorrogará automáticamente por periodos de cinco años, salvo preaviso de Norvalia de veinticuatro meses. El Distribuidor podrá oponerse con un preaviso de treinta días."]),
 ("Terminación", ["Cualquiera de las partes podrá desistir con un preaviso de seis meses.", "Cabe resolución por incumplimiento grave no subsanado en treinta días.", "A la terminación no procede compensación por clientela, en la medida en que la ley lo permita. Norvalia podrá recomprar existencias."],
  ["Solo el Distribuidor podrá desistir, con un preaviso de treinta días y sin indemnización.", "Norvalia solo podrá resolver por impago superior a 500.000 euros no subsanado en ciento ochenta días.", "A la terminación, por cualquier causa, Norvalia abonará una compensación por clientela equivalente a dos anualidades de margen bruto y recomprará todas las existencias a precio de tarifa."]),
 ("Cesión y cambio de Control", ["Ninguna de las partes podrá ceder el contrato sin consentimiento escrito de la otra.", "El cambio de Control se comunicará en quince días y permitirá a la otra parte resolver si el adquirente es competidor."],
  ["El Distribuidor podrá ceder libremente el contrato. Norvalia necesitará el consentimiento del Distribuidor.", "El cambio de Control de Norvalia requerirá el consentimiento del Distribuidor, que tendrá un derecho de adquisición preferente sobre la línea de negocio de los Productos al valor contable."]),
]
LEY2 = """## {n}. Ley aplicable y resolución de conflictos
{n}.1. El contrato se rige por el derecho de Inglaterra y Gales, con exclusión de las normas imperativas españolas sobre distribución.
{n}.2. Las controversias se resolverán mediante arbitraje confidencial en Londres, en inglés y con tres árbitros. Norvalia anticipará la totalidad de las costas.
{n}.3. El Distribuidor podrá solicitar medidas cautelares ante cualquier tribunal. Norvalia renuncia a esta facultad."""
CONF2 = CONF.replace("los tres años siguientes a su terminación", "los quince años siguientes a su terminación, únicamente respecto de la información del Distribuidor")


def cuerpo(rec):
    o = []
    for n, (t, a, b) in enumerate(C, 1):
        o.append(f"## {n}. {t}"); o += [f"{n}.{k}. {x}" for k, x in enumerate(b if rec else a, 1)]
    n = len(C) + 1
    # El contrato recibido omite auditoría, protección de datos e integridad.
    blo = [REP, CONF2, CONT, FM, INT, NOT, GEN, LEY2] if rec else [REP, CONF, RGPD, AUD, CONT, SOST, FM, COMP, INT, NOT, GEN, LEY]
    return "\n".join(o) + "\n" + cola(n, *blo)


def anexos(rec):
    r = lambda a, b: b if rec else a
    return f"""
!page
# ANEXO 1. PRODUCTOS
!cols 1.2,3.6,1.2
| Referencia | Descripción | Tarifa (€) |
""" + "\n".join(f"| NX-200-{101+7*i} | Conector industrial de {4+2*(i%5)} vías, serie {'ABCD'[i%4]} | {eur(2.1+.37*i, 2)} |" for i in range(14)) + (("\n" + "\n".join(f"| NX-300-{101+7*i} | Conector de potencia de {2+2*(i%3)} vías | {eur(4.4+.52*i, 2)} |" for i in range(8))) if rec else "") + f"""
# ANEXO 2. TERRITORIO
{r("Reino Unido e Irlanda.", "Reino Unido, Irlanda, Países Nórdicos, Benelux, Alemania, Francia, España y Portugal.")}
# ANEXO 3. {r("VOLÚMENES MÍNIMOS", "OBJETIVOS ORIENTATIVOS")}
!cols 2,1.6,1.6
| Año Contractual | Unidades | Compras (€) |
| 1 | 60.000 | 420.000 |
| 2 | 85.000 | 595.000 |
# ANEXO 4. DESCUENTOS{r("", " Y PRECIO MÍNIMO DE REVENTA")}
!cols 2.4,1.4,1.8
| Tramo anual de compras | Descuento | {r("Observaciones", "Precio mínimo de reventa")} |
| Hasta 250.000 euros | {r("18%", "35%")} | {r("Sobre tarifa", "95% de tarifa")} |
| De 250.000 a 500.000 euros | {r("22%", "40%")} | {r("Sobre tarifa", "95% de tarifa")} |
| Más de 500.000 euros | {r("25%", "45%")} | {r("Sobre tarifa", "95% de tarifa")} |
"""


def generar():
    d = parte(DIST, "N", "14 Alder Quay, Bristol, Reino Unido", "D. Alistair Wrenfield", "director", "el Distribuidor").replace("inscrita en el Registro Mercantil de Madrid, ", "sociedad constituida conforme al derecho de Inglaterra, ")
    t = f"""
# CONTRATO DE DISTRIBUCIÓN INTERNACIONAL
!c En Bristol, a 1 de octubre de 2026
### REUNIDOS
{nv("Norvalia")}
{d}
### EXPONEN
I. Que Norvalia fabrica conectores eléctricos industriales.
II. Que el Distribuidor opera una red comercial en el norte de Europa y desea distribuir los Productos.
III. Que las partes acuerdan las siguientes
### CLÁUSULAS
{cuerpo(True)}
!firma Por Norvalia;Pendiente de firma;||Por el Distribuidor;D. Alistair Wrenfield;Director
{anexos(True)}"""
    pdf(DIR, "contrato-recibido-kestrelby", est("Kestrelby Components", "Industrial distribution", "Georgia", "#2d3e50", "circ", ref="KBC-ES-2026 · Borrador de 1 de octubre de 2026", size=10), t, "Contrato de distribución internacional", ("CONTRATO DE DISTRIBUCIÓN INTERNACIONAL", "Borrador remitido por el Distribuidor", [NV, DIST, "", "1 de octubre de 2026"]), True)
    p = f"""
# PLANTILLA. CONTRATO DE DISTRIBUCIÓN
!i Modelo interno. Versión 4, enero de 2026. Los campos entre corchetes se completan en cada operación.
### REUNIDOS
De una parte, {NV}, representada por [representante]. En adelante, Norvalia.
De otra parte, [denominación social], con domicilio en [domicilio], representada por [representante]. En adelante, el Distribuidor.
### EXPONEN
I. Que Norvalia fabrica conectores eléctricos industriales.
II. Que el Distribuidor dispone de organización comercial en el Territorio.
III. Que las partes acuerdan las siguientes
### CLÁUSULAS
{cuerpo(False)}
Por Norvalia: [firma] Por el Distribuidor: [firma]
{anexos(False)}"""
    pdf(DIR, "plantilla-distribucion", est("Norvalia Conectores", "Modelos de contratación", "Times", "#1f3a5f", "hex", ref="Plantilla DIST-04 · Uso interno", size=10.8), p, "Plantilla de contrato de distribución", ("PLANTILLA", "Contrato de distribución internacional", ["Modelo DIST-04", "Enero de 2026"]), True)
