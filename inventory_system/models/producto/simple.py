"""
producto/simple.py
==================
Tipo de producto: Producto Simple (sin características especiales).

Ejemplo: electrónico, utensilio, ropa, etc.
"""

from .base import Producto
from .contratos import ProductoSimpleData


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

    @classmethod
    def from_dict(cls, datos: ProductoSimpleData) -> "ProductoSimple":
        """
        ✅ Construye ProductoSimple desde diccionario.
        
        Ventajas:
        - ProductoSimple es responsable de sus detalles de construcción
        - Factory no conoce el constructor
        - Cambios en constructor no afectan factory
        """
        cls.validar_datos_base(datos)
        
        return cls(
            id=datos["id"],
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            stock=int(datos["stock"]),
            stock_minimo=int(datos.get("stock_minimo", 5)),
            categoria=datos.get("categoria", "General"),
        )
