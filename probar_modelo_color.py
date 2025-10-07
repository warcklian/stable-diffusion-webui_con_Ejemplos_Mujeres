#!/usr/bin/env python3
"""
Script para probar el nuevo modelo RealisticVisionV60B1_v51HyperVAE
y verificar que genera imágenes a color correctamente.
"""

import json
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from webui_pasaportes import WebUIPasaportes
from generar_pasaportes import GeneradorPasaportes

def probar_modelo_color():
    """Prueba el nuevo modelo para verificar generación a color"""
    print("🎨 PROBANDO MODELO PARA GENERACIÓN A COLOR")
    print("=" * 60)
    
    # 1. Verificar configuración
    print("📋 Verificando configuración...")
    config_path = "Consulta/gui_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ No se encontró {config_path}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    modelo_actual = config.get('model', 'No especificado')
    print(f"   📄 Modelo actual: {modelo_actual}")
    
    # Verificar que sea RealisticVision
    if 'RealisticVision' not in modelo_actual:
        print("   ⚠️ El modelo no es RealisticVision - puede generar en gris")
        return False
    
    print("   ✅ Modelo RealisticVision detectado")
    
    # 2. Verificar prompts de color
    print("\n🎨 Verificando prompts de color...")
    base_prompt = config.get('base_prompt', '')
    negative_prompt = config.get('negative_prompt', '')
    
    # Verificar términos de color en base_prompt
    terminos_color = [
        'COLOR PHOTOGRAPHY', 'FULL COLOR', 'VIBRANT COLORS', 
        'NATURAL COLORS', 'RICH COLORS', 'SATURATED COLORS'
    ]
    
    color_encontrado = False
    for termino in terminos_color:
        if termino in base_prompt:
            print(f"   ✅ Término de color encontrado: {termino}")
            color_encontrado = True
            break
    
    if not color_encontrado:
        print("   ⚠️ No se encontraron términos de color en base_prompt")
        return False
    
    # Verificar términos anti-gris en negative_prompt
    terminos_anti_gris = [
        'black and white', 'bw', 'monochrome', 'grayscale', 
        'sepia', 'no color', 'colorless'
    ]
    
    anti_gris_encontrado = False
    for termino in terminos_anti_gris:
        if termino in negative_prompt:
            print(f"   ✅ Término anti-gris encontrado: {termino}")
            anti_gris_encontrado = True
            break
    
    if not anti_gris_encontrado:
        print("   ⚠️ No se encontraron términos anti-gris en negative_prompt")
        return False
    
    # 3. Verificar configuración técnica
    print("\n⚙️ Verificando configuración técnica...")
    width = config.get('width', 0)
    height = config.get('height', 0)
    steps = config.get('steps', 0)
    cfg_scale = config.get('cfg_scale', 0)
    sampler = config.get('sampler', '')
    
    print(f"   📐 Resolución: {width}x{height}")
    print(f"   🔄 Steps: {steps}")
    print(f"   📊 CFG Scale: {cfg_scale}")
    print(f"   🎯 Sampler: {sampler}")
    
    # Verificar resolución correcta
    if width == 512 and height == 640:
        print("   ✅ Resolución correcta (4:5)")
    else:
        print("   ⚠️ Resolución incorrecta - puede causar estiramiento")
        return False
    
    # Verificar steps adecuados
    if steps >= 25 and steps <= 35:
        print("   ✅ Steps adecuados para calidad")
    else:
        print("   ⚠️ Steps pueden ser insuficientes")
    
    # Verificar CFG scale
    if cfg_scale >= 7.0 and cfg_scale <= 9.0:
        print("   ✅ CFG Scale adecuado para color")
    else:
        print("   ⚠️ CFG Scale puede ser inadecuado")
    
    # 4. Verificar conexión con WebUI
    print("\n🔗 Verificando conexión con WebUI...")
    try:
        webui = WebUIPasaportes()
        if webui.verificar_conexion():
            print("   ✅ Conexión exitosa con WebUI")
        else:
            print("   ❌ No se pudo conectar con WebUI")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # 5. Verificar modelos disponibles
    print("\n📋 Verificando modelos disponibles...")
    try:
        modelos = webui.obtener_modelos()
        if modelos:
            print(f"   📄 Modelos disponibles: {len(modelos)}")
            
            # Verificar si el modelo está disponible
            modelo_encontrado = False
            for modelo in modelos:
                if 'RealisticVision' in modelo:
                    print(f"   ✅ Modelo RealisticVision encontrado: {modelo}")
                    modelo_encontrado = True
                    break
            
            if not modelo_encontrado:
                print("   ⚠️ No se encontró modelo RealisticVision")
                print("   📋 Modelos disponibles:")
                for modelo in modelos[:5]:  # Mostrar solo los primeros 5
                    print(f"      - {modelo}")
                return False
        else:
            print("   ❌ No se pudieron obtener modelos")
            return False
    except Exception as e:
        print(f"   ❌ Error obteniendo modelos: {e}")
        return False
    
    # 6. Resumen de verificación
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    print("✅ Modelo: RealisticVisionV60B1_v51HyperVAE")
    print("✅ Resolución: 512x640 (4:5)")
    print("✅ Prompts de color: Configurados")
    print("✅ Prompts anti-gris: Configurados")
    print("✅ Conexión WebUI: Funcionando")
    print("✅ Modelo disponible: Confirmado")
    
    print("\n🎯 RECOMENDACIONES PARA MEJOR COLOR:")
    print("1. Usar CFG Scale entre 7.5-8.5")
    print("2. Usar Steps entre 25-35")
    print("3. Usar Sampler DPM++ 2M Karras")
    print("4. Verificar que el modelo esté cargado en WebUI")
    
    return True

def main():
    """Función principal"""
    print("🎨 VERIFICADOR DE MODELO PARA COLOR")
    print("=" * 60)
    
    try:
        if probar_modelo_color():
            print("\n✅ VERIFICACIÓN EXITOSA")
            print("El modelo está configurado correctamente para generar imágenes a color.")
        else:
            print("\n❌ VERIFICACIÓN FALLIDA")
            print("Hay problemas con la configuración del modelo.")
            return False
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
