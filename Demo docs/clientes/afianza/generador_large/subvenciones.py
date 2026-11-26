"""Subvenciones: bases, 13 expedientes de gasto y resolución."""
import random
from .comun import ADM, NV, NV_CIF, NV_DOM
from .motor import cif, escaneo, est, eur, iban, pdf

DIR = "subvenciones_large"; REF = {}
EXP = "INNOVA-2025/00417"
TIP = [("Arial", "#234e70", "bar"), ("Georgia", "#6d4c1b", "hex"), ("Times", "#2f5d50", "esc"), ("Arial", "#7b2d26", "circ"), ("Times", "#4a3b2a", "x"), ("Arial", "#234e70", "bar"), ("Arial", "#3f3d7a", "hex"), ("Georgia", "#22577a", "circ"), ("Georgia", "#22577a", "circ"), ("Arial", "#1f3a5f", "hex"), ("Times", "#5f6f1f", "bar"), ("Arial", "#555555", "esc"), ("Georgia", "#8a4b08", "x")]
# archivo, proveedor, letra, n.º, fecha, (concepto, uds, precio)…, imputado, pago, concepto, observaciones, regla, criticidad
G = [
 ("01-sensores", "Sensores Hayedal, S.L.", "B", "F-118", "12 de marzo de 2025", "2025-03-12", [("Sensor de fuerza 500 N, clase 0,2", 8, 1450), ("Sensor de temperatura superficial", 12, 420), ("Módulo de adquisición 16 canales", 2, 3680)], 24000, "Transferencia de 10 de abril de 2025", "Sensores para el banco de ensayo del prototipo NX-500.", "", "NONE"),
 ("02-ingenieria", "Ingeniería Pinarea, S.L.", "B", "2025-77", "20 de mayo de 2025", "2025-05-20", [("Diseño mecánico del prototipo, horas", 260, 75), ("Simulación térmica, horas", 100, 85), ("Planos de fabricación, lote", 1, 2000)], 36300, "Transferencia de 18 de junio de 2025", "Diseño del prototipo NX-500.", "El importe imputado incluye la cuota de IVA de la factura.", "HIGH"),
 ("03-ensayos", "Ensayos Robledia, S.L.", "B", "R-009", "14 de enero de 2026", "2026-01-14", [("Ensayo de vibración según programa", 5, 1100), ("Ensayo de niebla salina 480 h", 4, 950), ("Informe acreditado", 2, 1600)], 12500, "Transferencia de 2 de febrero de 2026", "Ensayos del prototipo NX-500 realizados en diciembre de 2025.", "", "HIGH"),
 ("04-material", "Suministros Fresnalia, S.L.", "B", "A-451", "8 de septiembre de 2025", "2025-09-08", [("Tornillería y casquillos, lote", 1, 640), ("Resina y juntas, lote", 1, 960), ("Cableado y terminales, lote", 1, 1200)], 2800, "Efectivo el 8 de septiembre de 2025", "Pequeño material para el montaje del prototipo NX-500.", "Pagado por caja. Se adjunta recibo.", "HIGH"),
 ("05-gestion-tordo", "Tordalia Inversiones, S.L.", "B", "T-12", "30 de junio de 2025", "2025-06-30", [("Gestión del proyecto, primer semestre de 2025", 1, 15000)], 15000, "Transferencia de 15 de julio de 2025", "Gestión del proyecto. Empresa vinculada al administrador único del beneficiario.", "No consta autorización previa de la contratación con parte vinculada.", "HIGH"),
 ("06-sensores-bis", "Sensores Hayedal, S.L.", "B", "F-118", "12 de marzo de 2025", "2025-03-12", [("Sensor de fuerza 500 N, clase 0,2", 8, 1450), ("Sensor de temperatura superficial", 12, 420), ("Módulo de adquisición 16 canales", 2, 3680)], 24000, "Transferencia de 10 de abril de 2025", "Equipos de medida para validación del prototipo NX-500.", "", "HIGH"),
 ("07-software-simulacion", "Cálculo Abedular, S.L.", "B", "CA-2025-061", "3 de noviembre de 2025", "2025-11-03", [("Licencia anual de simulación electromagnética", 2, 7200), ("Puesta en marcha y formación, horas", 40, 90)], 18000, "Transferencia de 15 de abril de 2026", "Software de simulación para el prototipo NX-500.", "", "HIGH"),
 ("08-utillaje-fase-1", "Moldes Acebeda, S.L.", "B", "M-301", "16 de junio de 2025", "2025-06-16", [("Molde prototipo carcasa NX-500, primera parte", 1, 14500)], 14500, "Transferencia de 11 de julio de 2025", "Molde prototipo de la carcasa NX-500, primera parte. Pedido PC-25-0611.", "Sin ofertas alternativas, al no superar 15.000 euros.", "HIGH"),
 ("09-utillaje-fase-2", "Moldes Acebeda, S.L.", "B", "M-302", "17 de junio de 2025", "2025-06-17", [("Molde prototipo carcasa NX-500, segunda parte", 1, 14500)], 14500, "Transferencia de 11 de julio de 2025", "Molde prototipo de la carcasa NX-500, segunda parte. Pedido PC-25-0611.", "Sin ofertas alternativas, al no superar 15.000 euros.", "HIGH"),
 ("10-personal-propio", NV, "", "NP-2025", "31 de diciembre de 2025", "2025-12-31", [], 53200, "Transferencia de nóminas mensuales, última de 30 de diciembre de 2025", "Personal propio: una persona, 1.900 horas a 28 euros por hora, para el prototipo NX-500.", "", "HIGH"),
 ("11-prototipado", "Prototipos Castañar, S.L.", "B", "PR-88", "9 de octubre de 2025", "2025-10-09", [("Serie piloto de carcasas, unidades", 400, 14), ("Serie piloto de terminales, unidades", 800, 5)], 9600, "Transferencia de 7 de noviembre de 2025", "Serie piloto del prototipo NX-500.", "", "NONE"),
 ("12-informe-auditor", "Auditores Encinar, S.L.P.", "B", "AE-25-214", "19 de diciembre de 2025", "2025-12-19", [("Informe de revisión de la cuenta justificativa", 1, 1800)], 1800, "Transferencia de 20 de enero de 2026", "Informe de auditor exigido por las bases.", "", "NONE"),
 ("13-laboratorio-metrologia", "Metrología Alisal, S.L.", "B", "MA-1190", "2 de diciembre de 2025", "2025-12-02", [("Calibración de equipos del banco de ensayo", 8, 400)], 3200, "Transferencia de 30 de diciembre de 2025", "Calibración de los equipos de ensayo del prototipo NX-500.", "", "NONE"),
]


