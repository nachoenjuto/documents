"""Seguros: 5 pólizas."""
from .comun import ADM, NV, NV_CIF, NV_DOM
from .motor import est, eur, iban, pdf

FIRMA = {'A': 'D.ª Delfina Otero Cabal', 'B': 'D. Saturio Llorente Bas', 'G': 'D.ª Noemí Arrizabal Coll', 'D': 'D. Fermín Castrillo Pons'}
DIR = "seguros_large"; REF = {}

# Condiciones generales comunes a la práctica del sector, con {C} = compañía.
def generales(C, riesgo, extra=""):
    return f"""
!dos
# CONDICIONES GENERALES
## Artículo 1. Régimen legal
El contrato se rige por la Ley 50/1980, de 8 de octubre, de Contrato de Seguro, por las presentes condiciones generales, por las especiales y por las particulares. No serán válidas las cláusulas limitativas de los derechos de los asegurados que no hayan sido aceptadas expresamente y por escrito.
## Artículo 2. Definiciones
Asegurador: {C}, que asume el riesgo pactado a cambio de la prima.
Tomador: la persona que suscribe el contrato y a la que corresponden las obligaciones que de él derivan, salvo las que por su naturaleza deba cumplir el asegurado.
Asegurado: la persona titular del interés objeto del seguro.
Siniestro: todo hecho cuyas consecuencias estén cubiertas por alguna de las garantías. El conjunto de daños derivados de una misma causa constituye un solo siniestro.
Suma asegurada o límite: el importe máximo a cargo del asegurador por siniestro, anualidad o garantía, según se indique.
Franquicia: la cantidad que queda a cargo del asegurado en cada siniestro.
Carencia: el periodo inmediatamente posterior al hecho durante el que no se genera derecho a indemnización.
## Artículo 3. Objeto
El asegurador garantiza, dentro de los límites pactados, {riesgo}.
## Artículo 4. Declaración del riesgo
El tomador tiene el deber, antes de la conclusión del contrato, de declarar al asegurador, de acuerdo con el cuestionario que este le someta, todas las circunstancias por él conocidas que puedan influir en la valoración del riesgo. El contenido del cuestionario forma parte integrante de la póliza.
El asegurador podrá rescindir el contrato en el plazo de un mes desde que conozca la reserva o inexactitud. Si el siniestro sobreviene antes, la prestación se reducirá en la proporción entre la prima convenida y la que hubiera correspondido. Si medió dolo o culpa grave, quedará liberado del pago.
## Artículo 5. Agravación y disminución del riesgo
El tomador o el asegurado comunicarán, tan pronto como les sea posible, las circunstancias que agraven el riesgo y que, de haber sido conocidas, habrían llevado al asegurador a no contratar o a hacerlo en condiciones más gravosas. El asegurador podrá proponer una modificación en dos meses. El tomador dispondrá de quince días para aceptarla.
## Artículo 6. Toma de efecto y duración
El contrato entra en vigor en la fecha de efecto indicada, siempre que se haya pagado el primer recibo. La duración y el régimen de prórroga son los de las condiciones particulares, que prevalecen sobre este artículo.
Cuando se pacte prórroga, las partes podrán oponerse a ella mediante notificación escrita con un mes de antelación si la oposición procede del tomador y de dos meses si procede del asegurador.
## Artículo 7. Pago de la prima
Si por culpa del tomador la primera prima no ha sido pagada, el asegurador podrá resolver o exigir el pago. La falta de pago de las primas siguientes suspende la cobertura un mes después de su vencimiento. Si el asegurador no reclama en los seis meses siguientes, el contrato queda extinguido.
## Artículo 8. Comunicación del siniestro
El siniestro se comunicará en el plazo máximo de siete días desde su conocimiento, con las circunstancias conocidas y sus consecuencias. El incumplimiento dará derecho a reclamar los daños causados por la falta de declaración.
El tomador y el asegurado emplearán los medios a su alcance para aminorar las consecuencias. Los gastos razonables serán de cuenta del asegurador dentro de los límites pactados.
## Artículo 9. Peritación y pago
El asegurador satisfará la indemnización al término de las investigaciones necesarias para establecer la existencia del siniestro y su importe. En todo caso abonará, en cuarenta días desde la declaración, el importe mínimo de lo que pueda deber según las circunstancias conocidas.
Si las partes no se ponen de acuerdo, cada una designará un perito. En caso de discrepancia se nombrará un tercero, conforme al artículo 38 de la Ley.
## Artículo 10. Concurrencia de seguros
Cuando el mismo riesgo esté cubierto por varios aseguradores durante el mismo periodo, el tomador comunicará a cada uno los demás seguros. Ocurrido el siniestro, los aseguradores contribuirán en proporción a la propia suma asegurada, sin que pueda superarse la cuantía del daño.
## Artículo 11. Subrogación
Pagada la indemnización, el asegurador podrá ejercitar los derechos y acciones que por razón del siniestro correspondan al asegurado frente a los responsables, hasta el límite de lo pagado.
{extra}
## Artículo 12. Riesgos extraordinarios
Los riesgos extraordinarios serán indemnizados por el Consorcio de Compensación de Seguros en los términos de su normativa, cuando el recargo figure en el recibo.
## Artículo 13. Prescripción
Las acciones prescriben a los dos años si se trata de seguro de daños y a los cinco si es de personas.
## Artículo 14. Reclamaciones
El tomador, el asegurado y los terceros perjudicados podrán dirigirse al servicio de atención al cliente del asegurador, que resolverá en el plazo máximo de un mes, y después al servicio de reclamaciones del órgano de supervisión.
## Artículo 15. Protección de datos
El asegurador tratará los datos personales para gestionar el contrato, prevenir el fraude y cumplir sus obligaciones legales. Los interesados podrán ejercer sus derechos mediante escrito dirigido al domicilio social.
## Artículo 16. Jurisdicción
Será juez competente el del domicilio del asegurado.
!uno
"""


