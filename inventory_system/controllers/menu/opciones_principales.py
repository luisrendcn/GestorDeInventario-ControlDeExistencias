"""
menu/opciones_principales.py
============================
Mixin que maneja las opciones del menú principal.
"""

from utils import formato as fmt
from utils import validacion as val


class OpcionesPrincipalesMixin:
    """Mixin para procesar opciones del menú principal."""

    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal con estadísticas."""
        stats = self._facade.estadisticas()
        print(f"\n{fmt.linea_separadora()}")
        print(f"  MENÚ PRINCIPAL   |  Productos: {stats['total_productos']}  "
              f"|  Valor: ${stats['valor_inventario']:.2f}  "
              f"|  Stock bajo: {stats['productos_stock_bajo']}")
        print(fmt.linea_separadora())
        print("  [1] Gestión de Productos")
        print("  [2] Registrar Venta")
        print("  [3] Registrar Compra")
        print("  [4] Historial de Transacciones")
        print("  [5] Alertas de Stock Bajo")
        print("  [6] Estadísticas del Sistema")
        print("  [7] Log de Eventos")
        print("  [0] Salir")

    def procesar_opcion_principal(self, opcion: str) -> None:
        """Procesa la opción seleccionada en el menú principal."""
        acciones = {
            "1": self.menu_productos,
            "2": self.registrar_venta,
            "3": self.registrar_compra,
            "4": self.ver_historial,
            "5": self.ver_alertas,
            "6": self.ver_estadisticas,
            "7": self.ver_logs,
            "0": self.salir,
        }
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print(fmt.error("Opción inválida. Ingrese un número del 0 al 7."))

    def menu_productos(self) -> None:
        """Submenú de gestión de productos."""
        while True:
            print(fmt.encabezado("Gestión de Productos"))
            print("  [1] Listar todos los productos")
            print("  [2] Buscar producto por nombre")
            print("  [3] Ver detalle de producto")
            print("  [4] Crear nuevo producto")
            print("  [5] Editar producto")
            print("  [6] Eliminar producto")
            print("  [7] Importar productos desde Excel")
            print("  [0] Volver al menú principal")
            opcion = input("\n  Seleccione: ").strip()

            if opcion == "0":
                break
            elif opcion == "1":
                self.listar_productos()
            elif opcion == "2":
                self.buscar_producto()
            elif opcion == "3":
                self.ver_detalle_producto()
            elif opcion == "4":
                self.crear_producto()
            elif opcion == "5":
                self.editar_producto()
            elif opcion == "6":
                self.eliminar_producto()
            elif opcion == "7":
                self.importar_productos_excel()
            else:
                print(fmt.error("Opción inválida."))
