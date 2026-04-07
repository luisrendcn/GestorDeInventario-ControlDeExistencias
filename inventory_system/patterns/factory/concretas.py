"""
factory/concretas.py
====================
Fábricas concretas para cada tipo de producto.

Responsabilidad:
    - Implementar validación específica por tipo
    - Delegar construcción al método from_dict() del modelo
    - Mantener consistencia con Template Method
"""

from datetime import date
from typing import Dict, Any
from models import (
    Producto,
    ProductoSimple,
    ProductoPerecedero,
    ProductoDigital,
)
from .bases import ProductoFactory


class ProductoSimpleFactory(ProductoFactory):
    """
    Fábrica para crear productos simples (electrónicos, ropa, etc.).

    ✅ SIMPLIFICADA: Solo implementa validación y delegación a from_dict()
    """

    def _validar_campos_especificos(self, datos: Dict[str, Any]) -> None:
        """Validación específica de ProductoSimple."""
        # ProductoSimple no tiene requerimientos especiales más allá de los base
        pass

    def _construir_producto(self, datos: Dict[str, Any]) -> ProductoSimple:
        """
        ✅ DELEGACIÓN: ProductoSimple se construye a sí mismo.
        """
        return ProductoSimple.from_dict(datos)


class ProductoPerecederoFactory(ProductoFactory):
    """
    Fábrica para crear productos perecederos (alimentos, medicamentos).

    ✅ VALIDACIÓN ESPECÍFICA: Requiere 'fecha_vencimiento'
    """

    def _validar_campos_especificos(self, datos: Dict[str, Any]) -> None:
        """Validación específica de ProductoPerecedero."""
        if "fecha_vencimiento" not in datos:
            raise ValueError(
                "Los productos perecederos requieren 'fecha_vencimiento'."
            )

        # Validar formato de fecha ISO
        fecha = datos["fecha_vencimiento"]
        if isinstance(fecha, str):
            try:
                date.fromisoformat(fecha)
            except ValueError:
                raise ValueError(
                    f"Formato de fecha inválido: '{fecha}'. "
                    f"Esperado formato ISO (YYYY-MM-DD)."
                )

    def _construir_producto(self, datos: Dict[str, Any]) -> ProductoPerecedero:
        """
        ✅ DELEGACIÓN: ProductoPerecedero se construye a sí mismo.
        """
        return ProductoPerecedero.from_dict(datos)


class ProductoDigitalFactory(ProductoFactory):
    """
    Fábrica para crear productos digitales (software, licencias, e-books).

    ✅ VALIDACIÓN ESPECÍFICA: Requiere 'url_descarga'
    """

    def _validar_campos_especificos(self, datos: Dict[str, Any]) -> None:
        """Validación específica de ProductoDigital."""
        url = datos.get("url_descarga", "")
        if not url:
            raise ValueError("Los productos digitales requieren 'url_descarga'.")

    def _construir_producto(self, datos: Dict[str, Any]) -> ProductoDigital:
        """
        ✅ DELEGACIÓN: ProductoDigital se construye a sí mismo.
        """
        return ProductoDigital.from_dict(datos)
