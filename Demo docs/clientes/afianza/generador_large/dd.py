"""Due diligence: 10 documentos. REF recoge, por documento y campo, (valor, cita literal, criticidad)."""
import random
from datetime import date, timedelta
from .comun import ADM, AUD, COMP, CONF, CONT, DG, FM, GEN, INT, LEY, NOT, NV, NV_DOM, REP, RGPD, SOST, cola, nv, parte
from .motor import MES, escaneo, est, eur, iban, pdf

DIR = "due-diligence_large"
REF = {}
DELTA, BOREAL, LINCE = "Automoción Deltaria, S.A.", "Borealtia Energía y Distribución, S.A.", "Aceros Lincera, S.L."
BANCO, SAUCE, OLMO, TORDO = "Banco Merediano de Crédito, S.A.", "Inmuebles Saucedal, S.L.", "Olmera Software Industrial, S.L.", "Tordalia Inversiones, S.L."
F_ = lambda d: f"{d.day} de {MES[d.month-1]} de {d.year}"


def articulos(gama, n, seed, base):
    r = random.Random(seed); desc = ["Conector macho 4 vías IP67", "Conector hembra 4 vías IP67", "Conector macho 8 vías sellado", "Conector hembra 8 vías sellado", "Conector híbrido señal-potencia", "Carcasa con bloqueo secundario", "Terminal estañado 1,5 mm²", "Terminal plateado 2,5 mm²", "Pasamuros estanco M12", "Módulo de codificación", "Conector de alta corriente 60 A", "Tapa ciega con junta", "Conector modular 12 vías", "Conector modular 16 vías", "Soporte de fijación a panel"]
    o = []
    for i in range(n):
        o.append(f"| {gama}-{101+i*7} | {desc[i % len(desc)]} | {r.choice([200, 250, 500, 1000])} | {eur(base*r.uniform(.6, 2.4), 3)} | {r.choice([15, 20, 25, 30])} |")
    return "\n".join(o)


def delta():
    t = f"""
# CONTRATO MARCO DE SUMINISTRO
!c En Madrid, a 1 de abril de 2024
### REUNIDOS
{nv("el Proveedor")}
{parte(DELTA, "A", "avenida de la Industria, 220, 50197 Zaragoza", "D.ª Carmen Lasierra Pueyo", "directora de compras y apoderada", "el Cliente", "Zaragoza")}
Las partes se reconocen mutuamente capacidad legal suficiente para contratar y obligarse y, a tal efecto,
### EXPONEN
I. Que el Proveedor se dedica al diseño, fabricación y comercialización de conectores eléctricos industriales, que comercializa bajo las gamas NX-200, NX-300 y NX-500 y fabrica en su planta de Getafe.
II. Que el Cliente fabrica módulos eléctricos para líneas de montaje de automoción y requiere un suministro continuado, con calidad homologada y entregas sincronizadas con su programa de producción.
III. Que el Proveedor ha superado el proceso de homologación del Cliente, finalizado el 12 de febrero de 2024, y que ambas partes desean regular las condiciones que regirán todos los pedidos de los Productos.
IV. Que, en virtud de lo anterior, acuerdan suscribir el presente contrato marco, que se regirá por las siguientes
### CLÁUSULAS
## 1. Definiciones
1.1. Productos: los conectores y accesorios relacionados en el Anexo I, así como las evoluciones de diseño aprobadas por el Cliente conforme a la cláusula 7.
1.2. Pedido: la orden de compra emitida por el Cliente a través de su portal de proveedores, en firme o como entrega programada contra un pedido abierto.
1.3. Programa de Entregas: la previsión móvil de veintiséis semanas que el Cliente actualiza cada lunes y en la que las cuatro primeras semanas tienen carácter firme.
1.4. Planta de Destino: los centros del Cliente en Zaragoza, Vitoria y Martorell relacionados en el Anexo II.
1.5. Control: la titularidad, directa o indirecta, de la mayoría del capital o de los derechos de voto, o la facultad de nombrar a la mayoría del órgano de administración, en el sentido del artículo 42 del Código de Comercio.
1.6. Día Hábil: cualquier día que no sea sábado, domingo ni festivo en Madrid o en la localidad de la Planta de Destino.
## 2. Objeto
2.1. El presente contrato regula el suministro en España de conectores de la gama NX-200 y NX-300 para líneas de montaje, en las cantidades que resulten de los Pedidos.
2.2. El suministro se realizará mediante venta directa del Proveedor al Cliente, sin intermediación de distribuidores, con entrega en las Plantas de Destino.
2.3. El Cliente no asume compromiso de volumen mínimo ni de exclusividad. Las previsiones del Programa de Entregas fuera del horizonte firme tienen carácter orientativo y no generan derecho a indemnización, salvo lo previsto en la cláusula 4.5 para materiales de largo plazo de aprovisionamiento.
## 3. Pedidos y previsiones
3.1. Los Pedidos se entenderán aceptados si el Proveedor no los rechaza de forma motivada en los dos Días Hábiles siguientes a su recepción. Solo podrá rechazarlos si exceden en más de un 20% la capacidad reservada.
3.2. El Proveedor mantendrá una capacidad reservada de 310.000 unidades mensuales de la gama NX-200 y de 120.000 unidades mensuales de la gama NX-300, así como un almacén de seguridad equivalente a diez días de consumo medio.
3.3. El Cliente podrá modificar las cantidades del horizonte firme en un máximo del 15%, al alza o a la baja, con un preaviso de cinco Días Hábiles.
3.4. El Proveedor comunicará de inmediato cualquier circunstancia que pueda comprometer el Programa de Entregas y presentará en veinticuatro horas un plan de contingencia.
## 4. Precio y condiciones económicas
4.1. Los precios unitarios figuran en el Anexo I, en euros, DAP Planta de Destino (Incoterms 2020), embalaje retornable incluido e IVA no incluido.
4.2. A efectos de planificación, el volumen anual estimado es de 4.200.000 euros, IVA no incluido, según el desglose del Anexo II.
4.3. Los precios se revisan cada enero. La revisión aplicará la fórmula del Anexo I, que pondera el índice de precios del cobre, el de la poliamida técnica y el índice de coste laboral, con un límite anual del 4% en ambos sentidos.
4.4. El Proveedor aplicará una reducción por productividad del 1,5% anual acumulativo sobre los precios de la gama NX-200 durante los tres primeros años.
4.5. Si el Cliente cancela referencias con materiales de plazo de aprovisionamiento superior a doce semanas, abonará el coste acreditado de los materiales no reutilizables, con un máximo de seis semanas de consumo previsto.
4.6. Las facturas se emitirán en formato electrónico y se pagarán por transferencia a sesenta días desde la recepción de la mercancía. La demora devengará el interés previsto en la Ley 3/2004.
## 5. Entrega, transporte y embalaje
5.1. El Proveedor entregará los Productos en las ventanas horarias fijadas por cada Planta de Destino. El cumplimiento de entregas se medirá mensualmente y no será inferior al 98,5%.
5.2. El riesgo se transmite con la descarga en la Planta de Destino. La propiedad se transmite con la entrega.
5.3. Cada unidad de embalaje llevará etiqueta con referencia, índice de plano, lote, fecha de fabricación y cantidad, legible por los sistemas del Cliente.
5.4. El Cliente dispone de quince Días Hábiles para comunicar faltas y daños aparentes. La recepción no supone conformidad con la calidad.
## 6. Calidad y garantía
6.1. El Proveedor mantendrá la certificación de su sistema de gestión de la calidad y cumplirá el objetivo de 15 piezas no conformes por millón en la gama NX-200 y de 25 en la gama NX-300.
6.2. El Proveedor responde de los defectos durante 24 meses desde la entrega. La garantía comprende la sustitución de las piezas, los costes de selección, desmontaje y montaje y los costes de paro de línea acreditados.
6.3. Ante una no conformidad, el Proveedor presentará contención en veinticuatro horas, análisis de causa raíz en cinco Días Hábiles y acciones correctoras en quince.
6.4. El Cliente podrá auditar las instalaciones con un preaviso de cinco Días Hábiles. El Proveedor conservará los registros de trazabilidad durante quince años.
## 7. Cambios de producto y de proceso
7.1. Todo cambio de diseño, material, proceso, subproveedor o lugar de fabricación requerirá la aprobación escrita previa del Cliente, con una antelación mínima de ciento ochenta días.
7.2. En particular, el traslado total o parcial de la fabricación fuera de la planta de Getafe exigirá una nueva homologación completa a cargo del Proveedor, cuya duración ordinaria es de nueve meses.
7.3. Los utillajes específicos relacionados en el Anexo III son propiedad del Cliente y se encuentran en depósito en las instalaciones del Proveedor.
## 8. Propiedad industrial e intelectual
8.1. Cada parte conserva la titularidad de sus derechos preexistentes. El Proveedor garantiza que los Productos no infringen derechos de terceros y mantendrá indemne al Cliente frente a cualquier reclamación.
8.2. Los desarrollos específicos financiados por el Cliente serán de su propiedad. El Proveedor no los comercializará a terceros sin autorización.
## 9. Responsabilidad y seguros
9.1. El Proveedor mantendrá una póliza de responsabilidad civil con una cobertura de producto no inferior a 1.000.000 euros por siniestro y acreditará su vigencia cada año.
9.2. Salvo dolo, culpa grave, daños personales o infracción de derechos de terceros, la responsabilidad total de cada parte se limita al importe facturado en los doce meses anteriores.
## 10. Penalizaciones
10.1. El retraso en la entrega devenga un 1% del pedido por día, con un máximo del 15% del pedido. La penalización se aplicará por compensación en la primera factura pendiente.
10.2. El incumplimiento del objetivo de calidad durante tres meses consecutivos dará lugar a una bonificación del 2% de la facturación del trimestre.
10.3. Las penalizaciones tienen carácter cumulativo con la indemnización de los daños efectivamente causados en lo que excedan de aquellas.
## 11. Duración
11.1. El contrato entra en vigor en la fecha de su firma. El contrato vence el 31 de marzo de 2027.
11.2. No cabe prórroga tácita; cualquier prórroga requiere acuerdo escrito. Las partes iniciarán conversaciones al menos seis meses antes del vencimiento, sin que ello suponga obligación de renovar.
11.3. Terminado el contrato, el Proveedor atenderá los pedidos de recambio durante diez años en condiciones de mercado.
## 12. Terminación anticipada
12.1. Cualquiera de las partes podrá resolver el contrato por incumplimiento grave no subsanado en treinta días desde el requerimiento.
12.2. El Cliente podrá resolver de inmediato si el Proveedor pierde la certificación de calidad, incumple durante dos meses consecutivos el 90% de cumplimiento de entregas o incurre en insolvencia, en la medida en que la ley lo permita.
12.3. En caso de terminación, el Proveedor devolverá los utillajes y colaborará en el traspaso del suministro durante un máximo de nueve meses.
## 13. Cesión y cambio de Control
13.1. Ninguna de las partes podrá ceder su posición contractual sin el consentimiento escrito de la otra, salvo a sociedades de su grupo y previa notificación.
13.2. El Proveedor notificará al Cliente toda operación que pueda alterar su estructura de propiedad tan pronto como sus obligaciones de secreto lo permitan y, en todo caso, antes de su cierre.
13.3. Si cambia el control, directo o indirecto, del Proveedor, el Cliente podrá resolver el contrato sin penalización con un preaviso de 30 días. Esta facultad podrá ejercitarse durante los seis meses siguientes a la notificación del cierre.
{cola(14, REP, CONF, RGPD, AUD, CONT, SOST, FM, COMP, INT, NOT, GEN, LEY)}
Y en prueba de conformidad, las partes firman el presente contrato en el lugar y fecha indicados en el encabezamiento.
!firma Por el Proveedor;{ADM};Administrador único||Por el Cliente;D.ª Carmen Lasierra Pueyo;Apoderada
!page
# ANEXO I. PRODUCTOS Y PRECIOS
Precios unitarios vigentes desde el 1 de abril de 2024, en euros por pieza, IVA no incluido.
!cols 1.2,3.4,1,1.2,1.2
| Referencia | Descripción | Lote mínimo | Precio (€) | Plazo (días) |
{articulos("NX-200", 15, "a", 1.9)}
{articulos("NX-300", 12, "b", 3.1)}
### Fórmula de revisión
P1 = P0 × (0,35 + 0,30 × Cu1/Cu0 + 0,20 × Pa1/Pa0 + 0,15 × Cl1/Cl0), donde Cu es el precio medio del cobre del trimestre anterior, Pa el índice de poliamida técnica y Cl el índice de coste laboral armonizado de la industria. Los valores de referencia son los del primer trimestre de 2024.
!page
# ANEXO II. PLANTAS DE DESTINO Y VOLUMEN ESTIMADO
!cols 2,1.4,1.4,1.4
| Planta de Destino | Gama NX-200 (€) | Gama NX-300 (€) | Total anual (€) |
| Zaragoza | 1.260.000 | 540.000 | 1.800.000 |
| Vitoria | 840.000 | 410.000 | 1.250.000 |
| Martorell | 735.000 | 415.000 | 1.150.000 |
| Total | 2.835.000 | 1.365.000 | 4.200.000 |
# ANEXO III. UTILLAJES EN DEPÓSITO
!cols 1,4,1.2,1.4
| Código | Descripción | Año | Valor (€) |
| UT-014 | Molde de inyección carcasa 8 vías, 4 cavidades | 2022 | 46.800 |
| UT-015 | Molde de inyección carcasa 12 vías, 2 cavidades | 2023 | 39.500 |
| UT-021 | Troquel progresivo terminal 1,5 mm² | 2021 | 28.200 |
| UT-027 | Útil de ensamblado automático con visión artificial | 2024 | 61.000 |
| UT-031 | Banco de ensayo de estanqueidad IP67 | 2024 | 22.700 |
"""
    pdf(DIR, "01-suministro-delta", est("Automoción Deltaria", "Compras · Contratación de proveedores", "Arial", "#123f6d", "bar", ref="CMS-2024-0417 · Contrato marco de suministro", size=9.8), t, "Contrato marco de suministro", ("CONTRATO MARCO DE SUMINISTRO", "Conectores eléctricos gamas NX-200 y NX-300", ["entre", NV, "y", DELTA, "", "1 de abril de 2024", "Ref. CMS-2024-0417"]), True, ("nv", "dl"))
    REF["01-suministro-delta.pdf"] = dict(contraparte=(DELTA, DELTA, "NONE"), objeto=("Suministro en España de conectores NX-200 y NX-300 para líneas de montaje", "suministro en España de conectores de la gama NX-200 y NX-300 para líneas de montaje", "LOW"), importe=("4.200.000 euros anuales estimados, IVA no incluido", "el volumen anual estimado es de 4.200.000 euros, IVA no incluido", "MEDIUM"), vencimiento=("2027-03-31", "El contrato vence el 31 de marzo de 2027", "HIGH"), renovacion=("Sin prórroga tácita; exige acuerdo escrito", "No cabe prórroga tácita; cualquier prórroga requiere acuerdo escrito", "HIGH"), cambio_control=("El Cliente puede resolver sin penalización con 30 días de preaviso", "Si cambia el control, directo o indirecto, del Proveedor, el Cliente podrá resolver el contrato sin penalización con un preaviso de 30 días", "HIGH"), exclusividad=("El Cliente no asume exclusividad ni volumen mínimo", "El Cliente no asume compromiso de volumen mínimo ni de exclusividad", "LOW"), penalizacion=("Retraso: 1% del pedido por día, máximo 15%; bonificación del 2% por calidad", "El retraso en la entrega devenga un 1% del pedido por día, con un máximo del 15% del pedido", "MEDIUM"), garantias=("Garantía de 24 meses; seguro de RC de producto de al menos 1.000.000 euros por siniestro", "una cobertura de producto no inferior a 1.000.000 euros por siniestro", "MEDIUM"), ley_fuero=("Ley española; juzgados de Madrid capital", "El contrato se rige por la ley española", "NONE"))


