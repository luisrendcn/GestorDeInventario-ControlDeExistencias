"""
main.py
-------
Punto de entrada del Módulo de Gestión de Inventario.

Responsabilidad:
    - Configurar el entorno de Python (path).
    - Instanciar el controlador principal.
    - Capturar interrupciones de teclado (Ctrl+C) de forma elegante.

Uso:
    python main.py
"""

import sys
import os

# Agrega el directorio del proyecto al path para que los imports funcionen
# sin importar desde qué directorio se ejecute el script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.menu_controller import MenuController


def main() -> None:
    """Función principal que inicia la aplicación."""
    controlador = MenuController()
    try:
        controlador.iniciar()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario. ¡Hasta luego!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
