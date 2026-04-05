"""
controllers/menu_controller.py
-------------------------------
Controlador principal de la interfaz de línea de comandos (CLI).

Responsabilidad:
    - Mostrar menús y capturar la opción del usuario.
    - Delegar la lógica al Facade (SistemaInventarioFacade).
    - Manejar errores y mostrar resultados al usuario.

Aplica:
    - Separación de responsabilidades: solo maneja el flujo de UI.
    - No contiene lógica de negocio ni acceso directo a modelos.
"""

import sys
import os

# Asegura que los imports funcionen desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.facade import SistemaInventarioFacade
from utils import formato as fmt
from utils import validacion as val


class MenuController:
    """
    Controlador de la interfaz CLI.
    Coordina la interacción entre el usuario y el Facade del sistema.
    """

    def __init__(self):
        self._facade = SistemaInventarioFacade()
        self._corriendo = True

    # -----------------------------------------------------------------------
    # Bucle principal
    # -----------------------------------------------------------------------

    def iniciar(self) -> None:
        """Punto de entrada del controlador. Muestra el menú principal en bucle."""
        self._mostrar_bienvenida()
        self._cargar_datos_demo()

        while self._corriendo:
            self._mostrar_menu_principal()
            opcion = input("\n  Seleccione una opción: ").strip()
            self._procesar_opcion_principal(opcion)

    # -----------------------------------------------------------------------
    # Menú principal
    # -----------------------------------------------------------------------

    def _mostrar_menu_principal(self) -> None:
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

    def _procesar_opcion_principal(self, opcion: str) -> None:
        acciones = {
            "1": self._menu_productos,
            "2": self._registrar_venta,
            "3": self._registrar_compra,
            "4": self._ver_historial,
            "5": self._ver_alertas,
            "6": self._ver_estadisticas,
            "7": self._ver_logs,
            "0": self._salir,
        }
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print(fmt.error("Opción inválida. Ingrese un número del 0 al 7."))

    # -----------------------------------------------------------------------
    # Submenú de Productos
    # -----------------------------------------------------------------------

    def _menu_productos(self) -> None:
        while True:
            print(fmt.encabezado("Gestión de Productos"))
            print("  [1] Listar todos los productos")
            print("  [2] Buscar producto por nombre")
            print("  [3] Ver detalle de producto")
            print("  [4] Crear nuevo producto")
            print("  [5] Editar producto")
            print("  [6] Eliminar producto")
            print("  [0] Volver al menú principal")
            opcion = input("\n  Seleccione: ").strip()

            if opcion == "0":
                break
            elif opcion == "1":
                self._listar_productos()
            elif opcion == "2":
                self._buscar_producto()
            elif opcion == "3":
                self._ver_detalle_producto()
            elif opcion == "4":
                self._crear_producto()
            elif opcion == "5":
                self._editar_producto()
            elif opcion == "6":
                self._eliminar_producto()
            else:
                print(fmt.error("Opción inválida."))

    def _listar_productos(self) -> None:
        print(fmt.encabezado("Listado de Productos"))
        productos = self._facade.listar_productos()
        print(fmt.formatear_lista_productos(productos))
        input("\n  Presione Enter para continuar...")

    def _buscar_producto(self) -> None:
        print(fmt.encabezado("Buscar Producto"))
        nombre = val.leer_texto("Ingrese nombre o parte del nombre")
        productos = self._facade.buscar_productos(nombre)
        print(f"\n  Resultados para '{nombre}':")
        print(fmt.formatear_lista_productos(productos))
        input("\n  Presione Enter para continuar...")

    def _ver_detalle_producto(self) -> None:
        print(fmt.encabezado("Detalle de Producto"))
        id_producto = val.leer_texto("ID del producto")
        try:
            producto = self._facade.obtener_producto(id_producto)
            if producto is None:
                print(fmt.error(f"No se encontró el producto con ID '{id_producto}'."))
            else:
                print(fmt.formatear_producto_detalle(producto))
        except Exception as e:
            print(fmt.error(str(e)))
        input("\n  Presione Enter para continuar...")

    def _crear_producto(self) -> None:
        print(fmt.encabezado("Crear Nuevo Producto"))
        tipos = self._facade.tipos_producto_disponibles()
        print(f"  Tipos disponibles: {', '.join(tipos)}")

        try:
            tipo = val.leer_opcion("Tipo de producto", tipos)
            datos = self._capturar_datos_producto(tipo)
            producto = self._facade.crear_producto(tipo, datos)
            print(fmt.exito(f"Producto '{producto.nombre}' creado exitosamente con ID '{producto.id}'."))
        except ValueError as e:
            print(fmt.error(str(e)))
        input("\n  Presione Enter para continuar...")

    def _capturar_datos_producto(self, tipo: str) -> dict:
        """Captura los datos del usuario para crear un producto del tipo indicado."""
        datos = {
            "id": val.leer_texto("ID del producto (único)").upper(),
            "nombre": val.leer_texto("Nombre del producto"),
            "precio": val.leer_flotante("Precio unitario", minimo=0.0),
            "stock": val.leer_entero("Stock inicial", minimo=0),
            "stock_minimo": val.leer_entero("Stock mínimo de alerta", minimo=0),
        }

        if tipo == "simple":
            datos["categoria"] = val.leer_texto("Categoría (ej: Electrónica, Ropa)", obligatorio=False) or "General"

        elif tipo == "perecedero":
            datos["fecha_vencimiento"] = val.leer_fecha("Fecha de vencimiento")

        elif tipo == "digital":
            datos["url_descarga"] = val.leer_texto("URL de descarga", obligatorio=False)

        return datos

    def _editar_producto(self) -> None:
        print(fmt.encabezado("Editar Producto"))
        id_producto = val.leer_texto("ID del producto a editar").upper()

        producto = self._facade.obtener_producto(id_producto)
        if producto is None:
            print(fmt.error(f"No se encontró el producto con ID '{id_producto}'."))
            input("\n  Presione Enter para continuar...")
            return

        print(fmt.formatear_producto_detalle(producto))
        print(fmt.info("Deje en blanco para mantener el valor actual."))

        nuevos_datos = {}

        nombre = input(f"  Nuevo nombre [{producto.nombre}]: ").strip()
        if nombre:
            nuevos_datos["nombre"] = nombre

        precio_str = input(f"  Nuevo precio [${producto.precio:.2f}]: ").strip()
        if precio_str:
            try:
                nuevos_datos["precio"] = float(precio_str)
            except ValueError:
                print(fmt.error("Precio inválido, se mantendrá el actual."))

        stock_min_str = input(f"  Nuevo stock mínimo [{producto.stock_minimo}]: ").strip()
        if stock_min_str:
            try:
                nuevos_datos["stock_minimo"] = int(stock_min_str)
            except ValueError:
                print(fmt.error("Stock mínimo inválido, se mantendrá el actual."))

        # Campos específicos por tipo
        from models.producto import ProductoSimple, ProductoPerecedero, ProductoDigital

        if isinstance(producto, ProductoSimple):
            cat = input(f"  Nueva categoría [{producto.categoria}]: ").strip()
            if cat:
                nuevos_datos["categoria"] = cat

        elif isinstance(producto, ProductoPerecedero):
            fec = input(f"  Nueva fecha de vencimiento [{producto.fecha_vencimiento}] (YYYY-MM-DD): ").strip()
            if fec:
                try:
                    from datetime import date
                    nuevos_datos["fecha_vencimiento"] = date.fromisoformat(fec)
                except ValueError:
                    print(fmt.error("Fecha inválida, se mantendrá la actual."))

        elif isinstance(producto, ProductoDigital):
            url = input(f"  Nueva URL de descarga [{producto.url_descarga}]: ").strip()
            if url:
                nuevos_datos["url_descarga"] = url

        if not nuevos_datos:
            print(fmt.info("No se realizaron cambios."))
        else:
            try:
                self._facade.editar_producto(id_producto, nuevos_datos)
                print(fmt.exito("Producto actualizado correctamente."))
            except ValueError as e:
                print(fmt.error(str(e)))

        input("\n  Presione Enter para continuar...")

    def _eliminar_producto(self) -> None:
        print(fmt.encabezado("Eliminar Producto"))
        id_producto = val.leer_texto("ID del producto a eliminar").upper()

        producto = self._facade.obtener_producto(id_producto)
        if producto is None:
            print(fmt.error(f"No se encontró el producto con ID '{id_producto}'."))
            input("\n  Presione Enter para continuar...")
            return

        print(f"\n  Producto a eliminar: {fmt.formatear_producto(producto)}")

        if val.confirmar("Esta acción no se puede deshacer."):
            try:
                self._facade.eliminar_producto(id_producto)
                print(fmt.exito(f"Producto '{producto.nombre}' eliminado."))
            except ValueError as e:
                print(fmt.error(str(e)))
        else:
            print(fmt.info("Operación cancelada."))

        input("\n  Presione Enter para continuar...")

    # -----------------------------------------------------------------------
    # Ventas y Compras
    # -----------------------------------------------------------------------

    def _registrar_venta(self) -> None:
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

    def _registrar_compra(self) -> None:
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

    # -----------------------------------------------------------------------
    # Historial, alertas, estadísticas y logs
    # -----------------------------------------------------------------------

    def _ver_historial(self) -> None:
        print(fmt.encabezado("Historial de Transacciones"))
        transacciones = self._facade.historial_transacciones()
        print(fmt.formatear_lista_transacciones(transacciones))
        input("\n  Presione Enter para continuar...")

    def _ver_alertas(self) -> None:
        print(fmt.encabezado("Alertas de Stock Bajo"))
        productos = self._facade.productos_stock_bajo()
        if not productos:
            print(fmt.exito("Todos los productos tienen stock suficiente."))
        else:
            print(f"\n  {len(productos)} producto(s) con stock insuficiente:\n")
            for p in productos:
                print(fmt.formatear_producto(p))
        input("\n  Presione Enter para continuar...")

    def _ver_estadisticas(self) -> None:
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

    def _ver_logs(self) -> None:
        print(fmt.encabezado("Log de Eventos de Stock"))
        self._facade.mostrar_logs()
        input("\n  Presione Enter para continuar...")

    # -----------------------------------------------------------------------
    # Utilidades
    # -----------------------------------------------------------------------

    def _mostrar_bienvenida(self) -> None:
        print(f"\n{'═' * ANCHO_LINEA}")
        print(f"  MÓDULO DE GESTIÓN DE INVENTARIO")
        print(f"  Sistema profesional con patrones Factory, Facade y Observer")
        print(f"{'═' * ANCHO_LINEA}")
        print(f"  Versión 1.0  |  Python 3.8+  |  Sin dependencias externas")

    def _cargar_datos_demo(self) -> None:
        """Carga datos de muestra para facilitar las pruebas."""
        from datetime import date, timedelta

        productos_demo = [
            ("simple",     {"id": "ELEC001", "nombre": "Laptop HP 15",         "precio": 899.99, "stock": 10, "stock_minimo": 3, "categoria": "Electrónica"}),
            ("simple",     {"id": "ELEC002", "nombre": "Mouse Logitech M705",  "precio": 45.50,  "stock": 4,  "stock_minimo": 5, "categoria": "Electrónica"}),
            ("perecedero", {"id": "ALIM001", "nombre": "Yogur Natural",        "precio": 2.30,   "stock": 50, "stock_minimo": 10, "fecha_vencimiento": date.today() + timedelta(days=15)}),
            ("perecedero", {"id": "ALIM002", "nombre": "Leche Entera 1L",      "precio": 1.80,   "stock": 3,  "stock_minimo": 20, "fecha_vencimiento": date.today() + timedelta(days=5)}),
            ("digital",    {"id": "SOFT001", "nombre": "Licencia Office 365",  "precio": 149.00, "stock": 20, "stock_minimo": 5,  "url_descarga": "https://microsoft.com/office"}),
            ("digital",    {"id": "SOFT002", "nombre": "Adobe Photoshop",      "precio": 599.00, "stock": 2,  "stock_minimo": 3,  "url_descarga": "https://adobe.com/photoshop"}),
        ]

        for tipo, datos in productos_demo:
            try:
                self._facade.crear_producto(tipo, datos)
            except ValueError:
                pass  # Ignorar si ya existe (reinicio del programa)

        print(fmt.exito(f"Datos de demostración cargados ({len(productos_demo)} productos)."))

    def _salir(self) -> None:
        print(fmt.encabezado("Hasta luego"))
        print("  Gracias por usar el Módulo de Gestión de Inventario.")
        print(f"{'═' * ANCHO_LINEA}\n")
        self._corriendo = False


ANCHO_LINEA = 70
