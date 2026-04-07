"""
factory/bases.py
================
Fábrica abstracta con Template Method.

Responsabilidad:
    - Define algoritmo de creación consistente
    - Subclases implementan validación y construcción específica
    - Asegura que todos los productos sigan el mismo flujo
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Any
from models import Producto


class ProductoFactory(ABC):
    """
    Clase base abstracta para las fábricas de productos.

    ✅ PATRÓN: Template Method
    - Define el algoritmo de creación en la clase base
    - Subclases implementan validación específica y construcción
    - Asegura que TODOS sigan el mismo flujo
    """

    def crear_producto(self, datos: Dict[str, Any]) -> Producto:
        """
        Template Method: define el algoritmo de creación.

        Flujo:
        1. Validar campos base (común a todas)
        2. Validar campos específicos (subclase implementa)
        3. Construir producto (subclase implementa)

        ✅ VENTAJA: Consistencia asegurada por el patrón
        """
        self._validar_campos_base(datos)
        self._validar_campos_especificos(datos)
        return self._construir_producto(datos)

    def _validar_campos_base(self, datos: Dict[str, Any]) -> None:
        """
        ✅ RESPONSABILIDAD: Validación común a TODAS las fábricas.
        """
        requeridos = ["id", "nombre", "precio", "stock"]
        for campo in requeridos:
            if campo not in datos:
                raise ValueError(f"Campo requerido ausente: '{campo}'.")

        try:
            float(datos["precio"])
            int(datos["stock"])
        except (TypeError, ValueError):
            raise ValueError("Precio y stock deben ser numéricos.")

        if float(datos["precio"]) < 0:
            raise ValueError("El precio no puede ser negativo.")
        if int(datos["stock"]) < 0:
            raise ValueError("El stock no puede ser negativo.")

    @abstractmethod
    def _validar_campos_especificos(self, datos: Dict[str, Any]) -> None:
        """
        ✅ PUNTO DE EXTENSIÓN: Cada fábrica valida sus campos específicos.
        """
        pass

    @abstractmethod
    def _construir_producto(self, datos: Dict[str, Any]) -> Producto:
        """
        ✅ PUNTO DE EXTENSIÓN: Cada fábrica construye su producto.
        """
        pass
