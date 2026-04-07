#!/usr/bin/env python3
"""
scripts/import_productos.py
===========================
Script para importar productos desde un archivo Excel.

Uso:
    python import_productos.py generar_plantilla [tipo_empresa]
    python import_productos.py validar <archivo.xlsx>
    python import_productos.py importar <archivo.xlsx>

Ejemplos:
    # Generar plantilla para empresa de alimentos
    python import_productos.py generar_plantilla alimentos

    # Validar estructura del archivo
    python import_productos.py validar productos.xlsx

    # Importar productos
    python import_productos.py importar productos.xlsx
"""

import sys
import os
from pathlib import Path
from datetime import date

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from inventory_system.models.inventario import Inventario
from inventory_system.patterns.observer import SujetoStock
from inventory_system.services import InventarioService, ImportadorExcel
from inventory_system.utils import generar_plantilla_excel, validar_estructura_excel


def main():
    """Punto de entrada del script."""
    if len(sys.argv) < 2:
        print_ayuda()
        sys.exit(1)

    comando = sys.argv[1].lower()

    if comando == 'generar_plantilla':
        cmd_generar_plantilla()
    elif comando == 'validar':
        cmd_validar()
    elif comando == 'importar':
        cmd_importar()
    else:
        print(f"❌ Comando desconocido: {comando}")
        print_ayuda()
        sys.exit(1)


def cmd_generar_plantilla():
    """Genera una plantilla de Excel."""
    tipo_empresa = sys.argv[2] if len(sys.argv) > 2 else 'general'
    
    tipos_validos = ['general', 'alimentos', 'ropa', 'tecnologia']
    if tipo_empresa not in tipos_validos:
        print(f"❌ Tipo de empresa inválido. Opciones: {', '.join(tipos_validos)}")
        sys.exit(1)

    # Generar nombre de archivo
    hoy = date.today().strftime('%Y%m%d')
    nombre_archivo = f"productos_plantilla_{tipo_empresa}_{hoy}.xlsx"
    ruta_salida = Path('./') / nombre_archivo

    try:
        generar_plantilla_excel(str(ruta_salida), tipo_empresa)
        print(f"\n✅ Plantilla guardada en: {ruta_salida}")
        print(f"\n📋 Próximos pasos:")
        print(f"   1. Abre {nombre_archivo} en Excel")
        print(f"   2. Edita la fila 'Instrucciones' para entender el formato")
        print(f"   3. Reemplaza los datos de ejemplo con tus productos")
        print(f"   4. Guarda el archivo")
        print(f"   5. Ejecuta: python import_productos.py importar {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error generando plantilla: {str(e)}")
        sys.exit(1)


def cmd_validar():
    """Valida la estructura de un archivo Excel."""
    if len(sys.argv) < 3:
        print("❌ Uso: python import_productos.py validar <archivo.xlsx>")
        sys.exit(1)

    ruta_archivo = sys.argv[2]
    campos_obligatorios = ['nombre', 'precio_venta', 'stock']

    try:
        es_valido = validar_estructura_excel(ruta_archivo, campos_obligatorios)
        if not es_valido:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def cmd_importar():
    """Importa productos desde un archivo Excel."""
    if len(sys.argv) < 3:
        print("❌ Uso: python import_productos.py importar <archivo.xlsx>")
        sys.exit(1)

    ruta_archivo = sys.argv[2]

    print(f"\n📂 Importando productos desde: {ruta_archivo}")
    print("=" * 70)

    try:
        # Inicializar componentes
        inventario = Inventario()
        sujeto = SujetoStock()

        # Importar
        importador = ImportadorExcel(ruta_archivo)
        resultado = importador.importar(inventario, sujeto)

        # Mostrar resultado
        print(resultado.reporte_texto())

        # Detalles de productos creados
        if resultado.productos_creados:
            print("\n📦 PRODUCTOS IMPORTADOS EXITOSAMENTE:")
            print("-" * 70)
            for producto in resultado.productos_creados:
                print(f"  ✓ [{producto.tipo()}] {producto.nombre}")
                print(f"    ID: {producto.id} | Precio: ${producto.precio:.2f} | Stock: {producto.stock}")
                print(f"    {producto.info_adicional()}")
                print()

        # Resumen final
        print("=" * 70)
        if resultado.fallidos == 0:
            print(f"✅ IMPORTACIÓN COMPLETADA: {resultado.exitosos} productos importados sin errores")
        else:
            print(f"⚠️  IMPORTACIÓN PARCIAL: {resultado.exitosos} exitosos, {resultado.fallidos} fallidos")

        sys.exit(0 if resultado.fallidos == 0 else 1)

    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Archivo inválido: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error durante importación: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_ayuda():
    """Muestra el mensaje de ayuda."""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    IMPORTADOR DE PRODUCTOS - AYUDA                        ║
╚════════════════════════════════════════════════════════════════════════════╝

COMANDO: generar_plantilla [tipo_empresa]
  Genera un archivo Excel de plantilla con ejemplos.
  
  Tipos de empresa:
    - general      (default) - Plantilla genérica
    - alimentos    - Con columna de fecha_vencimiento
    - ropa         - Plantilla para ropa
    - tecnologia   - Con columna de url_descarga
  
  Ejemplos:
    python import_productos.py generar_plantilla alimentos
    python import_productos.py generar_plantilla ropa


COMANDO: validar <archivo.xlsx>
  Valida la estructura de un archivo Excel.
  
  Ejemplo:
    python import_productos.py validar productos.xlsx


COMANDO: importar <archivo.xlsx>
  Importa productos desde un archivo Excel.
  
  Columns requeridas:
    - nombre              (obligatorio)
    - precio_venta        (obligatorio)
    - stock               (obligatorio)
  
  Columnas opcionales:
    - categoria           (default: "General")
    - precio_compra       (para referencia)
    - stock_minimo        (default: 5)
    - fecha_vencimiento   (para productos perecederos)
    - url_descarga        (para productos digitales)
  
  Ejemplo:
    python import_productos.py importar productos.xlsx


FORMATO DE DATOS:
  - Precios: números decimales con punto (ej: 19.99)
  - Stock: números enteros (ej: 100)
  - Fechas: YYYY-MM-DD (ej: 2025-12-31)
  - URLs: texto completo con protocolo (ej: https://...)

FLUJO RECOMENDADO:
  1. Generar plantilla: python import_productos.py generar_plantilla alimentos
  2. Editar en Excel
  3. Guardar el archivo
  4. Validar: python import_productos.py validar productos.xlsx
  5. Importar: python import_productos.py importar productos.xlsx

Para más información, consulta la documentación en IMPORTACION_MASIVA.md
""")


if __name__ == '__main__':
    main()
