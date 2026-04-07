"""
producto/digital.py
===================
Tipo de producto: Producto Digital (software, suscripciones, e-books).

Ejemplo: software, suscripciones, e-books.
No tiene límite físico de stock real, se gestiona con licencias disponibles.
"""

from .base import Producto
from .contratos import ProductoDigitalData


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

    @classmethod
    def from_dict(cls, datos: ProductoDigitalData) -> "ProductoDigital":
        """
        ✅ Construye ProductoDigital desde diccionario.
        
        Mapeo explícito: stock (en datos) → licencias (en constructor).
        """
        cls.validar_datos_base(datos)
        
        # Validación específica
        url = datos.get("url_descarga", "")
        if not url:
            raise ValueError("Los productos digitales requieren 'url_descarga'.")
        
        # ✅ Mapeo explícito: stock → licencias
        return cls(
            id=datos["id"],
            nombre=datos["nombre"],
            precio=float(datos["precio"]),
            licencias=int(datos["stock"]),  # Mapeo semántico explícito
            stock_minimo=int(datos.get("stock_minimo", 2)),
            url_descarga=url,
        )
