"""
factory/registry.py
===================
Registro de fábricas con inyección de dependencias.

Responsabilidad:
    - Mantener registro de fábricas disponibles
    - Crear productos a través de las fábricas registradas
    - Permitir extensión sin mutabilidad global
    - Facilitar testing con inyección de dependencias
"""

from typing import Dict, Any
from models import Producto
from .bases import ProductoFactory
from .concretas import (
    ProductoSimpleFactory,
    ProductoPerecederoFactory,
    ProductoDigitalFactory,
)


class FactoryRegistry:
    """
    ✅ NUEVA: Registro de fábricas con inyección de dependencias.

    Ventajas:
    - Inmutabilidad: cambios crean NUEVA instancia
    - Sin estado global mutable
    - Extensible: se pueden registrar nuevas fábricas
    - Facilita testing: cada test obtiene su propia instancia
    """

    def __init__(self, fabricas: Dict[str, ProductoFactory] = None):
        """
        Inicializa el registro con fábricas por defecto.

        Args:
            fabricas: Diccionario adicional de fábricas personalizadas.
                     Se fusiona con las predeterminadas.
        """
        self._fabricas = {
            "simple": ProductoSimpleFactory(),
            "perecedero": ProductoPerecederoFactory(),
            "digital": ProductoDigitalFactory(),
        }

        if fabricas:
            self._fabricas.update(fabricas)

    def obtener_fabrica(self, tipo: str) -> ProductoFactory:
        """
        Retorna la fábrica correspondiente al tipo de producto.

        Args:
            tipo: 'simple', 'perecedero', 'digital', o tipo personalizado.

        Returns:
            Instancia de ProductoFactory.

        Raises:
            ValueError: Si el tipo no está registrado.
        """
        tipo = tipo.lower().strip()
        if tipo not in self._fabricas:
            tipos_validos = ", ".join(sorted(self._fabricas.keys()))
            raise ValueError(
                f"Tipo de producto desconocido: '{tipo}'. "
                f"Válidos: {tipos_validos}."
            )
        return self._fabricas[tipo]

    def crear_producto(self, tipo: str, datos: Dict[str, Any]) -> Producto:
        """
        Atajo para obtener la fábrica y crear el producto en un paso.

        Args:
            tipo: Tipo de producto.
            datos: Diccionario con datos del producto.

        Returns:
            Instancia de Producto.
        """
        return self.obtener_fabrica(tipo).crear_producto(datos)

    def con_fabrica_adicional(
        self, tipo: str, fabrica: ProductoFactory
    ) -> "FactoryRegistry":
        """
        ✅ CLAVE: Retorna NUEVA instancia con fábrica adicional (INMUTABLE).

        Ventajas:
        - No modifica el registro original
        - Cada cambio crea una nueva instancia
        - Perfecto para testing: no hay efectos secundarios

        Args:
            tipo: Tipo de producto.
            fabrica: Nueva fábrica a registrar.

        Returns:
            NUEVA instancia de FactoryRegistry con la fábrica adicional.
        """
        nuevas_fabricas = {**self._fabricas, tipo.lower(): fabrica}
        return FactoryRegistry(nuevas_fabricas)

    def tipos_disponibles(self) -> list:
        """Retorna lista de tipos de producto disponibles."""
        return sorted(self._fabricas.keys())

    def __repr__(self) -> str:
        tipos = ", ".join(self.tipos_disponibles())
        return f"FactoryRegistry(tipos=[{tipos}])"
