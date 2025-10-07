#!/usr/bin/env python3
"""
Instalador de Controles de Pasaportes en txt2img
===============================================

Este script verifica que la integración de pasaportes en txt2img esté funcionando.

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import os
from pathlib import Path

def main():
    print("🚀 Verificador de Integración de Pasaportes en txt2img")
    print("=" * 55)
    
    # Verificar que estamos en el directorio correcto
    if not Path("webui.py").exists():
        print("❌ Error: Ejecuta este script desde el directorio raíz de WebUI")
        return 1
    
    # Verificar archivos modificados
    archivos_modificados = [
        "modules/ui.py"
    ]
    
    print("🔍 Verificando archivos modificados...")
    for archivo in archivos_modificados:
        if Path(archivo).exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} no encontrado")
            return 1
    
    # Verificar archivos requeridos
    archivos_requeridos = [
        "generar_pasaportes.py",
        "Consulta/gui_config.json",
        "Consulta/optimized_prompts.json",
        "Consulta/intelligent_ethnic_data.json"
    ]
    
    print("\n🔍 Verificando archivos requeridos...")
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} no encontrado")
            return 1
    
    print("\n🎉 ¡Integración completada exitosamente!")
    print("\n📋 Cómo usar:")
    print("1. Ejecuta WebUI: ./webui.sh")
    print("2. Ve a la pestaña 'txt2img'")
    print("3. Busca el acordeón '🇻🇪 Pasaportes Venezolanos'")
    print("4. Selecciona nacionalidad, género y edad")
    print("5. Haz clic en '📝 Aplicar Prompt de Pasaporte'")
    print("6. Ajusta otros parámetros si es necesario")
    print("7. Haz clic en 'Generate' para crear la imagen")
    
    print(f"\n📁 Las imágenes se guardarán en:")
    print(f"   - Imágenes individuales: outputs/txt2img-images/")
    print(f"   - Generación masiva: outputs/pasaportes_masivos/")
    
    print(f"\n📋 Formato de nombres para generación masiva:")
    print(f"   pasaporte_{nacionalidad}_{genero}_{edad}_{timestamp}.png")
    
    print(f"\n🌍 Nacionalidades disponibles:")
    try:
        from generar_pasaportes import GeneradorPasaportes
        consulta_dir = Path("Consulta")
        if consulta_dir.exists():
            generador = GeneradorPasaportes(str(consulta_dir))
            nacionalidades = list(generador.datos_etnicos.keys())
            for nacionalidad in nacionalidades:
                print(f"   - {nacionalidad}")
        else:
            print("   - venezuelan, cuban, haitian, dominican, mexican, etc.")
    except Exception as e:
        print(f"   - Error al cargar nacionalidades: {e}")
    
    return 0

if __name__ == "__main__":
    exit(main())
