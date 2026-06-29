#### parte 4


# =============================================================================
# SECCION 11: CLASE PRINCIPAL DEL SISTEMA
# Unidad 3 - Relaciones entre clases (composicion y dependencia)
# SistemaInspeccion TIENE UNA ColaInsumos
# SistemaInspeccion TIENE UN RegistroDiario
# SistemaInspeccion USA UN MotorISO28591
# =============================================================================

class SistemaInspeccionGloria:
    """
    Clase principal que orquesta todo el sistema.
    Gestiona la cola de insumos, el motor ISO y el registro diario.
    """

    CASOS_PRUEBA = [
        ("Leche en polvo",      500,   "nuevo"),
        ("Azucar refinada",     1500,  "prueba_industrial"),
        ("Envases tetra brik",  10000, "homologado"),
        ("Cultivo lactico",     20,    "nuevo"),
        ("Estabilizante E471",  300,   "prueba_industrial"),
        ("Sal yodada",          800,   "homologado"),
    ]

    def __init__(self):
        self._cola    = ColaInsumos()
        self._registro= RegistroDiario()
        self._motor   = MotorISO28591()

    # ── operaciones de cola ───────────────────────────────────────────────
    def encolar_insumo(self, nombre: str, lote: int, tipo: str):
        try:
            insumo = Insumo(nombre, lote, tipo)
            self._cola.encolar(insumo)
            if insumo.es_critico():
                print(f"  ALERTA: '{nombre}' es un insumo critico (nuevo, lote > 500).")
        except (LoteInvalidoError, ProveedorInvalidoError, ValueError) as e:
            print(f"  Error al encolar: {e}")

    def cargar_casos_prueba(self):
        print(f"  Cargando {len(self.CASOS_PRUEBA)} casos de prueba...")
        for nombre, lote, tipo in self.CASOS_PRUEBA:
            self.encolar_insumo(nombre, lote, tipo)
        print(f"  Cola lista. Total en fila: {len(self._cola)}")

    def mostrar_cola(self):
        self._cola.mostrar()

    def procesar_cola_completa(self):
        if self._cola.esta_vacia():
            print("  No hay insumos en la cola.")
            return
        total = len(self._cola)
        print()
        print("=" * 60)
        print(f"   PROCESANDO COLA - {total} insumo(s)")
        print("=" * 60)
        contador = 0
        while not self._cola.esta_vacia():
            contador += 1
            try:
                insumo    = self._cola.desencolar()
                resultado = self._motor.procesar(insumo)
                self._registro.agregar(resultado)
                print(f"\n  [{contador}/{total}] {insumo.nombre}")
                self._mostrar_resultado(resultado)
            except ColaVaciaError as e:
                print(f"  {e}")
                break
            except RuntimeError as e:
                print(f"  Error de procesamiento: {e}")
        print(f"\n  Cola procesada. {contador} insumo(s) atendido(s).")

    def _mostrar_resultado(self, resultado: ResultadoInspeccion):
        r = resultado
        print(f"  Nivel    : {r.insumo.proveedor.nivel} - {r.insumo.proveedor.descripcion_nivel}")
        print(f"  Letra    : {r.letra_codigo} (ISO 2859-1 Tabla 1)")
        if r.n_muestras == 0:
            print(f"  Control  : SOLO INSPECCION")
        else:
            print(f"  Control  : INSPECCION + MUESTREO")
            print(f"  Muestras : {r.n_muestras}")
        if r.insumo.es_critico():
            print(f"  CRITICO  : SI - requiere atencion prioritaria")
        print("  " + "-" * 50)

    # ── operaciones de lista ──────────────────────────────────────────────
    def mostrar_registro(self):
        self._registro.mostrar_completo()

    def buscar_por_proveedor(self, tipo: str):
        try:
            resultados = self._registro.buscar_por_proveedor(tipo)
            print(f"\n  Busqueda por proveedor '{tipo}': {len(resultados)} resultado(s)")
            if resultados:
                print(f"  {'Insumo':<22} {'Lote':>7}  {'Control':<22}  {'Muestras'}")
                print("  " + "-" * 62)
                for r in resultados:
                    print(f"  {r.insumo.nombre:<22} {r.insumo.tamanio_lote:>7}  "
                          f"{r.tipo_control:<22}  {r.n_muestras}")
            if not resultados:
                print(f"  No hay registros con proveedor '{tipo}'.")
            # polimorfismo: el proveedor da su propia recomendacion
            proveedor = crear_proveedor(tipo)
            print(f"\n  Recomendacion: {proveedor.get_recomendacion()}")
        except ProveedorInvalidoError as e:
            print(f"  Error: {e}")

    def filtrar_por_control(self, tipo_control: str):
        resultados = self._registro.filtrar_por_control(tipo_control)
        print(f"\n  Filtro '{tipo_control}': {len(resultados)} insumo(s)")
        for r in resultados:
            print(f"  - {r.insumo.nombre} (lote: {r.insumo.tamanio_lote}, "
                  f"muestras: {r.n_muestras})")

    def mostrar_ordenado_por_lote(self):
        if self._registro.esta_vacio():
            print("  El registro esta vacio.")
            return
        ordenados = self._registro.ordenar_por_lote()
        print(f"\n  Lista ordenada por lote (mayor a menor):")
        print(f"  {'Pos':<5} {'Insumo':<22} {'Lote':>8}  {'Proveedor':<18}  {'Control'}")
        print("  " + "-" * 72)
        for i, r in enumerate(ordenados, start=1):
            print(f"  {i:<5} {r.insumo.nombre:<22} {r.insumo.tamanio_lote:>8}  "
                  f"{r.insumo.proveedor.tipo:<18}  {r.tipo_control}")

    def buscar_insumo_por_nombre(self, nombre: str):
        try:
            resultado = self._registro.buscar_por_nombre(nombre)
            print(f"\n  Insumo encontrado:")
            print(f"  {resultado.insumo.get_descripcion()}")
            print(f"  Control : {resultado.tipo_control}")
            print(f"  Detalle : {resultado.get_detalle()}")
        except InsumoNoEncontradoError as e:
            print(f"  {e}")

    def mostrar_estadisticas(self):
        self._registro.mostrar_estadisticas()

    # ── propiedades para el menu ──────────────────────────────────────────
    @property
    def n_pendientes(self) -> int:
        return len(self._cola)

    @property
    def n_procesados(self) -> int:
        return len(self._registro)



