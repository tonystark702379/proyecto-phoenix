
### PARTE - 1

from collections import deque
from abc import ABC, abstractmethod

# =============================================================================
# SISTEMA DE INSPECCION DE INSUMOS - GLORIA S.A.
# Version 3 - Programacion Orientada a Objetos
# Norma ISO 2859-1 / NTP-ISO 2859-1
# Curso: Fundamentos de Programacion 2
# Temas: Clases y Objetos, Herencia, Polimorfismo, Clases Abstractas,
#        Relaciones entre Clases, Manejo de Excepciones, Listas, Tuplas, Cadenas
# =============================================================================


# =============================================================================
# SECCION 1: EXCEPCIONES PERSONALIZADAS
# Unidad 4 - Manejo de excepciones
# =============================================================================

class LoteInvalidoError(Exception):
    def __init__(self, lote):
        super().__init__(f"Tamano de lote invalido: {lote}. Debe ser mayor o igual a 2.")
        self.lote = lote

class ProveedorInvalidoError(Exception):
    def __init__(self, tipo):
        super().__init__(f"Tipo de proveedor no reconocido: '{tipo}'.")
        self.tipo = tipo

class ColaVaciaError(Exception):
    def __init__(self):
        super().__init__("La cola esta vacia. No hay insumos pendientes.")

class InsumoNoEncontradoError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Insumo '{nombre}' no encontrado en el registro.")
        self.nombre = nombre


# =============================================================================
# SECCION 2: TABLAS ISO 2859-1
# Unidad 1 - Tuplas y listas
# =============================================================================

TABLA_LETRAS_CODIGO = [
    ((2,      8),          {"I": "A",  "II": "A",  "III": "B"}),
    ((9,      15),         {"I": "A",  "II": "B",  "III": "C"}),
    ((16,     25),         {"I": "B",  "II": "C",  "III": "D"}),
    ((26,     50),         {"I": "C",  "II": "D",  "III": "E"}),
    ((51,     90),         {"I": "C",  "II": "E",  "III": "F"}),
    ((91,     150),        {"I": "D",  "II": "F",  "III": "G"}),
    ((151,    280),        {"I": "E",  "II": "G",  "III": "H"}),
    ((281,    500),        {"I": "F",  "II": "H",  "III": "J"}),
    ((501,    1200),       {"I": "G",  "II": "J",  "III": "K"}),
    ((1201,   3200),       {"I": "H",  "II": "K",  "III": "L"}),
    ((3201,   10000),      {"I": "J",  "II": "L",  "III": "M"}),
    ((10001,  35000),      {"I": "K",  "II": "M",  "III": "N"}),
    ((35001,  150000),     {"I": "L",  "II": "N",  "III": "P"}),
    ((150001, 500000),     {"I": "M",  "II": "P",  "III": "Q"}),
    ((500001, float("inf"),{"I": "N",  "II": "Q",  "III": "R"})),
]

TABLA_MUESTRAS = {
    "A": 0, "B": 3,  "C": 5,   "D": 8,   "E": 13,
    "F": 20,"G": 32, "H": 50,  "J": 80,  "K": 125,
    "L": 200,"M": 315,"N": 500, "P": 800, "Q": 1250, "R": 2000,
}


# =============================================================================
# SECCION 3: CLASE ABSTRACTA BASE
# Unidad 2 - Clases abstractas e interfaces
# =============================================================================

class EntidadInspeccionable(ABC):
    """
    Clase abstracta base que define el contrato que deben cumplir
    todos los elementos que pueden ser inspeccionados en el sistema.
    Cualquier clase que herede de esta DEBE implementar los metodos abstractos.
    """

    @abstractmethod
    def get_descripcion(self) -> str:
        pass

    @abstractmethod
    def get_nivel_inspeccion(self) -> str:
        pass

    @abstractmethod
    def es_critico(self) -> bool:
        pass


# =============================================================================
# SECCION 4: CLASE PROVEEDOR
# Unidad 1 - Clases y objetos
# =============================================================================

