"""
models/producto.py
------------------
Clases de dominio para los productos del inventario.

Aplica:
- Abstracción con abc (clases abstractas e interfaces)
- Encapsulamiento con properties
- Herencia y polimorfismo
"""

from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional


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

    # --- Método abstracto ---

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


# ---------------------------------------------------------------------------
# Tipos concretos de productos (usados por Factory Method)
# ---------------------------------------------------------------------------

class ProductoSimple(Producto):
    """
    Producto estándar sin características especiales adicionales.
    Ejemplo: electrónico, utensilio, ropa, etc.
    """

    def __init__(self, id: str, nombre: str, precio: float, stock: int,
                 stock_minimo: int = 5, categoria: str = "General"):
        super().__init__(id, nombre, precio, stock, stock_minimo)
        self._categoria = categoria

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = valor.strip() if valor.strip() else "General"

    def tipo(self) -> str:
        return "Simple"

    def info_adicional(self) -> str:
        return f"Categoría: {self._categoria}"


class ProductoPerecedero(Producto):
    """
    Producto con fecha de vencimiento.
    Ejemplo: alimentos, medicamentos, cosméticos.

    Agrega la lógica de expiración al dominio.
    """

    def __init__(self, id: str, nombre: str, precio: float, stock: int,
                 fecha_vencimiento: date, stock_minimo: int = 5):
        super().__init__(id, nombre, precio, stock, stock_minimo)
        self._fecha_vencimiento = fecha_vencimiento

    @property
    def fecha_vencimiento(self) -> date:
        return self._fecha_vencimiento

    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor: date):
        self._fecha_vencimiento = valor

    @property
    def esta_vencido(self) -> bool:
        return date.today() > self._fecha_vencimiento

    @property
    def dias_para_vencer(self) -> int:
        delta = self._fecha_vencimiento - date.today()
        return delta.days

    def tipo(self) -> str:
        return "Perecedero"

    def info_adicional(self) -> str:
        estado = "VENCIDO" if self.esta_vencido else f"vence en {self.dias_para_vencer} días"
        return f"Vencimiento: {self._fecha_vencimiento} ({estado})"


class ProductoDigital(Producto):
    """
    Producto digital: no tiene límite físico de stock real,
    pero se gestiona con licencias disponibles.
    Ejemplo: software, suscripciones, e-books.
    """

    def __init__(self, id: str, nombre: str, precio: float, licencias: int,
                 stock_minimo: int = 2, url_descarga: str = ""):
        super().__init__(id, nombre, precio, licencias, stock_minimo)
        self._url_descarga = url_descarga

    @property
    def url_descarga(self) -> str:
        return self._url_descarga

    @url_descarga.setter
    def url_descarga(self, valor: str):
        self._url_descarga = valor

    def tipo(self) -> str:
        return "Digital"

    def info_adicional(self) -> str:
        url = self._url_descarga if self._url_descarga else "no especificada"
        return f"Licencias disponibles: {self._stock} | URL: {url}"
