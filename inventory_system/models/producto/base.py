"""
producto/base.py
================
Clase abstracta base Producto.

Responsabilidades:
    - Definir interfaz común para todos los productos
    - Encapsulamiento con properties
    - Gestión de stock
    - Validación centralizada
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Producto(ABC):
    """
    Clase abstracta base para todos los tipos de productos.
    Define la interfaz común que deben implementar todos los productos.
    """

    def __init__(self, id: str, nombre: str, precio: float, stock: int, stock_minimo: int = 5):
        self._id = id
        self._nombre = nombre
        self._precio = precio
        self._stock = stock
        self._stock_minimo = stock_minimo

    # --- Propiedades (encapsulamiento) ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor: int):
        if valor < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        self._stock_minimo = valor

    @property
    def stock_bajo(self) -> bool:
        """Retorna True si el stock actual está por debajo del mínimo."""
        return self._stock <= self._stock_minimo

    # --- Métodos de modificación de stock ---

    def agregar_stock(self, cantidad: int) -> None:
        """Incrementa el stock del producto (compras)."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        self._stock += cantidad

    def reducir_stock(self, cantidad: int) -> None:
        """Reduce el stock del producto (ventas)."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        if cantidad > self._stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self._stock}, solicitado: {cantidad}.")
        self._stock -= cantidad

    # --- Validación centralizada ---

    @classmethod
    def validar_datos_base(cls, datos: Dict[str, Any]) -> None:
        """
        ✅ Valida los campos comunes a TODOS los tipos de producto.
        
        Responsabilidad centralizada en el modelo, no en la fábrica.
        """
        requeridos = ["id", "nombre", "precio", "stock"]
        for campo in requeridos:
            if campo not in datos:
                raise ValueError(f"Campo requerido ausente: '{campo}'.")
        
        # Validación de tipos explícita
        try:
            float(datos["precio"])
            int(datos["stock"])
        except (TypeError, ValueError):
            raise ValueError("Precio y stock deben ser numéricos.")
        
        if float(datos["precio"]) < 0:
            raise ValueError("El precio no puede ser negativo.")
        if int(datos["stock"]) < 0:
            raise ValueError("El stock no puede ser negativo.")

    # --- Métodos abstractos ---

    @abstractmethod
    def tipo(self) -> str:
        """Retorna el tipo de producto como string."""
        pass

    @abstractmethod
    def info_adicional(self) -> str:
        """Retorna información adicional específica del tipo de producto."""
        pass

    def __repr__(self) -> str:
        return (
            f"[{self.tipo()}] ID: {self._id} | "
            f"Nombre: {self._nombre} | "
            f"Precio: ${self._precio:.2f} | "
            f"Stock: {self._stock} | "
            f"Mínimo: {self._stock_minimo}"
        )
