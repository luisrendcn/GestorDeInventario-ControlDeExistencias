"""
utils/formato.py
----------------
Utilidades de presentación para la interfaz de consola.

Aplica DRY: centraliza toda la lógica de formato para evitar duplicación.
"""

from typing import List, Any
from models.producto import Producto
from models.transaccion import Transaccion


ANCHO_LINEA = 70


def linea_separadora(caracter: str = "─", ancho: int = ANCHO_LINEA) -> str:
    return caracter * ancho


def encabezado(titulo: str, caracter: str = "═") -> str:
    linea = linea_separadora(caracter)
    return f"\n{linea}\n  {titulo.upper()}\n{linea}"


def subencabezado(titulo: str) -> str:
    return f"\n  ── {titulo} ──"


def formatear_producto(producto: Producto, indice: int = None) -> str:
    """Retorna una representación de una línea de un producto."""
    prefijo = f"{indice:>3}. " if indice is not None else "  • "
    alerta = " ⚠ STOCK BAJO" if producto.stock_bajo else ""
    return (
        f"{prefijo}[{producto.id}] {producto.nombre:<25} "
        f"${producto.precio:>8.2f}  "
        f"Stock: {producto.stock:>4}/{producto.stock_minimo:<4}"
        f" ({producto.tipo()}){alerta}"
    )


def formatear_producto_detalle(producto: Producto) -> str:
    """Retorna la representación detallada de un producto."""
    lineas = [
        subencabezado(f"DETALLE DEL PRODUCTO"),
        f"  ID          : {producto.id}",
        f"  Nombre      : {producto.nombre}",
        f"  Tipo        : {producto.tipo()}",
        f"  Precio      : ${producto.precio:.2f}",
        f"  Stock actual: {producto.stock}",
        f"  Stock mínimo: {producto.stock_minimo}",
        f"  Info extra  : {producto.info_adicional()}",
    ]
    if producto.stock_bajo:
        lineas.append(f"  ⚠  ADVERTENCIA: Stock por debajo del mínimo.")
    return "\n".join(lineas)


def formatear_lista_productos(productos: List[Producto]) -> str:
    """Formatea una lista de productos para mostrar en consola."""
    if not productos:
        return "  No se encontraron productos."
    lineas = []
    for i, p in enumerate(productos, start=1):
        lineas.append(formatear_producto(p, i))
    return "\n".join(lineas)


def formatear_transaccion(transaccion: Transaccion, indice: int = None) -> str:
    """Retorna una representación de una línea de una transacción."""
    prefijo = f"{indice:>3}. " if indice is not None else "  • "
    return (
        f"{prefijo}[{transaccion.tipo.value:<6}] "
        f"{transaccion.fecha.strftime('%Y-%m-%d %H:%M')}  "
        f"{transaccion.producto_nombre:<25} "
        f"x{transaccion.cantidad:>3}  "
        f"@ ${transaccion.precio_unitario:>8.2f}  "
        f"= ${transaccion.total:>10.2f}"
    )


def formatear_lista_transacciones(transacciones: List[Transaccion]) -> str:
    """Formatea la lista de transacciones."""
    if not transacciones:
        return "  No hay transacciones registradas."
    lineas = []
    for i, t in enumerate(transacciones, start=1):
        lineas.append(formatear_transaccion(t, i))
    return "\n".join(lineas)


def exito(mensaje: str) -> str:
    return f"\n  ✓ {mensaje}"


def error(mensaje: str) -> str:
    return f"\n  ✗ ERROR: {mensaje}"


def info(mensaje: str) -> str:
    return f"\n  ℹ {mensaje}"