def poliza(fn, st, C, ramo, num, efecto, venc, dur, datos, cobert, especiales, excl, terr, cuest, neta, total, riesgo, extra="", mediador="Correduría Alborada Riesgos, S.L."):
    ips = round(neta * .08, 2); otros = round(total - neta - ips, 2)
    t = f"""
!cab PÓLIZA DE {ramo.upper()};;Póliza {num} · Condiciones particulares
!cols 1.3,3
!nocab
| Aseguradora | {C} |
| Póliza | {num} |
| Tomador | {NV}, NIF {NV_CIF} |
| Domicilio | {NV_DOM} |
| Asegurado | El tomador{datos} |
| Mediador | {mediador} |
| Fecha de efecto | {efecto} |
| Vencimiento | {venc} |
| Duración | {dur} |
| Actividad | Fabricación de conectores eléctricos industriales |
## 1. Garantías y sumas aseguradas
{cobert}
## 2. Ámbito territorial
{terr}
## 3. Condiciones especiales
{especiales}
## 4. Exclusiones destacadas
{excl}
## 5. Prima
!cols 3,1.4
| Concepto | Importe (€) |
| Prima neta | {eur(neta)} |
| Impuesto sobre primas de seguro (8%) | {eur(ips)} |
| Recargos legales | {eur(otros)} |
| Total | {eur(total)} |
Prima total anual: {eur(total, 0)} euros. Forma de pago anual, mediante domiciliación en la cuenta {iban(num)}.
## 6. Aceptación de cláusulas limitativas
El tomador declara haber recibido las condiciones generales, especiales y particulares, y acepta de forma expresa las cláusulas limitativas de sus derechos destacadas en los apartados 3 y 4, en cumplimiento del artículo 3 de la Ley de Contrato de Seguro.
!firma El Tomador;{ADM};Administrador único||Por la Aseguradora;{FIRMA[C[0]]};Dirección de empresas
!page
# CUESTIONARIO DE DECLARACIÓN DEL RIESGO
!i Cumplimentado por el tomador. Forma parte de la póliza {num}.
{cuest}
!firma El Tomador;{ADM};Administrador único
{generales(C, riesgo, extra)}
# RECIBO DE PRIMA
!cols 1.6,3
!nocab
| Póliza | {num} |
| Periodo | Anualidad en curso desde {efecto} |
| Importe total | {eur(total)} euros |
| Domiciliación | {iban(num)} |
| Situación | Cobrado |
!sello {C.split(',')[0].upper()};;RECIBO COBRADO
"""
    pdf(DIR, fn, {**st, "ref": f"Póliza {num}"}, t, f"Póliza de {ramo}")


