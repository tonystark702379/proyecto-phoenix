

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