class Proveedor:
    """
    Representa a un proveedor de insumos de Gloria S.A.
    Encapsula el tipo y el nivel de inspeccion que le corresponde
    segun la norma ISO 2859-1.
    Relacion: un Insumo TIENE UN Proveedor (composicion).
    """

    TIPOS_VALIDOS = ("nuevo", "prueba_industrial", "homologado")

    NIVELES = {
        "nuevo":            ("III", "Reforzado  - Sin historial de calidad"),
        "prueba_industrial": ("II",  "Normal     - En evaluacion"),
        "homologado":       ("I",   "Reducido   - Historial verificado"),
    }

    def __init__(self, tipo: str):
        tipo = tipo.strip().lower()
        if tipo not in self.TIPOS_VALIDOS:
            raise ProveedorInvalidoError(tipo)
        self._tipo = tipo
        self._nivel, self._descripcion = self.NIVELES[tipo]

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def nivel(self) -> str:
        return self._nivel

    @property
    def descripcion_nivel(self) -> str:
        return self._descripcion

    def __str__(self) -> str:
        return f"{self._tipo.capitalize()} (Nivel {self._nivel} - {self._descripcion})"


### PARTE - 2

# =============================================================================
#SECCION 5: CLASE INSUMO (hereda de EntidadInspeccionable)
# Unidad 1 y 2 - Clases, objetos, herencia
# =============================================================================

class Insumo(EntidadInspeccionable):
    """
    Representa un insumo que llega a la planta de Gloria S.A.
    Hereda de EntidadInspeccionable e implementa sus metodos abstractos.
    Relacion de composicion con Proveedor: un Insumo TIENE UN Proveedor.
    """

    def __init__(self, nombre: str, tamanio_lote: int, tipo_proveedor: str):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del insumo no puede estar vacio.")
        if tamanio_lote < 2:
            raise LoteInvalidoError(tamanio_lote)

        self._nombre       = nombre
        self._tamanio_lote = tamanio_lote
        self._proveedor    = Proveedor(tipo_proveedor)   # composicion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tamanio_lote(self) -> int:
        return self._tamanio_lote

    @property
    def proveedor(self) -> Proveedor:
        return self._proveedor

    # Implementacion de metodos abstractos
    def get_descripcion(self) -> str:
        return (f"Insumo: {self._nombre} | "
                f"Lote: {self._tamanio_lote} unidades | "
                f"Proveedor: {self._proveedor.tipo}")

    def get_nivel_inspeccion(self) -> str:
        return self._proveedor.nivel

    def es_critico(self) -> bool:
        return self._proveedor.tipo == "nuevo" and self._tamanio_lote > 500

    def __str__(self) -> str:
        return f"{self._nombre} (lote={self._tamanio_lote}, proveedor={self._proveedor.tipo})"


# =============================================================================
# SECCION 6: CLASE RESULTADO DE INSPECCION
# Unidad 1 - Clases y objetos
# Unidad 3 - Relaciones entre clases (Resultado USA UN Insumo)
# =============================================================================

class ResultadoInspeccion:
    """
    Encapsula el resultado completo del analisis de un insumo
    segun la norma ISO 2859-1.
    Relacion de dependencia: ResultadoInspeccion USA UN Insumo.
    """

    def __init__(self, insumo: Insumo, letra_codigo: str, n_muestras: int):
        self._insumo       = insumo
        self._letra_codigo = letra_codigo
        self._n_muestras   = n_muestras
        self._tipo_control = "SOLO INSPECCION" if n_muestras == 0 else "INSPECCION + MUESTREO"

    @property
    def insumo(self) -> Insumo:
        return self._insumo

    @property
    def letra_codigo(self) -> str:
        return self._letra_codigo

    @property
    def n_muestras(self) -> int:
        return self._n_muestras

    @property
    def tipo_control(self) -> str:
        return self._tipo_control

    def get_detalle(self) -> str:
        if self._n_muestras == 0:
            return "Revision documental e inspeccion fisica. No se requiere muestreo."
        return f"Se deben tomar {self._n_muestras} muestras para analisis de laboratorio."

    def to_dict(self) -> dict:
        return {
            "insumo":           self._insumo.nombre,
            "tamanio_lote":     self._insumo.tamanio_lote,
            "tipo_proveedor":   self._insumo.proveedor.tipo,
            "nivel_inspeccion": f"Nivel {self._insumo.proveedor.nivel} - {self._insumo.proveedor.descripcion_nivel}",
            "letra_codigo":     self._letra_codigo,
            "n_muestras":       self._n_muestras,
            "tipo_control":     self._tipo_control,
            "es_critico":       self._insumo.es_critico(),
        }

    def __str__(self) -> str:
        return (f"{self._insumo.nombre} -> {self._tipo_control} "
                f"(letra={self._letra_codigo}, muestras={self._n_muestras})")