def adenda():
    t = f"""
# ADENDA N.º 1 AL CONTRATO MARCO DE SUMINISTRO
!c Referencia CMS-2024-0417/A1
!c En Zaragoza, a 15 de septiembre de 2025
### REUNIDOS
{nv("el Proveedor")}
{parte(DELTA, "A", "avenida de la Industria, 220, 50197 Zaragoza", "D. Íñigo Barasoain Goñi", "director general y apoderado", "el Cliente", "Zaragoza")}
### EXPONEN
I. Que el 1 de abril de 2024 suscribieron un contrato marco de suministro de conectores de las gamas NX-200 y NX-300 (el Contrato).
II. Que el Cliente va a renovar sus líneas de montaje en el primer trimestre de 2027, con un nuevo proceso de selección de proveedores, y precisa ajustar el calendario del Contrato.
III. Que durante el primer semestre de 2025 el cumplimiento de entregas fue del 94,1%, inferior al 98,5% pactado, por lo que las partes han acordado reforzar el régimen de penalizaciones.
IV. Que, en consecuencia, modifican el Contrato en los términos que siguen. Los términos en mayúscula tienen el significado que les atribuye el Contrato.
### ESTIPULACIONES
## Primera. Objeto
La presente adenda modifica el Contrato de suministro de conectores NX-200 y NX-300 en lo relativo a duración, penalizaciones, almacén de seguridad y proceso de renovación.
## Segunda. Modificación de la cláusula 11 (Duración)
La cláusula 11.1 queda sustituida por la siguiente: «El contrato entra en vigor en la fecha de su firma y vence el 28 de febrero de 2027.»
La cláusula 11.2 mantiene su redacción en cuanto a la exclusión de la prórroga tácita. Se añade que el Proveedor no tendrá derecho preferente en el nuevo proceso de selección.
## Tercera. Modificación de la cláusula 10 (Penalizaciones)
La cláusula 10.1 queda sustituida por la siguiente: «El retraso en la entrega devenga un 1,5% del pedido por día, con un máximo del 20% del pedido.»
Se añade una cláusula 10.4: «Si el cumplimiento de entregas es inferior al 95% durante dos trimestres consecutivos, el Cliente podrá reducir los volúmenes del Programa de Entregas hasta en un 40% sin compensación.»
## Cuarta. Almacén de seguridad
El almacén de seguridad de la cláusula 3.2 se eleva de diez a veinte días de consumo medio. El Proveedor completará la constitución antes del 30 de noviembre de 2025 y asumirá su coste financiero, que las partes estiman en 38.000 euros anuales.
## Quinta. Precios
No se modifica el volumen anual estimado. Los precios de la gama NX-300 se reducen un 0,8% desde el 1 de octubre de 2025. El detalle figura en el anexo a esta adenda.
## Sexta. Subsistencia
En lo no modificado expresamente, el Contrato continúa en vigor, incluida la facultad de resolución por cambio de Control de la cláusula 13.3. En caso de contradicción prevalecerá la presente adenda.
## Séptima. Ley y fuero
La adenda se rige por la ley española. Las partes se someten a los juzgados y tribunales de Madrid capital, conforme a la cláusula de jurisdicción del Contrato.
!firma Por el Proveedor;{ADM};Administrador único||Por el Cliente;D. Íñigo Barasoain Goñi;Director general
!page
# ANEXO. SEGUIMIENTO DE ENTREGAS Y PLAN DE MEJORA
!cols 1.2,1.3,1.3,1.3,2
| Mes de 2025 | Líneas previstas | Líneas en plazo | Cumplimiento | Causa principal |
| Enero | 412 | 396 | 96,1% | Rotura de utillaje UT-021 |
| Febrero | 398 | 379 | 95,2% | Retraso de fleje de acero |
| Marzo | 431 | 403 | 93,5% | Saturación de ensamblado |
| Abril | 405 | 377 | 93,1% | Saturación de ensamblado |
| Mayo | 420 | 391 | 93,1% | Absentismo en turno de noche |
| Junio | 434 | 406 | 93,5% | Saturación de ensamblado |
| Total | 2500 | 2352 | 94,1% | |
### Plan de mejora comprometido
- Segundo turno de ensamblado desde el 1 de octubre de 2025. Responsable: dirección de operaciones del Proveedor.
- Segunda fuente homologada de fleje de acero antes del 31 de enero de 2026. El Proveedor mantendrá, en todo caso, sus compromisos de compra vigentes.
- Reunión quincenal de seguimiento con la planta de Zaragoza hasta alcanzar el 98,5% durante tres meses consecutivos.
### Precios NX-300 desde el 1 de octubre de 2025
!cols 1.2,3.4,1,1.2,1.2
| Referencia | Descripción | Lote mínimo | Precio (€) | Plazo (días) |
{articulos("NX-300", 12, "b", 3.1 * .992)}
"""
    pdf(DIR, "09-adenda-delta", est("Automoción Deltaria", "Compras · Contratación de proveedores", "Arial", "#123f6d", "bar", ref="CMS-2024-0417/A1 · Adenda n.º 1"), t, "Adenda al contrato marco de suministro", rub=("nv", "dl2"))
    REF["09-adenda-delta.pdf"] = dict(contraparte=(DELTA, DELTA, "NONE"), objeto=("Adenda al suministro de conectores NX-200 y NX-300: duración y penalizaciones", "modifica el Contrato de suministro de conectores NX-200 y NX-300", "MEDIUM"), importe=("Sin cambio de volumen anual; precios NX-300 se reducen un 0,8%", "No se modifica el volumen anual estimado", "LOW"), vencimiento=("2027-02-28", "vence el 28 de febrero de 2027", "HIGH"), renovacion=("Sin prórroga tácita ni derecho preferente en la nueva selección", "el Proveedor no tendrá derecho preferente en el nuevo proceso de selección", "HIGH"), cambio_control=("Subsiste la facultad de resolución del Cliente por cambio de control", "incluida la facultad de resolución por cambio de Control de la cláusula 13.3", "HIGH"), exclusividad=None, penalizacion=("Retraso: 1,5% del pedido por día, máximo 20%; reducción de volúmenes hasta el 40%", "El retraso en la entrega devenga un 1,5% del pedido por día, con un máximo del 20% del pedido", "HIGH"), garantias=("Almacén de seguridad de veinte días a cargo del Proveedor", "El almacén de seguridad de la cláusula 3.2 se eleva de diez a veinte días de consumo medio", "LOW"), ley_fuero=("Ley española; juzgados de Madrid capital", "La adenda se rige por la ley española", "NONE"))


