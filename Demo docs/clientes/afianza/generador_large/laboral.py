"""Traspaso laboral: 7 personas (contrato y nómina) y extracto de convenio."""
import random
from .comun import ADM, NV, NV_CIF, NV_DOM
from .motor import dni, est, eur, iban, pdf

DIR = "traspaso-laboral_large"; REF = {}; NOMINAS = {}
CV = "Convenio colectivo de Norvalia Conectores, S.L. 2025-2027"
CCC = "28/0000001/00"; CCC2 = "45/0000002/00"
CX = "Código de cuenta de cotización: "
# código, nombre, categoría contrato, categoría nómina, modalidad, fin, jornada c, jornada n, salario c, salario n, antigüedad c, antigüedad n, ccc c, ccc n, irpf
P = [
 ("E01", "Marta Olivenza Crespo", "Técnico/a de calidad", "Técnico/a de calidad", "Indefinido ordinario a tiempo completo", "", 40, 40, 27500, 27500, ("1 de marzo de 2020", "2020-03-01"), None, CCC, CCC, 14.2),
 ("E02", "Julián Ceballos Rueda", "Oficial de primera", "Oficial de segunda", "Indefinido ordinario a tiempo completo", "", 40, 40, 26400, 23100, ("15 de mayo de 2018", "2018-05-15"), None, CCC, CCC, 10.6),
 ("E03", "Lorena Piquer Salas", "Administrativo/a", "Administrativo/a", "Temporal por circunstancias de la producción", "30 de junio de 2026", 30, 40, 18900, 18900, ("1 de enero de 2025", "2025-01-01"), ("1 de julio de 2025", "2025-07-01"), CCC, CCC, 6.1),
 ("E04", "Óscar Tébar Infante", "Especialista", "Especialista", "Indefinido ordinario a tiempo completo", "", 40, 40, 20400, 20400, ("9 de septiembre de 2022", "2022-09-09"), None, CCC, CCC, 7.8),
 ("E05", "Yolanda Mencía Robles", "Oficial de segunda", "Oficial de segunda", "Indefinido ordinario a tiempo completo", "", 40, 40, 23500, 23500, ("4 de abril de 2021", "2021-04-04"), None, CCC, CCC2, 9.9),
 ("E06", "Beatriz Anaya Lozano", "Técnico/a de calidad", "Técnico/a de calidad", "Indefinido ordinario a tiempo completo", "", 40, 40, 28000, 28000, ("2 de noviembre de 2019", "2019-11-02"), None, CCC, CCC, 13.5),
 ("E07", "Rubén Sanchidrián Mora", "Titulado/a de ingeniería", "Titulado/a de ingeniería", "Indefinido ordinario a tiempo completo", "", 40, 40, 34300, 34300, ("17 de enero de 2023", "2023-01-17"), None, CCC, CCC, 16.8),
]
FUN = {"Técnico/a de calidad": "control dimensional y eléctrico, gestión de no conformidades, auditorías de proceso y calibración de equipos de medida", "Oficial de primera": "ajuste y cambio de utillajes en prensas de corte, primeras piezas, mantenimiento de primer nivel y formación del turno", "Oficial de segunda": "conducción de línea de ensamblado, autocontrol, alimentación de materiales y registro de paradas", "Administrativo/a": "registro de pedidos, albaranes y facturas, atención telefónica y archivo", "Especialista": "montaje manual, verificación visual, embalaje y etiquetado", "Titulado/a de ingeniería": "industrialización de nuevas referencias, validación de procesos y seguimiento de indicadores de planta"}
ST = est("Norvalia Conectores", "Personas y organización", "Arial", "#1f3a5f", "hex", size=9.8)


