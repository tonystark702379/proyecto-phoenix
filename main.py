

from collections import deque   

TABLA_LETRAS_CODIGO = [
    # (lote_min, lote_max):  {Nivel I,   Nivel II,   Nivel III}
    ((2,        8),          {"I": "A",  "II": "A",  "III": "B"}),
    ((9,        15),         {"I": "A",  "II": "B",  "III": "C"}),
    ((16,       25),         {"I": "B",  "II": "C",  "III": "D"}),
    ((26,       50),         {"I": "C",  "II": "D",  "III": "E"}),
    ((51,       90),         {"I": "C",  "II": "E",  "III": "F"}),
    ((91,       150),        {"I": "D",  "II": "F",  "III": "G"}),
    ((151,      280),        {"I": "E",  "II": "G",  "III": "H"}),
    ((281,      500),        {"I": "F",  "II": "H",  "III": "J"}),
    ((501,      1200),       {"I": "G",  "II": "J",  "III": "K"}),
    ((1201,     3200),       {"I": "H",  "II": "K",  "III": "L"}),
    ((3201,     10000),      {"I": "J",  "II": "L",  "III": "M"}),
    ((10001,    35000),      {"I": "K",  "II": "M",  "III": "N"}),
    ((35001,    150000),     {"I": "L",  "II": "N",  "III": "P"}),
    ((150001,   500000),     {"I": "M",  "II": "P",  "III": "Q"}),
    ((500001,   float("inf"),{"I": "N",  "II": "Q",  "III": "R"})),
]


TABLA_MUESTRAS = {
    "A":  0,    # Solo inspección (lotes muy pequeños)
    "B":  3,
    "C":  5,
    "D":  8,
    "E":  13,
    "F":  20,
    "G":  32,
    "H":  50,
    "J":  80,
    "K":  125,
    "L":  200,
    "M":  315,
    "N":  500,
    "P":  800,
    "Q":  1250,
    "R":  2000,
}


cola_insumos_pendientes = deque()   # Cola vacía al iniciar el sistema


registro_diario = []   # Lista vacía al iniciar el sistema


def encolar_insumo(nombre, lote, tipo_proveedor):
    """
    FUNCIÓN DE COLA 1: Agrega un insumo al final de la cola de espera.

    Simula la llegada de un insumo a planta: se pone al final de la fila
    y espera su turno para ser inspeccionado.

    Operación usada: deque.append() → agrega al FINAL (cola FIFO)

    Parámetros:
        nombre         (str): Nombre del insumo
        lote           (int): Tamaño del lote
        tipo_proveedor (str): Tipo de proveedor
    """
    # Cada insumo se guarda como un diccionario con sus datos
    insumo = {
        "insumo":         nombre,
        "tamanio_lote":   lote,
        "tipo_proveedor": tipo_proveedor,
    }
    cola_insumos_pendientes.append(insumo)   
    print(f"  ✔ '{nombre}' encolado. Posición en fila: {len(cola_insumos_pendientes)}")


def desencolar_insumo():
    """
    FUNCIÓN DE COLA 2: Saca al primer insumo de la cola para inspeccionarlo.

    Comportamiento FIFO: siempre se atiende al que llegó primero.

    Operación usada: deque.popleft() → saca del FRENTE (cola FIFO)

    Retorna:
        dict: Datos del insumo que fue atendido, o None si la cola está vacía.
    """
    if len(cola_insumos_pendientes) == 0:
        print(" La cola está vacía. No hay insumos pendientes.")
        return None
    insumo = cola_insumos_pendientes.popleft()   
    return insumo


def mostrar_cola():
    """
    FUNCIÓN DE COLA 3: Muestra todos los insumos que están esperando en la cola.

    No elimina ningún elemento — solo permite visualizar el estado actual.
    """
    print()
    print("=" * 60)
    print("  COLA DE INSUMOS PENDIENTES DE INSPECCIÓN")
    print("=" * 60)

    if len(cola_insumos_pendientes) == 0:
        print("  La cola está vacía. No hay insumos en espera.")
    else:
        print(f"  Insumos en cola: {len(cola_insumos_pendientes)}")
        print(f"  (Se atenderán en este orden — FIFO)")
        print()
        print(f"  {'Pos':<5} {'Insumo':<22} {'Lote':>7}  {'Proveedor'}")
        print("  " + "-" * 52)


        for i, insumo in enumerate(cola_insumos_pendientes, start=1):
            print(
                f"  {i:<5} "
                f"{insumo['insumo']:<22} "
                f"{insumo['tamanio_lote']:>7}  "
                f"{insumo['tipo_proveedor']}"
            )

    print("=" * 60)


