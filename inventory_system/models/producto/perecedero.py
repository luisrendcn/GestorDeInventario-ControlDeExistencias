"""
producto/perecedero.py
======================
Tipo de producto: Producto Perecedero (con fecha de vencimiento).

Ejemplo: alimentos, medicamentos, cosméticos.
Agrega la lógica de expiración al dominio.
"""

from datetime import date
from .base import Producto
from .contratos import ProductoPerecederoData


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

    @classmethod
    def from_dict(cls, datos: ProductoPerecederoData) -> "ProductoPerecedero":
        """
        ✅ Construye ProductoPerecedero desde diccionario.
        
        NOTA: El parsing de fecha está aquí, no en la factory.
        Si cambia el formato de fecha, solo cambiar aquí.
        """
        cls.validar_datos_base(datos)
        
        if "fecha_vencimiento" not in datos:
            raise ValueError("Los productos perecederos requieren 'fecha_vencimiento'.")
        
        # ✅ Transformación: responsabilidad del modelo
        fecha = datos["fecha_vencimiento"]
        if isinstance(fecha, str):
            try:
                fecha = date.fromisoformat(fecha)  # ISO format: YYYY-MM-DD
            except ValueError:
                raise ValueError(
                    f"Formato de fecha inválido: '{fecha}'. "
                    f"Esperado: YYYY-MM-DD"
                )
        
        return cls(
            id=datos["id"],
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            stock=int(datos["stock"]),
            fecha_vencimiento=fecha,
            stock_minimo=int(datos.get("stock_minimo", 5)),
        )