def contrato(p):
    c, n, g, _, mod, fin, j, _, s, _, a, _, ccc, _, _ = p; m14 = s / 14
    temp = bool(fin); jt = f"{j} horas semanales"
    dur = f"El contrato es de carácter temporal y se extiende hasta el {fin}. La causa es el incremento ocasional de tareas administrativas por la implantación del nuevo sistema de gestión." if temp else "El contrato se concierta por tiempo indefinido."
    nov = f"""
!page
# ACUERDO DE REDUCCIÓN DE JORNADA POR GUARDA LEGAL
!c Getafe, a 24 de julio de 2026 · Código de empleado: {c}
De una parte, {NV}, y de otra, {n}, con antigüedad de {a[0]}, acuerdan:
## Primero. Reducción
Al amparo del artículo 37.6 del Estatuto de los Trabajadores, la jornada pasa de 40 a 30 horas semanales, con efectos desde el 1 de septiembre de 2026 y hasta nueva comunicación.
## Segundo. Horario
La prestación se realizará de lunes a viernes, de 8:30 a 14:30. La persona trabajadora comunicará con quince días de antelación la fecha de reincorporación a su jornada ordinaria.
## Tercero. Retribución
El salario se reduce en la misma proporción, del 25%. Desde la fecha de efectos, el salario bruto anual queda fijado en {eur(s*.75,0)} euros.
## Cuarto. Cotización y comunicación
La empresa comunicará la variación a la Tesorería General de la Seguridad Social y al gestor de nóminas. Los demás términos del contrato permanecen sin cambios.
!firma Por la empresa;{ADM};Administrador único||La persona trabajadora;{n};{c}
""" if c == "E06" else ""
    t = f"""
# CONTRATO DE TRABAJO {'TEMPORAL' if temp else 'INDEFINIDO'}
!c Código de empleado: {c}
!cols 1.3,3
!nocab
| Empresa | {NV}, NIF {NV_CIF} |
| Domicilio | {NV_DOM} |
| CCC | {CX}{ccc} |
| Representante | {ADM}, administrador único |
| Persona trabajadora | {n}, DNI {dni(n)} |
| N.º de afiliación | 00/{random.Random(n).randint(10000000, 99999999)}/00 |
| Código de empleado | {c} |
| Titulación y ocupación | {g} |
Las partes declaran que reúnen los requisitos exigidos para celebrar el presente contrato y acuerdan formalizarlo con arreglo a las siguientes
### CLÁUSULAS
## Primera. Prestación de servicios
La persona trabajadora prestará sus servicios con la categoría de {g}, en el centro de trabajo de Getafe. Las funciones comprenden {FUN[g]}, así como las tareas accesorias propias del grupo profesional.
La empresa podrá establecer la movilidad funcional dentro de los límites del artículo 39 del Estatuto de los Trabajadores.
## Segunda. Jornada
La jornada ordinaria será de {jt}, {'a tiempo parcial, ' if j < 40 else ''}prestadas de lunes a viernes, con los descansos que establece la ley y según el calendario del centro. Los turnos se publicarán con una antelación mínima de cinco días.
{'No se pactan horas complementarias. La jornada a tiempo completo comparable es de 40 horas semanales.' if j < 40 else 'La distribución irregular de la jornada se ajustará a lo previsto en el convenio.'}
## Tercera. Duración
{dur} Modalidad: {mod}.
La relación se inició el {a[0]}. Fecha de antigüedad: {a[0]}. Se establece un periodo de prueba conforme al convenio, en los términos del artículo 14 del Estatuto de los Trabajadores.
{'A su finalización, la persona trabajadora percibirá la indemnización prevista en el artículo 49.1.c del Estatuto de los Trabajadores.' if temp else ''}
## Cuarta. Retribución
La persona trabajadora percibirá un salario bruto anual de {eur(s,0)} euros, distribuido en 14 pagas de {eur(m14)} euros, por todos los conceptos salariales fijos. Las pagas extraordinarias se abonarán en junio y diciembre.
Las mejoras sobre las tablas del convenio podrán ser compensadas y absorbidas. Los gastos de desplazamiento se abonarán con justificación previa.
## Quinta. Vacaciones
La duración de las vacaciones anuales será de treinta días naturales, que se disfrutarán de acuerdo con el calendario pactado.
## Sexta. Convenio aplicable
En lo no previsto se estará a la legislación vigente y, en particular, al {CV}.
## Séptima. Prevención de riesgos
La empresa facilitará la formación e información preventiva del puesto, los equipos de protección y la vigilancia periódica de la salud. La persona trabajadora cumplirá las instrucciones recibidas y comunicará cualquier situación de riesgo.
## Octava. Confidencialidad y propiedad industrial
La persona trabajadora guardará secreto sobre los procesos, planos, clientes y condiciones económicas que conozca, durante la relación y después de ella. Los resultados obtenidos en el desempeño de sus funciones pertenecen a la empresa.
## Novena. Medios informáticos y registro de jornada
Los dispositivos, el correo y las aplicaciones corporativas se destinan a un uso profesional. La empresa podrá realizar controles proporcionados, conforme al protocolo interno. La jornada se registrará diariamente mediante el sistema establecido.
## Décima. Protección de datos
Los datos personales se tratarán para la gestión de la relación laboral, el pago de salarios y el cumplimiento de obligaciones legales. La persona trabajadora podrá ejercer sus derechos ante el departamento de Personas.
## Undécima. Comunicación
El contenido del contrato se comunicará al servicio público de empleo en el plazo de diez días desde su firma. Se entrega copia a la persona trabajadora y copia básica a la representación legal.
!firma Por la empresa;{ADM};Administrador único||La persona trabajadora;{n};{c}
{nov}"""
    pdf(DIR, f"{c}-contrato", {**ST, "ref": f"Contrato de trabajo · {c}"}, t, "Contrato de trabajo")
    red = c == "E06"; falta = c == "E04"
    REF[f"{c}-contrato.pdf"] = dict(persona=(c, f"Código de empleado: {c}", "NONE"), tipo_doc=("Contrato de trabajo" + (" y acuerdo de reducción de jornada" if red else ""), "ACUERDO DE REDUCCIÓN DE JORNADA POR GUARDA LEGAL" if red else f"CONTRATO DE TRABAJO {'TEMPORAL' if temp else 'INDEFINIDO'}", "NONE"), categoria=(g, f"con la categoría de {g}", "HIGH" if c == "E02" else "NONE"), modalidad=(mod + (f", hasta el {fin}" if fin else ""), f"se extiende hasta el {fin}" if fin else f"Modalidad: {mod}", "HIGH" if fin else "NONE"), jornada=("30 horas semanales desde el 01/09/2026 (antes 40)" if red else jt, "la jornada pasa de 40 a 30 horas semanales" if red else f"La jornada ordinaria será de {jt}", "HIGH" if red or c == "E03" else "NONE"), salario=("21.000 euros desde el 01/09/2026 (antes 28.000)" if red else f"{eur(s,0)} euros", "el salario bruto anual queda fijado en 21.000 euros" if red else f"un salario bruto anual de {eur(s,0)} euros", "HIGH" if red or falta or c == "E02" else "NONE"), antiguedad=(a[1], f"Fecha de antigüedad: {a[0]}", "MEDIUM" if c == "E03" else "NONE"), convenio=(CV, CV, "NONE"), ccc=(ccc, f"{CX}{ccc}", "HIGH" if c == "E05" else "NONE"))


