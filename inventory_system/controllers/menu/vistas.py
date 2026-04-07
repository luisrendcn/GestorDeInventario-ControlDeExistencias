"""
menu/vistas.py
==============
Mixin que maneja la visualización de historial, alertas, estadísticas y logs.
"""

from utils import formato as fmt


class VistasMixin:
    """Mixin para mostrar vistas de historial, alertas, estadísticas y logs."""

    def ver_historial(self) -> None:
        """Muestra el historial de transacciones."""
        print(fmt.encabezado("Historial de Transacciones"))
        transacciones = self._facade.historial_transacciones()
        print(fmt.formatear_lista_transacciones(transacciones))
        input("\n  Presione Enter para continuar...")

    def ver_alertas(self) -> None:
        """Muestra alertas de stock bajo."""
        print(fmt.encabezado("Alertas de Stock Bajo"))
        productos = self._facade.productos_stock_bajo()
        if not productos:
            print(fmt.exito("Todos los productos tienen stock suficiente."))
        else:
            print(f"\n  {len(productos)} producto(s) con stock insuficiente:\n")
            for p in productos:
                print(fmt.formatear_producto(p))
        input("\n  Presione Enter para continuar...")

    def ver_estadisticas(self) -> None:
        """Muestra estadísticas del sistema."""
        print(fmt.encabezado("Estadísticas del Sistema"))
        stats = self._facade.estadisticas()
        print(f"  Total de productos      : {stats['total_productos']}")
        print(f"  Valor del inventario    : ${stats['valor_inventario']:.2f}")
        print(f"  Productos con stock bajo: {stats['productos_stock_bajo']}")
        print(f"  Total transacciones     : {stats['total_transacciones']}")
        print(f"    - Ventas registradas  : {stats['total_ventas']}")
        print(f"    - Compras registradas : {stats['total_compras']}")
        print(f"  Ingresos por ventas     : ${stats['ingresos_ventas']:.2f}")
        print(f"  Costos de compras       : ${stats['costo_compras']:.2f}")
        balance = stats['ingresos_ventas'] - stats['costo_compras']
        print(f"  Balance (ventas-compras): ${balance:.2f}")
        input("\n  Presione Enter para continuar...")

    def ver_logs(self) -> None:
        """Muestra el log de eventos de stock."""
        print(fmt.encabezado("Log de Eventos de Stock"))
        self._facade.mostrar_logs()
        input("\n  Presione Enter para continuar...")
