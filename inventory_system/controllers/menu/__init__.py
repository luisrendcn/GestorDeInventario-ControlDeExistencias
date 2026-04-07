"""
menu/
-----
Módulo responsable de la interfaz CLI organizado por funcionalidad.

Estructura:
    - menu_controller.py: Clase coordinadora principal
    - opciones_principales.py: Manejo de opciones del menú principal
    - productos.py: Gestión de productos
    - transacciones.py: Ventas y compras
    - vistas.py: Visualización (historial, alertas, estadísticas)
    - utilidades.py: Funciones auxiliares (inicialización, salida)
"""

from .menu_controller import MenuController

__all__ = ['MenuController']
