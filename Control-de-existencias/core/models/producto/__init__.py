"""Clase Producto con todas las operaciones separadas en mixins atómicos."""

from datetime import datetime
from typing import Optional

from core.models.producto.propiedades import PropiedadesMixin
from core.models.producto.operaciones import OperacionesMixin
from core.models.producto.serializacion import SerializacionMixin


class Producto(PropiedadesMixin, OperacionesMixin, SerializacionMixin):
    """
    Entidad Producto de dominio (modelo de dominio puro).
    
    Representa un producto en el sistema de control de existencias.
    Encapsula datos y operaciones organizadas en mixins por responsabilidad máxima.
    
    RESPONSABILIDADES (composición de 3 mixins principales):
    
      1️⃣  PropiedadesMixin - Calcular estado derivado
            • StockBajoMixin - stock_bajo property
            • AgotadoMixin - agotado property
            • ValorTotalMixin - valor_total property
      
      2️⃣  OperacionesMixin - Mutación de stock
            • AgregarStockMixin - agregar_stock()
            • ReducirStockMixin - reducir_stock()
            • EstablecerStockMixin - establecer_stock()
      
      3️⃣  SerializacionMixin - Conversión a/desde formatos
            • ToDictMixin - to_dict()
            • ToTupleMixin - to_tuple()
            • FromDictMixin - from_dict()
            • FromRowMixin - from_row()
    
    ATRIBUTOS:
      • id (str): Identificador único del producto
      • nombre (str): Nombre del producto
      • precio (float): Precio unitario
      • stock (int): Cantidad actual disponible
      • stock_minimo (int): Mínimo recomendado (default 5)
      • descripcion (str): Descripción del producto (opcional)
      • created_at (datetime): Timestamp de creación
      • updated_at (datetime): Timestamp de última actualización
    """
    
    def __init__(
        self,
        id: str,
        nombre: str,
        precio: float,
        stock: int,
        stock_minimo: int = 5,
        descripcion: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)
        self.stock_minimo = int(stock_minimo)
        self.descripcion = descripcion or ""
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def __repr__(self) -> str:
        return f"Producto(id={self.id}, nombre={self.nombre}, stock={self.stock})"
