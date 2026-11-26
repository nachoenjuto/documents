"""Datos comunes del caso y cláusulas generales."""
from .motor import cif, dni
NV = "Norvalia Conectores, S.L."
NV_CIF = cif("B", "norvalia")
NV_DOM = "calle del Torno, 14, Polígono Industrial Las Encinas, 28906 Getafe (Madrid)"
ADM = "D. Ramiro Tordesillas Vega"
DG = "D.ª Elena Marchena Ruiz"


def nv(rol, quien=None):
    q, c = quien or (ADM, "administrador único")
    return f"De una parte, {NV}, con NIF {NV_CIF} y domicilio social en {NV_DOM}, inscrita en el Registro Mercantil de Madrid, representada en este acto por {q}, con DNI {dni(q)}, en su condición de {c}. En adelante, {rol}."


def parte(nombre, letra, dom, rep, cargo, rol, reg="Madrid", extra=""):
    return f"De otra parte, {nombre}, con NIF {cif(letra, nombre)} y domicilio social en {dom}, inscrita en el Registro Mercantil de {reg}, representada por {rep}, con DNI {dni(rep)}, en su condición de {cargo}.{extra} En adelante, {rol}."


# Cláusulas generales: {A} y {B} son las partes; {n} el número de cláusula.
CONF = """## {n}. Confidencialidad
{n}.1. Se considera Información Confidencial toda información técnica, comercial, financiera u organizativa que una de las partes facilite a la otra con ocasión del presente documento, en cualquier soporte y con independencia de que se identifique expresamente como tal, incluidos planos, tolerancias, procesos de fabricación, estructuras de coste, previsiones de demanda y datos de clientes.
{n}.2. La parte receptora se obliga a utilizar la Información Confidencial únicamente para el cumplimiento de sus obligaciones, a limitar el acceso a las personas de su organización que necesiten conocerla y a aplicar medidas de protección no inferiores a las que emplea para su propia información reservada.
{n}.3. No tendrá carácter confidencial la información que fuera de dominio público en el momento de su revelación, la que la parte receptora acredite que ya poseía legítimamente, la obtenida de un tercero no sujeto a secreto y la que deba revelarse por mandato legal o requerimiento de autoridad competente, en cuyo caso se notificará previamente a la otra parte cuando sea legalmente posible.
{n}.4. Las obligaciones de esta cláusula se mantendrán durante la vigencia de la relación y los tres años siguientes a su terminación. Finalizada la relación, la parte receptora devolverá o destruirá la Información Confidencial en el plazo de treinta días y certificará por escrito la destrucción si así se le solicita."""

RGPD = """## {n}. Protección de datos personales
{n}.1. Los datos personales de representantes y personas de contacto serán tratados por cada parte, como responsable independiente, con la finalidad de gestionar, mantener y ejecutar la relación entre ambas, sobre la base de su interés legítimo y del cumplimiento de obligaciones legales.
{n}.2. Los datos se conservarán mientras dure la relación y, después, debidamente bloqueados, durante los plazos de prescripción de las acciones que pudieran derivarse. No se prevén cesiones a terceros salvo obligación legal, ni transferencias internacionales.
{n}.3. Las personas interesadas podrán ejercer los derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad mediante escrito dirigido al domicilio de la parte correspondiente, así como presentar reclamación ante la autoridad de control.
{n}.4. Si la ejecución exigiera el acceso de una parte a datos personales de los que sea responsable la otra, ambas suscribirán con carácter previo el contrato de encargo de tratamiento previsto en el artículo 28 del Reglamento (UE) 2016/679."""

