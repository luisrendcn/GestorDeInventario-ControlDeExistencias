"""
producto/serializacion.py
==========================
Responsabilidad única: Convertir producto a formato serializable.
"""


class SerializacionMixin:
    """Mixin especializado en serialización."""
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para serialización."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "descripcion": self.descripcion,
            "valor_total": self.valor_total,
            "stock_bajo": self.stock_bajo,
            "agotado": self.agotado,
        }
