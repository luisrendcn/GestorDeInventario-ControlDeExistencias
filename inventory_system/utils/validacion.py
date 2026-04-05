"""
utils/validacion.py
-------------------
Utilidades de validación y captura de input desde la consola.

Aplica DRY: centraliza la lectura y validación de inputs del usuario,
evitando duplicación en los controladores.
"""

from datetime import date
from typing import Optional


def leer_texto(prompt: str, obligatorio: bool = True) -> str:
    """Lee una cadena de texto del usuario."""
    while True:
        valor = input(f"  {prompt}: ").strip()
        if valor:
            return valor
        if not obligatorio:
            return ""
        print("  El campo no puede estar vacío. Intente de nuevo.")


def leer_flotante(prompt: str, minimo: float = 0.0, opcional: bool = False) -> Optional[float]:
    """Lee un número flotante del usuario."""
    while True:
        raw = input(f"  {prompt}: ").strip()
        if opcional and raw == "":
            return None
        try:
            valor = float(raw)
            if valor < minimo:
                print(f"  El valor debe ser >= {minimo}. Intente de nuevo.")
                continue
            return valor
        except ValueError:
            print("  Por favor ingrese un número válido.")


def leer_entero(prompt: str, minimo: int = 0, opcional: bool = False) -> Optional[int]:
    """Lee un número entero del usuario."""
    while True:
        raw = input(f"  {prompt}: ").strip()
        if opcional and raw == "":
            return None
        try:
            valor = int(raw)
            if valor < minimo:
                print(f"  El valor debe ser >= {minimo}. Intente de nuevo.")
                continue
            return valor
        except ValueError:
            print("  Por favor ingrese un número entero válido.")


def leer_fecha(prompt: str) -> date:
    """Lee una fecha en formato YYYY-MM-DD del usuario."""
    while True:
        raw = input(f"  {prompt} (YYYY-MM-DD): ").strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("  Formato de fecha inválido. Use YYYY-MM-DD. Ejemplo: 2025-12-31")


def leer_opcion(prompt: str, opciones: list) -> str:
    """Lee una opción de una lista de valores válidos."""
    opciones_str = "/".join(str(o) for o in opciones)
    while True:
        valor = input(f"  {prompt} [{opciones_str}]: ").strip().lower()
        if valor in [str(o).lower() for o in opciones]:
            return valor
        print(f"  Opción inválida. Elija entre: {opciones_str}")


def confirmar(prompt: str) -> bool:
    """Solicita confirmación sí/no."""
    respuesta = leer_opcion(f"{prompt} ¿Confirmar?", ["s", "n"])
    return respuesta == "s"