def nomina(p):
    c, n, _, g, mod, fin, _, j, _, s, a0, a1, _, ccc, irpf = p; a = a1 or a0
    paga = round(s / 14, 2); base_s = round(paga * .82, 2); plus = round(paga - base_s, 2); prorr = round(paga * 2 / 12, 2); bcc = round(paga + prorr, 2)
    temp = bool(fin); ded = [("Contingencias comunes", bcc, 4.70), ("Mecanismo de equidad intergeneracional", bcc, .15), ("Desempleo", bcc, 1.60 if temp else 1.55), ("Formación profesional", bcc, .10)]
    dl = [(x, b, t_, round(b * t_ / 100, 2)) for x, b, t_ in ded]; ret = round(paga * irpf / 100, 2); td = round(sum(x[3] for x in dl) + ret, 2); liq = round(paga - td, 2)
    emp = [("Contingencias comunes", 23.60), ("Mecanismo de equidad intergeneracional", .75), ("AT y EP", 3.60), ("Desempleo", 6.70 if temp else 5.50), ("FOGASA", .20), ("Formación profesional", .60)]
    NOMINAS[c] = (paga, base_s, plus, dl, ret, td, liq)
    t = f"""
!cab RECIBO INDIVIDUAL DEL PAGO DE SALARIOS;;Nómina de octubre de 2026 · Periodo de liquidación del 1 al 31 de octubre de 2026 · 31 días
!cols 1.2,2.2,1.2,2.2
!nocab
| Empresa | {NV} | Trabajador/a | {n} |
| NIF | {NV_CIF} | DNI | {dni(n)} |
| Domicilio | {NV_DOM} | Código de empleado | {c} |
| CCC | {ccc} | Categoría | {g} |
| Centro | Getafe | Antigüedad | {a[0]} |
Código de empleado: {c}. Categoría profesional: {g}. Fecha de antigüedad: {a[0]}. {CX}{ccc}.
Jornada: {j} horas semanales. Salario bruto anual: {eur(s,0)} euros, en 14 pagas. Convenio: {CV}.
## I. Devengos
!cols 1,3,1.2,1.2
| Código | Concepto | Unidades | Importe (€) |
| 001 | Salario base | 31 | {eur(base_s)} |
| 014 | Plus de convenio | 31 | {eur(plus)} |
| Total | A. Total devengado | | {eur(paga)} |
## II. Deducciones
!cols 3,1.2,1,1.2
| Concepto | Base (€) | Tipo (%) | Importe (€) |
""" + "\n".join(f"| {x} | {eur(b)} | {eur(tt)} | {eur(i)} |" for x, b, tt, i in dl) + f"""
| Retención a cuenta del IRPF | {eur(paga)} | {eur(irpf)} | {eur(ret)} |
| Total B. Total a deducir | | | {eur(td)} |
!caja Líquido total a percibir (A - B): {eur(liq)} euros
Forma de pago: transferencia a {iban(n)}. Fecha de abono: 30 de octubre de 2026.
## III. Bases de cotización y aportación de la empresa
!cols 3,1.2,1,1.2
| Concepto | Base (€) | Tipo (%) | Aportación (€) |
""" + "\n".join(f"| {x} | {eur(bcc)} | {eur(tt)} | {eur(round(bcc*tt/100,2))} |" for x, tt in emp) + f"""
| Total aportación de la empresa | | | {eur(sum(round(bcc*tt/100,2) for _, tt in emp))} |
Remuneración mensual: {eur(paga)} euros. Prorrata de pagas extraordinarias: {eur(prorr)} euros. Base de contingencias comunes: {eur(bcc)} euros. Base sujeta a retención: {eur(paga)} euros.
!firma Firma y sello de la empresa;{ADM};{NV}||Recibí;{n};{c}
"""
    pdf(DIR, f"{c}-nomina-octubre-2026", {**ST, "marca": "Gestoría Peñalara Nóminas", "lema": "Servicio de administración de personal", "color": "#37474f", "logo": "x", "size": 7.6, "ref": f"Nómina 10/2026 · {c}"}, t, "Nómina de octubre de 2026")
    REF[f"{c}-nomina-octubre-2026.pdf"] = dict(persona=(c, f"Código de empleado: {c}", "NONE"), tipo_doc=("Nómina de octubre de 2026", "Nómina de octubre de 2026", "NONE"), categoria=(g, f"Categoría profesional: {g}", "HIGH" if c == "E02" else "NONE"), modalidad=None, jornada=(f"{j} horas semanales", f"Jornada: {j} horas semanales", "HIGH" if c in ("E03", "E06") else "NONE"), salario=(f"{eur(s,0)} euros, en 14 pagas", f"Salario bruto anual: {eur(s,0)} euros, en 14 pagas", "HIGH" if c in ("E02", "E04", "E06") else "NONE"), antiguedad=(a[1], f"Fecha de antigüedad: {a[0]}", "MEDIUM" if c == "E03" else "NONE"), convenio=(CV, CV, "NONE"), ccc=(ccc, f"{CX}{ccc}", "HIGH" if c == "E05" else "NONE"))


