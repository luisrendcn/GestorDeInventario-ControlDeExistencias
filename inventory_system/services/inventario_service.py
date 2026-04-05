"""
services/inventario_service.py
------------------------------
Servicio de negocio para la gestión del inventario.

Contiene la lógica de negocio (SRP): coordina el repositorio (Inventario),
las notificaciones (SujetoStock) y la creación de transacciones.

Aplica:
- SRP: solo gestiona lógica de inventario
- DIP: depende de abstracciones (Inventario, SujetoStock), no de concretos
"""

from typing import Dict, Any, Optional
from models.inventario import Inventario
from models.producto import Producto
from models.transaccion import TipoTransaccion
from patterns.observer import SujetoStock


class InventarioService:
    """
    Lógica de negocio para gestionar el inventario de productos.
    Coordina el repositorio, las notificaciones y las transacciones.
    """

    def __init__(self, inventario: Inventario, sujeto: SujetoStock):
        self._inventario = inventario
        self._sujeto = sujeto

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto al inventario."""
        self._inventario.agregar(producto)

    def editar_producto(self, id: str, nuevos_datos: Dict[str, Any]) -> Producto:
        """
        Actualiza los campos editables de un producto.

        Campos editables comunes: nombre, precio, stock_minimo.
        Campos específicos por tipo: categoria, fecha_vencimiento, url_descarga.
        """
        from datetime import date
        from models.producto import ProductoSimple, ProductoPerecedero, ProductoDigital

        producto = self._inventario.obtener_o_error(id)

        if "nombre" in nuevos_datos:
            producto.nombre = nuevos_datos["nombre"]
        if "precio" in nuevos_datos:
            producto.precio = float(nuevos_datos["precio"])
        if "stock_minimo" in nuevos_datos:
            producto.stock_minimo = int(nuevos_datos["stock_minimo"])

        # Campos específicos por tipo de producto
        if isinstance(producto, ProductoSimple) and "categoria" in nuevos_datos:
            producto.categoria = nuevos_datos["categoria"]

        if isinstance(producto, ProductoPerecedero) and "fecha_vencimiento" in nuevos_datos:
            fecha = nuevos_datos["fecha_vencimiento"]
            if isinstance(fecha, str):
                fecha = date.fromisoformat(fecha)
            producto.fecha_vencimiento = fecha

        if isinstance(producto, ProductoDigital) and "url_descarga" in nuevos_datos:
            producto.url_descarga = nuevos_datos["url_descarga"]

        return producto

    def eliminar_producto(self, id: str) -> Producto:
        """Elimina un producto del inventario."""
        return self._inventario.eliminar(id)

    def registrar_venta(self, producto_id: str, cantidad: int, transaccion_service) -> object:
        """
        Procesa una venta:
        1. Valida existencia del producto
        2. Reduce el stock
        3. Crea la transacción
        4. Notifica a los observadores
        """
        producto = self._inventario.obtener_o_error(producto_id)
        producto.reducir_stock(cantidad)  # Lanza error si stock insuficiente
        transaccion = transaccion_service.registrar(
            tipo=TipoTransaccion.VENTA,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        )
        self._sujeto.notificar(producto, "venta", cantidad)
        return transaccion

    def registrar_compra(
        self,
        producto_id: str,
        cantidad: int,
        transaccion_service,
        precio_unitario: Optional[float] = None,
    ) -> object:
        """
        Procesa una compra:
        1. Valida existencia del producto
        2. Aumenta el stock
        3. Crea la transacción
        4. Notifica a los observadores
        """
        producto = self._inventario.obtener_o_error(producto_id)
        precio = precio_unitario if precio_unitario is not None else producto.precio
        producto.agregar_stock(cantidad)
        transaccion = transaccion_service.registrar(
            tipo=TipoTransaccion.COMPRA,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio,
        )
        self._sujeto.notificar(producto, "compra", cantidad)
        return transaccion
