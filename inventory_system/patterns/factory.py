"""
patterns/factory.py
-------------------
PATRÓN CREACIONAL: Factory Method (Método de Fábrica)

Problema resuelto:
    El código cliente necesita crear distintos tipos de productos
    (Simple, Perecedero, Digital) sin depender de sus constructores
    concretos. El Factory Method centraliza y desacopla la creación.

Participantes:
    - ProductoFactory (clase abstracta): define el método de fábrica
    - ProductoSimpleFactory: crea ProductoSimple
    - ProductoPerecederoFactory: crea ProductoPerecedero
    - ProductoDigitalFactory: crea ProductoDigital
    - FactoryManager: selector de fábrica por tipo (clave de extensión)
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Any
from models.producto import Producto, ProductoSimple, ProductoPerecedero, ProductoDigital


# ---------------------------------------------------------------------------
# Fábrica abstracta
# ---------------------------------------------------------------------------

class ProductoFactory(ABC):
    """
    Clase base abstracta para las fábricas de productos.
    Define el contrato del Factory Method: crear_producto().
    """

    @abstractmethod
    def crear_producto(self, datos: Dict[str, Any]) -> Producto:
        """
        Método de fábrica: crea y retorna un producto concreto.

        Args:
            datos: Diccionario con los datos del producto.
                   Cada fábrica concreta define qué campos espera.

        Returns:
            Una instancia concreta de Producto.
        """
        pass

    def _validar_campos_base(self, datos: Dict[str, Any]) -> None:
        """Valida los campos comunes a todos los tipos de producto."""
        requeridos = ["id", "nombre", "precio", "stock"]
        for campo in requeridos:
            if campo not in datos:
                raise ValueError(f"Campo requerido ausente: '{campo}'.")
        if datos["precio"] < 0:
            raise ValueError("El precio no puede ser negativo.")
        if datos["stock"] < 0:
            raise ValueError("El stock no puede ser negativo.")


# ---------------------------------------------------------------------------
# Fábricas concretas
# ---------------------------------------------------------------------------

class ProductoSimpleFactory(ProductoFactory):
    """Fábrica para crear productos simples (electrónicos, ropa, etc.)."""

    def crear_producto(self, datos: Dict[str, Any]) -> ProductoSimple:
        self._validar_campos_base(datos)
        return ProductoSimple(
            id=datos["id"],
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            stock=int(datos["stock"]),
            stock_minimo=int(datos.get("stock_minimo", 5)),
            categoria=datos.get("categoria", "General"),
        )


class ProductoPerecederoFactory(ProductoFactory):
    """Fábrica para crear productos perecederos (alimentos, medicamentos)."""

    def crear_producto(self, datos: Dict[str, Any]) -> ProductoPerecedero:
        self._validar_campos_base(datos)
        if "fecha_vencimiento" not in datos:
            raise ValueError("Los productos perecederos requieren 'fecha_vencimiento'.")

        fecha = datos["fecha_vencimiento"]
        if isinstance(fecha, str):
            fecha = date.fromisoformat(fecha)  # Acepta formato YYYY-MM-DD

        return ProductoPerecedero(
            id=datos["id"],
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            stock=int(datos["stock"]),
            fecha_vencimiento=fecha,
            stock_minimo=int(datos.get("stock_minimo", 5)),
        )


class ProductoDigitalFactory(ProductoFactory):
    """Fábrica para crear productos digitales (software, licencias, e-books)."""

    def crear_producto(self, datos: Dict[str, Any]) -> ProductoDigital:
        self._validar_campos_base(datos)
        return ProductoDigital(
            id=datos["id"],
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            licencias=int(datos["stock"]),
            stock_minimo=int(datos.get("stock_minimo", 2)),
            url_descarga=datos.get("url_descarga", ""),
        )


# ---------------------------------------------------------------------------
# Manager de fábricas (extensión sin modificar código existente — OCP)
# ---------------------------------------------------------------------------

class FactoryManager:
    """
    Administrador de fábricas. Asocia tipos de producto a sus fábricas.
    Permite registrar nuevas fábricas sin modificar código existente (OCP).
    """

    _fabricas: Dict[str, ProductoFactory] = {
        "simple": ProductoSimpleFactory(),
        "perecedero": ProductoPerecederoFactory(),
        "digital": ProductoDigitalFactory(),
    }

    @classmethod
    def obtener_fabrica(cls, tipo: str) -> ProductoFactory:
        """
        Retorna la fábrica correspondiente al tipo de producto.

        Args:
            tipo: 'simple', 'perecedero', o 'digital'.

        Returns:
            Instancia de ProductoFactory.

        Raises:
            ValueError: Si el tipo no está registrado.
        """
        tipo = tipo.lower().strip()
        if tipo not in cls._fabricas:
            tipos_validos = ", ".join(cls._fabricas.keys())
            raise ValueError(f"Tipo de producto desconocido: '{tipo}'. Válidos: {tipos_validos}.")
        return cls._fabricas[tipo]

    @classmethod
    def crear_producto(cls, tipo: str, datos: Dict[str, Any]) -> Producto:
        """Atajo para obtener la fábrica y crear el producto en un paso."""
        return cls.obtener_fabrica(tipo).crear_producto(datos)

    @classmethod
    def registrar_fabrica(cls, tipo: str, fabrica: ProductoFactory) -> None:
        """
        Registra una nueva fábrica personalizada.
        Permite extender el sistema sin modificar este archivo (OCP).
        """
        cls._fabricas[tipo.lower()] = fabrica

    @classmethod
    def tipos_disponibles(cls) -> list:
        return list(cls._fabricas.keys())
