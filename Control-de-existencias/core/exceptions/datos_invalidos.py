"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: core/exceptions/datos_invalidos.py              ║
║                  RESPONSABILIDAD: Validación de datos fallida              ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Indicar que los datos proporcionados no cumplen validación.
   
💡 CASOS:
   • JSON malformado
   • Parámetros con valores inválidos
   • Tipos de datos incorrectos
   • Valores fuera de rango
"""

from core.exceptions.inventario_error import InventarioError


class DatosInvalidos(InventarioError):
    """
    Los datos proporcionados son inválidos.
    
    RESPONSABILIDAD: 1
    • Indicar que la validación de datos falló
    
    Lanzada por:
        • CrearProductoService.validar()
        • ActualizarProductoService.validar()
        • Schema validators
    """
    pass
