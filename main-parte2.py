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

    def _init_(self, insumo: Insumo, letra_codigo: str, n_muestras: int):
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

    def _str_(self) -> str:
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
    def _init_(self):
        super()._init_("nuevo")

    def get_recomendacion(self) -> str:
        return "Aplicar inspeccion completa. Solicitar certificados de calidad al proveedor."


class ProveedorPrueba(Proveedor):
    """
    Proveedor en etapa de prueba industrial. Hereda de Proveedor.
    """
    def _init_(self):
        super()._init_("prueba_industrial")

    def get_recomendacion(self) -> str:
        return "Mantener seguimiento. Evaluar conformidad para posible homologacion."


class ProveedorHomologado(Proveedor):
    """
    Proveedor homologado con historial verificado. Hereda de Proveedor.
    """
    def _init_(self):
        super()._init_("homologado")

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

