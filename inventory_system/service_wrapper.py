#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess

os.chdir(r"C:\Users\luisr\OneDrive\Proyectos\Gestion de inventario\Code-Companion\inventory_system")

max_retries = 0  # Reintentos infinitos
retry_count = 0

while True:
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando servidor...")
        result = subprocess.run([r"C:\Users\luisr\AppData\Local\Python\pythoncore-3.14-64\python.exe", "run.py"], check=False)
        
        if result.returncode != 0:
            retry_count += 1
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ Servidor falló (reintento {retry_count})")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
        else:
            break
    except KeyboardInterrupt:
        print("\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Servicio detenido")
        break
    except Exception as e:
        retry_count += 1
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error: {e}")
        time.sleep(5)