def bases():
    t = """
# BASES REGULADORAS DE LAS AYUDAS A LA INNOVACIÓN INDUSTRIAL
!c Programa INNOVA. Convocatoria 2025
!c Agencia de Innovación Territorial del Valle
### PREÁMBULO
La innovación de producto y de proceso es un factor determinante de la competitividad de la industria. El programa INNOVA tiene por finalidad apoyar proyectos de desarrollo experimental de pequeñas y medianas empresas industriales, mediante subvenciones en régimen de concurrencia competitiva.
## Artículo 1. Objeto
Las presentes bases regulan la concesión, justificación y control de las ayudas a proyectos de desarrollo de prototipos y validación en entorno industrial.
## Artículo 2. Régimen jurídico
Las ayudas se rigen por estas bases, por la convocatoria y por la Ley 38/2003, General de Subvenciones, y su reglamento.
## Artículo 3. Personas beneficiarias
Podrán ser beneficiarias las pequeñas y medianas empresas con establecimiento industrial, al corriente de sus obligaciones tributarias y de Seguridad Social y no incursas en prohibición para obtener subvenciones.
## Artículo 4. Cuantía
La intensidad será del 60% del gasto subvencionable, con un máximo de 150.000 euros por proyecto.
## Artículo 5. Compatibilidad
Las ayudas son compatibles con otras para el mismo fin, siempre que el conjunto no supere el coste de la actividad.
## Artículo 6. Periodo de ejecución y de pago
6.1. Son elegibles los gastos facturados entre el 1 de enero y el 31 de diciembre de 2025 y pagados antes del 31 de marzo de 2026.
6.2. No se admitirán gastos cuya factura se emita fuera del periodo, aunque la actividad se haya realizado dentro de él.
## Artículo 7. Gastos subvencionables
7.1. Son subvencionables, si responden de manera indubitada a la naturaleza del proyecto: colaboraciones externas, materiales y componentes, utillaje de prototipo, equipamiento de ensayo, licencias, personal propio e informe de auditor.
7.2. Personal propio. El coste por hora se obtiene dividiendo el coste anual entre la jornada. Se admite un máximo de 1.720 horas anuales por persona.
7.3. Informe de auditor. Máximo de 2.000 euros.
7.4. Los gastos de dirección y gestión del proyecto no superarán el 10% del presupuesto.
## Artículo 8. Gastos no subvencionables
8.1. El IVA recuperable no es subvencionable.
8.2. Tampoco lo son los intereses, recargos, sanciones, gastos de representación, terrenos e inmuebles.
8.3. Una misma factura solo puede imputarse una vez, en este o en otro proyecto.
## Artículo 9. Contratación y ofertas
9.1. Cuando el gasto con un mismo proveedor por un mismo objeto supere 15.000 euros, IVA excluido, se aportarán tres ofertas previas, salvo que no exista en el mercado suficiente número de entidades.
9.2. No podrá fraccionarse un contrato con el fin de eludir este requisito.
## Artículo 10. Partes vinculadas
La contratación con partes vinculadas exige autorización previa y que se realice en condiciones de mercado, conforme al artículo 29.7 de la Ley General de Subvenciones.
## Artículo 11. Medios de pago
11.1. Solo se admite transferencia bancaria. No se admiten pagos en efectivo.
11.2. El pago se acreditará con justificante bancario en el que consten ordenante, beneficiario, importe, fecha y factura.
## Artículo 12. Solicitudes y evaluación
Las solicitudes se presentarán por medios electrónicos. La evaluación atenderá a la calidad técnica (45 puntos), el impacto (30) y la capacidad de ejecución (25). Se exigirá un mínimo de 60 puntos.
## Artículo 13. Resolución y modificación
La resolución se notificará en seis meses. Las modificaciones se solicitarán antes de que finalice el plazo de ejecución. Se admiten compensaciones entre partidas de hasta el 15%.
## Artículo 14. Justificación
14.1. La cuenta justificativa con informe de auditor se presentará antes del 30 de abril de 2026.
14.2. Por cada gasto se aportará ficha de imputación, factura, justificante de pago y acreditación de la entrega o del servicio.
14.3. Las facturas llevarán estampilla con el porcentaje de imputación y el expediente.
## Artículo 15. Reintegro
15.1. Procederá el reintegro, con intereses de demora, en los casos del artículo 37 de la Ley General de Subvenciones.
15.2. Si el gasto justificado no alcanza el 60% del aprobado, procederá el reintegro total.
## Artículo 16. Publicidad
Las beneficiarias harán constar la ayuda en la documentación y en las instalaciones del proyecto.
## Artículo 17. Control
Las beneficiarias se someterán a las actuaciones de comprobación y conservarán los documentos durante cinco años.
!page
# ANEXO. MODELO DE FICHA DE IMPUTACIÓN
!cols 1.2,3
| Campo | Instrucciones |
| Proveedor y NIF | Los que figuren en la factura |
| Base e IVA | Importes desglosados de la factura |
| Importe imputado | Sin IVA recuperable |
| Pago | Medio y fecha de salida de fondos |
| Vinculación | Declaración de vinculación y fecha de la autorización |
| Ofertas | Número de ofertas y motivo de la elección |
"""
    pdf(DIR, "00-bases", est("Agencia de Innovación del Valle", "Programa INNOVA", "Times", "#14406b", "esc", size=11, ref="INNOVA 2025 · Bases reguladoras"), t, "Bases reguladoras INNOVA 2025")
    REF["00-bases.pdf"] = dict(tipo_doc=("Bases reguladoras", "BASES REGULADORAS DE LAS AYUDAS A LA INNOVACIÓN INDUSTRIAL", "NONE"), proveedor=("Agencia de Innovación Territorial del Valle", "Agencia de Innovación Territorial del Valle", "NONE"), numero=None, fecha=None, base=None, iva=None, importe_imputado=None, pago=("Solo transferencia bancaria; pago antes del 31/03/2026", "Solo se admite transferencia bancaria. No se admiten pagos en efectivo", "NONE"), concepto=("Ayudas a prototipos y validación industrial", "ayudas a proyectos de desarrollo de prototipos y validación en entorno industrial", "NONE"), condiciones=("Facturas de 2025 pagadas antes del 31/03/2026; sin IVA; sin efectivo; vinculadas con autorización; tres ofertas desde 15.000 euros; 1.720 horas; sin duplicados", "Son elegibles los gastos facturados entre el 1 de enero y el 31 de diciembre de 2025 y pagados antes del 31 de marzo de 2026", "HIGH"))


