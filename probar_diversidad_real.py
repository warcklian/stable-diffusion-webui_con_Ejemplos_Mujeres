#!/usr/bin/env python3
"""
Script para probar la diversidad real en la generación de características
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_massive_diversity():
    """Prueba la diversidad en generación masiva"""
    print("🧬 PROBANDO DIVERSIDAD EN GENERACIÓN MASIVA")
    print("=" * 60)
    
    # Importar la función
    from modules.ui import generar_caracteristicas_etnicas_diversas
    
    # Generar 10 perfiles diferentes
    perfiles = []
    for i in range(10):
        print(f"\n📋 Generando perfil {i+1}/10...")
        perfil = generar_caracteristicas_etnicas_diversas(
            nacionalidad="venezuelan",
            genero="mujer",
            edad=25,
            region="aleatorio"
        )
        perfiles.append(perfil)
        
        # Mostrar características clave
        print(f"   🏙️ Región: {perfil['region']}")
        print(f"   🎨 Piel: {perfil['skin_tone']}")
        print(f"   💇 Cabello: {perfil['hair_color']} {perfil['hair_style']}")
        print(f"   👁️ Ojos: {perfil['eye_color']} {perfil['eye_shape']}")
        print(f"   👃 Nariz: {perfil['nose_shape']}")
        print(f"   👄 Labios: {perfil['lip_shape']}")
        print(f"   🎭 Cara: {perfil['face_shape']}")
        print(f"   🎯 Cejas: {perfil['eyebrows']}")
        print(f"   🦴 Mandíbula: {perfil['jawline']}")
        print(f"   💎 Pómulos: {perfil['cheekbones']}")
        if perfil['freckles'] != "none":
            print(f"   ✨ Pecas: {perfil['freckles']}")
        if perfil['moles'] != "none":
            print(f"   🔸 Lunares: {perfil['moles']}")
        if perfil['scars'] != "none":
            print(f"   🩹 Cicatrices: {perfil['scars']}")
    
    # Analizar diversidad
    print(f"\n📊 ANÁLISIS DE DIVERSIDAD:")
    print("=" * 40)
    
    # Contar regiones únicas
    regiones = [p['region'] for p in perfiles]
    regiones_unicas = set(regiones)
    print(f"🏙️ Regiones únicas: {len(regiones_unicas)}/10 ({regiones_unicas})")
    
    # Contar tonos de piel únicos
    pieles = [p['skin_tone'] for p in perfiles]
    pieles_unicas = set(pieles)
    print(f"🎨 Tonos de piel únicos: {len(pieles_unicas)}/10 ({pieles_unicas})")
    
    # Contar colores de cabello únicos
    cabellos = [p['hair_color'] for p in perfiles]
    cabellos_unicos = set(cabellos)
    print(f"💇 Colores de cabello únicos: {len(cabellos_unicos)}/10 ({cabellos_unicos})")
    
    # Contar formas de cara únicas
    caras = [p['face_shape'] for p in perfiles]
    caras_unicas = set(caras)
    print(f"🎭 Formas de cara únicas: {len(caras_unicas)}/10 ({caras_unicas})")
    
    # Contar formas de nariz únicas
    narices = [p['nose_shape'] for p in perfiles]
    narices_unicas = set(narices)
    print(f"👃 Formas de nariz únicas: {len(narices_unicas)}/10 ({narices_unicas})")
    
    # Contar formas de labios únicas
    labios = [p['lip_shape'] for p in perfiles]
    labios_unicos = set(labios)
    print(f"👄 Formas de labios únicas: {len(labios_unicos)}/10 ({labios_unicos})")
    
    # Calcular score de diversidad
    total_caracteristicas = len(regiones_unicas) + len(pieles_unicas) + len(cabellos_unicos) + len(caras_unicas) + len(narices_unicas) + len(labios_unicos)
    max_posible = 6 * 10  # 6 características x 10 perfiles
    score_diversidad = (total_caracteristicas / max_posible) * 100
    
    print(f"\n🎯 SCORE DE DIVERSIDAD: {score_diversidad:.1f}%")
    
    if score_diversidad >= 80:
        print("✅ EXCELENTE DIVERSIDAD - Cada imagen será única")
    elif score_diversidad >= 60:
        print("⚠️ DIVERSIDAD MODERADA - Algunas imágenes pueden ser similares")
    else:
        print("❌ DIVERSIDAD BAJA - Muchas imágenes serán similares")
    
    return score_diversidad

def test_genetic_diversity():
    """Prueba la diversidad en generación genética"""
    print("\n\n🧬 PROBANDO DIVERSIDAD EN GENERACIÓN GENÉTICA")
    print("=" * 60)
    
    try:
        from genetic_diversity_engine_advanced import AdvancedGeneticDiversityEngine
        
        engine = AdvancedGeneticDiversityEngine()
        
        # Generar 5 perfiles genéticos diferentes
        perfiles = []
        for i in range(5):
            print(f"\n📋 Generando perfil genético {i+1}/5...")
            perfil = engine.generate_advanced_genetic_profile(
                nationality="venezuelan",
                region="aleatorio",
                gender="mujer",
                age=25,
                beauty_control="normal",
                skin_control="auto",
                hair_control="auto",
                eye_control="auto"
            )
            perfiles.append(perfil)
            
            # Mostrar características clave
            print(f"   🆔 ID: {perfil.image_id}")
            print(f"   🏙️ Región: {perfil.region}")
            print(f"   🎨 Piel: {perfil.skin_tone}")
            print(f"   💇 Cabello: {perfil.hair_color} {perfil.hair_style}")
            print(f"   👁️ Ojos: {perfil.eye_color} {perfil.eye_shape}")
            print(f"   👃 Nariz: {perfil.nose_shape}")
            print(f"   👄 Labios: {perfil.lip_shape}")
            print(f"   🎭 Cara: {perfil.face_shape}")
            print(f"   🎯 Cejas: {perfil.eyebrows}")
            print(f"   🦴 Mandíbula: {perfil.jawline}")
            print(f"   💎 Pómulos: {perfil.cheekbones}")
            print(f"   🎨 Textura piel: {perfil.skin_texture}")
            print(f"   ✨ Pecas: {perfil.freckles}")
            print(f"   🔸 Lunares: {perfil.moles}")
            print(f"   🩹 Cicatrices: {perfil.scars}")
            print(f"   🎯 Score unicidad: {perfil.uniqueness_score:.3f}")
        
        # Analizar diversidad
        print(f"\n📊 ANÁLISIS DE DIVERSIDAD GENÉTICA:")
        print("=" * 40)
        
        # Contar características únicas
        regiones = [p.region for p in perfiles]
        pieles = [p.skin_tone for p in perfiles]
        cabellos = [p.hair_color for p in perfiles]
        caras = [p.face_shape for p in perfiles]
        narices = [p.nose_shape for p in perfiles]
        labios = [p.lip_shape for p in perfiles]
        
        print(f"🏙️ Regiones únicas: {len(set(regiones))}/5 ({set(regiones)})")
        print(f"🎨 Tonos de piel únicos: {len(set(pieles))}/5 ({set(pieles)})")
        print(f"💇 Colores de cabello únicos: {len(set(cabellos))}/5 ({set(cabellos)})")
        print(f"🎭 Formas de cara únicas: {len(set(caras))}/5 ({set(caras)})")
        print(f"👃 Formas de nariz únicas: {len(set(narices))}/5 ({set(narices)})")
        print(f"👄 Formas de labios únicas: {len(set(labios))}/5 ({set(labios)})")
        
        # Score promedio de unicidad
        scores_unicidad = [p.uniqueness_score for p in perfiles]
        score_promedio = sum(scores_unicidad) / len(scores_unicidad)
        print(f"🎯 Score promedio de unicidad: {score_promedio:.3f}")
        
        if score_promedio >= 0.8:
            print("✅ EXCELENTE DIVERSIDAD GENÉTICA")
        elif score_promedio >= 0.6:
            print("⚠️ DIVERSIDAD GENÉTICA MODERADA")
        else:
            print("❌ DIVERSIDAD GENÉTICA BAJA")
        
        return score_promedio
        
    except Exception as e:
        print(f"❌ Error probando diversidad genética: {e}")
        return 0

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE DIVERSIDAD REAL")
    print("=" * 60)
    
    # Probar diversidad masiva
    score_masivo = test_massive_diversity()
    
    # Probar diversidad genética
    score_genetico = test_genetic_diversity()
    
    # Resumen final
    print(f"\n\n📊 RESUMEN FINAL DE DIVERSIDAD")
    print("=" * 50)
    print(f"🎯 Generación Masiva: {score_masivo:.1f}%")
    print(f"🧬 Generación Genética: {score_genetico*100:.1f}%")
    
    if score_masivo >= 80 and score_genetico >= 0.8:
        print("✅ ¡EXCELENTE! Ambas generaciones tienen diversidad real")
        print("🎉 Cada imagen será única y diferente")
    elif score_masivo >= 60 and score_genetico >= 0.6:
        print("⚠️ Diversidad moderada - Algunas imágenes pueden ser similares")
    else:
        print("❌ Diversidad baja - Necesita más mejoras")
    
    print("\n🎯 RECOMENDACIONES:")
    if score_masivo < 80:
        print("   - Mejorar variación en generación masiva")
    if score_genetico < 0.8:
        print("   - Mejorar variación en generación genética")
    if score_masivo >= 80 and score_genetico >= 0.8:
        print("   - ¡Sistema listo para generar imágenes únicas!")
