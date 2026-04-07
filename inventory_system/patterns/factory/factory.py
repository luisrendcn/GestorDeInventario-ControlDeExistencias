"""
factory/factory.py
==================
Coordinador: FactoryManager con compatibilidad global.

Responsabilidad:
    - Mantener registry global para compatibilidad
    - Proporcionar interfaz estática para creación
    - Permitir registro de fábricas personalizadas
    - Asegurar no hay breaking changes con código anterior
"""

from typing import Dict, Any
from models import Producto
from .bases import ProductoFactory
from .registry import FactoryRegistry


# Instancia global para compatibilidad y funciones de conveniencia
_registry_global = FactoryRegistry()


def obtener_fabrica(tipo: str) -> ProductoFactory:
    """Compatibilidad: obtener fábrica del registry global."""
    return _registry_global.obtener_fabrica(tipo)


def crear_producto(tipo: str, datos: Dict[str, Any]) -> Producto:
    """Compatibilidad: crear producto con registry global."""
    return _registry_global.crear_producto(tipo, datos)


def tipos_disponibles() -> list:
    """Compatibilidad: obtener tipos del registry global."""
    return _registry_global.tipos_disponibles()


# ---------------------------------------------------------------------------
# FactoryManager como alias para compatibilidad (DEPRECATED)
# ---------------------------------------------------------------------------


class FactoryManager:
    """
    ⚠️ DEPRECATED: Use FactoryRegistry en su lugar.

    Se mantiene por compatibilidad con código anterior.
    Todos los métodos delegan al registry global.
    """

    @classmethod
    def obtener_fabrica(cls, tipo: str) -> ProductoFactory:
        """Retorna la fábrica correspondiente al tipo de producto."""
        return _registry_global.obtener_fabrica(tipo)

    @classmethod
    def crear_producto(cls, tipo: str, datos: Dict[str, Any]) -> Producto:
        """Atajo para obtener la fábrica y crear el producto en un paso."""
        return _registry_global.crear_producto(tipo, datos)

    @classmethod
    def registrar_fabrica(cls, tipo: str, fabrica: ProductoFactory) -> None:
        """
        Registra una nueva fábrica personalizada.
        Permite extender el sistema sin modificar este archivo (OCP).
        """
        global _registry_global
        _registry_global = _registry_global.con_fabrica_adicional(tipo, fabrica)

    @classmethod
    def tipos_disponibles(cls) -> list:
        """Retorna lista de tipos disponibles."""
        return _registry_global.tipos_disponibles()
