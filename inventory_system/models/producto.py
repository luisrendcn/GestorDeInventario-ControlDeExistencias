"""
models/producto.py
==================
Modelo genérico de Producto para Control de Existencias.

Sin tipos específicos - solo el dominio de negocio.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Producto:
    """Modelo genérico de Producto."""
    
    id: str
    nombre: str
    precio: float
    stock: int
    stock_minimo: int = 5
    descripcion: Optional[str] = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validaciones al crear producto."""
        if not self.id or not self.nombre:
            raise ValueError("ID y nombre son requeridos")
        if self.precio < 0:
            raise ValueError("Precio no puede ser negativo")
        if self.stock < 0:
            raise ValueError("Stock no puede ser negativo")
        if self.stock_minimo < 0:
            raise ValueError("Stock mínimo no puede ser negativo")
    
    @property
    def stock_bajo(self) -> bool:
        """Retorna True si stock está bajo el mínimo."""
        return self.stock <= self.stock_minimo
    
    @property
    def agotado(self) -> bool:
        """Retorna True si stock = 0."""
        return self.stock == 0
    
    @property
    def valor_total(self) -> float:
        """Valor total del producto en stock."""
        return self.precio * self.stock
    
    def agregar_stock(self, cantidad: int) -> None:
        """Incrementar stock (entrada)."""
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        self.stock += cantidad
    
    def reducir_stock(self, cantidad: int) -> None:
        """Reducir stock (salida)."""
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        if cantidad > self.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}, solicitado: {cantidad}")
        self.stock -= cantidad
    
    def ajustar_stock(self, nuevo_stock: int) -> None:
        """Ajustar stock a un valor específico (auditoría)."""
        if nuevo_stock < 0:
            raise ValueError("Stock no puede ser negativo")
        self.stock = nuevo_stock
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para serialización."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "descripcion": self.descripcion,
            "valor_total": self.valor_total,
            "stock_bajo": self.stock_bajo,
            "agotado": self.agotado,
        }