def convenio():
    t = f"""
# {CV.upper()}
!c Extracto facilitado para el traspaso. Vigencia: 1 de enero de 2025 a 31 de diciembre de 2027
## Artículo 1. Ámbito
El convenio se aplica a la totalidad de la plantilla del centro de Getafe, con exclusión del personal de alta dirección.
## Artículo 2. Vigencia y denuncia
Estará en vigor hasta el 31 de diciembre de 2027 y se prorrogará por años naturales si no media denuncia con dos meses de antelación. Denunciado, se mantendrá su contenido normativo hasta su sustitución.
## Artículo 8. Clasificación profesional
Los grupos profesionales son los del Anexo I. La realización habitual de funciones de grupo superior durante más de seis meses en un año u ocho en dos dará derecho a reclamar el ascenso y, en todo caso, la diferencia salarial.
## Artículo 12. Jornada
La jornada máxima anual es de 1.752 horas de trabajo efectivo, a razón de 40 horas semanales de promedio. El calendario se negociará antes del 15 de diciembre.
## Artículo 14. Distribución irregular
La empresa podrá distribuir de forma irregular hasta el 8% de la jornada, con un preaviso de cinco días y compensación dentro del semestre.
## Artículo 17. Estructura salarial
El salario se compone de salario base y plus de convenio. Las tablas del Anexo I tienen carácter de mínimo para la jornada a tiempo completo y se reducen en proporción en la jornada parcial o reducida.
## Artículo 18. Pagas extraordinarias
Se abonarán dos pagas, en junio y diciembre, por el importe de una mensualidad de salario base y plus de convenio.
## Artículo 19. Incremento
Para 2026 se aplica un incremento del 3% sobre las tablas de 2025, ya incorporado al Anexo I. Los atrasos se abonarán antes del 31 de marzo.
## Artículo 22. Antigüedad
No se devenga complemento de antigüedad. La fecha de antigüedad se computa desde el inicio de la relación, incluidas las contrataciones temporales sin interrupción significativa.
## Artículo 25. Contratación temporal
La duración máxima de los contratos por circunstancias de la producción será de seis meses, ampliable hasta un año si así lo establece el convenio sectorial. La continuidad en la prestación tras la expiración del plazo convierte la relación en indefinida.
## Artículo 31. Reducción de jornada
Las reducciones por guarda legal se aplicarán en nómina desde la fecha de efectos, con reducción proporcional del salario.
## Artículo 36. Cambio de gestor
En caso de cambio de prestador del servicio de nóminas, la empresa entregará los contratos, sus novaciones y las doce últimas nóminas.
!page
# ANEXO I. TABLAS SALARIALES 2026
Salario mínimo bruto anual por grupo, para 40 horas semanales y en 14 pagas. La categoría de Especialista tiene un mínimo de 21.300 euros brutos anuales.
!cols 2.6,1.2,1.2,1.4
| Categoría | Base mensual (€) | Plus mensual (€) | Mínimo anual (€) |
""" + "\n".join(f"| {g} | {eur(x/14*.82)} | {eur(x/14*.18)} | {eur(x,0)} |" for g, x in [("Titulado/a de ingeniería", 31000), ("Técnico/a de calidad", 26800), ("Oficial de primera", 25900), ("Oficial de segunda", 22900), ("Especialista", 21300), ("Administrativo/a", 18200)]) + """
# ANEXO II. PERMISOS RETRIBUIDOS
!cols 3.4,1.4
| Motivo | Duración |
| Matrimonio o registro de pareja de hecho | 15 días |
| Accidente o enfermedad grave de familiares | 5 días |
| Fallecimiento de cónyuge o familiar de primer grado | 3 días |
| Traslado del domicilio habitual | 1 día |
| Asuntos propios | 2 días |
"""
    pdf(DIR, "00-convenio-extracto", est("Comisión negociadora", "Norvalia Conectores, S.L.", "Times", "#333333", "x", size=10.8, ref="Convenio colectivo 2025-2027 · Extracto"), t, "Extracto de convenio colectivo")
    REF["00-convenio-extracto.pdf"] = dict(persona=None, tipo_doc=("Extracto de convenio colectivo con tablas 2026", "Extracto facilitado para el traspaso", "NONE"), categoria=("Especialista y otras cinco categorías", "La categoría de Especialista", "NONE"), modalidad=("Temporal: máximo seis meses, ampliable a un año; si continúa, indefinido", "La continuidad en la prestación tras la expiración del plazo convierte la relación en indefinida", "MEDIUM"), jornada=("40 horas semanales; 1.752 horas anuales", "a razón de 40 horas semanales de promedio", "NONE"), salario=("Mínimos 2026: Especialista 21.300 euros; Oficial de primera 25.900; Oficial de segunda 22.900; Técnico/a 26.800; Administrativo/a 18.200", "La categoría de Especialista tiene un mínimo de 21.300 euros brutos anuales", "HIGH"), antiguedad=None, convenio=(CV, "Para 2026 se aplica un incremento del 3%", "NONE"), ccc=None)


def generar():
    convenio()
    for p in P: contrato(p); nomina(p)