# =============================================================================
# SECCION 7: CLASES DE PROVEEDOR CON HERENCIA Y POLIMORFISMO
# Unidad 2 - Herencia y polimorfismo
# =============================================================================

class ProveedorNuevo(Proveedor):
    """
    Proveedor nuevo sin historial. Hereda de Proveedor.
    Sobreescribe get_descripcion para comportamiento especifico.
    """
    def __init__(self):
        super().__init__("nuevo")

    def get_recomendacion(self) -> str:
        return "Aplicar inspeccion completa. Solicitar certificados de calidad al proveedor."


class ProveedorPrueba(Proveedor):
    """
    Proveedor en etapa de prueba industrial. Hereda de Proveedor.
    """
    def __init__(self):
        super().__init__("prueba_industrial")

    def get_recomendacion(self) -> str:
        return "Mantener seguimiento. Evaluar conformidad para posible homologacion."


class ProveedorHomologado(Proveedor):
    """
    Proveedor homologado con historial verificado. Hereda de Proveedor.
    """
    def __init__(self):
        super().__init__("homologado")

    def get_recomendacion(self) -> str:
        return "Inspeccion reducida. Mantener actualizados los registros de conformidad."


def crear_proveedor(tipo: str) -> Proveedor:
    """
    Polimorfismo: devuelve la subclase correcta segun el tipo.
    El codigo que llama a esta funcion no necesita saber que subclase recibe.
    """
    tipo = tipo.strip().lower()
    if tipo == "nuevo":
        return ProveedorNuevo()
    elif tipo == "prueba_industrial":
        return ProveedorPrueba()
    elif tipo == "homologado":
        return ProveedorHomologado()
    else:
        raise ProveedorInvalidoError(tipo)



### PARTE - 3

# =============================================================================
#SECCION 8: CLASE MOTOR ISO 2859-1
# Unidad 1 - Clases y objetos
# Unidad 3 - Relaciones: SistemaInspeccion USA Motor ISO
# =============================================================================

class MotorISO28591:
    """
    Encapsula toda la logica de la norma ISO 2859-1.
    Determina la letra codigo y el numero de muestras para un insumo dado.
    """

    @staticmethod
    def obtener_letra_codigo(tamanio_lote: int, nivel: str) -> str:
        for (lote_min, lote_max), niveles in TABLA_LETRAS_CODIGO:
            if lote_min <= tamanio_lote <= lote_max:
                return niveles[nivel]
        raise LoteInvalidoError(tamanio_lote)

    @staticmethod
    def obtener_n_muestras(letra: str) -> int:
        return TABLA_MUESTRAS.get(letra, 0)

    def procesar(self, insumo: Insumo) -> ResultadoInspeccion:
        try:
            letra  = self.obtener_letra_codigo(insumo.tamanio_lote, insumo.proveedor.nivel)
            n      = self.obtener_n_muestras(letra)
            return ResultadoInspeccion(insumo, letra, n)
        except LoteInvalidoError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error al procesar insumo '{insumo.nombre}': {e}")


# =============================================================================
# SECCION 9: CLASE COLA DE INSUMOS
# Unidad 1 - Clases y objetos
# Unidad 3 - Relaciones: SistemaInspeccion TIENE UNA ColaInsumos
# =============================================================================

class ColaInsumos:
    """
    Gestiona la fila de insumos pendientes de inspeccion.
    Comportamiento FIFO usando deque.
    """

    def __init__(self):
        self._cola: deque = deque()

    def encolar(self, insumo: Insumo):
        self._cola.append(insumo)
        print(f"  '{insumo.nombre}' encolado. Posicion en fila: {len(self._cola)}")

    def desencolar(self) -> Insumo:
        if self.esta_vacia():
            raise ColaVaciaError()
        return self._cola.popleft()

    def esta_vacia(self) -> bool:
        return len(self._cola) == 0

    def __len__(self) -> int:
        return len(self._cola)

    def __iter__(self):
        return iter(self._cola)

    def mostrar(self):
        print()
        print("=" * 60)
        print("   COLA DE INSUMOS PENDIENTES")
        print("=" * 60)
        if self.esta_vacia():
            print("  La cola esta vacia.")
            return
        print(f"  Insumos en espera: {len(self._cola)} (orden FIFO)")
        print()
        print(f"  {'Pos':<5} {'Insumo':<22} {'Lote':>7}  {'Proveedor':<18} {'Critico'}")
        print("  " + "-" * 62)
        for i, insumo in enumerate(self._cola, start=1):
            critico = "SI" if insumo.es_critico() else "no"
            print(f"  {i:<5} {insumo.nombre:<22} {insumo.tamanio_lote:>7}  "
                  f"{insumo.proveedor.tipo:<18} {critico}")
        print("=" * 60)


