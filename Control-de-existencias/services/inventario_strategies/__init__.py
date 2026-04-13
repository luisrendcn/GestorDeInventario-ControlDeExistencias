"""
PATRÓN: STRATEGY

Estrategias de movimiento de inventario.
Cada estrategia tiene su PROPIA CARPETA con responsabilidades separadas.

ESTRUCTURA:
├── entrada/          → Estrategia de entrada (suma sin validación)
├── salida/           → Estrategia de salida (resta con validación)
└── ajuste/           → Estrategia de ajuste (asigna valor exacto)

DENTRO DE CADA CARPETA:
├── validar_*.py      → Validación de datos
├── (operacion).py    → Operación aritmética/lógica
├── registrar_*.py    → Persistencia en BD
├── *_strategy.py     → Clase orquestadora
└── __init__.py       → Exports
"""

from services.inventario_strategies.entrada import EntradaStrategy
from services.inventario_strategies.salida import SalidaStrategy
from services.inventario_strategies.ajuste import AjusteStrategy

__all__ = [
    'EntradaStrategy',
    'SalidaStrategy',
    'AjusteStrategy',
]