def boreal():
    t = f"""
# CONTRATO DE DISTRIBUCIÓN
!c En Madrid, a 15 de enero de 2023
### REUNIDOS
{nv("Norvalia")}
{parte(BOREAL, "A", "calle de la Ría, 48, 48009 Bilbao", "D.ª Nerea Aguirrezabala Otxoa", "consejera delegada", "el Distribuidor", "Bizkaia")}
### EXPONEN
I. Que Norvalia fabrica conectores eléctricos industriales, entre ellos la gama NX-200, y desea reforzar su presencia en los sectores energético, ferroviario y de automatización.
II. Que el Distribuidor dispone de una red de once delegaciones, equipo comercial especializado y capacidad logística en España y Portugal.
III. Que ambas partes han convenido establecer una relación estable de distribución con arreglo a las siguientes
### CLÁUSULAS
## 1. Objeto
1.1. Norvalia nombra al Distribuidor, que acepta, para la distribución de conectores de la gama NX-200 en España y Portugal (el Territorio). El Distribuidor compra y revende en nombre y por cuenta propios.
1.2. Son Productos los conectores de la gama NX-200 incluidos en cada momento en el catálogo de Norvalia, con sus accesorios y recambios, según el Anexo 1.
1.3. Norvalia podrá incorporar o retirar referencias con un preaviso de noventa días. La retirada total de la gama requerirá acuerdo entre las partes.
## 2. Obligaciones del Distribuidor
2.1. Promover activamente la venta de los Productos, mantener personal técnico formado y atender las consultas posteriores a la venta en primera instancia.
2.2. Mantener existencias equivalentes a seis semanas de venta media en sus almacenes de Bilbao, Madrid y Oporto.
2.3. Entregar cada trimestre un informe de ventas por referencia, sector y provincia, una previsión a doce meses y la relación de ofertas superiores a 50.000 euros.
2.4. No fabricar ni distribuir en el Territorio productos que compitan con los Productos durante los cinco primeros años de vigencia.
2.5. Emplear las marcas de Norvalia conforme a su manual de identidad y cesar en su uso en los sesenta días siguientes a la terminación.
## 3. Obligaciones de Norvalia
3.1. Suministrar los Productos en plazo y calidad, facilitar documentación técnica y prestar formación, al menos dos veces al año.
3.2. Trasladar al Distribuidor las consultas comerciales de terceros relativas a los Productos que reciba desde el Territorio.
3.3. Informar con antelación razonable de los cambios de catálogo, precio y condiciones de fabricación.
## 4. Precio y volumen de compras
4.1. Los Productos se facturarán a precio de tarifa con los descuentos del Anexo 1. Norvalia podrá revisar la tarifa una vez al año con un preaviso de sesenta días.
4.2. Las compras anuales del Distribuidor ascienden a 2.100.000 euros, importe tomado de la media de los dos ejercicios anteriores y que las partes adoptan como objetivo de referencia.
4.3. Alcanzado el objetivo, el Distribuidor percibirá un rappel del 3%, y del 4,5% si lo supera en más de un 15%.
4.4. El Distribuidor fijará libremente sus precios de reventa. Cualquier indicación de precio por parte de Norvalia tendrá carácter de recomendación.
4.5. Las facturas se abonarán a sesenta días mediante domiciliación bancaria.
## 5. Pedidos y entregas
5.1. Los pedidos se confirman en un plazo de cinco días hábiles. Las entregas se realizarán FCA planta de Getafe (Incoterms 2020).
5.2. El plazo ordinario de entrega será de veinte días hábiles. En los pedidos urgentes, Norvalia hará sus mejores esfuerzos para servir en ocho.
5.3. El Distribuidor examinará la mercancía a su recepción y comunicará los defectos aparentes en diez días.
## 6. Garantía y responsabilidad por producto
6.1. Norvalia garantiza los Productos durante veinticuatro meses frente a defectos de diseño, material o fabricación. La garantía comprende reparación o sustitución.
6.2. Cada parte mantendrá asegurada su responsabilidad civil y facilitará certificado a solicitud de la otra.
## 7. Duración
7.1. El contrato entra en vigor en la fecha de su firma y está vigente hasta el 14 de enero de 2028.
7.2. Llegado el vencimiento, se renovará con prórrogas automáticas de un año salvo preaviso de seis meses notificado por cualquiera de las partes.
## 8. Régimen territorial y comercial
8.1. Norvalia concede al Distribuidor la exclusividad de venta de la gama NX-200 en España y Portugal, también frente a ventas directas de Norvalia. La exclusividad alcanza a todos los sectores y canales, con independencia del volumen y de la naturaleza del cliente final.
8.2. En consecuencia, Norvalia no venderá los Productos en el Territorio a terceros distintos del Distribuidor ni nombrará agentes u otros distribuidores. Las relaciones preexistentes figuran en el Anexo 2.
8.3. Norvalia podrá suministrar fuera del Territorio sin limitación y atender las ventas pasivas que la normativa de competencia no permita restringir.
8.4. El Distribuidor mantendrá la exclusividad mientras alcance, en cada periodo de dos años, el 75% del objetivo de la cláusula 4.2.
## 9. Incumplimiento de la exclusividad
9.1. El incumplimiento de la exclusividad obliga a Norvalia a pagar 350.000 euros por cada año o fracción en que se produzca, con independencia del margen obtenido y del número de operaciones.
9.2. Esta cantidad tiene carácter de cláusula penal sustitutiva de daños, sin perjuicio de la facultad del Distribuidor de exigir el cumplimiento o instar la resolución.
9.3. El Distribuidor podrá solicitar una vez al año un certificado de ventas directas en el Territorio emitido por el auditor de Norvalia.
## 10. Terminación
10.1. Cualquiera de las partes podrá resolver por incumplimiento esencial no subsanado en cuarenta y cinco días.
10.2. A la terminación, Norvalia podrá recomprar las existencias en buen estado a precio de coste. El Distribuidor renuncia a la compensación por clientela en la medida en que la ley lo permita.
10.3. El cambio de control de cualquiera de las partes no dará lugar por sí mismo a la terminación, pero será comunicado a la otra en los quince días siguientes.
{cola(11, REP, CONF, RGPD, AUD, CONT, SOST, FM, COMP, INT, NOT, GEN, LEY)}
!firma Por Norvalia;{ADM};Administrador único||Por el Distribuidor;D.ª Nerea Aguirrezabala Otxoa;Consejera delegada
!page
# ANEXO 1. PRODUCTOS, TARIFA Y DESCUENTOS
!cols 1.2,3.4,1,1.2,1.2
| Referencia | Descripción | Lote mínimo | Tarifa (€) | Dto. (%) |
{articulos("NX-200", 28, "c", 2.6)}
# ANEXO 2. RELACIONES PREEXISTENTES EXCLUIDAS
!cols 2.4,2,1.6
| Cliente | Producto | Fin de la excepción |
| Ferrotrac Servicios, S.L. | NX-200, recambios | 31 de diciembre de 2023 |
| Elevaciones Cantal, S.A. | NX-200, módulos de 4 vías | 30 de junio de 2023 |
No existen otras relaciones preexistentes a la fecha de firma.
!page
# ANEXO 3. INFORME TRIMESTRAL DE VENTAS (MODELO)
!cols 1.2,1.4,1.4,1.4,1.4
| Sector | T1 (€) | T2 (€) | T3 (€) | T4 (€) |
| Energía | 198.400 | 211.900 | 187.300 | 224.600 |
| Ferroviario | 121.700 | 118.200 | 109.500 | 132.800 |
| Automatización | 143.600 | 151.100 | 138.900 | 156.300 |
| Otros | 49.100 | 52.400 | 47.800 | 56.400 |
| Total | 512.800 | 533.600 | 483.500 | 570.100 |
"""
    pdf(DIR, "02-distribucion-boreal", est("Norvalia Conectores", "Dirección comercial", "Georgia", "#7a2e1d", "hex", ref="Contrato de distribución · NX-200 · España y Portugal", size=9.8), t, "Contrato de distribución", ("CONTRATO DE DISTRIBUCIÓN", "Gama NX-200 · España y Portugal", [NV, BOREAL, "", "15 de enero de 2023"]), True, ("nv", "bo"))
    REF["02-distribucion-boreal.pdf"] = dict(contraparte=(BOREAL, BOREAL, "NONE"), objeto=("Distribución de conectores NX-200 en España y Portugal", "distribución de conectores de la gama NX-200 en España y Portugal", "LOW"), importe=("2.100.000 euros anuales de compras", "Las compras anuales del Distribuidor ascienden a 2.100.000 euros", "MEDIUM"), vencimiento=("2028-01-14", "está vigente hasta el 14 de enero de 2028", "NONE"), renovacion=("Prórrogas automáticas de un año salvo preaviso de seis meses", "prórrogas automáticas de un año salvo preaviso de seis meses", "LOW"), cambio_control=("No termina el contrato; comunicación en 15 días", "El cambio de control de cualquiera de las partes no dará lugar por sí mismo a la terminación", "LOW"), exclusividad=("A favor del Distribuidor: NX-200 en España y Portugal, también frente a ventas directas de Norvalia", "Norvalia concede al Distribuidor la exclusividad de venta de la gama NX-200 en España y Portugal, también frente a ventas directas de Norvalia", "HIGH"), penalizacion=("350.000 euros por cada año o fracción de incumplimiento de la exclusividad", "El incumplimiento de la exclusividad obliga a Norvalia a pagar 350.000 euros por cada año o fracción", "HIGH"), garantias=("Garantía de producto de veinticuatro meses", "Norvalia garantiza los Productos durante veinticuatro meses", "NONE"), ley_fuero=("Ley española; juzgados de Madrid capital", "El contrato se rige por la ley española", "NONE"))


