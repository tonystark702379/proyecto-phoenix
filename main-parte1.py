
# PARTE 1

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
    def _init_(self, lote):
        super()._init_(f"Tamano de lote invalido: {lote}. Debe ser mayor o igual a 2.")
        self.lote = lote

class ProveedorInvalidoError(Exception):
    def _init_(self, tipo):
        super()._init_(f"Tipo de proveedor no reconocido: '{tipo}'.")
        self.tipo = tipo

class ColaVaciaError(Exception):
    def _init_(self):
        super()._init_("La cola esta vacia. No hay insumos pendientes.")

class InsumoNoEncontradoError(Exception):
    def _init_(self, nombre):
        super()._init_(f"Insumo '{nombre}' no encontrado en el registro.")
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

    def _init_(self, tipo: str):
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

    def _str_(self) -> str:
        return f"{self._tipo.capitalize()} (Nivel {self._nivel} - {self._descripcion})"
    
