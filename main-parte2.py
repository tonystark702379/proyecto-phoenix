# =============================================================================
# SECCION 5: CLASE INSUMO (hereda de EntidadInspeccionable)
# =============================================================================

class Insumo(EntidadInspeccionable):
    """
    Representa un insumo que llega a la planta de Gloria S.A.
    Hereda de EntidadInspeccionable e implementa sus metodos abstractos.
    Relacion de composicion con Proveedor: un Insumo TIENE UN Proveedor.
    """

    def _init_(self, nombre: str, tamanio_lote: int, tipo_proveedor: str):
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

    def _str_(self) -> str:
        return f"{self._nombre} (lote={self._tamanio_lote}, proveedor={self._proveedor.tipo})"