def carta():
    t = f"""
!c Bilbao, 3 de febrero de 2025
{NV}
A la atención de {ADM}
{NV_DOM}
### Asunto: ampliación del contrato de distribución de 15 de enero de 2023. Gama NX-300
Estimado Ramiro:
Tras la reunión mantenida el pasado 22 de enero en vuestras oficinas, y como contrapartida al esfuerzo comercial realizado por {BOREAL} para la introducción de la nueva gama, confirmamos por la presente carta (la Carta) los términos acordados. La Carta complementa el contrato de distribución suscrito el 15 de enero de 2023 (el Contrato), cuyos términos definidos se utilizan aquí con el mismo significado.
## 1. Ampliación de Productos
Se incorpora la gama NX-300 a la distribución en España y Portugal, con efectos desde el 1 de marzo de 2025. El catálogo inicial comprende las referencias relacionadas en la hoja adjunta.
## 2. Exclusividad
La exclusividad de la cláusula 8 del Contrato se extiende a la gama NX-300 en España y Portugal, también frente a ventas directas de Norvalia. No se establecen relaciones preexistentes excluidas para esta gama.
## 3. Penalización
El incumplimiento de la exclusividad de la gama NX-300 devengará una penalización adicional de 350.000 euros por cada año o fracción, acumulable a la prevista en la cláusula 9 del Contrato.
## 4. Volumen
Borealtia estima compras de la gama NX-300 por 480.000 euros anuales a partir del segundo ejercicio. La estimación no constituye compromiso de compra.
## 5. Lanzamiento
Borealtia invertirá 60.000 euros en acciones de lanzamiento durante 2025, incluidas dos ferias sectoriales, demostradores y formación de su red. Norvalia aportará muestras sin cargo por un valor máximo de 12.000 euros a precio de tarifa.
## 6. Duración
La Carta se mantendrá en vigor mientras lo esté el Contrato, cuyo plazo vigente finaliza el 14 de enero de 2028, y seguirá su mismo régimen de prórrogas automáticas anuales.
## 7. Confidencialidad
Las partes mantendrán reservado el contenido de la Carta, que no será comunicado a la red comercial ni a clientes de ninguna de ellas.
## 8. Otros extremos
En lo no previsto será de aplicación el Contrato, incluida su cláusula de ley aplicable y jurisdicción: ley española y juzgados de Madrid capital.
Os rogamos que nos devolváis copia firmada en señal de conformidad.
Un cordial saludo,
!firma Por Borealtia;D.ª Nerea Aguirrezabala Otxoa;Consejera delegada||Recibido y conforme, por Norvalia;{ADM};Administrador único
!sello NORVALIA CONECTORES;;RECIBIDO 07 FEB 2025
!page
### Hoja adjunta. Catálogo inicial NX-300
!cols 1.2,3.4,1,1.2,1.2
| Referencia | Descripción | Lote mínimo | Tarifa (€) | Dto. (%) |
{articulos("NX-300", 20, "d", 3.6)}
### Calendario de lanzamiento
!cols 1.4,4,1.4
| Fecha | Acción | Presupuesto (€) |
| Marzo de 2025 | Formación técnica de las once delegaciones | 9.500 |
| Abril de 2025 | Feria sectorial de automatización | 21.000 |
| Junio de 2025 | Demostradores para ingenierías | 11.500 |
| Octubre de 2025 | Feria sectorial de energía | 18.000 |
| Total | | 60.000 |
"""
    pdf(DIR, "10-carta-boreal", est("Borealtia", "Energía y Distribución", "Georgia", "#0f5b52", "circ", ref="Borealtia Energía y Distribución, S.A."), t, "Carta de acuerdo NX-300")
    REF["10-carta-boreal.pdf"] = dict(contraparte=(BOREAL, BOREAL, "NONE"), objeto=("Ampliación de la distribución a la gama NX-300 en España y Portugal", "Se incorpora la gama NX-300 a la distribución en España y Portugal", "MEDIUM"), importe=("480.000 euros anuales estimados, sin compromiso", "estima compras de la gama NX-300 por 480.000 euros anuales", "LOW"), vencimiento=("2028-01-14", "cuyo plazo vigente finaliza el 14 de enero de 2028", "NONE"), renovacion=("Prórrogas automáticas anuales, como el Contrato", "seguirá su mismo régimen de prórrogas automáticas anuales", "LOW"), cambio_control=None, exclusividad=("A favor de Borealtia: NX-300 en España y Portugal, también frente a ventas directas de Norvalia", "se extiende a la gama NX-300 en España y Portugal, también frente a ventas directas de Norvalia", "HIGH"), penalizacion=("350.000 euros adicionales por año o fracción, acumulables", "una penalización adicional de 350.000 euros por cada año o fracción", "HIGH"), garantias=None, ley_fuero=("Ley española; juzgados de Madrid capital", "ley española y juzgados de Madrid capital", "NONE"))


def lince():
    t = f"""
# CONTRATO MARCO DE COMPRA DE MATERIA PRIMA
!c En Getafe, a 10 de junio de 2025
### REUNIDOS
{nv("el Comprador")}
{parte(LINCE, "B", "polígono La Fundición, parcela 9, 33400 Avilés (Asturias)", "D. Baldomero Quirós Llaneza", "consejero delegado", "el Vendedor", "Asturias")}
### EXPONEN
I. Que el Vendedor transforma y comercializa fleje de acero laminado en frío y dispone de capacidad para atender las necesidades del Comprador.
II. Que el Comprador desea asegurar el abastecimiento de la materia prima de sus terminales y contactos, y el Vendedor, amortizar la inversión en la línea de corte de precisión dedicada.
### CLÁUSULAS
## 1. Objeto
1.1. El contrato regula la compra de fleje de acero para conectores, en las calidades, espesores y tolerancias del Anexo A.
1.2. El Vendedor reservará una capacidad anual de 620 toneladas en su línea de corte número 3.
## 2. Pedidos y planificación
2.1. El Comprador enviará antes del día 20 de cada mes el pedido en firme del mes siguiente y una previsión de los cinco posteriores.
2.2. El Vendedor confirmará en tres días hábiles. La falta de confirmación equivale a aceptación si la cantidad no supera en un 10% la previsión.
2.3. Las bobinas se servirán con un peso unitario entre 180 y 240 kilogramos, salvo petición distinta en el pedido.
## 3. Precio
3.1. El precio base es de 1.480 euros por tonelada, al que se añade el extra de calidad y espesor del Anexo A y el recargo de aleación del mes de entrega.
3.2. El precio base se revisará cada seis meses según el índice de referencia de acero laminado en frío del norte de Europa, en la parte en que la variación supere el 3%.
3.3. El pago se realizará a cuarenta y cinco días desde la fecha de factura mediante transferencia. El Vendedor podrá exigir seguro de crédito cuando el saldo vivo supere 250.000 euros.
## 4. Entregas
4.1. Las entregas se realizan en la planta de Getafe en quince días desde el pedido en firme, DAP (Incoterms 2020).
4.2. El retraso superior a cinco días dará derecho a un descuento del 0,5% del importe de la entrega por día, con un máximo del 5%.
4.3. Se admite una tolerancia de cantidad del 5% por posición de pedido.
## 5. Calidad y certificados
5.1. Cada bobina se acompañará de certificado de inspección 3.1 según norma EN 10204 con composición, características mecánicas y rugosidad.
5.2. El Comprador dispondrá de treinta días para reclamar defectos. El material defectuoso será sustituido o abonado, con los costes de transformación acreditados hasta el doble de su valor.
## 6. Obligaciones de volumen
6.1. Atendida la reserva de capacidad, el Comprador adquirirá al menos 900.000 euros por año natural, importe que se medirá por facturación neta de abonos y recargos de aleación.
6.2. En 2025 el volumen se prorrateará por los días transcurridos desde la firma.
6.3. Si no se alcanza el mínimo, el Comprador abonará el 40% de la diferencia. El Vendedor emitirá la factura en enero del año siguiente, con vencimiento a treinta días.
6.4. Los pedidos rechazados por calidad y los no servidos por causa del Vendedor computarán como adquiridos.
## 7. Duración
7.1. El contrato entra en vigor a su firma y vence el 9 de junio de 2028, sin prórroga automática.
7.2. La terminación anticipada por voluntad del Comprador no le libera del compromiso de los años naturales pendientes, que se liquidará conforme a la cláusula 6.3.
## 8. Cesión y cambio de socios
8.1. El contrato no puede cederse sin consentimiento escrito de la otra parte. No tendrá la consideración de cesión el cambio en el accionariado del Comprador siempre que se mantengan sus compromisos.
## 9. Reserva de dominio
9.1. El material permanecerá en propiedad del Vendedor hasta su pago íntegro. El Comprador podrá transformarlo en el curso ordinario de su actividad.
{cola(10, REP, CONF, RGPD, AUD, CONT, SOST, FM, COMP, INT, NOT, GEN, LEY)}
!firma Por el Vendedor;D. Baldomero Quirós Llaneza;Consejero delegado||Por el Comprador;{ADM};Administrador único
!page
# ANEXO A. CALIDADES, TOLERANCIAS Y EXTRAS
!cols 1.3,1.2,1.2,1.4,1.4,1.3
| Calidad | Espesor (mm) | Ancho (mm) | Tolerancia (mm) | Rugosidad Ra (µm) | Extra (€/t) |
""" + "\n".join(f"| {q} | {e} | {a} | ±{tol} | {ra} | {ex} |" for q, e, a, tol, ra, ex in [("DC01+LC", "0,20", "18,0", "0,008", "0,4-0,8", "112"), ("DC01+LC", "0,25", "22,5", "0,010", "0,4-0,8", "98"), ("DC01+LC", "0,30", "24,0", "0,010", "0,6-1,0", "91"), ("DC03+LC", "0,32", "31,0", "0,012", "0,6-1,0", "104"), ("DC03+LC", "0,40", "36,5", "0,012", "0,6-1,0", "88"), ("DC04+LC", "0,50", "42,0", "0,015", "0,8-1,2", "83"), ("DC04+LC", "0,60", "48,0", "0,015", "0,8-1,2", "79"), ("C50S+A", "0,35", "20,0", "0,010", "0,3-0,6", "167"), ("C67S+A", "0,40", "16,0", "0,010", "0,3-0,6", "182"), ("C75S+QT", "0,45", "14,5", "0,008", "0,2-0,5", "238")]) + """
# ANEXO B. SEGUIMIENTO DE COMPRAS
Información facilitada por el Vendedor para el control del compromiso anual. Facturación neta acumulada de 2026 a 30 de septiembre.
!cols 2,1.5,1.5,1.5
| Trimestre de 2026 | Toneladas | Facturación neta (€) | Acumulado (€) |
| Primer trimestre | 118 | 186.400 | 186.400 |
| Segundo trimestre | 109 | 171.900 | 358.300 |
| Tercer trimestre | 97 | 152.700 | 511.000 |
A 30 de septiembre de 2026 restan 389.000 euros para alcanzar el compromiso del ejercicio.
"""
    pdf(DIR, "03-compra-acero-lince", est("Aceros Lincera", "Fleje de precisión · Avilés", "Arial", "#4b4f58", "bar", ref="LIN/NC/2025-06 · Contrato marco de compra"), t, "Contrato marco de compra", rub=("li", "nv"))
    REF["03-compra-acero-lince.pdf"] = dict(contraparte=(LINCE, LINCE, "NONE"), objeto=("Compra de fleje de acero para conectores", "compra de fleje de acero para conectores", "NONE"), importe=("Mínimo de 900.000 euros por año natural", "el Comprador adquirirá al menos 900.000 euros por año natural", "HIGH"), vencimiento=("2028-06-09", "vence el 9 de junio de 2028", "NONE"), renovacion=("Sin prórroga automática", "sin prórroga automática", "NONE"), cambio_control=("Cesión con consentimiento; el cambio de accionariado no es cesión si se mantienen los compromisos", "No tendrá la consideración de cesión el cambio en el accionariado del Comprador", "LOW"), exclusividad=None, penalizacion=("40% de la diferencia hasta el mínimo; a 30/09/2026 restan 389.000 euros", "Si no se alcanza el mínimo, el Comprador abonará el 40% de la diferencia", "HIGH"), garantias=("Reserva de dominio hasta el pago íntegro", "El material permanecerá en propiedad del Vendedor hasta su pago íntegro", "LOW"), ley_fuero=("Ley española; juzgados de Madrid capital", "El contrato se rige por la ley española", "NONE"))


