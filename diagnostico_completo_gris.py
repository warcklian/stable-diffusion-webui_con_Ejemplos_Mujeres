#!/usr/bin/env python3
"""
Diagnóstico completo del problema de imágenes en gris
Identifica todas las fuentes de prompts y configuraciones
"""

import json
import os
import sys
from pathlib import Path

def diagnosticar_todas_las_fuentes():
    """Diagnostica todas las fuentes posibles del problema de imágenes en gris"""
    print("🔍 DIAGNÓSTICO COMPLETO DE PROBLEMA GRIS")
    print("=" * 80)
    
    # 1. Verificar gui_config.json
    print("\n📋 1. VERIFICANDO gui_config.json...")
    config_path = "Consulta/gui_config.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        base_prompt = config.get('base_prompt', '')
        negative_prompt = config.get('negative_prompt', '')
        
        # Verificar términos de color
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
        
        print(f"   📊 Términos de color en gui_config.json: {color_count}/{len(terminos_color)}")
        
        # Verificar términos anti-gris
        terminos_anti_gris = [
            'black and white', 'bw', 'monochrome', 'grayscale', 'sepia',
            'vintage', 'old', 'aged', 'faded', 'washed out', 'desaturated'
        ]
        
        anti_gris_count = 0
        for termino in terminos_anti_gris:
            if termino in negative_prompt:
                anti_gris_count += 1
                print(f"   ✅ {termino}")
        
        print(f"   📊 Términos anti-gris en gui_config.json: {anti_gris_count}/{len(terminos_anti_gris)}")
        
        # Verificar modelo
        modelo = config.get('model', '')
        print(f"   📄 Modelo configurado: {modelo}")
        
        if not modelo or modelo == "":
            print("   ⚠️  ADVERTENCIA: Modelo no especificado en gui_config.json")
        else:
            print("   ✅ Modelo especificado correctamente")
            
    else:
        print("   ❌ gui_config.json no encontrado")
    
    # 2. Verificar webui_massive_generator.py
    print("\n📋 2. VERIFICANDO webui_massive_generator.py...")
    massive_path = "webui_massive_generator.py"
    
    if os.path.exists(massive_path):
        with open(massive_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si usa gui_config.json
        if "gui_config.json" in content:
            print("   ✅ webui_massive_generator.py usa gui_config.json")
        else:
            print("   ❌ webui_massive_generator.py NO usa gui_config.json")
        
        # Verificar si tiene términos de color hardcodeados
        if "COLOR PHOTOGRAPHY" in content:
            print("   ✅ webui_massive_generator.py tiene términos de color")
        else:
            print("   ❌ webui_massive_generator.py NO tiene términos de color")
            
    else:
        print("   ❌ webui_massive_generator.py no encontrado")
    
    # 3. Verificar otros archivos de generación
    print("\n📋 3. VERIFICANDO OTROS ARCHIVOS DE GENERACIÓN...")
    
    archivos_generacion = [
        "generar_pasaportes.py",
        "webui_pasaportes.py", 
        "genetic_diversity_engine.py",
        "genetic_diversity_engine_advanced.py"
    ]
    
    for archivo in archivos_generacion:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "COLOR PHOTOGRAPHY" in content:
                print(f"   ✅ {archivo} tiene términos de color")
            else:
                print(f"   ❌ {archivo} NO tiene términos de color")
        else:
            print(f"   ⚠️  {archivo} no encontrado")
    
    # 4. Verificar plantillas
    print("\n📋 4. VERIFICANDO PLANTILLAS...")
    templates_dir = Path("Consulta/templates")
    
    if templates_dir.exists():
        templates = list(templates_dir.glob("*.json"))
        print(f"   📁 Encontradas {len(templates)} plantillas")
        
        for template in templates:
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Verificar si tiene prompts
                if 'prompts' in data.get('config', {}):
                    prompts = data['config']['prompts']
                    base_prompt = prompts.get('base_prompt', '')
                    
                    if "COLOR PHOTOGRAPHY" in base_prompt:
                        print(f"   ✅ {template.name} tiene términos de color")
                    else:
                        print(f"   ❌ {template.name} NO tiene términos de color")
                else:
                    print(f"   ⚠️  {template.name} no tiene sección prompts")
                    
            except Exception as e:
                print(f"   ❌ Error leyendo {template.name}: {e}")
    else:
        print("   ❌ Directorio de plantillas no encontrado")
    
    # 5. Verificar conexión WebUI
    print("\n📋 5. VERIFICANDO CONEXIÓN CON WEBUI...")
    try:
        import requests
        response = requests.get("http://127.0.0.1:7860", timeout=5)
        if response.status_code == 200:
            print("   ✅ WebUI está ejecutándose")
        else:
            print("   ❌ WebUI no responde correctamente")
    except Exception as e:
        print(f"   ❌ WebUI no está ejecutándose: {e}")
    
    # 6. Resumen y recomendaciones
    print("\n🎯 RESUMEN Y RECOMENDACIONES:")
    print("=" * 50)
    
    if color_count >= 8 and anti_gris_count >= 6:
        print("✅ gui_config.json está correctamente configurado")
    else:
        print("❌ gui_config.json necesita términos de color")
    
    if "gui_config.json" in content if os.path.exists(massive_path) else False:
        print("✅ webui_massive_generator.py usa gui_config.json")
    else:
        print("❌ webui_massive_generator.py necesita usar gui_config.json")
    
    print("\n💡 RECOMENDACIONES:")
    print("1. Asegúrate de que WebUI esté ejecutándose")
    print("2. Verifica que el modelo esté cargado en WebUI")
    print("3. Si usas el generador masivo, debe usar gui_config.json")
    print("4. Si usas plantillas, deben tener términos de color")

if __name__ == "__main__":
    diagnosticar_todas_las_fuentes()
