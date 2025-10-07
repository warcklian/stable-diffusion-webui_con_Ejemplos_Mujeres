#!/usr/bin/env python3
"""
Script para probar directamente con WebUI sin usar nuestro código
"""

import requests
import base64
import json
from pathlib import Path

def probar_directo_webui():
    """Prueba directamente con WebUI para verificar si el problema está en nuestro código"""
    print("🔍 PROBANDO DIRECTAMENTE CON WEBUI")
    print("=" * 60)
    
    # Configuración de la API
    api_url = "http://127.0.0.1:7860"
    
    # Verificar conexión
    print("🔗 Verificando conexión con WebUI...")
    try:
        response = requests.get(f"{api_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ WebUI está ejecutándose")
        else:
            print("   ❌ WebUI no está ejecutándose")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # Verificar modelo actual
    print("\n📋 Verificando modelo actual...")
    try:
        response = requests.get(f"{api_url}/sdapi/v1/options")
        if response.status_code == 200:
            options = response.json()
            modelo_actual = options.get('sd_model_checkpoint', 'No especificado')
            print(f"   📄 Modelo actual: {modelo_actual}")
            
            if 'skin texture style v5' in modelo_actual:
                print("   ✅ Modelo correcto cargado")
            else:
                print("   ⚠️ Modelo incorrecto - puede ser la causa del problema")
        else:
            print("   ⚠️ No se pudieron obtener opciones - continuando con prueba")
    except Exception as e:
        print(f"   ⚠️ Error obteniendo opciones - continuando con prueba: {e}")
    
    # Generar imagen de prueba directa
    print("\n🎨 Generando imagen de prueba directa...")
    try:
        payload = {
            "prompt": "COLOR PHOTOGRAPHY, FULL COLOR IMAGE, VIBRANT COLORS, NATURAL COLORS, RICH COLORS, SATURATED COLORS, COLORFUL IMAGE, COLOR PHOTO, COLOR PORTRAIT, COLOR HEADSHOT, venezuelan passport photo, SAIME standards, official document photo, government ID photo, mujer Venezuela, 18-60 years old, front view, frontal view, looking directly at camera, direct eye contact, neutral expression, serious expression, no smile, no laughing, mouth closed, eyes open and visible, head centered and straight, frontal position, rectangular passport format, 4:5 aspect ratio, natural head proportions, no vertical stretching, proper head positioning, head positioned in upper 50% of image, face fills 60% of image height, shoulders at bottom 20% of image, head and shoulders composition, passport photo proportions 4:5, proper rectangular framing, no head stretching, natural head proportions, professional lighting, uniform lighting, even lighting, high contrast, 35mm x 45mm dimensions, 300 DPI resolution, professional quality, high resolution, 512x640 pixels, ultra high quality, no head accessories, natural makeup, beard or mustache if permanent characteristic, no dark glasses, no reflections, sharp and focused image, correct exposure, no grain, no distortion, PNG high quality format, pure white background, solid white background, clean white background, uniform white background, plain white background, studio white background, high resolution, piel morena, castaño oscuro cabello ondulado cabello suelto, ojos marrones claros, ojos almendrados, párpados dobles, natural facial structure, natural ethnic characteristics, natural wrinkles, natural expression lines, natural eye area, natural skin texture, natural age spots, natural pores, natural skin, natural moles, natural asymmetry, natural imperfections, natural features, natural hair graying, natural hair texture, natural hair density, natural hair loss, clean appearance, neat presentation, appropriate attire, modest clothing, common appearance, natural skin texture, slight asymmetry, authentic facial features, natural hair texture, regular citizen, regular person, professional headshot photography, direct portrait photography, strictly frontal view, no three quarter view, no side view, no profile view, head and shoulders visible, shoulders must be visible, sufficient head space, no head crop, full head visible, perfectly centered composition, professional studio lighting, no shadows, passport photo requirements, ID photo standards, official document standards, government photo standards, SAIME standards, venezuelan passport specifications",
            "negative_prompt": "black and white, bw, monochrome, grayscale, sepia, vintage, old, aged, faded, washed out, desaturated, muted colors, dull colors, pale colors, weak colors, faded colors, washed out colors, desaturated colors, muted, dull, pale, weak, faded, washed out, desaturated, no color, colorless, achromatic, monochromatic, grayscale, sepia tone, vintage look, old look, aged look, faded look, washed out look, desaturated look, muted look, dull look, pale look, weak look, faded look, washed out look, desaturated look, 3/4 view, side profile, looking away, smiling, laughing, multiple people, double exposure, passport document visible, photo of photo, magazine model, overly perfect, artificial lighting, shadows, background objects, jewelry, glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, beauty contest, professional headshot, studio lighting, dramatic lighting, soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, duplicate, watermark, text, signature, date, stamp, border, frame, perfect skin, flawless skin, airbrushed, photoshopped, model look, supermodel appearance, celebrity look, fashion model, beauty model, perfect features, flawless features, extreme beauty, perfect beauty, perfect symmetry, flawless symmetry, perfect proportions, flawless proportions, perfect skin texture, flawless skin texture, perfect facial features, flawless facial features, perfect bone structure, flawless bone structure, perfect skin tone, flawless skin tone, perfect hair, flawless hair, perfect eyes, flawless eyes, perfect lips, flawless lips, perfect nose, flawless nose, perfect jawline, flawless jawline, perfect cheekbones, flawless cheekbones, perfect eyebrows, flawless eyebrows, perfect teeth, flawless teeth, perfect smile, flawless smile, perfect complexion, flawless complexion, perfect appearance, flawless appearance, perfect face, flawless face, perfect look, flawless look, perfect beauty, flawless beauty, perfect model, flawless model, perfect portrait, flawless portrait, perfect headshot, flawless headshot, perfect photo, flawless photo, perfect image, flawless image, perfect picture, flawless picture, perfect shot, flawless shot, perfect capture, flawless capture, perfect rendering, flawless rendering, perfect generation, flawless generation, perfect creation, flawless creation, perfect result, flawless result, perfect output, flawless output, three quarter view, side view, profile view, watermark, signature, cropped at neck, only head, no shoulders, head cut off, shoulders missing, head cut off at top, head cropped at top, top of head missing, multiple people, double exposure, passport document visible, photo of photo, magazine model, overly perfect, artificial lighting, shadows, background objects, jewelry, glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, beauty contest, professional headshot, studio lighting, dramatic lighting, soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, duplicate, watermark, text, signature, date, stamp, border, frame, WHITE BACKGROUND, COLORED BACKGROUND, SOLID BACKGROUND, TEXTURED BACKGROUND, GRADIENT BACKGROUND, PATTERN BACKGROUND, BACKGROUND, BACKDROP, WALL, SURFACE, FLOOR, CEILING, ENVIRONMENT, SCENE, SETTING, LOCATION, PLACE, ROOM, INTERIOR, EXTERIOR, OUTDOOR, INDOOR, STUDIO BACKGROUND, PHOTO STUDIO, BACKGROUND WALL, BACKGROUND SURFACE",
            "width": 512,
            "height": 640,
            "steps": 35,
            "cfg_scale": 9.0,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1,
            "n_iter": 1,
            "save_images": False,
            "send_images": True
        }
        
        print("   📤 Enviando solicitud a WebUI...")
        response = requests.post(f"{api_url}/api/txt2img", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if 'images' in result and result['images']:
                print("   ✅ Imagen generada correctamente")
                
                # Decodificar y guardar imagen
                image_data = base64.b64decode(result['images'][0])
                
                # Guardar imagen de prueba
                output_dir = Path("prueba_directa_webui")
                output_dir.mkdir(exist_ok=True)
                
                imagen_path = output_dir / "prueba_directa.png"
                with open(imagen_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"   💾 Imagen guardada: {imagen_path}")
                print(f"   📊 Tamaño: {len(image_data)} bytes")
                
                # Análisis básico
                if len(image_data) > 1000:
                    print("   ✅ Imagen válida generada")
                    print("   💡 Revisa la imagen para verificar si está a color")
                    return True
                else:
                    print("   ❌ Imagen demasiado pequeña")
                    return False
            else:
                print("   ❌ No se recibieron imágenes")
                return False
        else:
            print(f"   ❌ Error en la solicitud: {response.status_code}")
            print(f"   📄 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error generando imagen: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 PROBADOR DIRECTO DE WEBUI")
    print("=" * 60)
    
    try:
        if probar_directo_webui():
            print("\n✅ PRUEBA DIRECTA EXITOSA")
            print("La generación directa con WebUI funcionó correctamente.")
            print("💡 Revisa la imagen en prueba_directa_webui/prueba_directa.png")
            print("🔍 Si la imagen está a color, el problema está en nuestro código.")
            print("🔍 Si la imagen está en gris, el problema está en WebUI.")
        else:
            print("\n❌ PRUEBA DIRECTA FALLIDA")
            print("No se pudo generar la imagen directamente con WebUI.")
            return False
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