def procesar_cola_completa():
    """
    FUNCIÓN DE COLA 4: Procesa todos los insumos de la cola uno por uno.

    Vacía la cola completa, inspeccionando cada insumo en orden FIFO
    y guardando cada resultado en la lista registro_diario.
    """
    if len(cola_insumos_pendientes) == 0:
        print(" No hay insumos en la cola para procesar.")
        return

    total = len(cola_insumos_pendientes)
    print()
    print("=" * 60)
    print(f" PROCESANDO COLA — {total} insumo(s) en fila")
    print("=" * 60)

    contador = 0
    # Mientras haya insumos en la cola, los sacamos y procesamos
    while len(cola_insumos_pendientes) > 0:
        contador += 1
        # Desencolar: sacar al primero (FIFO)
        insumo = cola_insumos_pendientes.popleft()

        print(f"\n  [{contador}/{total}] Procesando: {insumo['insumo']}...")

        # Procesar el insumo con la lógica ISO 2859-1
        resultado = procesar_insumo(
            insumo["insumo"],
            insumo["tamanio_lote"],
            insumo["tipo_proveedor"]
        )

        if resultado:
            mostrar_resultado(resultado)
            # Guardar en la LISTA de registro diario
            registro_diario.append(resultado)

    print()
    print(f"  ✔ Cola procesada. {contador} insumo(s) atendido(s).")


# =============================================================================
# SECCIÓN 4: FUNCIONES DE LA LISTA (registro diario)
# =============================================================================

def mostrar_registro_diario():
    """
    FUNCIÓN DE LISTA 1: Muestra todos los insumos procesados en la sesión.

    Recorre la lista completa y muestra cada registro en formato tabla.
    Operación: recorrido con enumerate().
    """
    print()
    print("=" * 60)
    print("   REGISTRO DIARIO DE INSUMOS PROCESADOS")
    print("=" * 60)

    if len(registro_diario) == 0:
        print("  No se procesó ningún insumo en esta sesión.")
    else:
        print(f"  Total registros en lista: {len(registro_diario)}")
        print()
        print(f"  {'N°':<4} {'Insumo':<20} {'Lote':>6} {'Proveedor':<18} {'Control':<25} {'Muestras':>8}")
        print("  " + "-" * 84)

        for i, reg in enumerate(registro_diario, start=1):
            print(
                f"  {i:<4} "
                f"{reg['insumo']:<20} "
                f"{reg['tamanio_lote']:>6} "
                f"{reg['tipo_proveedor']:<18} "
                f"{reg['tipo_control']:<25} "
                f"{reg['n_muestras']:>8}"
            )

    print("=" * 60)


def buscar_en_lista_por_proveedor(tipo_proveedor):
    """
    FUNCIÓN DE LISTA 2: Busca en la lista todos los insumos de un tipo de proveedor.

    Recorre la lista y filtra los registros que coincidan con el tipo buscado.
    Operación: list comprehension con condición (filtrado).

    Parámetros:
        tipo_proveedor (str): El tipo a buscar ("nuevo", "prueba_industrial", "homologado")
    """
   
    resultados = [reg for reg in registro_diario
                  if reg["tipo_proveedor"] == tipo_proveedor]

    print()
    print(f"  Búsqueda en lista — Proveedor: '{tipo_proveedor}'")
    print(f"  Registros encontrados: {len(resultados)}")

    if resultados:
        print()
        print(f"  {'Insumo':<22} {'Lote':>7}  {'Control':<25}  {'Muestras':>8}")
        print("  " + "-" * 68)
        for reg in resultados:
            print(
                f"  {reg['insumo']:<22} "
                f"{reg['tamanio_lote']:>7}  "
                f"{reg['tipo_control']:<25}  "
                f"{reg['n_muestras']:>8}"
            )
    else:
        print(f"  No hay registros con tipo de proveedor '{tipo_proveedor}'.")


