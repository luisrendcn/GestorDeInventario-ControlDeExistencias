"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  ARCHIVO: core/exceptions/inventario_error.py             ║
║                  RESPONSABILIDAD: Excepción base de inventario             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 ÚNICA RESPONSABILIDAD:
   Definir la excepción base para todas las excepciones del dominio.
   
💡 USO:
   Serve como clase padre para todas las excepciones de inventario,
   permitiendo capturar todas las excepciones del dominio de una vez.
"""


class InventarioError(Exception):
    """
    Excepción base para errores de inventario.
    
    RESPONSABILIDAD: 1
    • Clase base para todas las excepciones del dominio
    
    Uso:
        try:
            ...
        except InventarioError:
            # Captura todas las excepciones de negocios
    """
    pass
