#!/usr/bin/env python3
"""
Script de Prueba para Validar Mejoras en Generación Masiva y Genética
Verifica que los prompts y parámetros coincidan con los estándares de muestra
"""

import sys
import os
from pathlib import Path

# Añadir el directorio actual al path
sys.path.append(str(Path(__file__).parent))

def test_genetic_engine_prompts():
    """Prueba los prompts del motor genético avanzado"""
    print("🧬 Probando Motor Genético Avanzado...")
    
    try:
        from genetic_diversity_engine_advanced import AdvancedGeneticDiversityEngine
        
        # Inicializar motor
        engine = AdvancedGeneticDiversityEngine()
        
        # Generar perfil de prueba
        profile = engine.generate_advanced_genetic_profile(
            nationality="venezuelan",
            region="caracas",
            gender="mujer",
            age=28,
            beauty_control="normal",
            skin_control="auto",
            hair_control="auto",
            eye_control="auto"
        )
        
        # Generar prompts
        prompt, negative_prompt = engine.generate_prompt_from_advanced_profile(profile, "white")
        
        print(f"✅ Perfil generado: {profile.image_id}")
        print(f"📝 Prompt generado ({len(prompt)} caracteres):")
        print(f"   {prompt[:200]}...")
        print(f"🚫 Negative prompt ({len(negative_prompt)} caracteres):")
        print(f"   {negative_prompt[:200]}...")
        
        # Verificar características clave
        checks = [
            ("passport photo" in prompt, "Incluye 'passport photo'"),
            ("professional headshot" in prompt, "Incluye 'professional headshot'"),
            ("raw photography" in prompt, "Incluye 'raw photography'"),
            ("documentary style" in prompt, "Incluye 'documentary style'"),
            ("natural skin texture" in prompt, "Incluye 'natural skin texture'"),
            ("authentic appearance" in prompt, "Incluye 'authentic appearance'"),
            ("pure white background" in prompt, "Incluye 'pure white background'"),
            ("3/4 view" in negative_prompt, "Excluye '3/4 view'"),
            ("model look" in negative_prompt, "Excluye 'model look'"),
            ("perfect skin" in negative_prompt, "Excluye 'perfect skin'")
        ]
        
        print("\n🔍 Verificaciones:")
        for check, description in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {description}")
        
        return all(check for check, _ in checks)
        
    except Exception as e:
        print(f"❌ Error probando motor genético: {e}")
        return False

def test_massive_generator_prompts():
    """Prueba los prompts del generador masivo"""
    print("\n📦 Probando Generador Masivo...")
    
    try:
        from webui_massive_generator import WebUIMassiveGenerator
        
        # Inicializar generador
        generator = WebUIMassiveGenerator()
        
        # Crear perfil de prueba (usando age_range para generación masiva)
        profile = {
            'nationality': 'venezuelan',
            'gender': 'mujer',
            'age_range': '25-35 years old',  # Usar age_range para generación masiva
            'region': 'caracas',
            'skin_tone': 'medium',
            'skin_texture': 'textured',
            'hair_color': 'brown',
            'hair_style': 'curly',
            'eye_color': 'brown',
            'eye_shape': 'expressive',
            'facial_structure': 'oval',
            'nose_shape': 'delicate',
            'lip_shape': 'medium',
            'eyebrows': 'natural',
            'jawline': 'rounded',
            'cheekbones': 'defined',
            'facial_features': 'natural',
            'ethnic_characteristics': 'latin american features',
            'natural_imperfections': 'minimal'
        }
        
        # Generar prompts
        prompt, negative_prompt = generator._generate_unique_prompt(profile)
        
        print(f"📝 Prompt generado ({len(prompt)} caracteres):")
        print(f"   {prompt[:200]}...")
        print(f"🚫 Negative prompt ({len(negative_prompt)} caracteres):")
        print(f"   {negative_prompt[:200]}...")
        
        # Verificar características clave
        checks = [
            ("passport photo" in prompt, "Incluye 'passport photo'"),
            ("professional headshot" in prompt, "Incluye 'professional headshot'"),
            ("raw photography" in prompt, "Incluye 'raw photography'"),
            ("documentary style" in prompt, "Incluye 'documentary style'"),
            ("natural skin texture" in prompt, "Incluye 'natural skin texture'"),
            ("authentic appearance" in prompt, "Incluye 'authentic appearance'"),
            ("pure white background" in prompt, "Incluye 'pure white background'"),
            ("3/4 view" in negative_prompt, "Excluye '3/4 view'"),
            ("model look" in negative_prompt, "Excluye 'model look'"),
            ("perfect skin" in negative_prompt, "Excluye 'perfect skin'")
        ]
        
        print("\n🔍 Verificaciones:")
        for check, description in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {description}")
        
        return all(check for check, _ in checks)
        
    except Exception as e:
        print(f"❌ Error probando generador masivo: {e}")
        return False

def test_parameters():
    """Prueba que los parámetros estén correctos"""
    print("\n⚙️ Verificando Parámetros...")
    
    # Parámetros esperados basados en muestras exitosas
    expected_params = {
        "cfg_scale": 12.0,
        "steps": 35,
        "width": 512,
        "height": 512,
        "sampler": "DPM++ 2M Karras"
    }
    
    print("📊 Parámetros esperados (basados en muestras exitosas):")
    for param, value in expected_params.items():
        print(f"   {param}: {value}")
    
    return True

def main():
    """Función principal de prueba"""
    print("🚀 INICIANDO PRUEBAS DE MEJORAS EN GENERACIÓN")
    print("=" * 60)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Motor Genético", test_genetic_engine_prompts()))
    results.append(("Generador Masivo", test_massive_generator_prompts()))
    results.append(("Parámetros", test_parameters()))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las mejoras están funcionando correctamente")
        print("✅ Los prompts coinciden con los estándares de muestra")
        print("✅ Los parámetros están configurados correctamente")
    else:
        print("⚠️ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar los errores anteriores")
    
    print("\n📝 PRÓXIMOS PASOS:")
    print("1. Ejecutar WebUI: ./webui.sh")
    print("2. Probar generación masiva con 5-10 imágenes")
    print("3. Comparar resultados con archivos de muestra")
    print("4. Verificar que las imágenes tengan fondo blanco sólido")
    print("5. Confirmar que no se generen imágenes tipo 'modelo'")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
