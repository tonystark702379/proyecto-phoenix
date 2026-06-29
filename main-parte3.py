

# =============================================================================
# SECCION 8: CLASE MOTOR ISO 2859-1
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

    def _init_(self):
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

    def _len_(self) -> int:
        return len(self._cola)

    def _iter_(self):
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

    def _init_(self):
        self._registros: list = []

    def agregar(self, resultado: ResultadoInspeccion):
        self._registros.append(resultado)

    def _len_(self) -> int:
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