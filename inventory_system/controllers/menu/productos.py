"""
menu/productos.py
=================
Mixin que maneja la gestión de productos.
"""

from datetime import date
from utils import formato as fmt
from utils import validacion as val


class ProductosMixin:
    """Mixin para gestionar operaciones con productos."""

    def listar_productos(self) -> None:
        """Lista todos los productos disponibles."""
        print(fmt.encabezado("Listado de Productos"))
        productos = self._facade.listar_productos()
        print(fmt.formatear_lista_productos(productos))
        input("\n  Presione Enter para continuar...")

    def buscar_producto(self) -> None:
        """Busca productos por nombre."""
        print(fmt.encabezado("Buscar Producto"))
        nombre = val.leer_texto("Ingrese nombre o parte del nombre")
        productos = self._facade.buscar_productos(nombre)
        print(f"\n  Resultados para '{nombre}':")
        print(fmt.formatear_lista_productos(productos))
        input("\n  Presione Enter para continuar...")

    def ver_detalle_producto(self) -> None:
        """Muestra el detalle completo de un producto."""
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

    def crear_producto(self) -> None:
        """Crea un nuevo producto."""
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

    def editar_producto(self) -> None:
        """Edita un producto existente."""
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

    def eliminar_producto(self) -> None:
        """Elimina un producto existente."""
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

    def importar_productos_excel(self) -> None:
        """Importa productos desde un archivo Excel."""
        try:
            from services import ImportadorExcel
        except ImportError:
            print(fmt.error("ImportadorExcel no está disponible."))
            input("\n  Presione Enter para continuar...")
            return

        print(fmt.encabezado("Importar Productos desde Excel"))
        print("""
  Opciones:
  [1] Importar desde archivo existente
  [2] Generar plantilla de ejemplo
  [0] Volver
        """)
        
        opcion = input("  Seleccione: ").strip()

        if opcion == "0":
            return
        elif opcion == "2":
            self._generar_plantilla_excel()
            return
        elif opcion != "1":
            print(fmt.error("Opción inválida."))
            input("\n  Presione Enter para continuar...")
            return

        # Pedir ruta del archivo
        ruta_archivo = val.leer_texto("Ruta del archivo Excel (.xlsx)")
        
        try:
            print(f"\n  📂 Importando desde: {ruta_archivo}")
            print("  " + "=" * 66)

            # Crear importador
            importador = ImportadorExcel(ruta_archivo)
            
            # Importar
            resultado = importador.importar(
                self._facade._inventario,
                self._facade._sujeto
            )

            # Mostrar resultado
            print(resultado.reporte_texto())

            # Detalles de productos creados
            if resultado.productos_creados:
                print("\n  📦 PRODUCTOS IMPORTADOS:")
                print("  " + "-" * 66)
                for producto in resultado.productos_creados[:5]:  # Mostrar primeros 5
                    print(f"    ✓ [{producto.tipo()}] {producto.nombre}")
                    print(f"      Precio: ${producto.precio:.2f} | Stock: {producto.stock}")
                
                if len(resultado.productos_creados) > 5:
                    print(f"    ... y {len(resultado.productos_creados) - 5} más")

            # Resumen
            print("\n  " + "=" * 66)
            if resultado.fallidos == 0:
                print(fmt.exito(f"✅ IMPORTACIÓN EXITOSA: {resultado.exitosos} productos"))
            else:
                print(fmt.info(f"⚠️  {resultado.exitosos} exitosos, {resultado.fallidos} errores"))

        except FileNotFoundError:
            print(fmt.error(f"Archivo no encontrado: {ruta_archivo}"))
        except ValueError as e:
            print(fmt.error(f"Archivo inválido: {str(e)}"))
        except ImportError:
            print(fmt.error("Se requiere openpyxl. Ejecuta: pip install openpyxl"))
        except Exception as e:
            print(fmt.error(f"Error durante importación: {str(e)}"))

        input("\n  Presione Enter para continuar...")

    @staticmethod
    def _generar_plantilla_excel() -> None:
        """Genera un archivo plantilla de Excel."""
        try:
            from utils import generar_plantilla_excel
        except ImportError:
            print(fmt.error("Utilidades de Excel no disponibles."))
            return

        print("\n  Tipos de empresa:")
        print("    [1] General")
        print("    [2] Alimentos (con vencimiento)")
        print("    [3] Ropa")
        print("    [4] Tecnología (con URL descarga)")
        
        tipo_opcion = input("\n  Seleccione tipo de empresa [1]: ").strip() or "1"
        
        tipos_map = {
            "1": "general",
            "2": "alimentos",
            "3": "ropa",
            "4": "tecnologia"
        }
        
        tipo_empresa = tipos_map.get(tipo_opcion, "general")

        try:
            from datetime import date
            hoy = date.today().strftime('%Y%m%d')
            nombre_archivo = f"productos_plantilla_{tipo_empresa}_{hoy}.xlsx"
            
            generar_plantilla_excel(nombre_archivo, tipo_empresa)
            print(fmt.exito(f"Plantilla creada: {nombre_archivo}"))
            
        except Exception as e:
            print(fmt.error(f"Error generando plantilla: {str(e)}"))