def prestamo():
    ds = []; y, m = 2022, 8; sal = 3500000
    while sal > 0:
        sal -= 125000; ds.append(f"| {len(ds)+1} | {F_(date(y, m, 20))} | {eur(125000, 0)} | {eur(sal, 0)} |"); m += 3
        if m > 12: m -= 12; y += 1
    t = f"""
# PÓLIZA DE PRÉSTAMO MERCANTIL A TIPO VARIABLE
!c Número 9999-0412-88-0017730
!c En Madrid, a 20 de mayo de 2022
### INTERVIENEN
De una parte, {BANCO}, con domicilio en paseo de los Olmos, 11, 28004 Madrid, representado por D.ª Asunción Valdeolmos Prat y D. Tirso Carballeda Mos, apoderados mancomunados. En adelante, el Banco.
{nv("el Prestatario").replace("De una parte", "De otra parte")}
Las partes otorgan la presente póliza con arreglo a las condiciones particulares y generales que siguen.
### CONDICIONES PARTICULARES
!cols 1.5,3
!nocab
| Principal | 3.500.000 euros |
| Finalidad | Ampliación de la planta de Getafe y adquisición de maquinaria |
| Plazo | Siete años |
| Vencimiento final | 20 de mayo de 2029 |
| Amortización | 28 cuotas trimestrales constantes de capital de 125.000 euros |
| Tipo de interés | Euríbor a 12 meses más 2,25%, con revisión anual |
| Comisión de apertura | 0,60% sobre el principal |
| Comisión de amortización anticipada voluntaria | 0,50% sobre el capital amortizado |
| Interés de demora | Tipo vigente más 4 puntos porcentuales |
| Cuenta de domiciliación | {iban("banco")} |
| Garantías | Prenda sobre participaciones e hipoteca mobiliaria sobre maquinaria |
### CONDICIONES GENERALES
## 1. Definiciones
1.1. Deuda Financiera Neta: suma de préstamos, créditos, arrendamientos financieros, efectos descontados, confirming con coste y cualquier otra financiación con coste, menos tesorería y equivalentes de libre disposición.
1.2. EBITDA: resultado de explotación más amortizaciones, deterioros y provisiones no recurrentes, según las cuentas anuales auditadas y sin ajustes distintos de los aceptados por el Banco.
1.3. Cambio de Control: la adquisición por una o varias personas, actuando concertadamente, de una participación igual o superior al 30% del capital o de los derechos de voto del Prestatario, o el cese de su administrador único sin conformidad previa del Banco.
1.4. Efecto Material Adverso: todo hecho que perjudique de forma sustancial la capacidad del Prestatario de atender sus obligaciones de pago o el valor de las garantías.
1.5. Contratos Relevantes: los de arrendamiento de la planta productiva y los de suministro que representen más del 10% de la cifra de negocios.
## 2. Principal y disposición
2.1. El Banco concede un préstamo de 3.500.000 euros para financiar la ampliación de la planta. El importe se abona en este acto en la cuenta de domiciliación.
2.2. El Prestatario destinará los fondos a la finalidad pactada y lo acreditará con facturas en los seis meses siguientes.
## 3. Intereses y comisiones
3.1. El capital pendiente devengará interés diario al Euríbor a 12 meses más 2,25%, liquidable por trimestres vencidos sobre año de 360 días. Si el índice fuera negativo, se considerará cero.
3.2. Cuando el índice de referencia no se publique, se aplicará el sustitutivo que designe el administrador del índice y, en su defecto, el último conocido.
3.3. Las cantidades impagadas devengarán el interés de demora desde el día siguiente a su vencimiento, sin necesidad de requerimiento.
## 4. Amortización
4.1. El préstamo vence el 20 de mayo de 2029, con amortización trimestral conforme al cuadro del Anexo 1.
4.2. El Prestatario podrá amortizar anticipadamente, en importes no inferiores a 50.000 euros, con un preaviso de quince días.
4.3. Amortización anticipada obligatoria. El Prestatario destinará a amortizar el 100% de las indemnizaciones de seguro no reinvertidas y el 50% del precio de venta de activos por encima de 200.000 euros anuales.
## 5. Declaraciones del Prestatario
5.1. El Prestatario declara estar válidamente constituido, no estar incurso en causa de disolución, hallarse al corriente de sus obligaciones tributarias y de Seguridad Social y no conocer litigios que puedan tener Efecto Material Adverso.
5.2. Estas declaraciones se entenderán reiteradas en cada fecha de liquidación.
## 6. Obligaciones de información
6.1. El Prestatario entrega cuentas auditadas antes del 30 de junio de cada año, junto con el certificado de cumplimiento de ratios según el Anexo 2.
6.2. Entregará balance y cuenta de resultados trimestrales en los cuarenta y cinco días siguientes al cierre y comunicará de inmediato cualquier causa de vencimiento anticipado.
6.3. Comunicará la resolución, vencimiento o falta de renovación de los Contratos Relevantes con una antelación mínima de seis meses.
## 7. Obligaciones financieras
7.1. La deuda financiera neta no superará 3,0 veces el EBITDA, ratio que se medirá al cierre de cada ejercicio.
7.2. El Prestatario no repartirá dividendos si la ratio supera 2,5 veces tras la distribución.
7.3. El Prestatario no concederá préstamos ni efectuará pagos a partes vinculadas fuera del curso ordinario por más de 50.000 euros anuales sin consentimiento del Banco.
## 8. Otras obligaciones
8.1. El Prestatario no otorgará garantías reales sobre sus activos, mantendrá asegurados los bienes hipotecados por su valor de reposición y conservará la explotación en la planta de Getafe.
8.2. El préstamo tendrá como mínimo el mismo rango que las restantes obligaciones ordinarias del Prestatario.
## 9. Vencimiento anticipado
9.1. El Banco podrá declarar vencido el préstamo en caso de impago de cualquier cantidad, incumplimiento de las obligaciones de las condiciones 6 a 8, falsedad de las declaraciones o Efecto Material Adverso.
9.2. Vencimiento cruzado. El impago o el vencimiento anticipado de cualquier otra deuda del Prestatario superior a 100.000 euros facultará al Banco para exigir el reembolso total.
9.3. La pérdida del derecho de uso de la planta de Getafe sin alternativa aceptada por el Banco será causa de vencimiento anticipado.
9.4. Declarado el vencimiento, el Prestatario reembolsará capital, intereses y gastos en diez días hábiles.
## 10. Cambio de Control
10.1. Un cambio de control no autorizado permite al Banco exigir la amortización anticipada total. El Prestatario solicitará la autorización con cuarenta y cinco días de antelación.
10.2. El silencio del Banco no equivaldrá a autorización.
## 11. Garantías
11.1. En garantía del cumplimiento se constituye prenda sobre el 100% de las participaciones del Prestatario e hipoteca sobre la maquinaria relacionada en el Anexo 3.
11.2. Los derechos de voto corresponderán a los socios mientras no exista causa de vencimiento anticipado notificada.
11.3. Las garantías subsistirán hasta el íntegro pago. Los gastos de constitución y cancelación serán de cuenta del Prestatario.
## 12. Cesión por el Banco
12.1. El Banco podrá ceder total o parcialmente el préstamo a entidades financieras o fondos, con notificación al Prestatario.
{cola(13, REP, CONF, RGPD, COMP, INT, NOT, GEN, LEY)}
!firma Por el Banco;D.ª Asunción Valdeolmos Prat;Apoderada||Por el Banco;D. Tirso Carballeda Mos;Apoderado||Por el Prestatario;{ADM};Administrador único
!page
# ANEXO 1. CUADRO DE AMORTIZACIÓN DE CAPITAL
!cols .6,2,1.4,1.6
| N.º | Fecha | Cuota de capital (€) | Capital pendiente (€) |
""" + "\n".join(ds) + f"""
!page
# ANEXO 2. CERTIFICADO DE CUMPLIMIENTO DE RATIOS
Ejercicio cerrado el 31 de diciembre de 2025. Emitido el 26 de junio de 2026 a partir de las cuentas anuales auditadas.
!cols 4,1.6
| Concepto | Importe (€) |
| Préstamo Banco Merediano (capital pendiente) | 1.750.000 |
| Pólizas de crédito de circulante | 3.600.000 |
| Arrendamientos financieros | 1.240.000 |
| Confirming con coste | 1.012.000 |
| Tesorería y equivalentes | -410.000 |
| Total deuda financiera neta | 7.192.000 |
!cols 4,1.6
| Concepto | Importe (€) |
| Resultado de explotación | 1.610.000 |
| Amortizaciones | 820.000 |
| Provisiones no recurrentes | 50.000 |
| Total EBITDA | 2.480.000 |
El certificado de cierre de 2025 recoge una ratio de 2,9 veces, frente al máximo de 3,0 veces de la condición 7.1.
!firma Por el Prestatario;{ADM};Administrador único
# ANEXO 3. MAQUINARIA HIPOTECADA
!cols 1,4,1,1.4
| Código | Descripción | Año | Valor (€) |
| MQ-01 | Prensa de corte progresivo 80 t | 2019 | 285.000 |
| MQ-02 | Prensa de corte progresivo 125 t | 2022 | 412.000 |
| MQ-05 | Inyectora eléctrica 120 t | 2021 | 148.000 |
| MQ-06 | Inyectora eléctrica 160 t | 2022 | 176.000 |
| MQ-09 | Línea de ensamblado NX-200 | 2022 | 690.000 |
| MQ-10 | Línea de ensamblado NX-300 | 2023 | 745.000 |
| MQ-14 | Línea de estañado en continuo | 2018 | 310.000 |
| Total | | | 2.766.000 |
"""
    pdf(DIR, "04-prestamo-banco", est("Banco Merediano", "Banca de empresas", "Arial", "#5b1238", "bar", ref="Póliza 9999-0412-88-0017730", size=9.5), t, "Póliza de préstamo", rub=("b1", "nv"))
    REF["04-prestamo-banco.pdf"] = dict(contraparte=(BANCO, BANCO, "NONE"), objeto=("Préstamo para ampliar la planta de Getafe", "El Banco concede un préstamo de 3.500.000 euros para financiar la ampliación de la planta", "NONE"), importe=("Principal de 3.500.000 euros", "El Banco concede un préstamo de 3.500.000 euros", "MEDIUM"), vencimiento=("2029-05-20", "El préstamo vence el 20 de mayo de 2029", "NONE"), renovacion=None, cambio_control=("Desde el 30% del capital; sin autorización, amortización anticipada total", "Un cambio de control no autorizado permite al Banco exigir la amortización anticipada total", "HIGH"), exclusividad=None, penalizacion=("Vencimiento cruzado por deudas superiores a 100.000 euros; demora de 4 puntos", "El impago o el vencimiento anticipado de cualquier otra deuda del Prestatario superior a 100.000 euros", "HIGH"), garantias=("Deuda neta/EBITDA máx. 3,0 (2,9 en 2025); prenda 100% participaciones e hipoteca de maquinaria; pagos a vinculadas máx. 50.000 euros", "El certificado de cierre de 2025 recoge una ratio de 2,9 veces, frente al máximo de 3,0 veces", "HIGH"), ley_fuero=("Ley española; juzgados de Madrid capital", "El contrato se rige por la ley española", "NONE"))


