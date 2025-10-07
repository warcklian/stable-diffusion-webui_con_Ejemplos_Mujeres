#!/usr/bin/env python3
"""
Script de diagnóstico para identificar por qué las imágenes salen en gris
"""

import json
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from webui_pasaportes import WebUIPasaportes
from generar_pasaportes import GeneradorPasaportes

def diagnosticar_problema_gris():
    """Diagnostica por qué las imágenes salen en gris"""
    print("🔍 DIAGNÓSTICO DE PROBLEMA GRIS")
    print("=" * 60)
    
    # 1. Verificar configuración actual
    print("📋 Verificando configuración actual...")
    config_path = "Consulta/gui_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ No se encontró {config_path}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f"   📄 Modelo: {config.get('model', 'No especificado')}")
    print(f"   📐 Resolución: {config.get('width', 0)}x{config.get('height', 0)}")
    print(f"   🔄 Steps: {config.get('steps', 0)}")
    print(f"   📊 CFG Scale: {config.get('cfg_scale', 0)}")
    print(f"   🎯 Sampler: {config.get('sampler', 'No especificado')}")
    
    # 2. Verificar prompts de color
    print("\n🎨 Analizando prompts de color...")
    base_prompt = config.get('base_prompt', '')
    negative_prompt = config.get('negative_prompt', '')
    
    # Contar términos de color
    terminos_color = [
        'COLOR PHOTOGRAPHY', 'FULL COLOR', 'VIBRANT COLORS', 
        'NATURAL COLORS', 'RICH COLORS', 'SATURATED COLORS',
        'COLORFUL', 'COLOR IMAGE', 'COLOR PHOTO', 'COLOR PORTRAIT'
    ]
    
    color_count = 0
    for termino in terminos_color:
        if termino in base_prompt:
            color_count += 1
            print(f"   ✅ {termino}")
    
    print(f"   📊 Términos de color encontrados: {color_count}/{len(terminos_color)}")
    
    # Contar términos anti-gris
    terminos_anti_gris = [
        'black and white', 'bw', 'monochrome', 'grayscale', 
        'sepia', 'no color', 'colorless', 'desaturated'
    ]
    
    anti_gris_count = 0
    for termino in terminos_anti_gris:
        if termino in negative_prompt:
            anti_gris_count += 1
            print(f"   ✅ {termino}")
    
    print(f"   📊 Términos anti-gris encontrados: {anti_gris_count}/{len(terminos_anti_gris)}")
    
    # 3. Verificar conexión con WebUI
    print("\n🔗 Verificando conexión con WebUI...")
    try:
        webui = WebUIPasaportes()
        if webui.verificar_conexion():
            print("   ✅ WebUI está ejecutándose")
        else:
            print("   ❌ WebUI no está ejecutándose")
            print("   💡 Ejecuta WebUI primero: python3 webui.py")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # 4. Verificar modelo activo
    print("\n📋 Verificando modelo activo...")
    try:
        modelos = webui.obtener_modelos()
        if modelos:
            print(f"   📄 Modelos disponibles: {len(modelos)}")
            
            # Buscar modelo skin_texture_style_v5
            modelo_encontrado = None
            for modelo in modelos:
                if 'skin_texture_style_v5' in modelo:
                    modelo_encontrado = modelo
                    break
            
            if modelo_encontrado:
                print(f"   ✅ Modelo encontrado: {modelo_encontrado}")
                
                # Intentar cambiar al modelo
                if webui.cambiar_modelo(modelo_encontrado):
                    print(f"   ✅ Modelo cambiado a: {modelo_encontrado}")
                else:
                    print("   ⚠️ No se pudo cambiar el modelo")
            else:
                print("   ❌ Modelo skin_texture_style_v5 no encontrado")
                print("   📋 Modelos disponibles:")
                for modelo in modelos[:5]:
                    print(f"      - {modelo}")
                return False
        else:
            print("   ❌ No se pudieron obtener modelos")
            return False
    except Exception as e:
        print(f"   ❌ Error obteniendo modelos: {e}")
        return False
    
    # 5. Generar imagen de prueba con diagnóstico
    print("\n🎨 Generando imagen de prueba...")
    try:
        # Crear configuración de prueba optimizada para color
        config_prueba = {
            'prompt_positivo': 'COLOR PHOTOGRAPHY, FULL COLOR IMAGE, VIBRANT COLORS, NATURAL COLORS, RICH COLORS, SATURATED COLORS, COLORFUL IMAGE, COLOR PHOTO, COLOR PORTRAIT, COLOR HEADSHOT, venezuelan passport photo, SAIME standards, official document photo, government ID photo, mujer Venezuela, 18-60 years old, front view, frontal view, looking directly at camera, direct eye contact, neutral expression, serious expression, no smile, no laughing, mouth closed, eyes open and visible, head centered and straight, frontal position, rectangular passport format, 4:5 aspect ratio, natural head proportions, no vertical stretching, proper head positioning, head positioned in upper 50% of image, face fills 60% of image height, shoulders at bottom 20% of image, head and shoulders composition, passport photo proportions 4:5, proper rectangular framing, no head stretching, natural head proportions, professional lighting, uniform lighting, even lighting, high contrast, 35mm x 45mm dimensions, 300 DPI resolution, professional quality, high resolution, 512x640 pixels, ultra high quality, no head accessories, natural makeup, beard or mustache if permanent characteristic, no dark glasses, no reflections, sharp and focused image, correct exposure, no grain, no distortion, PNG high quality format, pure white background, solid white background, clean white background, uniform white background, plain white background, studio white background, high resolution, piel morena, castaño oscuro cabello ondulado cabello suelto, ojos marrones claros, ojos almendrados, párpados dobles, natural facial structure, natural ethnic characteristics, natural wrinkles, natural expression lines, natural eye area, natural skin texture, natural age spots, natural pores, natural skin, natural moles, natural asymmetry, natural imperfections, natural features, natural hair graying, natural hair texture, natural hair density, natural hair loss, clean appearance, neat presentation, appropriate attire, modest clothing, common appearance, natural skin texture, slight asymmetry, authentic facial features, natural hair texture, regular citizen, regular person, professional headshot photography, direct portrait photography, strictly frontal view, no three quarter view, no side view, no profile view, head and shoulders visible, shoulders must be visible, sufficient head space, no head crop, full head visible, perfectly centered composition, professional studio lighting, no shadows, passport photo requirements, ID photo standards, official document standards, government photo standards, SAIME standards, venezuelan passport specifications',
            'prompt_negativo': 'black and white, bw, monochrome, grayscale, sepia, vintage, old, aged, faded, washed out, desaturated, muted colors, dull colors, pale colors, weak colors, faded colors, washed out colors, desaturated colors, muted, dull, pale, weak, faded, washed out, desaturated, no color, colorless, achromatic, monochromatic, grayscale, sepia tone, vintage look, old look, aged look, faded look, washed out look, desaturated look, muted look, dull look, pale look, weak look, faded look, washed out look, desaturated look, 3/4 view, side profile, looking away, smiling, laughing, multiple people, double exposure, passport document visible, photo of photo, magazine model, overly perfect, artificial lighting, shadows, background objects, jewelry, glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, beauty contest, professional headshot, studio lighting, dramatic lighting, soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, duplicate, watermark, text, signature, date, stamp, border, frame, perfect skin, flawless skin, airbrushed, photoshopped, model look, supermodel appearance, celebrity look, fashion model, beauty model, perfect features, flawless features, extreme beauty, perfect beauty, perfect symmetry, flawless symmetry, perfect proportions, flawless proportions, perfect skin texture, flawless skin texture, perfect facial features, flawless facial features, perfect bone structure, flawless bone structure, perfect skin tone, flawless skin tone, perfect hair, flawless hair, perfect eyes, flawless eyes, perfect lips, flawless lips, perfect nose, flawless nose, perfect jawline, flawless jawline, perfect cheekbones, flawless cheekbones, perfect eyebrows, flawless eyebrows, perfect teeth, flawless teeth, perfect smile, flawless smile, perfect complexion, flawless complexion, perfect appearance, flawless appearance, perfect face, flawless face, perfect look, flawless look, perfect beauty, flawless beauty, perfect model, flawless model, perfect portrait, flawless portrait, perfect headshot, flawless headshot, perfect photo, flawless photo, perfect image, flawless image, perfect picture, flawless picture, perfect shot, flawless shot, perfect capture, flawless capture, perfect rendering, flawless rendering, perfect generation, flawless generation, perfect creation, flawless creation, perfect result, flawless result, perfect output, flawless output, three quarter view, side view, profile view, watermark, signature, cropped at neck, only head, no shoulders, head cut off, shoulders missing, head cut off at top, head cropped at top, top of head missing, multiple people, double exposure, passport document visible, photo of photo, magazine model, overly perfect, artificial lighting, shadows, background objects, jewelry, glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, beauty contest, professional headshot, studio lighting, dramatic lighting, soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, duplicate, watermark, text, signature, date, stamp, border, frame, WHITE BACKGROUND, COLORED BACKGROUND, SOLID BACKGROUND, TEXTURED BACKGROUND, GRADIENT BACKGROUND, PATTERN BACKGROUND, BACKGROUND, BACKDROP, WALL, SURFACE, FLOOR, CEILING, ENVIRONMENT, SCENE, SETTING, LOCATION, PLACE, ROOM, INTERIOR, EXTERIOR, OUTDOOR, INDOOR, STUDIO BACKGROUND, PHOTO STUDIO, BACKGROUND WALL, BACKGROUND SURFACE',
            'configuracion_tecnica': {
                'width': 512,
                'height': 640,
                'steps': 35,
                'cfg_scale': 9.0,
                'sampler': 'DPM++ 2M Karras'
            }
        }
        
        # Generar imagen
        imagen_bytes = webui.generar_imagen(config_prueba)
        
        if imagen_bytes:
            # Guardar imagen de prueba
            output_dir = Path("diagnostico_gris_output")
            output_dir.mkdir(exist_ok=True)
            
            imagen_path = output_dir / "diagnostico_color.png"
            with open(imagen_path, 'wb') as f:
                f.write(imagen_bytes)
            
            print(f"   ✅ Imagen generada: {imagen_path}")
            print(f"   📊 Tamaño: {len(imagen_bytes)} bytes")
            
            # Análisis básico de la imagen
            if len(imagen_bytes) > 1000:  # Imagen válida
                print("   ✅ Imagen generada correctamente")
                print("   💡 Revisa la imagen para verificar si está a color")
                return True
            else:
                print("   ❌ Imagen demasiado pequeña - posible error")
                return False
        else:
            print("   ❌ No se pudo generar la imagen")
            return False
            
    except Exception as e:
        print(f"   ❌ Error generando imagen: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO DE PROBLEMA GRIS")
    print("=" * 60)
    
    try:
        if diagnosticar_problema_gris():
            print("\n✅ DIAGNÓSTICO COMPLETADO")
            print("Revisa la imagen generada en diagnostico_gris_output/diagnostico_color.png")
            print("💡 Si la imagen sigue en gris, el problema puede estar en:")
            print("   1. Configuración de WebUI")
            print("   2. Modelo específico")
            print("   3. Parámetros de generación")
        else:
            print("\n❌ DIAGNÓSTICO FALLIDO")
            print("No se pudo completar el diagnóstico.")
            return False
    except Exception as e:
        print(f"\n❌ Error durante el diagnóstico: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