def filtrar_lista_por_control(tipo_control):
    """
    FUNCIÓN DE LISTA 3: Filtra la lista por tipo de control aplicado.

    Separa los insumos que requirieron solo INSPECCIÓN de los que
    requirieron INSPECCIÓN + MUESTREO.
    Operación: list comprehension con condición (filtrado).

    Parámetros:
        tipo_control (str): "SOLO INSPECCIÓN" o "INSPECCIÓN + MUESTREO"
    """
    filtrados = [reg for reg in registro_diario
                 if reg["tipo_control"] == tipo_control]

    print()
    print(f"  Filtro en lista — Control: '{tipo_control}'")
    print(f"  Insumos que aplican este control: {len(filtrados)}")

    if filtrados:
        for reg in filtrados:
            print(f"    • {reg['insumo']} (lote: {reg['tamanio_lote']}, "
                  f"proveedor: {reg['tipo_proveedor']}, "
                  f"muestras: {reg['n_muestras']})")


def ordenar_lista_por_lote():
    """
    FUNCIÓN DE LISTA 4: Muestra la lista ordenada por tamaño de lote (mayor a menor).

    No modifica el registro_diario original — crea una copia ordenada.
    Operación: sorted() con key= y reverse=True.
    """
    if len(registro_diario) == 0:
        print(" La lista de registros está vacía.")
        return

    lista_ordenada = sorted(registro_diario,
                            key=lambda reg: reg["tamanio_lote"],
                            reverse=True)   # De mayor a menor lote

    print()
    print(" LISTA ORDENADA POR TAMAÑO DE LOTE (mayor → menor)")
    print(f"  {'Pos':<5} {'Insumo':<22} {'Lote':>8}  {'Proveedor':<18}  {'Control'}")
    print("  " + "-" * 75)

    for i, reg in enumerate(lista_ordenada, start=1):
        print(
            f"  {i:<5} "
            f"{reg['insumo']:<22} "
            f"{reg['tamanio_lote']:>8}  "
            f"{reg['tipo_proveedor']:<18}  "
            f"{reg['tipo_control']}"
        )


def resumen_estadistico_lista():
    """
    FUNCIÓN DE LISTA 5: Genera un resumen estadístico del registro diario.

    Calcula totales, promedios y conteos usando operaciones sobre la lista.
    Operaciones: len(), sum(), max(), min(), list comprehension para conteo.
    """
    print()
    print("=" * 60)
    print(" RESUMEN ESTADÍSTICO DEL REGISTRO DIARIO")
    print("=" * 60)

    if len(registro_diario) == 0:
        print("  No hay datos para generar el resumen.")
        print("=" * 60)
        return

    total = len(registro_diario)

    # Conteos por tipo de control (usando list comprehension)
    solo_inspeccion   = len([r for r in registro_diario if r["tipo_control"] == "SOLO INSPECCIÓN"])
    con_muestreo      = len([r for r in registro_diario if r["tipo_control"] == "INSPECCIÓN + MUESTREO"])

    # Conteos por tipo de proveedor
    nuevos        = len([r for r in registro_diario if r["tipo_proveedor"] == "nuevo"])
    en_prueba     = len([r for r in registro_diario if r["tipo_proveedor"] == "prueba_industrial"])
    homologados   = len([r for r in registro_diario if r["tipo_proveedor"] == "homologado"])

    # Estadísticas de lotes
    lotes = [r["tamanio_lote"] for r in registro_diario]
    lote_max = max(lotes)
    lote_min = min(lotes)
    lote_prom = sum(lotes) / total

    # Estadísticas de muestras (solo los que tienen muestreo)
    muestras = [r["n_muestras"] for r in registro_diario if r["n_muestras"] > 0]
    total_muestras = sum(muestras) if muestras else 0

    print(f"  Total de insumos procesados   : {total}")
    print()
    print(f"  Por tipo de control:")
    print(f"    Solo inspección             : {solo_inspeccion}")
    print(f"    Inspección + Muestreo       : {con_muestreo}")
    print()
    print(f"  Por tipo de proveedor:")
    print(f"    Nuevos                      : {nuevos}")
    print(f"    En prueba industrial        : {en_prueba}")
    print(f"    Homologados                 : {homologados}")
    print()
    print(f"  Estadísticas de lotes:")
    print(f"    Lote más grande             : {lote_max} unidades")
    print(f"    Lote más pequeño            : {lote_min} unidades")
    print(f"    Promedio de lote            : {lote_prom:.1f} unidades")
    print()
    print(f"  Total de muestras a tomar     : {total_muestras}")
    print("=" * 60)