# =============================================================================
# SECCION 12: MENUS
# =============================================================================

def ingresar_insumo_manual() -> tuple:
    print()
    while True:
        nombre = input("  Nombre del insumo       : ").strip()
        if nombre:
            break
        print("  El nombre no puede estar vacio.")
    while True:
        try:
            lote = int(input("  Tamano del lote (unid.) : "))
            if lote >= 2:
                break
            print("  El lote debe ser al menos 2.")
        except ValueError:
            print("  Ingrese un numero entero valido.")
    print("  Tipos validos: nuevo | prueba_industrial | homologado")
    while True:
        tipo = input("  Tipo de proveedor       : ").strip().lower()
        if tipo in Proveedor.TIPOS_VALIDOS:
            break
        print(f"  Opciones validas: {', '.join(Proveedor.TIPOS_VALIDOS)}")
    return nombre, lote, tipo


def submenu_cola(sistema: SistemaInspeccionGloria):
    while True:
        print()
        print("  GESTION DE COLA (FIFO)")
        print("  1. Encolar insumo manualmente")
        print("  2. Cargar casos de prueba")
        print("  3. Ver cola actual")
        print("  4. Procesar toda la cola")
        print("  5. Volver")
        opcion = input("\n  Opcion: ").strip()
        if opcion == "1":
            try:
                nombre, lote, tipo = ingresar_insumo_manual()
                sistema.encolar_insumo(nombre, lote, tipo)
            except Exception as e:
                print(f"  Error inesperado: {e}")
        elif opcion == "2":
            sistema.cargar_casos_prueba()
        elif opcion == "3":
            sistema.mostrar_cola()
        elif opcion == "4":
            sistema.procesar_cola_completa()
        elif opcion == "5":
            break
        else:
            print("  Opcion no valida.")
        input("\n  ENTER para continuar...")


def submenu_lista(sistema: SistemaInspeccionGloria):
    while True:
        print()
        print("  GESTION DE LISTA (REGISTRO DIARIO)")
        print("  1. Ver registro completo")
        print("  2. Buscar por tipo de proveedor")
        print("  3. Filtrar por tipo de control")
        print("  4. Ver lista ordenada por lote")
        print("  5. Buscar insumo por nombre")
        print("  6. Resumen estadistico")
        print("  7. Volver")
        opcion = input("\n  Opcion: ").strip()
        if opcion == "1":
            sistema.mostrar_registro()
        elif opcion == "2":
            print("  Opciones: nuevo | prueba_industrial | homologado")
            tipo = input("  Tipo a buscar: ").strip().lower()
            sistema.buscar_por_proveedor(tipo)
        elif opcion == "3":
            print("  Opciones: SOLO INSPECCION | INSPECCION + MUESTREO")
            ctrl = input("  Control a filtrar: ").strip()
            sistema.filtrar_por_control(ctrl)
        elif opcion == "4":
            sistema.mostrar_ordenado_por_lote()
        elif opcion == "5":
            nombre = input("  Nombre del insumo: ").strip()
            sistema.buscar_insumo_por_nombre(nombre)
        elif opcion == "6":
            sistema.mostrar_estadisticas()
        elif opcion == "7":
            break
        else:
            print("  Opcion no valida.")
        input("\n  ENTER para continuar...")


def menu_principal():
    print("=" * 60)
    print("   SISTEMA DE INSPECCION DE INSUMOS - GLORIA S.A.")
    print("   Norma ISO 2859-1 / NTP-ISO 2859-1")
    print("   Version 3 - Programacion Orientada a Objetos")
    print("=" * 60)

    sistema = SistemaInspeccionGloria()

    while True:
        print()
        print(f"  Cola: {sistema.n_pendientes} pendiente(s) | "
              f"Lista: {sistema.n_procesados} procesado(s)")
        print()
        print("  1. Gestionar COLA de insumos (FIFO)")
        print("  2. Consultar LISTA (registro diario)")
        print("  3. Salir")

        opcion = input("\n  Opcion: ").strip()

        if opcion == "1":
            submenu_cola(sistema)
        elif opcion == "2":
            submenu_lista(sistema)
        elif opcion == "3":
            print()
            print("  Resumen final de la sesion:")
            sistema.mostrar_estadisticas()
            print("  Sistema cerrado.")
            print("=" * 60)
            break
        else:
            print("  Opcion no valida.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if _name_ == "_main_":
    menu_principal()


    