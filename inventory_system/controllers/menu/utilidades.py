"""
menu/utilidades.py
==================
Mixin que maneja funciones auxiliares (inicialización, bienvenida, datos demo, salida).
"""

from datetime import date, timedelta
from utils import formato as fmt


ANCHO_LINEA = 70


class UtilidadesMixin:
    """Mixin para funciones auxiliares de inicialización y salida."""

    def mostrar_bienvenida(self) -> None:
        """Muestra el mensaje de bienvenida."""
        print(f"\n{'═' * ANCHO_LINEA}")
        print(f"  MÓDULO DE GESTIÓN DE INVENTARIO")
        print(f"  Sistema profesional con patrones Factory, Facade y Observer")
        print(f"{'═' * ANCHO_LINEA}")
        print(f"  Versión 1.0  |  Python 3.8+  |  Sin dependencias externas")

    def cargar_datos_demo(self) -> None:
        """Carga datos de muestra para facilitar las pruebas."""
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

    def salir(self) -> None:
        """Muestra mensaje de despedida y termina la aplicación."""
        print(fmt.encabezado("Hasta luego"))
        print("  Gracias por usar el Módulo de Gestión de Inventario.")
        print(f"{'═' * ANCHO_LINEA}\n")
        self._corriendo = False