def gasto(i, g):
    fn, prov, letra, num, f, iso, lin, imp, pago, con, obs, risk = g; base = sum(u * p for _, u, p in lin); iva = round(base * .21, 2)
    fo, col, lg = TIP[i]; marca = prov.split(",")[0]; per = fn.startswith("10"); red = fn == "06-sensores-bis"
    sc = {}
    fic = est("Norvalia Conectores", "Proyecto NX-500 · Cuenta justificativa", "Arial", "#1f3a5f", "hex", ref=f"{EXP} · Ficha {fn[:2]}")
    ficha = f"""
!cab FICHA DE IMPUTACIÓN N.º {fn[:2]};;Expediente {EXP} · Proyecto: prototipo de conector de alta corriente NX-500
!cols 1.4,3
!nocab
| Beneficiario | {NV}, NIF {NV_CIF} |
| Proveedor | {prov}{', NIF ' + cif(letra, prov) if letra else ''} |
| Documento | {'Relación de horas' if per else 'Factura'} {num} |
| Fecha de emisión | {f} |
| Partida | {'Personal propio' if per else 'Colaboraciones, materiales y equipamiento'} |
Proveedor: {prov}
Número de {'documento' if per else 'factura'}: {num}. Fecha de emisión: {f}.
""" + ("Coste de personal: 53.200,00 euros. No procede IVA.\n" if per else f"Base imponible: {eur(base)} euros. Cuota de IVA: {eur(iva)} euros.\n") + f"""
Importe imputado al proyecto: {eur(imp)} euros.
Forma y fecha de pago: {pago}.
Concepto: {con}
{obs}
!cols 2.4,1.4,2.4
| Comprobación interna | Resultado | Observaciones |
| Documento original archivado | Sí | Carpeta {fn[:2]} |
| Estampilla de imputación | {'No' if red else 'Sí'} | {'Copia digital' if red else '100%'} |
| Justificante de pago | Sí | Ver documento adjunto |
| Entrega o servicio acreditado | Sí | {'Partes de horas' if per else 'Albarán o acta'} |
| Ofertas alternativas | {'Sí' if base > 15000 and i != 4 else 'No procede'} | {'Archivo de compras' if base > 15000 else 'Importe inferior al umbral'} |
!firma Elaborado por;D. Horacio Belinchón Tello;Administración||Conforme;{ADM};Administrador único
"""
    if per:
        r = random.Random(7); hs = [165, 152, 168, 158, 166, 160, 162, 104, 168, 176, 160, 161]; assert sum(hs) == 1900
        cuerpo = f"""
!page
# RELACIÓN DE HORAS Y COSTES DE PERSONAL {num}
Persona: código E07, titulado/a de ingeniería. Dedicación al proyecto durante 2025.
!cols 1.6,1,1.2,1.6
| Mes de 2025 | Horas | Coste por hora (€) | Importe (€) |
""" + "\n".join(f"| {m} | {h} | 28,00 | {eur(h*28)} |" for m, h in zip("Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre".split(), hs)) + f"""
| Total | 1.900 | | 53.200,00 |
Coste anual de empresa: 48.160,00 euros. Coste por hora: 48.160,00 / 1.720 = 28,00 euros.
!page
# PARTES DE HORAS POR PAQUETE DE TRABAJO
!cols 1.4,1,1,1,1
| Mes | PT1 Diseño | PT2 Prototipo | PT3 Ensayo | Total |
""" + "\n".join(f"| {m} | {(a:=int(h*.3))} | {(b:=int(h*.45))} | {h-a-b} | {h} |" for m, h in zip("Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre".split(), hs)) + f"""
!firma Persona trabajadora;Rubén Sanchidrián Mora;E07||Responsable;{ADM};Administrador único
!page
# REMESAS DE NÓMINA
!cols 1.6,1.6,2
| Mes | Fecha de transferencia | Referencia |
""" + "\n".join(f"| {m} | {28 if k==2 else 30}/{k:02d}/2025 | RN-25{k:02d} |" for k, m in enumerate("Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre".split(), 1)) + "\n"
        pdf(DIR, fn, fic, ficha + cuerpo, f"Expediente {fn[:2]}")
    else:
        ped = "PC-25-0611" if fn[:2] in ("08", "09") else f"PC-25-{random.Random(num).randint(100, 590):04d}"
        fac = f"""
!cab FACTURA {num};;{prov} · NIF {cif(letra, prov)}
!cols 1.2,2.2,1.2,2.2
!nocab
| Cliente | {NV} | Factura | {num} |
| NIF | {NV_CIF} | Fecha | {f} |
| Domicilio | {NV_DOM} | Pedido | {ped} |
!cols 3.4,.8,1.1,1.2
| Descripción | Uds. | Precio (€) | Importe (€) |
""" + "\n".join(f"| {d} | {u} | {eur(p)} | {eur(u*p)} |" for d, u, p in lin) + f"""
!cols 3,1.4
| Resumen | Importe (€) |
| Base imponible | {eur(base)} |
| IVA 21% | {eur(iva)} |
| Total factura | {eur(base+iva)} |
Forma de pago: {'contado' if fn[:2]=='04' else 'transferencia a 30 días'}. Cuenta: {iban(prov)}.
Proyecto: prototipo NX-500.
""" + (f"!sello IMPUTADO 100%;;EXP. {EXP}\n" if not red else "") + (f"!i Vinculación: la sociedad emisora está participada al 100% por {ADM}.\n" if fn[:2] == "05" else "") + f"""
!page
# ALBARÁN Y CONFORMIDAD
!cols 1.2,3
!nocab
| Pedido | {ped} |
| Entregado a | Almacén de Getafe. Recepción del proyecto NX-500 |
| Fecha de recepción | {'18 de diciembre de 2025' if fn[:2]=='03' else f} |
!cols 3.6,1,1.4
| Descripción | Uds. | Estado |
""" + "\n".join(f"| {d} | {u} | Conforme |" for d, u, _ in lin) + f"""
!firma Recibido;D. Horacio Belinchón Tello;Administración||Entregado;Departamento de expediciones;{marca}
"""
        if fn[:2] == "04":
            sc["tk"] = escaneo(["SUMINISTROS FRESNALIA, S.L.", "RECIBI EN EFECTIVO", "", "Factura: A-451", "Fecha:   08/09/2025", "De:      NORVALIA CONECTORES, S.L.", "", "Base:        2.800,00 EUR", "IVA 21%:       588,00 EUR", "TOTAL:       3.388,00 EUR", "", "Forma de pago: EFECTIVO", "", "Gracias por su visita"], 5, 720, 980)
            pg = "### Copia digitalizada del recibo\n!scan tk\n"
        else:
            fp = pago.replace("Transferencia de ", "")
            pg = f"""
# JUSTIFICANTE DE TRANSFERENCIA
!i Copia para el ordenante.
!cols 1.4,3
!nocab
| Ordenante | {NV} |
| Cuenta de cargo | {iban('banco')} |
| Beneficiario | {prov} |
| Cuenta de abono | {iban(prov)} |
| Importe | {eur(base+iva)} euros |
| Fecha de la operación | {fp} |
| Concepto | Factura {num} |
| Referencia | TR{random.Random(prov+num).randint(10**9, 10**10-1)} |
!sello BANCO MEREDIANO;;OPERACIÓN REALIZADA
"""
        # expediente: ficha con imagen de Norvalia y documentos del proveedor, unidos en un PDF
        import io
        from pypdf import PdfReader, PdfWriter
        from .motor import BASE
        pdf(DIR, "_a", fic, ficha, "a"); pdf(DIR, "_b", est(marca, "", fo, col, lg, ref=f"Factura {num}", sello="#8b1a1a"), fac, "b")
        bk = est(marca, "", fo, col, lg, ref="Recibo") if sc else est("Banco Merediano", "Banca de empresas", "Arial", "#5b1238", "bar", ref="Justificante de operación", sello="#5b1238")
        pdf(DIR, "_c", bk, pg, "c", scans=sc)
        w = PdfWriter()
        for x in "_a", "_b", "_c":
            for p in PdfReader(str(BASE / DIR / f"{x}.pdf")).pages: w.add_page(p)
        w.add_metadata({"/Title": f"Expediente de gasto {fn[:2]}", "/Author": "Norvalia Conectores"})
        w.write(str(BASE / DIR / f"{fn}.pdf"))
        for x in "_a", "_b", "_c": (BASE / DIR / f"{x}.pdf").unlink()
    vp = prov + (", vinculada al administrador único" if i == 4 else "")
    REF[f"{fn}.pdf"] = dict(tipo_doc=("Expediente de gasto: " + ("horas de personal" if per else "ficha, factura y pago"), f"FICHA DE IMPUTACIÓN N.º {fn[:2]}", "NONE"), proveedor=(vp, f"Proveedor: {prov}", "HIGH" if i == 4 else "NONE"), numero=(num, f"Número de {'documento' if per else 'factura'}: {num}", "HIGH" if i in (0, 5) else "NONE"), fecha=(iso, f"Fecha de emisión: {f}", "HIGH" if i == 2 else "MEDIUM" if i in (7, 8) else "NONE"), base=("53.200,00 euros, sin IVA" if per else f"{eur(base)} euros", "Coste de personal: 53.200,00 euros" if per else f"Base imponible: {eur(base)} euros", "NONE"), iva=None if per else (f"{eur(iva)} euros", f"Cuota de IVA: {eur(iva)} euros", "NONE"), importe_imputado=(f"{eur(imp)} euros", f"Importe imputado al proyecto: {eur(imp)} euros", risk if i in (1, 5, 9) else "NONE"), pago=(pago, f"Forma y fecha de pago: {pago}", "HIGH" if i in (3, 6) else "NONE"), concepto=(con.rstrip(".") + (". Sin autorización previa" if i == 4 else ""), "No consta autorización previa de la contratación con parte vinculada" if i == 4 else con.rstrip("."), "HIGH" if i in (4, 7, 8, 9) else "NONE"), condiciones=None)