def nave():
    t = f"""
# CONTRATO DE ARRENDAMIENTO PARA USO DISTINTO DE VIVIENDA
!c En Getafe, a 1 de enero de 2017
### REUNIDOS
De una parte, {SAUCE}, con domicilio social en calle de la Alameda, 3, 28901 Getafe (Madrid), representada por D. Leandro Saúco Pedraza, en su condición de administrador solidario. En adelante, el Arrendador.
{nv("el Arrendatario").replace("De una parte", "De otra parte")}
### EXPONEN
I. Que el Arrendador es dueño de la nave industrial sita en calle del Torno, 14, del Polígono Industrial Las Encinas de Getafe, con una superficie construida de 6.480 metros cuadrados, inscrita en el Registro de la Propiedad de Getafe.
II. Que el Arrendatario desarrolla su actividad de fabricación de conectores y necesita disponer de un inmueble adecuado.
III. Que ambas partes convienen el arrendamiento conforme a la Ley 29/1994 de Arrendamientos Urbanos, con sujeción a las siguientes
### ESTIPULACIONES
## 1. Objeto
1.1. Es objeto del contrato el arrendamiento de la nave industrial de Getafe, única planta productiva del Arrendatario, con sus oficinas, muelles, patio de maniobras y quince plazas de aparcamiento.
1.2. El inmueble se entrega en el estado que refleja el acta del Anexo I, que el Arrendatario declara conocer y aceptar.
## 2. Uso
2.1. El inmueble se destina a fabricación y almacén. No podrá darse otro uso sin consentimiento escrito del Arrendador.
2.2. Corresponde al Arrendatario la obtención y mantenimiento de las licencias de actividad y de las autorizaciones medioambientales.
## 3. Duración
3.1. El plazo es de diez años. El arrendamiento vence el 31 de diciembre de 2026.
3.2. No existe derecho de prórroga a favor del Arrendatario. La permanencia en el inmueble tras el vencimiento no supondrá tácita reconducción y devengará la indemnización de la estipulación 11.3.
3.3. El plazo es de obligado cumplimiento. El desistimiento anticipado obligará al pago de las rentas pendientes, con un máximo de doce mensualidades.
## 4. Renta
4.1. La renta inicial se fijó en 18.000 euros mensuales y se actualiza cada 1 de enero según la variación del índice general de precios al consumo, con el detalle del Anexo II.
4.2. Desde el 1 de enero de 2026, la renta es de 264.000 euros anuales, más IVA, pagadera por meses anticipados de 22.000 euros en los siete primeros días.
4.3. El impago total o parcial de una mensualidad facultará al Arrendador para instar el desahucio, además de devengar interés legal incrementado en dos puntos.
## 5. Gastos y tributos
5.1. Son de cuenta del Arrendatario los suministros, la tasa de residuos y su participación en los gastos del polígono. El impuesto sobre bienes inmuebles será abonado por el Arrendador y repercutido al Arrendatario.
## 6. Conservación y obras
6.1. El Arrendador realizará las reparaciones estructurales. El Arrendatario asumirá el mantenimiento ordinario, las instalaciones y los daños derivados de su actividad.
6.2. Las obras requerirán autorización escrita y quedarán en beneficio del inmueble sin indemnización, salvo la maquinaria y las instalaciones desmontables.
6.3. A la finalización, el Arrendatario retirará la línea de estañado, realizará un estudio de suelos y entregará certificado de descontaminación si procede. El plazo estimado de desmantelamiento y traslado es de catorce semanas.
## 7. Seguros
7.1. El Arrendatario contratará un seguro de daños sobre el continente por valor de reposición a nuevo, con designación del Arrendador como beneficiario, y un seguro de responsabilidad civil no inferior a 1.000.000 euros.
## 8. Cesión, subarriendo y cambio de control
8.1. Se prohíben la cesión y el subarriendo sin consentimiento escrito del Arrendador.
8.2. El cambio de control del Arrendatario se considera cesión y exige el consentimiento previo del Arrendador, que podrá denegarlo o condicionarlo a una actualización de renta a valor de mercado.
8.3. El incumplimiento de esta estipulación será causa de resolución de pleno derecho.
## 9. Garantía
9.1. El Arrendatario entrega fianza legal de dos mensualidades y aval bancario por 132.000 euros a primer requerimiento, con vigencia hasta tres meses después de la entrega de llaves.
## 10. Derechos de adquisición preferente
10.1. El Arrendatario renuncia expresamente a los derechos de tanteo y retracto en caso de venta del inmueble.
10.2. En caso de venta, el adquirente se subrogará en el contrato hasta su vencimiento.
## 11. Entrega de la posesión
11.1. Llegado el vencimiento, el Arrendatario entregará el inmueble libre, vacuo y expedito, sin necesidad de requerimiento.
11.2. Las partes levantarán acta de estado. Los desperfectos no imputables al uso ordinario serán de cuenta del Arrendatario.
11.3. El retraso en la entrega devengará una indemnización diaria de 2.200 euros, equivalente al triple de la renta diaria.
{cola(12, REP, CONF, RGPD, INT, NOT, GEN, LEY)}
!firma El Arrendador;D. Leandro Saúco Pedraza;Administrador solidario||El Arrendatario;{ADM};Administrador único
!page
# ANEXO II. EVOLUCIÓN DE LA RENTA
!cols 1,1.6,1.6
| Año | Renta mensual (€) | Renta anual (€) |
""" + "\n".join(f"| {a} | {eur(m,0)} | {eur(m*12,0)} |" for a, m in [(2017, 18000), (2018, 18200), (2019, 18420), (2020, 18570), (2021, 18480), (2022, 19680), (2023, 20800), (2024, 21440), (2025, 21600), (2026, 22000)]) + """
### ANEXO I. ACTA DE ESTADO E INVENTARIO
El acta firmada el 1 de enero de 2017 se incorpora como copia digitalizada en la página siguiente.
!page
!scan acta
"""
    sc = {"acta": escaneo(["ACTA DE ESTADO E INVENTARIO", "Nave industrial. Calle del Torno, 14. Getafe", "Fecha: 1 de enero de 2017", "", "Cubierta: panel sandwich. Estado: bueno", "Solera: hormigon fratasado. Fisuras zona 3", "Muelles de carga: 4 uds. Operativos", "Puente grua 5 t: 2 uds. Revision 11/2016", "Centro de transformacion 630 kVA: bueno", "Red contra incendios BIE: 12 uds", "Extintores: 38 uds", "Climatizacion oficinas: 6 splits", "Alumbrado: fluorescente, 14 tubos fundidos", "Aseos y vestuarios: 2 nucleos", "Vallado perimetral: 310 m", "Plazas de aparcamiento: 15", "", "Lectura contador electrico: 884.213 kWh", "Lectura contador agua: 12.907 m3", "", "Observaciones: mancha de humedad en", "fachada norte, sin filtracion activa.", "", "El Arrendador          El Arrendatario", "", "  L. Sauco             R. Tordesillas"], 3)}
    pdf(DIR, "05-arrendamiento-nave", est("Inmuebles Saucedal", "Suelo y naves industriales", "Times", "#3d5a2a", "esc", ref="Arrendamiento nave calle del Torno, 14", size=10.6), t, "Contrato de arrendamiento", rub=("sa", "nv"), scans=sc)
    REF["05-arrendamiento-nave.pdf"] = dict(contraparte=(SAUCE, SAUCE, "NONE"), objeto=("Arrendamiento de la nave de Getafe, única planta productiva", "arrendamiento de la nave industrial de Getafe, única planta productiva del Arrendatario", "HIGH"), importe=("264.000 euros anuales, más IVA", "la renta es de 264.000 euros anuales, más IVA", "MEDIUM"), vencimiento=("2026-12-31", "El arrendamiento vence el 31 de diciembre de 2026", "HIGH"), renovacion=("Sin derecho de prórroga ni tácita reconducción", "No existe derecho de prórroga a favor del Arrendatario", "HIGH"), cambio_control=("Se considera cesión; exige consentimiento previo del Arrendador", "El cambio de control del Arrendatario se considera cesión y exige el consentimiento previo del Arrendador", "HIGH"), exclusividad=None, penalizacion=("2.200 euros diarios por retraso en la entrega", "El retraso en la entrega devengará una indemnización diaria de 2.200 euros", "HIGH"), garantias=("Fianza de dos mensualidades y aval bancario de 132.000 euros", "aval bancario por 132.000 euros", "LOW"), ley_fuero=("Ley española; juzgados de Madrid capital", "El contrato se rige por la ley española", "NONE"))


