

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