# =============================================================================
# SECCIÓN 5: FUNCIONES DE PROCESAMIENTO (lógica ISO 2859-1)
# =============================================================================

def obtener_letra_codigo(tamanio_lote, nivel_inspeccion):
    """
    Busca la letra código en la Tabla 1 de la ISO 2859-1.

    Parámetros:
        tamanio_lote     (int): Número de unidades del lote recibido.
        nivel_inspeccion (str): Nivel de inspección: "I", "II" o "III".

    Retorna:
        str: La letra código correspondiente (ej: "A", "B", ..., "R").
             Retorna None si el lote está fuera del rango definido.
    """
    for (lote_min, lote_max), niveles in TABLA_LETRAS_CODIGO:
        if lote_min <= tamanio_lote <= lote_max:
            return niveles[nivel_inspeccion]
    return None


def obtener_numero_muestras(letra_codigo):
    """
    Obtiene el número de muestras a tomar según la Tabla 2 de la ISO 2859-1.

    Parámetros:
        letra_codigo (str): La letra código obtenida de la Tabla 1.

    Retorna:
        int: Número de muestras (0 = solo inspección, sin muestreo).
    """
    return TABLA_MUESTRAS.get(letra_codigo, 0)


def determinar_nivel_inspeccion(tipo_proveedor):
    """
    Determina el nivel de inspección según el tipo de proveedor (ISO 2859-1).

    Parámetros:
        tipo_proveedor (str): "nuevo", "prueba_industrial" u "homologado"

    Retorna:
        tuple: (nivel, descripcion)
    """
    niveles = {
        "nuevo":             ("III", "Reforzado  - Proveedor nuevo sin historial"),
        "prueba_industrial":  ("II",  "Normal     - Proveedor en evaluación"),
        "homologado":         ("I",   "Reducido   - Proveedor con historial confirmado"),
    }
    return niveles.get(tipo_proveedor, (None, "Tipo de proveedor no reconocido"))


def procesar_insumo(nombre_insumo, tamanio_lote, tipo_proveedor):
    """
    Función principal de procesamiento: aplica la lógica ISO 2859-1
    para determinar el tipo de control de calidad del insumo.

    Parámetros:
        nombre_insumo  (str): Nombre del insumo
        tamanio_lote   (int): Tamaño del lote recibido
        tipo_proveedor (str): Tipo de proveedor

    Retorna:
        dict: Resultado completo del análisis, o None si hay error.
    """
    # Paso 1: Nivel de inspección según tipo de proveedor
    nivel, descripcion_nivel = determinar_nivel_inspeccion(tipo_proveedor)
    if nivel is None:
        print(f" ERROR: Tipo de proveedor '{tipo_proveedor}' no reconocido.")
        return None

    # Paso 2: Letra código desde Tabla 1
    letra_codigo = obtener_letra_codigo(tamanio_lote, nivel)
    if letra_codigo is None:
        print(f" ERROR: Tamaño de lote {tamanio_lote} fuera de rango.")
        return None

    # Paso 3: Número de muestras desde Tabla 2
    n_muestras = obtener_numero_muestras(letra_codigo)

    # Paso 4: Tipo de control
    if n_muestras == 0:
        tipo_control = "SOLO INSPECCIÓN"
        detalle = "Revisión documental e inspección física. No se requiere muestreo."
    else:
        tipo_control = "INSPECCIÓN + MUESTREO"
        detalle = f"Se deben tomar {n_muestras} muestras para análisis de laboratorio."

    resultado = {
        "insumo":           nombre_insumo,
        "tamanio_lote":     tamanio_lote,
        "tipo_proveedor":   tipo_proveedor,
        "nivel_inspeccion": f"Nivel {nivel} - {descripcion_nivel}",
        "letra_codigo":     letra_codigo,
        "n_muestras":       n_muestras,
        "tipo_control":     tipo_control,
        "detalle":          detalle,
    }
    return resultado


