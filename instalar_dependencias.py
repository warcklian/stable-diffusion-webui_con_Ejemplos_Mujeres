#!/usr/bin/env python3
"""
Instalador de Dependencias para Generación de Pasaportes
========================================================

Este script instala las dependencias necesarias para los scripts de generación
de imágenes de pasaportes venezolanos.

Dependencias:
- requests: Para comunicación con la API de WebUI
- Pillow: Para procesamiento de imágenes
- argparse: Para manejo de argumentos (incluido en Python estándar)
- json: Para manejo de archivos JSON (incluido en Python estándar)
- pathlib: Para manejo de rutas (incluido en Python estándar)

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import subprocess
import sys
import os

def instalar_dependencia(paquete: str) -> bool:
    """
    Instala una dependencia usando pip.
    
    Args:
        paquete: Nombre del paquete a instalar
        
    Returns:
        True si la instalación fue exitosa, False en caso contrario
    """
    try:
        print(f"📦 Instalando {paquete}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", paquete], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {paquete} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar {paquete}: {e}")
        print(f"   Salida de error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al instalar {paquete}: {e}")
        return False

def verificar_dependencia(paquete: str) -> bool:
    """
    Verifica si una dependencia está instalada.
    
    Args:
        paquete: Nombre del paquete a verificar
        
    Returns:
        True si está instalado, False en caso contrario
    """
    try:
        __import__(paquete)
        return True
    except ImportError:
        return False

def main():
    """Función principal del instalador."""
    print("🚀 Instalador de Dependencias para Generación de Pasaportes")
    print("=" * 60)
    
    # Lista de dependencias necesarias
    dependencias = [
        ("requests", "requests"),
        ("PIL", "Pillow")
    ]
    
    dependencias_faltantes = []
    
    # Verificar dependencias existentes
    print("🔍 Verificando dependencias existentes...")
    for modulo, paquete in dependencias:
        if verificar_dependencia(modulo):
            print(f"✅ {paquete} ya está instalado")
        else:
            print(f"❌ {paquete} no está instalado")
            dependencias_faltantes.append(paquete)
    
    if not dependencias_faltantes:
        print("\n🎉 ¡Todas las dependencias están instaladas!")
        return 0
    
    # Instalar dependencias faltantes
    print(f"\n📦 Instalando {len(dependencias_faltantes)} dependencias faltantes...")
    
    exitosos = 0
    for paquete in dependencias_faltantes:
        if instalar_dependencia(paquete):
            exitosos += 1
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE INSTALACIÓN")
    print("=" * 30)
    print(f"✅ Dependencias instaladas: {exitosos}")
    print(f"❌ Dependencias fallidas: {len(dependencias_faltantes) - exitosos}")
    
    if exitosos == len(dependencias_faltantes):
        print("\n🎉 ¡Todas las dependencias se instalaron correctamente!")
        print("💡 Ahora puedes usar los scripts de generación de pasaportes")
        return 0
    else:
        print(f"\n⚠️  {len(dependencias_faltantes) - exitosos} dependencias no se pudieron instalar")
        print("💡 Intenta instalar manualmente las dependencias faltantes:")
        for paquete in dependencias_faltantes:
            if not verificar_dependencia(paquete.split()[0].lower()):
                print(f"   pip install {paquete}")
        return 1

if __name__ == "__main__":
    exit(main())