def erp():
    t = f"""
# CONTRATO DE LICENCIA DE USO DE SOFTWARE
!c Madrid, 3 de octubre de 2024
### PARTES
{parte(OLMO, "B", "calle del Compás, 27, 28037 Madrid", "D.ª Iria Moscoso Landín", "directora general", "el Licenciante").replace("De otra parte", "De una parte")}
{nv("el Licenciatario").replace("De una parte", "De otra parte")}
### ANTECEDENTES
I. El Licenciante es titular del programa de planificación y control de producción denominado Olmera Planta, versión 7 (el Programa).
II. El Licenciatario desea implantarlo en su planta de Getafe en sustitución de su sistema anterior.
### CLÁUSULAS
## 1. Objeto
1.1. El Licenciante concede una licencia de uso del ERP de producción para 120 usuarios nominales, no exclusiva, limitada al centro de Getafe.
1.2. La licencia comprende los módulos de planificación, trazabilidad, calidad, almacén y mantenimiento. La relación figura en el Anexo 1.
1.3. El servicio se presta en la nube del Licenciante, alojada en centros de datos situados en la Unión Europea.
## 2. Precio
2.1. La cuota anual es de 78.000 euros, IVA no incluido, facturada por anualidades anticipadas.
2.2. La cuota se actualizará cada año con el índice de precios al consumo más un punto. Los usuarios adicionales se facturarán a 690 euros anuales.
2.3. Superado el número de usuarios, el Licenciante regularizará con efecto retroactivo al inicio de la anualidad.
## 3. Duración
3.1. El contrato tiene una duración inicial de tres años. Vence el 2 de octubre de 2027, con prórroga anual automática salvo preaviso de 90 días.
3.2. La baja anticipada del Licenciatario no dará derecho a devolución de cuotas.
## 4. Implantación
4.1. La implantación se realizará según el plan del Anexo 2. La aceptación se entenderá producida por el uso en producción durante treinta días sin incidencias bloqueantes.
4.2. El Licenciatario designará un responsable de proyecto y facilitará los datos maestros depurados.
## 5. Soporte y niveles de servicio
5.1. Soporte en días laborables de 9:00 a 18:00, por portal y teléfono. No se incluye atención en turnos de noche ni en fines de semana.
5.2. La disponibilidad mensual objetivo es del 99,0%, medida fuera de ventanas de mantenimiento. Los tiempos de respuesta figuran en el Anexo 3.
5.3. El incumplimiento de la disponibilidad durante dos meses seguidos dará derecho a una bonificación del 5% de la cuota mensual equivalente.
## 6. Propiedad intelectual
6.1. El Programa y su documentación son propiedad del Licenciante. Se prohíbe la ingeniería inversa, salvo en lo que permita la ley, y la cesión de credenciales.
6.2. Los datos introducidos son propiedad del Licenciatario, que podrá exportarlos en formato abierto hasta sesenta días después de la terminación.
## 7. Intransferibilidad
7.1. La licencia es intransferible, también en fusiones o escisiones, salvo pago de una nueva cuota de alta de 60.000 euros.
7.2. A estos efectos se equipara a la transferencia la integración del Licenciatario en un grupo que utilice el Programa en otros centros.
## 8. Garantía y responsabilidad
8.1. El Licenciante garantiza que el Programa funciona de acuerdo con su documentación. La garantía no cubre usos indebidos ni modificaciones de terceros.
8.2. La responsabilidad del Licenciante se limita a las cuotas abonadas en los seis meses anteriores, con exclusión del lucro cesante y de las pérdidas de producción.
## 9. Seguridad de la información
9.1. El Licenciante realizará copias diarias con retención de treinta días, cifrará las comunicaciones y notificará los incidentes de seguridad en cuarenta y ocho horas.
9.2. El acceso remoto del Licenciatario podrá protegerse con doble factor de autenticación, cuya activación corresponde al Licenciatario para cada perfil.
{cola(10, REP, CONF, RGPD, AUD, CONT, FM, COMP, INT, NOT, GEN)}
!firma Por el Licenciante;D.ª Iria Moscoso Landín;Directora general||Por el Licenciatario;{ADM};Administrador único
!page
# ANEXO 1. MÓDULOS Y USUARIOS
!cols 2.2,1,1.6
| Módulo | Usuarios | Cuota anual (€) |
| Planificación y secuenciación | 18 | 16.400 |
| Trazabilidad y lotes | 42 | 21.300 |
| Calidad y no conformidades | 22 | 14.700 |
| Almacén y expediciones | 26 | 15.900 |
| Mantenimiento de planta | 12 | 9.700 |
| Total | 120 | 78.000 |
# ANEXO 2. PLAN DE IMPLANTACIÓN
!cols .6,3.4,1.4,1.4
| Fase | Contenido | Inicio | Fin |
| 1 | Análisis y parametrización | 07/10/2024 | 15/11/2024 |
| 2 | Migración de datos maestros | 18/11/2024 | 20/12/2024 |
| 3 | Formación de usuarios clave | 08/01/2025 | 24/01/2025 |
| 4 | Piloto en línea NX-200 | 27/01/2025 | 28/02/2025 |
| 5 | Despliegue completo | 03/03/2025 | 11/04/2025 |
# ANEXO 3. TIEMPOS DE RESPUESTA
!cols 1.2,3,1.4,1.4
| Prioridad | Definición | Respuesta | Resolución |
| Crítica | Parada de producción | 1 hora | 8 horas |
| Alta | Función principal degradada | 4 horas | 2 días |
| Media | Incidencia con alternativa | 1 día | 5 días |
| Baja | Consulta o mejora | 3 días | Según plan |
"""
    pdf(DIR, "06-licencia-erp", est("Olmera Software", "Sistemas para planta", "Arial", "#1f6f8b", "circ", ref="OLM-2024-1003 · Licencia Olmera Planta"), t, "Contrato de licencia de software", rub=("ol", "nv"))
    REF["06-licencia-erp.pdf"] = dict(contraparte=(OLMO, OLMO, "NONE"), objeto=("Licencia de uso del ERP de producción para 120 usuarios", "licencia de uso del ERP de producción para 120 usuarios", "NONE"), importe=("78.000 euros anuales, IVA no incluido", "La cuota anual es de 78.000 euros", "LOW"), vencimiento=("2027-10-02", "Vence el 2 de octubre de 2027", "NONE"), renovacion=("Prórroga anual automática salvo preaviso de 90 días", "con prórroga anual automática salvo preaviso de 90 días", "LOW"), cambio_control=("Intransferible, también en fusiones o escisiones, salvo pago de 60.000 euros", "La licencia es intransferible, también en fusiones o escisiones, salvo pago de una nueva cuota de alta de 60.000 euros", "MEDIUM"), exclusividad=("Licencia no exclusiva, limitada a Getafe", "no exclusiva, limitada al centro de Getafe", "NONE"), penalizacion=("Bonificación del 5% por indisponibilidad; regularización retroactiva de usuarios", "dará derecho a una bonificación del 5% de la cuota mensual equivalente", "LOW"), garantias=("Responsabilidad limitada a seis meses de cuotas", "La responsabilidad del Licenciante se limita a las cuotas abonadas en los seis meses anteriores", "LOW"), ley_fuero=None)