def mostrar_resultado(resultado):
    """
    Muestra en pantalla el resultado del procesamiento de un insumo.
    """
    print()
    print("-" * 60)
    print(" RESULTADO DEL ANÁLISIS")
    print("-" * 60)
    print(f"  Insumo          : {resultado['insumo']}")
    print(f"  Tamaño de lote  : {resultado['tamanio_lote']} unidades")
    print(f"  Tipo proveedor  : {resultado['tipo_proveedor']}")
    print(f"  Nivel inspección: {resultado['nivel_inspeccion']}")
    print(f"  Letra código    : {resultado['letra_codigo']} (ISO 2859-1, Tabla 1)")
    print()

    if resultado["n_muestras"] == 0:
        print(" CONTROL APLICABLE: SOLO INSPECCIÓN")
        print(f"  → {resultado['detalle']}")
    else:
        print(" CONTROL APLICABLE: INSPECCIÓN + MUESTREO")
        print(f"  → Número de muestras requeridas: {resultado['n_muestras']}")
        print(f"  → {resultado['detalle']}")

    print("-" * 60)


def ingresar_insumo_manual():
    """
    Solicita los datos de un insumo al usuario con validaciones.

    Retorna:
        tuple: (nombre, lote, tipo_proveedor)
    """
    print()
    print("  Ingrese los datos del insumo:")

    while True:
        nombre = input("  Nombre del insumo       : ").strip()
        if nombre:
            break
        print(" El nombre no puede estar vacío.")

    while True:
        try:
            lote = int(input("  Tamaño del lote (unid.) : "))
            if lote >= 2:
                break
            else:
                print(" El lote debe ser de al menos 2 unidades.")
        except ValueError:
            print(" Ingrese un número entero válido.")

    tipos_validos = ["nuevo", "prueba_industrial", "homologado"]
    print("  Tipos válidos: nuevo | prueba_industrial | homologado")
    while True:
        tipo = input("  Tipo de proveedor       : ").strip().lower()
        if tipo in tipos_validos:
            break
        print(f" Opciones válidas: {', '.join(tipos_validos)}")

    return nombre, lote, tipo


# =============================================================================
# SECCIÓN 6: CASOS DE PRUEBA PREDEFINIDOS
# =============================================================================
# Estos casos simulan situaciones reales de la planta Gloria S.A.
# Se usan para poblar la cola y demostrar el flujo completo del sistema.

CASOS_DE_PRUEBA = [
    # (nombre_insumo,          tamanio_lote,  tipo_proveedor)
    ("Leche en polvo",          500,           "nuevo"),
    ("Azucar refinada",         1500,          "prueba_industrial"),
    ("Envases tetra brik",      10000,         "homologado"),
    ("Cultivo lactico",         20,            "nuevo"),
    ("Estabilizante E471",      300,           "prueba_industrial"),
    ("Sal yodada",              800,           "homologado"),
]


# =============================================================================
# SECCIÓN 7: SUBMENÚS
# =============================================================================

