"""
menu/transacciones.py
=====================
Mixin que maneja ventas y compras.
"""

from utils import formato as fmt
from utils import validacion as val


class TransaccionesMixin:
    """Mixin para registrar ventas y compras."""

    def registrar_venta(self) -> None:
        """Registra una venta."""
        print(fmt.encabezado("Registrar Venta"))
        productos = self._facade.listar_productos()
        if not productos:
            print(fmt.info("No hay productos disponibles."))
            input("\n  Presione Enter para continuar...")
            return

        print(fmt.formatear_lista_productos(productos))

        try:
            id_producto = val.leer_texto("\n  ID del producto a vender").upper()
            cantidad = val.leer_entero("Cantidad a vender", minimo=1)
            transaccion = self._facade.registrar_venta(id_producto, cantidad)
            print(fmt.exito(f"Venta registrada: {transaccion}"))
        except ValueError as e:
            print(fmt.error(str(e)))

        input("\n  Presione Enter para continuar...")

    def registrar_compra(self) -> None:
        """Registra una compra."""
        print(fmt.encabezado("Registrar Compra"))
        productos = self._facade.listar_productos()
        if not productos:
            print(fmt.info("No hay productos disponibles. Cree un producto primero."))
            input("\n  Presione Enter para continuar...")
            return

        print(fmt.formatear_lista_productos(productos))

        try:
            id_producto = val.leer_texto("\n  ID del producto a comprar").upper()
            cantidad = val.leer_entero("Cantidad a comprar", minimo=1)
            precio_str = input("  Precio de costo unitario (Enter = usar precio actual): ").strip()
            precio = float(precio_str) if precio_str else None
            transaccion = self._facade.registrar_compra(id_producto, cantidad, precio)
            print(fmt.exito(f"Compra registrada: {transaccion}"))
        except ValueError as e:
            print(fmt.error(str(e)))

        input("\n  Presione Enter para continuar...")