# =============================================================================
# SECCION 10: CLASE REGISTRO DIARIO
# Unidad 1 - Clases y objetos, Listas
# Unidad 3 - Relaciones: SistemaInspeccion TIENE UN RegistroDiario
# =============================================================================

class RegistroDiario:
    """
    Historial permanente de todos los insumos inspeccionados.
    Ofrece busqueda, filtrado, ordenamiento y estadisticas.
    """

    def __init__(self):
        self._registros: list = []

    def agregar(self, resultado: ResultadoInspeccion):
        self._registros.append(resultado)

    def __len__(self) -> int:
        return len(self._registros)

    def esta_vacio(self) -> bool:
        return len(self._registros) == 0

    def buscar_por_proveedor(self, tipo: str) -> list:
        return [r for r in self._registros
                if r.insumo.proveedor.tipo == tipo]

    def filtrar_por_control(self, tipo_control: str) -> list:
        return [r for r in self._registros
                if r.tipo_control == tipo_control.upper()]

    def ordenar_por_lote(self, descendente: bool = True) -> list:
        return sorted(self._registros,
                      key=lambda r: r.insumo.tamanio_lote,
                      reverse=descendente)

    def buscar_por_nombre(self, nombre: str) -> ResultadoInspeccion:
        nombre = nombre.strip().lower()
        for r in self._registros:
            if r.insumo.nombre.lower() == nombre:
                return r
        raise InsumoNoEncontradoError(nombre)

    def mostrar_completo(self):
        print()
        print("=" * 70)
        print("   REGISTRO DIARIO DE INSUMOS PROCESADOS")
        print("=" * 70)
        if self.esta_vacio():
            print("  No se proceso ningun insumo.")
            print("=" * 70)
            return
        print(f"  Total: {len(self._registros)} registro(s)")
        print()
        print(f"  {'N':<4} {'Insumo':<20} {'Lote':>6} {'Proveedor':<18} "
              f"{'Control':<22} {'Muestras':>8} {'Critico'}")
        print("  " + "-" * 84)
        for i, r in enumerate(self._registros, start=1):
            critico = "SI" if r.insumo.es_critico() else "-"
            print(f"  {i:<4} {r.insumo.nombre:<20} {r.insumo.tamanio_lote:>6} "
                  f"{r.insumo.proveedor.tipo:<18} {r.tipo_control:<22} "
                  f"{r.n_muestras:>8} {critico:>7}")
        print("=" * 70)

    def mostrar_estadisticas(self):
        print()
        print("=" * 60)
        print("   RESUMEN ESTADISTICO")
        print("=" * 60)
        if self.esta_vacio():
            print("  No hay datos.")
            print("=" * 60)
            return

        total = len(self._registros)
        solo  = len(self.filtrar_por_control("SOLO INSPECCION"))
        mues  = len(self.filtrar_por_control("INSPECCION + MUESTREO")  )
        nuevos  = len(self.buscar_por_proveedor("nuevo"))
        prueba  = len(self.buscar_por_proveedor("prueba_industrial"))
        homol   = len(self.buscar_por_proveedor("homologado"))
        criticos= len([r for r in self._registros if r.insumo.es_critico()])
        lotes   = [r.insumo.tamanio_lote for r in self._registros]
        muestras_total = sum(r.n_muestras for r in self._registros)

        print(f"  Total procesados         : {total}")
        print(f"  Solo inspeccion          : {solo}")
        print(f"  Inspeccion + Muestreo    : {mues}")
        print(f"  Proveedores nuevos       : {nuevos}")
        print(f"  Proveedores en prueba    : {prueba}")
        print(f"  Proveedores homologados  : {homol}")
        print(f"  Insumos criticos         : {criticos}")
        print(f"  Lote maximo              : {max(lotes)} unidades")
        print(f"  Lote minimo              : {min(lotes)} unidades")
        print(f"  Promedio de lote         : {sum(lotes)/total:.1f} unidades")
        print(f"  Total muestras a tomar   : {muestras_total}")
        print("=" * 60)


#### PARTE - 4

# =============================================================================
#SECCION 11: CLASE PRINCIPAL DEL SISTEMA
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


if __name__ == "__main__":
    menu_principal()