def submenu_cola():
    """
    Submenú dedicado a las operaciones de la COLA de insumos pendientes.
    """
    while True:
        print()
        print("  ┌─────────────────────────────────────────┐")
        print("  │        GESTIÓN DE COLA (FIFO)           │")
        print("  ├─────────────────────────────────────────┤")
        print("  │  1. Encolar un insumo manualmente       │")
        print("  │  2. Cargar casos de prueba a la cola    │")
        print("  │  3. Ver cola actual (insumos en espera) │")
        print("  │  4. Procesar toda la cola               │")
        print("  │  5. Volver al menú principal            │")
        print("  └─────────────────────────────────────────┘")
        print()

        opcion = input("  Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            nombre, lote, tipo = ingresar_insumo_manual()
            encolar_insumo(nombre, lote, tipo)
            input("\n  Presione ENTER para continuar...")

        elif opcion == "2":
            print()
            print(f"  Cargando {len(CASOS_DE_PRUEBA)} casos de prueba a la cola...")
            for nombre, lote, tipo in CASOS_DE_PRUEBA:
                encolar_insumo(nombre, lote, tipo)
            print(f"\n  Cola cargada. Total en fila: {len(cola_insumos_pendientes)}")
            input("\n  Presione ENTER para continuar...")

        elif opcion == "3":
            mostrar_cola()
            input("\n  Presione ENTER para continuar...")

        elif opcion == "4":
            procesar_cola_completa()
            input("\n  Presione ENTER para continuar...")

        elif opcion == "5":
            break

        else:
            print(" Opción no válida. Intente nuevamente.")


def submenu_lista():
    """
    Submenú dedicado a las operaciones de la LISTA (registro diario).
    """
    while True:
        print()
        print("  ┌──────────────────────────────────────────────┐")
        print("  │       GESTIÓN DE LISTA (REGISTRO DIARIO)     │")
        print("  ├──────────────────────────────────────────────┤")
        print("  │  1. Ver registro completo                    │")
        print("  │  2. Buscar por tipo de proveedor             │")
        print("  │  3. Filtrar por tipo de control              │")
        print("  │  4. Ver lista ordenada por tamaño de lote    │")
        print("  │  5. Resumen estadístico                      │")
        print("  │  6. Volver al menú principal                 │")
        print("  └──────────────────────────────────────────────┘")
        print()

        opcion = input("  Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            mostrar_registro_diario()
            input("\n  Presione ENTER para continuar...")

        elif opcion == "2":
            tipos_validos = ["nuevo", "prueba_industrial", "homologado"]
            print(f"  Opciones: {', '.join(tipos_validos)}")
            tipo = input("  Tipo de proveedor a buscar: ").strip().lower()
            buscar_en_lista_por_proveedor(tipo)
            input("\n  Presione ENTER para continuar...")

        elif opcion == "3":
            print("  Opciones: SOLO INSPECCIÓN | INSPECCIÓN + MUESTREO")
            ctrl = input("  Tipo de control a filtrar: ").strip().upper()
            filtrar_lista_por_control(ctrl)
            input("\n  Presione ENTER para continuar...")

        elif opcion == "4":
            ordenar_lista_por_lote()
            input("\n  Presione ENTER para continuar...")

        elif opcion == "5":
            resumen_estadistico_lista()
            input("\n  Presione ENTER para continuar...")

        elif opcion == "6":
            break

        else:
            print(" Opción no válida. Intente nuevamente.")


# =============================================================================
# SECCIÓN 8: MENÚ PRINCIPAL
# =============================================================================

def mostrar_bienvenida():
    """Muestra el encabezado del sistema."""
    print("=" * 60)
    print("   SISTEMA DE INSPECCIÓN DE INSUMOS - GLORIA S.A.")
    print("   Basado en la Norma ISO 2859-1 / NTP-ISO 2859-1")
    print("=" * 60)
    print()
    print("  Estructuras de datos activas:")
    print("  • COLA  : insumos pendientes de inspección")
    print("  • LISTA : registro histórico de insumos procesados")
    print()


def menu_principal():
    """
    Menú principal del sistema. Gestiona la navegación entre módulos.
    """
    mostrar_bienvenida()

    while True:
        print()
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║           MENÚ PRINCIPAL                         ║")
        print("  ╠══════════════════════════════════════════════════╣")
        print(f"   Cola: {len(cola_insumos_pendientes)} pendiente(s) │ Lista: {len(registro_diario)} procesado(s)".ljust(51))
        print("  ╠══════════════════════════════════════════════════╣")
        print("  ║  1. Gestionar COLA de insumos (FIFO)             ║")
        print("  ║  2. Consultar LISTA (registro diario)            ║")
        print("  ║  3. Salir del sistema                            ║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()

        opcion = input("  Seleccione una opción (1-3): ").strip()
 
        if opcion == "1":
            submenu_cola()

        elif opcion == "2":
            submenu_lista()

        elif opcion == "3":
            print()
            print("  Generando resumen final de la sesión...")
            resumen_estadistico_lista()
            print()
            print("  Sistema cerrado. ¡Hasta luego!")
            print("=" * 60)
            break

        else:
            print(" Opción no válida. Ingrese 1, 2 o 3.")


# =============================================================================
# SECCIÓN 9: PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    menu_principal()