#!/usr/bin/env python3
"""
Script para probar el modelo original skin_texture_style_v5.safetensors
que funcionaba bien antes de los cambios.
"""

import json
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from webui_pasaportes import WebUIPasaportes
from generar_pasaportes import GeneradorPasaportes

def probar_modelo_original():
    """Prueba el modelo original skin_texture_style_v5.safetensors"""
    print("🎨 PROBANDO MODELO ORIGINAL: skin_texture_style_v5.safetensors")
    print("=" * 70)
    
    # 1. Verificar configuración actual
    print("📋 Verificando configuración actual...")
    config_path = "Consulta/gui_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ No se encontró {config_path}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    modelo_actual = config.get('model', 'No especificado')
    print(f"   📄 Modelo actual: {modelo_actual}")
    
    # Verificar que sea el modelo correcto
    if 'skin_texture_style_v5' not in modelo_actual:
        print("   ⚠️ El modelo no es skin_texture_style_v5")
        return False
    
    print("   ✅ Modelo skin_texture_style_v5 detectado")
    
    # 2. Verificar configuración técnica
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
    
    # 3. Verificar prompts de color
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
    
    # 4. Verificar conexión con WebUI
    print("\n🔗 Verificando conexión con WebUI...")
    try:
        webui = WebUIPasaportes()
        if webui.verificar_conexion():
            print("   ✅ Conexión exitosa con WebUI")
        else:
            print("   ❌ No se pudo conectar con WebUI")
            print("   💡 Ejecuta WebUI primero: python3 webui.py")
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
                if 'skin_texture_style_v5' in modelo:
                    print(f"   ✅ Modelo skin_texture_style_v5 encontrado: {modelo}")
                    modelo_encontrado = True
                    break
            
            if not modelo_encontrado:
                print("   ⚠️ No se encontró modelo skin_texture_style_v5")
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
    
    # 6. Cambiar al modelo si es necesario
    print("\n🔄 Verificando modelo activo...")
    try:
        modelo_skin_texture = None
        for modelo in modelos:
            if 'skin_texture_style_v5' in modelo:
                modelo_skin_texture = modelo
                break
        
        if modelo_skin_texture:
            print(f"   📄 Modelo encontrado: {modelo_skin_texture}")
            
            # Intentar cambiar al modelo
            if webui.cambiar_modelo(modelo_skin_texture):
                print(f"   ✅ Modelo cambiado a: {modelo_skin_texture}")
            else:
                print("   ⚠️ No se pudo cambiar el modelo (puede estar ya activo)")
        else:
            print("   ❌ Modelo skin_texture_style_v5 no encontrado")
            return False
    except Exception as e:
        print(f"   ❌ Error cambiando modelo: {e}")
        return False
    
    # 7. Resumen de verificación
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 70)
    print("✅ Modelo: skin_texture_style_v5.safetensors")
    print("✅ Resolución: 512x640 (4:5)")
    print("✅ Prompts de color: Configurados")
    print("✅ Prompts anti-gris: Configurados")
    print("✅ Conexión WebUI: Funcionando")
    print("✅ Modelo disponible: Confirmado")
    
    print("\n🎯 CONFIGURACIÓN OPTIMIZADA PARA SKIN_TEXTURE_STYLE_V5:")
    print("1. Modelo: skin_texture_style_v5.safetensors")
    print("2. Resolución: 512x640 (4:5)")
    print("3. Steps: 30 (óptimo para este modelo)")
    print("4. CFG Scale: 8.0 (óptimo para color)")
    print("5. Sampler: DPM++ 2M Karras")
    print("6. Prompts: Optimizados para color y realismo")
    
    return True

def main():
    """Función principal"""
    print("🎨 VERIFICADOR DE MODELO ORIGINAL")
    print("=" * 70)
    
    try:
        if probar_modelo_original():
            print("\n✅ VERIFICACIÓN EXITOSA")
            print("El modelo original está configurado correctamente.")
            print("💡 Este modelo funcionaba bien antes de los cambios.")
        else:
            print("\n❌ VERIFICACIÓN FALLIDA")
            print("Hay problemas con la configuración del modelo original.")
            return False
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