FM = """## {n}. Fuerza mayor
{n}.1. Ninguna de las partes responderá del incumplimiento o del retraso debido a causas de fuerza mayor, entendiendo por tales los sucesos imprevisibles o que, previstos, fueran inevitables y ajenos a su control razonable, conforme al artículo 1105 del Código Civil.
{n}.2. No se considerarán fuerza mayor los conflictos laborales limitados al personal de la parte afectada, las averías de maquinaria derivadas de un mantenimiento deficiente, la falta de liquidez ni el incumplimiento de subcontratistas, salvo que estos se encuentren a su vez en situación de fuerza mayor.
{n}.3. La parte afectada lo comunicará a la otra en un plazo máximo de cuarenta y ocho horas, con indicación de la causa, la duración previsible y las medidas adoptadas. Si la situación se prolonga más de noventa días consecutivos, cualquiera de las partes podrá dar por terminada la relación sin indemnización."""

COMP = """## {n}. Integridad y cumplimiento normativo
{n}.1. Las partes declaran conocer y cumplir la normativa aplicable en materia de prevención de la corrupción, blanqueo de capitales, defensa de la competencia, control de exportaciones y derechos humanos, y disponer de medidas proporcionadas de prevención de delitos.
{n}.2. Ninguna de las partes ofrecerá, prometerá, entregará ni aceptará, directa o indirectamente, ventajas indebidas a empleados, directivos, autoridades o funcionarios públicos con el fin de obtener o conservar negocio.
{n}.3. Cada parte comunicará sin demora a la otra cualquier investigación o procedimiento que pudiera afectar a la ejecución de lo pactado. El incumplimiento grave de esta cláusula facultará a la parte cumplidora para resolver con efectos inmediatos."""

GEN = """## {n}. Disposiciones generales
{n}.1. Acuerdo completo. El presente documento, con sus anexos, recoge el acuerdo íntegro de las partes sobre su objeto y sustituye cualquier negociación, oferta o acuerdo anterior. Las condiciones generales de cualquiera de las partes no serán de aplicación aunque figuren en pedidos, albaranes o facturas.
{n}.2. Modificaciones. Toda modificación exigirá documento escrito firmado por representantes con poder suficiente de ambas partes. La tolerancia de un incumplimiento no supone renuncia ni novación.
{n}.3. Nulidad parcial. La nulidad o ineficacia de una estipulación no afectará a las restantes. Las partes negociarán de buena fe su sustitución por otra válida que se aproxime lo más posible a su finalidad económica.
{n}.4. Prelación. En caso de contradicción prevalecerá el cuerpo del documento sobre los anexos, salvo que el anexo posterior indique expresamente lo contrario.
{n}.5. Independencia. Nada de lo pactado crea sociedad, agencia, relación laboral ni mandato entre las partes, que actúan como empresarios independientes.
{n}.6. Firma. El documento se firma por duplicado y a un solo efecto. Las partes reconocen plena validez a la firma electrónica cualificada y a las copias digitalizadas de los ejemplares firmados."""

NOT = """## {n}. Notificaciones
{n}.1. Las notificaciones se realizarán por escrito y por un medio que deje constancia de su contenido y recepción, en los domicilios que figuran en la comparecencia, a la atención de las personas firmantes.
{n}.2. Las comunicaciones ordinarias de carácter operativo, como pedidos, avisos de expedición e incidencias, podrán remitirse por correo electrónico entre las personas designadas por cada parte. No tendrán este carácter las que se refieran a resolución, prórroga, modificación o reclamación de cantidades.
{n}.3. El cambio de domicilio o de persona de contacto surtirá efectos desde su notificación fehaciente a la otra parte."""

LEY = """## {n}. Ley aplicable y jurisdicción
{n}.1. El contrato se rige por la ley española. Con renuncia a cualquier otro fuero que pudiera corresponderles, las partes se someten a los juzgados y tribunales de Madrid capital para la resolución de cuantas controversias deriven de su validez, interpretación, cumplimiento o terminación.
{n}.2. Antes de acudir a la vía judicial, las partes intentarán alcanzar una solución negociada durante un plazo de treinta días desde la notificación de la controversia por escrito."""