def direccion():
    t = f"""
# CONTRATO DE TRABAJO DE PERSONAL DE ALTA DIRECCIÓN
!c En Getafe, a 1 de septiembre de 2021
### REUNIDOS
{nv("la Sociedad")}
De otra parte, {DG}, mayor de edad, con código interno de empleo AD-01. En adelante, la Alta Directiva o AD-01.
### EXPONEN
I. Que la Sociedad precisa cubrir la Dirección General, con poderes inherentes a la titularidad de la empresa y relativos a sus objetivos generales.
II. Que AD-01 reúne la formación y experiencia necesarias y ambas partes desean formalizar una relación laboral especial de alta dirección al amparo del Real Decreto 1382/1985, de 1 de agosto.
### CLÁUSULAS
## 1. Objeto
1.1. Es objeto del contrato la prestación de servicios de Dirección General, con dependencia directa del órgano de administración.
1.2. Corresponden a AD-01 la dirección comercial, industrial, financiera y de personas, la propuesta de presupuesto anual y la representación ordinaria ante clientes, bancos y Administraciones, dentro de los límites del poder del Anexo I.
1.3. AD-01 es la interlocutora principal de los tres mayores clientes y del equipo de ingeniería que desarrolla la gama NX-500.
## 2. Dedicación
2.1. Dedicación plena y exclusiva. La participación en órganos de otras sociedades requerirá autorización escrita.
2.2. La jornada será la necesaria para el desempeño del cargo. El centro de trabajo es la planta de Getafe, con disponibilidad para viajar.
## 3. Duración
3.1. Contrato indefinido, con un periodo de prueba de nueve meses ya superado a la fecha de cualquier revisión posterior.
## 4. Retribución
4.1. La retribución fija es de 145.000 euros brutos anuales, en doce pagas, revisable cada enero de común acuerdo.
4.2. Retribución variable de hasta el 30% de la fija, según el cumplimiento de los objetivos del Anexo II.
4.3. Beneficios: vehículo de empresa de gama media, seguro médico familiar, seguro de vida por dos anualidades y aportación del 3% a un instrumento de previsión.
4.4. Los gastos de viaje y representación se reembolsarán con justificante.
## 5. Vacaciones
5.1. Treinta días naturales al año, que se fijarán de acuerdo con las necesidades de la Sociedad.
## 6. Extinción
6.1. AD-01 podrá desistir con un preaviso de tres meses. La Sociedad podrá desistir con preaviso de seis meses o su compensación, y abonará una indemnización de doce meses de retribución fija.
6.2. El despido declarado improcedente dará derecho a la indemnización de la cláusula 6.1, salvo que proceda una superior.
6.3. En caso de extinción procedente por incumplimiento grave no habrá indemnización.
## 7. Cambio de control
7.1. Si cambia el control de la sociedad, AD-01 podrá extinguir el contrato y percibir una indemnización de 24 meses de retribución fija.
7.2. La facultad se ejercitará en los tres meses siguientes a la inscripción o conocimiento del cambio, incluida la sustitución del administrador único acordada en el marco de la operación.
7.3. La indemnización se devengará también si la Sociedad extingue el contrato en los seis meses anteriores al cierre de una operación en negociación.
## 8. No competencia
8.1. Durante doce meses tras la extinción, AD-01 no prestará servicios a empresas competidoras en España y Portugal, compensados con el 50% de la retribución fija.
8.2. El incumplimiento obligará a devolver lo percibido y a abonar una cantidad equivalente a seis meses de retribución fija.
8.3. La Sociedad solo podrá renunciar al pacto con acuerdo de AD-01.
## 9. Invenciones
9.1. Las invenciones y desarrollos realizados en el ejercicio del cargo pertenecen a la Sociedad, conforme a la Ley 24/2015 de Patentes.
{cola(10, CONF, RGPD, COMP, INT, NOT, GEN, LEY)}
!firma Por la Sociedad;{ADM};Administrador único||La Alta Directiva;{DG};AD-01
!page
# ANEXO I. LÍMITES DEL PODER
!cols 3.4,1.6,1.6
| Facultad | Individual | Con el administrador |
| Contratos de venta | Hasta 250.000 € | Sin límite |
| Compras e inversiones | Hasta 60.000 € | Sin límite |
| Apertura de cuentas y financiación | No | Sí |
| Contratación de personal | Hasta 45.000 €/año | Sin límite |
| Litigios y transacciones | Hasta 30.000 € | Sin límite |
# ANEXO II. OBJETIVOS DE RETRIBUCIÓN VARIABLE
!cols 3.4,1,2.2
| Objetivo | Peso | Medición |
| EBITDA sobre presupuesto | 45% | Cuentas auditadas |
| Cumplimiento de entregas a clientes principales | 25% | Promedio anual |
| Renovación de contratos de cliente | 20% | Contratos firmados |
| Accidentabilidad y absentismo | 10% | Índice de frecuencia |
"""
    pdf(DIR, "07-alta-direccion", est("Norvalia Conectores", "Secretaría de la sociedad", "Times", "#1f3a5f", "hex", ref="Confidencial · AD-01", size=10.6), t, "Contrato de alta dirección", rub=("nv", "ad"))
    REF["07-alta-direccion.pdf"] = dict(contraparte=("Dirección General, AD-01", "con código interno de empleo AD-01", "NONE"), objeto=("Prestación de servicios de Dirección General", "prestación de servicios de Dirección General", "NONE"), importe=("145.000 euros brutos anuales fijos y variable de hasta el 30%", "La retribución fija es de 145.000 euros brutos anuales", "MEDIUM"), vencimiento=("Indefinido", "Contrato indefinido", "NONE"), renovacion=None, cambio_control=("Puede extinguir con indemnización de 24 meses de fijo (290.000 euros)", "Si cambia el control de la sociedad, AD-01 podrá extinguir el contrato y percibir una indemnización de 24 meses de retribución fija", "HIGH"), exclusividad=("Dedicación plena y exclusiva a la Sociedad", "Dedicación plena y exclusiva", "LOW"), penalizacion=("Desistimiento: 12 meses; no competencia: 12 meses al 50%", "abonará una indemnización de doce meses de retribución fija", "MEDIUM"), garantias=None, ley_fuero=("Ley española; juzgados de Madrid capital", "El contrato se rige por la ley española", "NONE"))


def tordo():
    meses = "\n".join(f"| TI-{25000+i+1} | {MES[i]} de 2025 | Servicios generales de asesoramiento y gestión | 15.000 |" for i in range(12))
    t = f"""
# CONTRATO DE PRESTACIÓN DE SERVICIOS DE GESTIÓN
!c En Madrid, a 2 de febrero de 2023
### REUNIDOS
De una parte, {TORDO}, sociedad participada al 100% por quien ejerce de administrador único de Norvalia, con domicilio en calle del Estanque, 5, 28010 Madrid, representada por {ADM}. En adelante, el Prestador.
De otra parte, {NV}, representada por {ADM}, administrador único. En adelante, Norvalia o el Cliente.
### EXPONEN
I. Que el Prestador dispone de experiencia en el asesoramiento y la gestión de sociedades industriales.
II. Que Norvalia está interesada en recibir dichos servicios de forma continuada.
### CLÁUSULAS
## 1. Objeto
1.1. El Prestador prestará servicios generales de asesoramiento y gestión, según necesidades, en materia estratégica, financiera, comercial y de relaciones institucionales.
1.2. El Prestador determinará los medios y el tiempo de dedicación que considere oportunos.
## 2. Precio
2.1. El precio es un importe fijo de 180.000 euros anuales, sin detalle de horas ni entregables, más el IVA aplicable, facturado por doceavas partes de 15.000 euros.
2.2. El precio se actualizará cada dos años, al alza, en el porcentaje que comunique el Prestador, con un máximo del 10%.
2.3. Los gastos de viaje, alojamiento y representación se reembolsarán aparte, sin límite anual.
## 3. Forma de prestación
3.1. Los servicios se prestarán verbalmente, en reuniones o por escrito, a criterio del Prestador, que no estará obligado a emitir informes.
3.2. El Prestador podrá subcontratar total o parcialmente los servicios.
## 4. Duración
4.1. El contrato es de duración indefinida. Norvalia solo puede resolver con un preaviso de 18 meses.
4.2. El Prestador podrá resolver en cualquier momento con un preaviso de quince días.
## 5. Indemnización
5.1. La resolución sin preaviso obliga a pagar las cuotas pendientes del periodo de preaviso.
5.2. Si Norvalia fuera objeto de venta, fusión o cambio de socios, el contrato continuará en vigor y obligará a sus sucesores.
## 6. Vinculación
6.1. Las partes dejan constancia de que el Prestador está participado al 100% por quien ejerce de administrador único de Norvalia.
6.2. Las partes manifiestan que el precio responde a condiciones de mercado. No se adjunta informe de valoración.
## 7. Responsabilidad
7.1. El Prestador no asume obligación de resultado. Su responsabilidad se limita a los honorarios de un mes.
{cola(8, CONF, RGPD, NOT)}
### Firma
Firmado en Madrid el 2 de febrero de 2024, con efectos desde la fecha del encabezado.
!firma El Prestador;{ADM};Administrador||Norvalia;{ADM};Administrador único
!page
# ANEXO. FACTURACIÓN DE 2025
!cols 1.1,1.6,3.4,1.2
| Factura | Periodo | Concepto | Base (€) |
{meses}
| Total | | | 180.000 |
No constan partes de trabajo, actas ni entregables asociados a las facturas del ejercicio.
"""
    pdf(DIR, "08-servicios-tordo", est("Tordalia Inversiones", "", "Times", "#4a3b2a", "x", ref="Contrato de servicios", size=11), t, "Contrato de servicios de gestión")
    REF["08-servicios-tordo.pdf"] = dict(contraparte=(f"{TORDO}, participada al 100% por el administrador único de Norvalia (parte vinculada)", "sociedad participada al 100% por quien ejerce de administrador único de Norvalia", "HIGH"), objeto=("Servicios generales de asesoramiento y gestión, según necesidades", "servicios generales de asesoramiento y gestión, según necesidades", "MEDIUM"), importe=("180.000 euros anuales fijos, sin detalle de horas ni entregables", "importe fijo de 180.000 euros anuales, sin detalle de horas ni entregables", "HIGH"), vencimiento=("Indefinido; firma fechada el 02/02/2024 y encabezado el 02/02/2023", "Firmado en Madrid el 2 de febrero de 2024, con efectos desde la fecha del encabezado", "MEDIUM"), renovacion=("Duración indefinida; Norvalia solo resuelve con 18 meses de preaviso", "Norvalia solo puede resolver con un preaviso de 18 meses", "HIGH"), cambio_control=("Continúa en vigor y obliga a los sucesores", "el contrato continuará en vigor y obligará a sus sucesores", "HIGH"), exclusividad=None, penalizacion=("Cuotas pendientes del preaviso si se resuelve sin él", "La resolución sin preaviso obliga a pagar las cuotas pendientes del periodo de preaviso", "HIGH"), garantias=None, ley_fuero=None)


def generar():
    for f in (delta, boreal, lince, prestamo, nave, erp, direccion, tordo, adenda, carta): f()
