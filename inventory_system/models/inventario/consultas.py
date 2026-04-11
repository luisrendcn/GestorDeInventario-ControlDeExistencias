"""
inventario/consultas.py
=======================
Mixin que maneja consultas y estadísticas del inventario.

Responsabilidad:
    - Consultas de existencias
    - Análisis de stock
    - Estadísticas y reportes
"""

from typing import List, Dict, Tuple


class ConsultasMixin:
    """
    Mixin para consultas, filtros y estadísticas de inventario.
    Especializado en Control de Existencias.
    """

    def existe(self, id: str) -> bool:
        """
        Comprueba si existe un producto con ese ID.
        
        Args:
            id: ID del producto a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return id in self._productos

    def total_productos(self) -> int:
        """
        Número total de productos en el inventario.
        
        Returns:
            Cantidad de productos únicos
        """
        return len(self._productos)

    def valor_total_inventario(self) -> float:
        """
        Calcula el valor total del inventario (precio × stock).
        
        Returns:
            Valor monetario total en existencias
        """
        return sum(p.precio * p.stock for p in self._productos.values())

    def productos_con_stock_bajo(self) -> List['Producto']:
        """
        Retorna productos cuyo stock está por debajo del mínimo.
        
        Returns:
            Lista de productos con stock bajo
        """
        return [p for p in self._productos.values() if p.stock_bajo]

    def productos_agotados(self) -> List['Producto']:
        """
        Retorna productos sin stock (stock = 0).
        
        Returns:
            Lista de productos agotados
        """
        return [p for p in self._productos.values() if p.stock == 0]

    def productos_disponibles(self) -> List['Producto']:
        """
        Retorna productos con stock disponible (stock > 0).
        
        Returns:
            Lista de productos disponibles
        """
        return [p for p in self._productos.values() if p.stock > 0]

    def obtener_stock_actual(self, producto_id: str) -> int:
        """
        Obtiene el stock actual de un producto.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Stock actual del producto
            
        Raises:
            ValueError: Si el producto no existe
        """
        producto = self.obtener_o_error(producto_id)
        return producto.stock

    def obtener_productos_por_rango_stock(self, minimo: int, maximo: int) -> List['Producto']:
        """
        Retorna productos cuyo stock está dentro de un rango.
        
        Args:
            minimo: Stock mínimo (inclusive)
            maximo: Stock máximo (inclusive)
            
        Returns:
            Lista de productos en el rango especificado
        """
        return [
            p for p in self._productos.values() 
            if minimo <= p.stock <= maximo
        ]

    def obtener_stock_total(self) -> int:
        """
        Obtiene la cantidad total de unidades en stock.
        
        Returns:
            Suma total de unidades de todos los productos
        """
        return sum(p.stock for p in self._productos.values())

    def obtener_reporte_stock(self) -> Dict:
        """
        Genera un reporte completo del estado del inventario.
        
        Returns:
            Diccionario con estadísticas de stock
        """
        productos_todos = list(self._productos.values())
        
        return {
            'total_productos': self.total_productos(),
            'total_unidades': self.obtener_stock_total(),
            'valor_total': self.valor_total_inventario(),
            'productos_disponibles': len(self.productos_disponibles()),
            'productos_agotados': len(self.productos_agotados()),
            'productos_stock_bajo': len(self.productos_con_stock_bajo()),
            'stock_promedio': (
                self.obtener_stock_total() / self.total_productos() 
                if self.total_productos() > 0 else 0
            ),
            'precio_promedio': (
                sum(p.precio for p in productos_todos) / len(productos_todos)
                if productos_todos else 0
            ),
            'valor_promedio_producto': (
                self.valor_total_inventario() / self.total_productos()
                if self.total_productos() > 0 else 0
            )
        }

    def obtener_productos_mayor_stock(self, limite: int = 5) -> List['Producto']:
        """
        Retorna los productos con mayor cantidad de stock.
        
        Args:
            limite: Número máximo de productos a retornar
            
        Returns:
            Lista de productos ordenados por stock descendente
        """
        return sorted(
            self._productos.values(),
            key=lambda p: p.stock,
            reverse=True
        )[:limite]

    def obtener_productos_menor_stock(self, limite: int = 5) -> List['Producto']:
        """
        Retorna los productos con menor cantidad de stock.
        
        Args:
            limite: Número máximo de productos a retornar
            
        Returns:
            Lista de productos ordenados por stock ascendente
        """
        return sorted(
            self._productos.values(),
            key=lambda p: p.stock
        )[:limite]

    def obtener_productos_mayor_valor(self, limite: int = 5) -> List['Producto']:
        """
        Retorna los productos con mayor valor total (precio × stock).
        
        Args:
            limite: Número máximo de productos a retornar
            
        Returns:
            Lista de productos ordenados por valor total descendente
        """
        return sorted(
            self._productos.values(),
            key=lambda p: p.precio * p.stock,
            reverse=True
        )[:limite]

    def analizar_stock_por_rango(self) -> Dict[str, List['Producto']]:
        """
        Agrupa productos en categorías según su nivel de stock.
        
        Returns:
            Diccionario con categorías: 'agotado', 'critico', 'bajo', 'normal', 'alto'
        """
        agotado = []
        critico = []
        bajo = []
        normal = []
        alto = []
        
        for producto in self._productos.values():
            if producto.stock == 0:
                agotado.append(producto)
            elif producto.stock < producto.stock_minimo // 2:
                critico.append(producto)
            elif producto.stock < producto.stock_minimo:
                bajo.append(producto)
            elif producto.stock <= producto.stock_minimo * 2:
                normal.append(producto)
            else:
                alto.append(producto)
        
        return {
            'agotado': agotado,
            'critico': critico,
            'bajo': bajo,
            'normal': normal,
            'alto': alto
        }

    def validar_integridad_stock(self) -> Tuple[bool, List[str]]:
        """
        Valida que todos los stocks sean válidos (no negativos).
        
        Returns:
            Tupla (es_válido, lista_de_errores)
        """
        errores = []
        for producto in self._productos.values():
            if producto.stock < 0:
                errores.append(
                    f"Stock negativo en '{producto.nombre}' (ID: {producto.id}): {producto.stock}"
                )
        
        return (len(errores) == 0, errores)