def cola(n, *bloques):
    """Añade cláusulas generales numeradas a partir de n."""
    out = []
    for b in bloques:
        out.append(b.replace("{n}", str(n))); n += 1
    return "\n".join(out)

REP = """## {n}. Declaraciones y garantías de las partes
{n}.1. Cada parte declara que está válidamente constituida, que dispone de capacidad y poderes suficientes para obligarse y que la firma y ejecución de este documento no contraviene sus estatutos, ni pacto, resolución o norma que le resulte de aplicación.
{n}.2. Cada parte declara hallarse al corriente de sus obligaciones tributarias, laborales y de Seguridad Social, no haber solicitado ni tener intención de solicitar su declaración de concurso y no conocer procedimiento alguno que pueda comprometer de forma sustancial el cumplimiento de lo pactado.
{n}.3. Las declaraciones se entienden formuladas en la fecha de firma y mantenidas durante toda la vigencia. La parte que conozca su inexactitud sobrevenida lo comunicará a la otra en un plazo de diez días, junto con las medidas que proponga adoptar."""

AUD = """## {n}. Registros y verificación
{n}.1. Las partes conservarán la documentación acreditativa de la ejecución, de los importes facturados y de los controles realizados durante un mínimo de seis años desde su emisión, o durante el plazo superior que exija la normativa aplicable.
{n}.2. Con un preaviso de diez días hábiles, en horario ordinario y no más de una vez al año salvo indicios fundados de incumplimiento, cada parte podrá verificar, por sí o mediante un tercero independiente sujeto a secreto, los registros directamente relacionados con el objeto de este documento.
{n}.3. La verificación no comprenderá costes internos, márgenes, información de terceros ni secretos empresariales. Su coste será asumido por quien la solicite, salvo que revele una diferencia superior al 3% del importe revisado, en cuyo caso lo asumirá la parte incumplidora."""

CONT = """## {n}. Continuidad de la actividad
{n}.1. Cada parte mantendrá un plan de continuidad proporcionado a su actividad, que contemplará al menos la pérdida de instalaciones, de sistemas de información, de proveedores críticos y de personal clave, y lo revisará con periodicidad anual.
{n}.2. Cuando se produzca una interrupción que pueda afectar a la otra parte, la parte afectada activará su plan, designará un interlocutor permanente e informará de la evolución cada cuarenta y ocho horas hasta la recuperación del servicio ordinario.
{n}.3. La existencia del plan no exime del cumplimiento de las obligaciones asumidas ni amplía los supuestos de fuerza mayor."""

SOST = """## {n}. Sostenibilidad y condiciones de trabajo
{n}.1. Las partes respetarán los derechos laborales fundamentales, la prohibición del trabajo infantil y forzoso, la igualdad de trato y la normativa de prevención de riesgos, y requerirán un compromiso equivalente a los terceros que intervengan en la ejecución.
{n}.2. Cada parte gestionará sus residuos, emisiones y sustancias conforme a la legislación ambiental y facilitará a la otra la información que razonablemente precise para sus propias obligaciones de reporte, incluidos el contenido reciclado y la huella de carbono cuando disponga de ellos.
{n}.3. El incumplimiento grave y no corregido de esta cláusula en un plazo de sesenta días desde el requerimiento se considerará incumplimiento esencial."""

INT = """## {n}. Interpretación
{n}.1. Los títulos de las cláusulas se incluyen para facilitar la lectura y no afectan a su interpretación. Las referencias a una norma comprenden sus modificaciones y la que la sustituya.
{n}.2. Salvo indicación expresa de días hábiles, los plazos por días se computan en días naturales. Si el último día fuera inhábil en el lugar de cumplimiento, el plazo se entenderá prorrogado hasta el primer día hábil siguiente, salvo en los pagos, que se anticiparán al inmediato anterior.
{n}.3. Los importes se expresan en euros y, salvo mención en contrario, no incluyen los impuestos indirectos aplicables, que se repercutirán al tipo vigente en cada momento."""
