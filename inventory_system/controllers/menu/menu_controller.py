"""
menu/menu_controller.py
=======================
Controlador principal de la interfaz CLI.

Responsabilidad:
    - Coordinar la interacción entre el usuario y el sistema
    - Delegar operaciones a mixins especializados
    - Mantener el bucle principal

Aplica:
    - Separación de responsabilidades por funcionalidad
    - Mixins para organizar métodos relacionados
    - Patrón Facade para acceso a la lógica de negocio
"""

import sys
import os

# Asegura que los imports funcionen desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.facade import SistemaInventarioFacade
from .opciones_principales import OpcionesPrincipalesMixin
from .productos import ProductosMixin
from .transacciones import TransaccionesMixin
from .vistas import VistasMixin
from .utilidades import UtilidadesMixin


class MenuController(
    OpcionesPrincipalesMixin,
    ProductosMixin,
    TransaccionesMixin,
    VistasMixin,
    UtilidadesMixin
):
    """
    Controlador de la interfaz CLI.
    
    Hereda funcionalidad de múltiples mixins:
    - OpcionesPrincipalesMixin: Menú principal y navegación
    - ProductosMixin: Gestión de productos
    - TransaccionesMixin: Ventas y compras
    - VistasMixin: Historial, alertas, estadísticas, logs
    - UtilidadesMixin: Inicialización, bienvenida, salida
    """

    def __init__(self):
        self._facade = SistemaInventarioFacade()
        self._corriendo = True

    def iniciar(self) -> None:
        """Punto de entrada del controlador. Muestra el menú principal en bucle."""
        self.mostrar_bienvenida()
        self.cargar_datos_demo()

        while self._corriendo:
            self.mostrar_menu_principal()
            opcion = input("\n  Seleccione una opción: ").strip()
            self.procesar_opcion_principal(opcion)