def generar():
    A = est("Alfara Seguros", "Empresas", "Arial", "#0b4f6c", "circ"); B = est("Beturia Seguros", "Responsabilidad y daños", "Georgia", "#6b2d5c", "esc"); G = est("Gamelia Seguros", "Riesgos tecnológicos", "Arial", "#2a5d34", "hex"); D = est("Deleida Seguros", "Daños industriales", "Times", "#8a3b12", "bar", size=10.6)
    poliza("01-rc-general", A, "Alfara Seguros, S.A.", "Responsabilidad Civil General", "RC-0001-884213", "1 de julio de 2026", "30 de junio de 2027", "Vence el 30 de junio de 2027, con prórroga anual", "", """
!cols 2.4,2.2,1.6
| Garantía | Límite | Franquicia (€) |
| Explotación | 1.500.000 euros por siniestro y anualidad | 3.000 |
| Patronal, por víctima | Sublímite de 300.000 euros | 3.000 |
| Producto y trabajos terminados | Sublímite de 600.000 euros por siniestro y anualidad | 3.000 |
| Contaminación accidental | Sublímite de 300.000 euros | 6.000 |
| Defensa y fianzas | Incluida en el límite | 0 |
El límite de indemnización es de 1.500.000 euros por siniestro y anualidad. La franquicia general es de 3.000 euros por siniestro.
Quedan cubiertas las garantías de explotación, patronal y RC de producto con un sublímite de 600.000 euros.
""", """
3.1. Delimitación temporal. Se cubren las reclamaciones presentadas durante la vigencia por hechos ocurridos en los dos años anteriores.
3.2. Garantía de producto. Opera desde la entrega a terceros y alcanza a los daños materiales, personales y perjuicios consecutivos. No se aplica en exceso de otras pólizas, con las que concurre conforme al artículo 10.
3.3. Regularización. La prima se calcula sobre una facturación de 18.600.000 euros y se regulariza al cierre de cada anualidad.
3.4. Unión y mezcla. Los daños a productos de terceros por incorporación de los conectores se cubren con un sublímite de 150.000 euros.
""", """
- Se excluyen los daños por productos exportados fuera de la Unión Europea y la retirada de producto.
- Daños a bienes confiados, en depósito o bajo custodia del asegurado, incluidos utillajes de clientes.
- Multas, sanciones y penalizaciones contractuales, aunque deriven de un retraso en la entrega.
- Daños por amianto, campos electromagnéticos y contaminación gradual.
- Responsabilidades asumidas por contrato que excedan de las legales.
""", "Unión Europea. Se cubren únicamente las reclamaciones formuladas ante tribunales de un Estado miembro.", """
!cols 3,2.4
| Pregunta | Respuesta del tomador |
| Facturación del último ejercicio | 18.600.000 euros |
| Número de empleados | 94 |
| Exporta fuera de la Unión Europea | Sí. México, 1.350.000 euros anuales |
| Custodia bienes de terceros | Sí, utillajes de clientes |
| Siniestros en los últimos cinco años | Dos, por importe total de 11.700 euros |
| Tiene otros seguros de responsabilidad | No contesta |
""", 13000, 14200, "la responsabilidad civil que pueda derivarse para el asegurado, por daños causados involuntariamente a terceros en el ejercicio de la actividad declarada")
    REF["01-rc-general.pdf"] = dict(aseguradora=("Alfara Seguros, S.A.", "Alfara Seguros, S.A.", "NONE"), ramo=("Responsabilidad Civil General", "Póliza RC-0001-884213", "NONE"), coberturas=("Explotación, patronal y RC de producto con sublímite de 600.000 euros", "explotación, patronal y RC de producto con un sublímite de 600.000 euros", "MEDIUM"), limite=("1.500.000 euros por siniestro y anualidad", "El límite de indemnización es de 1.500.000 euros por siniestro y anualidad", "NONE"), franquicia=("3.000 euros por siniestro", "La franquicia general es de 3.000 euros por siniestro", "NONE"), exclusiones=("Productos exportados fuera de la UE, retirada de producto y utillajes de clientes", "Se excluyen los daños por productos exportados fuera de la Unión Europea y la retirada de producto", "HIGH"), territorio=("Unión Europea; el tomador declara exportación a México por 1.350.000 euros", "Se cubren únicamente las reclamaciones formuladas ante tribunales de un Estado miembro", "HIGH"), vencimiento=("2027-06-30", "Vence el 30 de junio de 2027, con prórroga anual", "NONE"), prima=("14.200 euros anuales", "Prima total anual: 14.200 euros", "NONE"))

    poliza("02-rc-producto", B, "Beturia Seguros, S.A.", "Responsabilidad Civil de Producto", "RP-0002-310775", "1 de abril de 2026", "31 de marzo de 2027", "Vence el 31 de marzo de 2027, con prórroga anual salvo oposición", "", """
!cols 2.4,2.4,1.4
| Garantía | Límite | Franquicia (€) |
| RC de producto | 600.000 euros por siniestro y anualidad | 6.000 |
| Unión y mezcla | Sublímite de 200.000 euros | 6.000 |
| Gastos de desmontaje y montaje | Sublímite de 60.000 euros | 6.000 |
| Defensa y fianzas | Incluida en el límite | 0 |
Se cubre la RC de producto por daños a terceros, hasta 600.000 euros por siniestro y anualidad.
La franquicia es de 6.000 euros por siniestro.
""", """
3.1. Delimitación temporal. Se cubren las reclamaciones presentadas durante la vigencia, con retroactividad de un año.
3.2. Productos asegurados: conectores de las gamas NX-200, NX-300 y NX-500, con independencia del sector de destino.
3.3. Serie. Los daños con una misma causa de diseño o fabricación se consideran un solo siniestro, ocurrido en la fecha del primero.
3.4. Trazabilidad. El asegurado conservará registros de lote durante diez años. El incumplimiento permite al asegurador reducir la indemnización.
3.5. Concurrencia. El tomador declara no tener contratada otra cobertura de producto.
""", """
- Se excluyen la retirada de producto y las reclamaciones en EE. UU. y Canadá.
- Coste de reparación o sustitución del propio producto.
- Perjuicios puramente económicos, paros de línea y penalizaciones contractuales.
- Productos destinados a aeronaves o a dispositivos médicos implantables.
- Reclamaciones por prototipos no homologados.
""", "Unión Europea. Las ventas declaradas en México quedan fuera del ámbito, pendientes de suplemento que no ha sido emitido.", """
!cols 3,2.4
| Pregunta | Respuesta del tomador |
| Facturación por producto propio | 18.600.000 euros |
| Ventas en España y Portugal | 14.900.000 euros |
| Ventas en resto de la Unión Europea | 2.350.000 euros |
| Ventas en México | 1.350.000 euros |
| Ventas en EE. UU. y Canadá | 0 euros |
| Retiradas de producto en cinco años | Una, en 2024, lote NX-300 |
| Otra cobertura de producto en vigor | No |
""", 9000, 9800, "la responsabilidad civil del asegurado por daños causados a terceros por los productos asegurados después de su entrega")
    REF["02-rc-producto.pdf"] = dict(aseguradora=("Beturia Seguros, S.A.", "Beturia Seguros, S.A.", "NONE"), ramo=("Responsabilidad Civil de Producto", "Póliza RP-0002-310775", "NONE"), coberturas=("RC de producto por daños a terceros; declara no tener otra cobertura de producto", "El tomador declara no tener contratada otra cobertura de producto", "HIGH"), limite=("600.000 euros por siniestro y anualidad", "hasta 600.000 euros por siniestro y anualidad", "MEDIUM"), franquicia=("6.000 euros por siniestro", "La franquicia es de 6.000 euros por siniestro", "NONE"), exclusiones=("Retirada de producto, reclamaciones en EE. UU. y Canadá, paros de línea", "Se excluyen la retirada de producto y las reclamaciones en EE. UU. y Canadá", "MEDIUM"), territorio=("Unión Europea; ventas en México fuera del ámbito", "Las ventas declaradas en México quedan fuera del ámbito", "HIGH"), vencimiento=("2027-03-31", "Vence el 31 de marzo de 2027", "LOW"), prima=("9.800 euros anuales", "Prima total anual: 9.800 euros", "NONE"))

    poliza("03-do", {**A, "lema": "Líneas financieras"}, "Alfara Seguros, S.A.", "Responsabilidad de Administradores y Directivos", "DO-0003-117402", "16 de diciembre de 2025", "15 de diciembre de 2026", "Vence el 15 de diciembre de 2026, sin prórroga automática", ", sus administradores y directivos", """
!cols 2.6,2.2,1.4
| Garantía | Límite | Franquicia (€) |
| Responsabilidad personal | 1.000.000 euros por anualidad | 0 |
| Reembolso a la sociedad | Incluido en el límite | 10.000 |
| Gastos de defensa | Incluidos en el límite | 0 |
| Gastos de rehabilitación de imagen | Sublímite de 50.000 euros | 0 |
| Inspecciones y procedimientos administrativos | Sublímite de 100.000 euros | 0 |
El límite agregado es de 1.000.000 euros por anualidad. Se cubren los gastos de defensa y responsabilidad de administradores.
Sin franquicia para personas físicas.
""", """
3.1. Base de reclamación. Se cubren las reclamaciones formuladas por primera vez contra los asegurados durante el periodo de seguro y notificadas antes de su vencimiento.
3.2. Cambio de control. Se entiende por tal la fusión, la venta de todos o la mayoría de los activos o la adquisición de más del 50% de los derechos de voto. Desde esa fecha la cobertura se limita a los actos anteriores.
3.3. Periodo de descubrimiento. No se contrata periodo de descubrimiento posterior. Podrá solicitarse antes del vencimiento, por doce meses y con una sobreprima del 125%.
3.4. Renovación. La oferta de renovación requerirá cuestionario actualizado y las últimas cuentas auditadas, que deberán recibirse antes del 30 de noviembre de 2026.
3.5. Separabilidad. El conocimiento de un asegurado no se imputará a los demás, salvo el del administrador único.
""", """
- Se excluyen las reclamaciones por actos posteriores a un cambio de control.
- Operaciones con partes vinculadas no aprobadas conforme a la ley.
- Dolo, enriquecimiento ilícito o ventaja personal, declarados por sentencia firme.
- Hechos conocidos o litigios anteriores a la fecha de efecto.
- Daños personales y materiales.
""", "Todo el mundo, salvo EE. UU. y Canadá.", """
!cols 3,2.4
| Pregunta | Respuesta del tomador |
| Patrimonio neto | 5.940.000 euros |
| Resultado del último ejercicio | 618.000 euros |
| Está prevista una operación societaria | No |
| Existen operaciones con partes vinculadas | No |
| Litigios en curso contra administradores | No |
| Fecha del cuestionario | 2 de diciembre de 2025 |
""", 5000, 5400, "los perjuicios y gastos de defensa derivados de reclamaciones contra administradores y directivos por actos negligentes en el ejercicio de su cargo")
    REF["03-do.pdf"] = dict(aseguradora=("Alfara Seguros, S.A.", "Alfara Seguros, S.A.", "NONE"), ramo=("Responsabilidad de Administradores y Directivos (D&O)", "Póliza DO-0003-117402", "NONE"), coberturas=("Gastos de defensa y responsabilidad de administradores; sin periodo de descubrimiento", "No se contrata periodo de descubrimiento posterior", "HIGH"), limite=("1.000.000 euros por anualidad", "El límite agregado es de 1.000.000 euros por anualidad", "LOW"), franquicia=("Sin franquicia para personas físicas; 10.000 euros en reembolso a la sociedad", "Sin franquicia para personas físicas", "NONE"), exclusiones=("Actos posteriores a un cambio de control y operaciones vinculadas no aprobadas", "Se excluyen las reclamaciones por actos posteriores a un cambio de control", "HIGH"), territorio=("Todo el mundo, salvo EE. UU. y Canadá", "Todo el mundo, salvo EE. UU. y Canadá", "NONE"), vencimiento=("2026-12-15", "Vence el 15 de diciembre de 2026, sin prórroga automática", "HIGH"), prima=("5.400 euros anuales", "Prima total anual: 5.400 euros", "NONE"))

    poliza("04-cyber", G, "Gamelia Seguros, S.A.", "Ciberriesgos", "CY-0004-902561", "1 de marzo de 2026", "28 de febrero de 2027", "Vence el 28 de febrero de 2027, con prórroga anual sujeta a cuestionario", "", """
!cols 2.6,2.4,1.5
| Garantía | Límite | Carencia o franquicia |
| Respuesta a incidentes | 250.000 euros por anualidad | 5.000 euros |
| Pérdida de beneficios | Incluida en el límite | 72 horas |
| Responsabilidad por datos personales | Incluida en el límite | 5.000 euros |
| Restauración de sistemas | Sublímite de 100.000 euros | 5.000 euros |
| Fraude por suplantación | Sublímite de 25.000 euros | 5.000 euros |
El límite agregado es de 250.000 euros por anualidad. La facturación anual declarada es de 18.600.000 euros.
Se cubren la respuesta a incidentes, la pérdida de beneficios y la responsabilidad por datos personales. Se aplican 72 horas de carencia en pérdida de beneficios.
""", """
3.1. Medidas mínimas. Son condición de cobertura la copia de seguridad semanal desconectada, la actualización de sistemas en treinta días y la autenticación multifactor en todos los accesos remotos y cuentas con privilegios.
3.2. Servicio de respuesta. El asegurado comunicará el incidente al centro de atención en cuarenta y ocho horas y utilizará los proveedores designados por el asegurador.
3.3. Interrupción de proveedor. La caída del proveedor de nube se cubre con un sublímite de 40.000 euros.
3.4. Sistemas industriales. Los equipos de planta conectados se incluyen si están segmentados de la red de oficinas.
""", """
- Se excluye el ransomware si no hay autenticación multifactor en todos los accesos remotos.
- Fallos de infraestructura pública, energía o telecomunicaciones.
- Guerra, operaciones de Estado y sanciones internacionales.
- Multas y sanciones no asegurables.
- Sistemas sin soporte del fabricante.
""", "Todo el mundo.", """
!cols 3.4,2.6
| Pregunta | Respuesta del tomador |
| Facturación anual | 18.600.000 euros |
| Autenticación multifactor en accesos remotos | Parcial: oficinas sí; planta y mantenimiento, no |
| Copias desconectadas | Semanales |
| Sistemas sin soporte | Dos equipos de la línea de estañado |
| Registros de datos personales | 1.100 |
| Incidentes en tres años | Uno, correo fraudulento, sin pérdida |
En el cuestionario, el tomador declara autenticación multifactor parcial.
""", 6500, 7100, "los gastos propios y la responsabilidad del asegurado derivados de un incidente de seguridad o de privacidad")
    REF["04-cyber.pdf"] = dict(aseguradora=("Gamelia Seguros, S.A.", "Gamelia Seguros, S.A.", "NONE"), ramo=("Ciberriesgos", "Póliza CY-0004-902561", "NONE"), coberturas=("Respuesta a incidentes, pérdida de beneficios y datos; el tomador declara MFA parcial", "el tomador declara autenticación multifactor parcial", "HIGH"), limite=("250.000 euros por anualidad; facturación declarada de 18.600.000 euros", "El límite agregado es de 250.000 euros por anualidad. La facturación anual declarada es de 18.600.000 euros", "HIGH"), franquicia=("72 horas de carencia en pérdida de beneficios; 5.000 euros", "Se aplican 72 horas de carencia en pérdida de beneficios", "LOW"), exclusiones=("Ransomware sin MFA en todos los accesos remotos; sistemas sin soporte", "Se excluye el ransomware si no hay autenticación multifactor en todos los accesos remotos", "HIGH"), territorio=("Todo el mundo", "Todo el mundo", "NONE"), vencimiento=("2027-02-28", "Vence el 28 de febrero de 2027", "LOW"), prima=("7.100 euros anuales", "Prima total anual: 7.100 euros", "NONE"))

    poliza("05-danos-materiales", D, "Deleida Seguros, S.A.", "Daños Materiales Industriales", "DM-0005-447190", "1 de febrero de 2026", "31 de enero de 2027", "Vence el 31 de enero de 2027, con prórroga anual", " y, en cuanto al continente, Inmuebles Saucedal, S.L.", """
!cols 2.4,2.2,1.6
| Partida | Suma asegurada (€) | Franquicia (€) |
| Continente | 2.900.000 | 10.000 |
| Maquinaria e instalaciones | 2.300.000 | 10.000 |
| Existencias | 800.000 | 10.000 |
| Pérdida de beneficios, 12 meses | 1.200.000 | 5 días |
La suma asegurada de contenido es de 3.100.000 euros, frente a un valor declarado de 5.400.000 euros en el cuestionario.
Se cubren incendio, explosión, daños por agua, fenómenos atmosféricos, robo, avería de maquinaria y pérdida de beneficios.
La franquicia general es de 10.000 euros por siniestro y de cinco días en pérdida de beneficios.
""", """
3.1. Valoración. Los bienes se valoran a nuevo, con el límite del doble de su valor real.
3.2. Regla proporcional. Si en el momento del siniestro la suma asegurada es inferior al valor del interés, la indemnización se reducirá en la misma proporción, conforme al artículo 30 de la Ley. No se pacta derogación.
3.3. Situación del riesgo: calle del Torno, 14, Getafe. El traslado de la actividad a otro inmueble requiere comunicación y aceptación previa y suspende la cobertura hasta entonces.
3.4. Beneficiarios. Inmuebles Saucedal, S.L. en cuanto al continente y Banco Merediano de Crédito, S.A. en cuanto a la maquinaria hipotecada.
3.5. Medidas de prevención. Mantenimiento anual de la red de mangueras, extintores y detección.
""", """
- Se excluyen el desgaste y la falta de mantenimiento.
- Bienes propiedad de terceros en depósito, salvo inclusión expresa.
- Daños a moldes y utillajes durante su uso.
- Paralización por falta de suministro externo superior a 24 horas.
- Obras, desmontaje y traslado de maquinaria.
""", "Situación del riesgo en Getafe, España. Transporte entre centros no incluido.", """
!cols 3.4,2.2
| Pregunta | Respuesta del tomador |
| Valor de reposición del continente | 2.900.000 euros |
| Valor de reposición de maquinaria e instalaciones | 4.200.000 euros |
| Valor máximo de existencias | 1.200.000 euros |
| Valor declarado de contenido | 5.400.000 euros |
| Bienes de terceros en depósito | 198.200 euros en utillajes |
| Régimen de ocupación | Arrendamiento hasta el 31 de diciembre de 2026 |
""", 18900, 21600, "los daños materiales directos sufridos por los bienes asegurados y, en su caso, la pérdida de beneficios consecutiva", "")
    REF["05-danos-materiales.pdf"] = dict(aseguradora=("Deleida Seguros, S.A.", "Deleida Seguros, S.A.", "NONE"), ramo=("Daños Materiales Industriales", "Póliza DM-0005-447190", "NONE"), coberturas=("Incendio, agua, robo, avería y pérdida de beneficios; regla proporcional sin derogar", "Se cubren incendio, explosión, daños por agua, fenómenos atmosféricos, robo, avería de maquinaria y pérdida de beneficios", "MEDIUM"), limite=("Contenido 3.100.000 euros frente a 5.400.000 declarados; continente 2.900.000", "La suma asegurada de contenido es de 3.100.000 euros, frente a un valor declarado de 5.400.000 euros", "HIGH"), franquicia=("10.000 euros por siniestro; cinco días en pérdida de beneficios", "La franquicia general es de 10.000 euros por siniestro", "LOW"), exclusiones=("Bienes de terceros en depósito, desmontaje y traslado de maquinaria", "Obras, desmontaje y traslado de maquinaria", "MEDIUM"), territorio=("Getafe; un traslado suspende la cobertura", "Situación del riesgo en Getafe, España", "HIGH"), vencimiento=("2027-01-31", "Vence el 31 de enero de 2027", "MEDIUM"), prima=("21.600 euros anuales", "Prima total anual: 21.600 euros", "NONE"))
