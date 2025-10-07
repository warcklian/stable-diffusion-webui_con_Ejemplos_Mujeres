#!/usr/bin/env python3
"""
Script de prueba para la generación masiva de pasaportes
======================================================

Este script prueba la funcionalidad de generación masiva usando la API de WebUI.

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import requests
import json
import time
from pathlib import Path

def probar_api_webui():
    """Prueba si la API de WebUI está funcionando."""
    try:
        # Verificar que WebUI esté corriendo
        response = requests.get("http://127.0.0.1:7860/sdapi/v1/options", timeout=5)
        if response.status_code == 200:
            print("✅ API de WebUI está funcionando")
            return True
        else:
            print(f"❌ API de WebUI respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a WebUI. ¿Está ejecutándose?")
        return False
    except Exception as e:
        print(f"❌ Error al probar API: {e}")
        return False

def probar_generacion_simple():
    """Prueba una generación simple de imagen."""
    try:
        api_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
        
        payload = {
            "prompt": "a person, passport photo, professional headshot, clean background",
            "negative_prompt": "blurry, low quality, distorted",
            "width": 512,
            "height": 512,
            "steps": 20,
            "cfg_scale": 7.0,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1,
            "n_iter": 1,
            "save_images": True,
            "send_images": True
        }
        
        print("🔄 Enviando solicitud a la API...")
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'images' in result and len(result['images']) > 0:
                print("✅ Imagen generada exitosamente")
                print(f"📊 Información: {len(result['images'])} imagen(es) recibida(s)")
                return True
            else:
                print("❌ No se recibieron imágenes en la respuesta")
                return False
        else:
            print(f"❌ Error en la API: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en la generación: {e}")
        return False

def main():
    """Función principal del script de prueba."""
    print("🧪 Prueba de Generación Masiva de Pasaportes")
    print("=" * 50)
    
    # Probar API
    if not probar_api_webui():
        print("\n💡 Solución:")
        print("1. Asegúrate de que WebUI esté ejecutándose: ./webui.sh")
        print("2. Espera a que aparezca 'Running on local URL: http://127.0.0.1:7860'")
        print("3. Ejecuta este script nuevamente")
        return False
    
    # Probar generación simple
    print("\n🔄 Probando generación simple...")
    if probar_generacion_simple():
        print("\n✅ ¡Todo está funcionando correctamente!")
        print("\n🚀 Ahora puedes usar el botón 'Generar Masivo' en WebUI")
        return True
    else:
        print("\n❌ Hay problemas con la generación de imágenes")
        return False

if __name__ == "__main__":
    main()
