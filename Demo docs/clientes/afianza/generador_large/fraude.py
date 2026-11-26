"""CSV de notas de gasto con patrones plantados (pestaña Fraude & Riesgo)."""
import csv, random
from datetime import date, timedelta
from .motor import BASE

CAB = "id_gasto,empleado_id,empleado,departamento,fecha,categoria,proveedor,importe,moneda,metodo_pago,aprobador,estado,notas".split(",")
E = {"EMP-014": ("Laura Gómez", "Marketing", "Carlos Pena"), "EMP-022": ("Javier Soto", "IT", "Marta Vidal"), "EMP-031": ("Marta Ibáñez", "Ventas", "Carlos Pena"), "EMP-007": ("Pedro Salas", "Operaciones", "Marta Vidal"), "EMP-045": ("Sonia Reyes", "Finanzas", "David Ortega"), "EMP-052": ("David Ortega", "Finanzas", "Carlos Pena"), "EMP-063": ("Elena Marchena", "Dirección", "Ramiro Tordesillas"), "EMP-071": ("Hugo Cifuentes", "Ventas", "Carlos Pena"), "EMP-080": ("Horacio Belinchón", "Administración", "David Ortega")}
TC = "Tarjeta corporativa"


def generar():
    r = random.Random(2026); F = []
    def g(e, d, cat, prov, imp, met=TC, ap=None, est="Aprobado", nota=""): F.append([e, d, cat, prov, imp, met, ap or E[e][2], est, nota])
    cat = [("Transporte", ["Tren alta velocidad", "Taxi urbano", "Aparcamiento centro"], 8, 140), ("Comidas", ["Restaurante La Ribera", "Cafetería Norte", "Mesón del Puente"], 11, 68), ("Alojamiento", ["Hotel Almazara", "Hotel Puerta Sur"], 84, 156), ("Material de oficina", ["Papelería Trazos"], 9, 75), ("Software", ["Licencias Nube"], 25, 290), ("Formación", ["Aula Técnica"], 40, 320)]
    ini = date(2026, 7, 1)
    while len(F) < 92:
        d = ini + timedelta(days=r.randrange(92))
        if d.weekday() > 4: continue
        c, ps, a, b = r.choice(cat); g(r.choice([e for e in E if e != "EMP-031"]), d, c, r.choice(ps), round(r.uniform(a, b), 2))
    D = lambda m, d: date(2026, m, d)
    # 1. importes justo por debajo de 500 €   2. duplicados   3. fraccionamiento de servicio   4. autoaprobación
    for m, d, p, i in [(7, 3, "Hotel Miralar", 499), (7, 9, "Restaurante Costa Serena", 498.5), (7, 16, "Restaurante Costa Serena", 497), (7, 23, "Hotel Miralar", 499), (8, 27, "Restaurante Costa Serena", 496.8), (9, 10, "Hotel Miralar", 499)]: g("EMP-031", D(m, d), "Comidas" if p[0] == "R" else "Alojamiento", p, i, nota="Reunión con cliente")
    for d, n in ((14, ""), (17, "Ticket reenviado")): g("EMP-071", D(7, d), "Comidas", "Asador Los Robles", 186.40, nota=n)
    for d, e in ((7, "EMP-014"), (8, "EMP-007"), (9, "EMP-022"), (10, "EMP-080")): g(e, D(9, d), "Consultoría", "Vía Solana Servicios, S.L.", 2900, "Transferencia", nota="Servicios generales")
    g("EMP-045", D(8, 5), "Formación", "Aula Técnica", 640, ap="Sonia Reyes"); g("EMP-052", D(9, 2), "Consultoría", "Vía Solana Servicios, S.L.", 2900, "Transferencia", ap="David Ortega", nota="Sin contrato de referencia")
    # 5. parte vinculada   6. fines de semana y vacaciones   7. efectivo   8. kilometraje imposible   9. categoría impropia   10. números redondos
    for m in (7, 8, 9): g("EMP-063", D(m, 30), "Consultoría", "Tordalia Inversiones, S.L.", 3800, "Transferencia", nota="Gastos de representación del contrato de gestión, sin justificantes")
    for d in (8, 9, 15, 16): g("EMP-031", D(8, d), "Comidas", "Chiringuito Cala Blanca", 92.5 + d, nota="Empleada en vacaciones del 3 al 23 de agosto según RRHH")
    g("EMP-080", D(9, 18), "Material de oficina", "Suministros Fresnalia, S.L.", 1980, "Efectivo", nota="Recibo manuscrito"); g("EMP-071", D(9, 15), "Kilometraje", "Vehículo propio", 712.50, "Reembolso", nota="3.750 km en un día a 0,19 euros")
    g("EMP-071", D(9, 15), "Alojamiento", "Hotel Puerta Sur", 118, nota="Misma fecha, Sevilla"); g("EMP-031", D(9, 24), "Material de oficina", "Joyería Cerval", 320)
    for d in (4, 18): g("EMP-014", D(9, d), "Publicidad", "Impulso Digital Norte", 5000, "Transferencia", nota="Aprobado el mismo día de la solicitud")
    F.sort(key=lambda x: (x[1], x[0])); p = BASE / "fraude_large"; p.mkdir(exist_ok=True)
    with open(p / "notas-gasto-2026-t3.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(CAB)
        for k, (e, d, c, pr, i, m, ap, es, n) in enumerate(F, 1): w.writerow([f"GTO-2026-T3-{k:03d}", e, E[e][0], E[e][1], d.isoformat(), c, pr, f"{i:.2f}", "EUR", m, ap, es, n])