def resolucion():
    t = f"""
# RESOLUCIÓN DE CONCESIÓN
!c Programa INNOVA. Convocatoria 2025 · Expediente {EXP}
### ANTECEDENTES
Primero. Con fecha 14 de noviembre de 2024, {NV} solicitó ayuda para el proyecto «Prototipo de conector de alta corriente NX-500».
Segundo. La comisión de evaluación otorgó al proyecto 78 puntos, por encima del mínimo exigido.
Tercero. La empresa ha acreditado hallarse al corriente de sus obligaciones tributarias y de Seguridad Social.
### RESUELVO
## Primero. Concesión
Conceder a {NV} una subvención de 144.000 euros, equivalente al 60% de un presupuesto subvencionable de 240.000 euros.
## Segundo. Presupuesto aprobado
!cols 3,1.6
| Partida | Presupuesto (€) |
| Colaboraciones externas | 62.000 |
| Materiales y componentes | 14.000 |
| Utillaje de prototipo | 42.000 |
| Equipamiento de ensayo y licencias | 58.000 |
| Personal propio | 48.160 |
| Gestión del proyecto | 13.840 |
| Informe de auditor | 2.000 |
| Total | 240.000 |
## Tercero. Anticipo
Se abona un anticipo del 50%, por importe de 72.000 euros. El resto se abonará tras la comprobación de la cuenta justificativa.
## Cuarto. Condiciones
El proyecto se ejecutará entre el 1 de enero y el 31 de diciembre de 2025, con sujeción a las bases reguladoras. No se ha solicitado ni concedido autorización para contratar con partes vinculadas.
## Quinto. Garantía
No se exige garantía por el anticipo, atendido su importe.
## Sexto. Recursos
Contra esta resolución cabe recurso de reposición en el plazo de un mes, o recurso contencioso-administrativo en el de dos meses.
Fecha de la resolución: 20 de diciembre de 2024.
!firma La dirección de la Agencia;D.ª Casilda Fontecha Riaño;Directora
!sello AGENCIA DE INNOVACIÓN;;REGISTRO DE SALIDA
"""
    pdf(DIR, "14-resolucion", est("Agencia de Innovación del Valle", "Programa INNOVA", "Times", "#14406b", "esc", size=11, ref=EXP), t, "Resolución de concesión")
    REF["14-resolucion.pdf"] = dict(tipo_doc=("Resolución de concesión", "RESOLUCIÓN DE CONCESIÓN", "NONE"), proveedor=("Agencia de Innovación del Valle", "Agencia de Innovación del Valle", "NONE"), numero=(EXP, f"Expediente {EXP}", "NONE"), fecha=("2024-12-20", "Fecha de la resolución: 20 de diciembre de 2024", "NONE"), base=("Presupuesto subvencionable de 240.000 euros", "un presupuesto subvencionable de 240.000 euros", "NONE"), iva=None, importe_imputado=None, pago=("Anticipo del 50%: 72.000 euros", "Se abona un anticipo del 50%, por importe de 72.000 euros", "MEDIUM"), concepto=("Prototipo de conector de alta corriente NX-500; subvención de 144.000 euros", "una subvención de 144.000 euros", "NONE"), condiciones=("Ejecución en 2025; sin autorización para partes vinculadas", "No se ha solicitado ni concedido autorización para contratar con partes vinculadas", "HIGH"))


def generar():
    bases()
    for i, g in enumerate(G):
        b = sum(u * p for _, u, p in g[6])
        if i not in (1, 9): assert b == g[7], (g[0], b, g[7])
        gasto(i, g)
    resolucion()
