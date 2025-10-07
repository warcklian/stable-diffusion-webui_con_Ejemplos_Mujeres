#!/usr/bin/env python3
"""
Script simple para probar la diversidad real en la generación de características
"""

import random
import time
import hashlib

def generar_caracteristicas_etnicas_diversas(nacionalidad, genero, edad, region="aleatorio"):
    """Genera características étnicas diversas para el método masivo básico."""
    
    # Agregar timestamp y múltiples factores para máxima aleatoriedad
    unique_seed = int(time.time() * 1000000) + random.randint(1, 999999) + hash(f"{nacionalidad}{genero}{edad}{region}") % 1000000
    random.seed(unique_seed)
    
    # Si la región es "aleatorio", seleccionar una región aleatoria
    if region == "aleatorio":
        regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
        region = random.choice(regiones_disponibles)
    
    # Características de piel por nacionalidad - EXPANDIDAS para mayor diversidad
    skin_tones = {
        "venezuelan": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
        "cuban": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
        "haitian": ["medium-dark", "dark", "very-dark", "ebony", "mahogany", "chocolate", "coffee", "rich brown"],
        "dominican": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
        "mexican": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"],
        "brazilian": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey", "dark", "rich brown"],
        "american": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey", "dark", "rich brown", "pale", "ivory"]
    }
    
    # Colores de cabello por nacionalidad - EXPANDIDOS para mayor diversidad
    hair_colors = {
        "venezuelan": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
        "cuban": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
        "haitian": ["black", "dark brown", "brown", "chocolate", "espresso", "mahogany", "jet black", "raven"],
        "dominican": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
        "mexican": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"],
        "brazilian": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze", "blonde", "light brown", "honey"],
        "american": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze", "blonde", "light brown", "honey", "red", "strawberry blonde", "platinum"]
    }
    
    # Colores de ojos por nacionalidad - EXPANDIDOS para mayor diversidad
    eye_colors = {
        "venezuelan": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
        "cuban": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
        "haitian": ["dark brown", "brown", "chocolate", "coffee", "mahogany", "ebony", "rich brown"],
        "dominican": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
        "mexican": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"],
        "brazilian": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany", "green", "emerald", "olive"],
        "american": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany", "green", "emerald", "olive", "blue", "steel blue", "gray", "gray-blue"]
    }
    
    # Estilos de cabello - EXPANDIDOS para mayor diversidad
    hair_styles = ["straight", "wavy", "curly", "coily", "braided", "ponytail", "bun", "pixie", "bob", "long", "shoulder-length", "layered", "textured", "voluminous", "sleek", "messy", "styled", "natural", "professional", "casual"]
    
    # Formas de cara - EXPANDIDAS para mayor diversidad
    face_shapes = ["oval", "round", "square", "heart", "diamond", "long", "triangular", "pear", "inverted triangle", "rectangular", "angular", "soft", "defined", "symmetrical"]
    
    # Características faciales - ULTRA EXPANDIDAS para máxima diversidad
    facial_features = {
        "nose": ["straight", "aquiline", "button", "wide", "narrow", "small", "prominent", "delicate", "strong", "refined", "classic", "distinctive", "roman", "snub", "hooked", "bulbous", "pointed", "flat", "upturned", "downturned", "asymmetric", "perfect", "crooked", "broad", "thin", "long", "short"],
        "lips": ["full", "medium", "thin", "wide", "narrow", "plump", "defined", "natural", "shapely", "expressive", "delicate", "strong", "pouty", "bow-shaped", "heart-shaped", "straight", "curved", "asymmetric", "perfect", "uneven", "thick", "thin", "long", "short", "prominent", "subtle"],
        "eyes": ["almond", "round", "hooded", "deep-set", "wide-set", "close-set", "upturned", "downturned", "monolid", "double-lid", "expressive", "intense", "gentle", "piercing", "sleepy", "alert", "droopy", "cat-like", "downturned", "upturned", "asymmetric", "perfect", "uneven", "large", "small", "prominent", "recessed"]
    }
    
    # Seleccionar características aleatorias con influencia regional
    skin_tone = random.choice(skin_tones.get(nacionalidad, ["medium", "olive", "tan"]))
    hair_color = random.choice(hair_colors.get(nacionalidad, ["black", "dark brown", "brown"]))
    eye_color = random.choice(eye_colors.get(nacionalidad, ["dark brown", "brown", "hazel"]))
    hair_style = random.choice(hair_styles)
    face_shape = random.choice(face_shapes)
    nose_shape = random.choice(facial_features["nose"])
    lip_shape = random.choice(facial_features["lips"])
    eye_shape = random.choice(facial_features["eyes"])
    
    # Agregar variaciones adicionales ULTRA DIVERSAS para máxima unicidad
    additional_traits = {
        "freckles": random.choice(["none", "light", "moderate", "heavy", "scattered", "concentrated", "bridge", "cheeks", "forehead"]) if random.random() < 0.4 else "none",
        "eyebrows": random.choice(["thick", "medium", "thin", "arched", "straight", "defined", "natural", "bushy", "sparse", "uneven", "perfect", "asymmetric", "high", "low", "close", "wide", "angled", "curved"]),
        "jawline": random.choice(["strong", "soft", "defined", "rounded", "angular", "delicate", "square", "pointed", "weak", "prominent", "recessed", "asymmetric", "perfect", "uneven", "wide", "narrow"]),
        "cheekbones": random.choice(["high", "medium", "low", "prominent", "subtle", "defined", "sharp", "soft", "angular", "rounded", "asymmetric", "perfect", "uneven", "wide", "narrow", "hollow", "full"]),
        "skin_texture": random.choice(["smooth", "textured", "natural", "mature", "youthful", "rough", "fine", "coarse", "porous", "tight", "loose", "elastic", "dry", "oily", "combination"]),
        "facial_hair": random.choice(["clean-shaven", "stubble", "beard", "mustache", "goatee", "sideburns", "full-beard", "trimmed", "unkempt", "styled", "patchy", "thick", "thin"]) if genero == "hombre" else "none",
        "moles": random.choice(["none", "small", "medium", "large", "multiple", "cheek", "chin", "forehead", "nose"]) if random.random() < 0.2 else "none",
        "scars": random.choice(["none", "small", "faint", "visible", "cheek", "chin", "forehead"]) if random.random() < 0.1 else "none",
        "acne": random.choice(["none", "mild", "moderate", "severe", "scattered", "concentrated"]) if random.random() < 0.15 else "none",
        "wrinkles": random.choice(["none", "fine", "moderate", "deep", "forehead", "eye", "mouth", "neck"]) if edad > 30 and random.random() < 0.3 else "none"
    }
    
    return {
        "region": region,
        "skin_tone": skin_tone,
        "skin_texture": additional_traits["skin_texture"],
        "hair_color": hair_color,
        "hair_style": hair_style,
        "eye_color": eye_color,
        "eye_shape": eye_shape,
        "face_shape": face_shape,
        "nose_shape": nose_shape,
        "lip_shape": lip_shape,
        "eyebrows": additional_traits["eyebrows"],
        "jawline": additional_traits["jawline"],
        "cheekbones": additional_traits["cheekbones"],
        "facial_hair": additional_traits["facial_hair"],
        "freckles": additional_traits["freckles"],
        "moles": additional_traits["moles"],
        "scars": additional_traits["scars"],
        "acne": additional_traits["acne"],
        "wrinkles": additional_traits["wrinkles"]
    }

def test_diversity():
    """Prueba la diversidad en generación masiva"""
    print("🧬 PROBANDO DIVERSIDAD EN GENERACIÓN MASIVA")
    print("=" * 60)
    
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

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE DIVERSIDAD REAL")
    print("=" * 60)
    
    # Probar diversidad masiva
    score_masivo = test_diversity()
    
    # Resumen final
    print(f"\n\n📊 RESUMEN FINAL DE DIVERSIDAD")
    print("=" * 50)
    print(f"🎯 Generación Masiva: {score_masivo:.1f}%")
    
    if score_masivo >= 80:
        print("✅ ¡EXCELENTE! La generación masiva tiene diversidad real")
        print("🎉 Cada imagen será única y diferente")
    elif score_masivo >= 60:
        print("⚠️ Diversidad moderada - Algunas imágenes pueden ser similares")
    else:
        print("❌ Diversidad baja - Necesita más mejoras")
    
    print("\n🎯 RECOMENDACIONES:")
    if score_masivo < 80:
        print("   - Mejorar variación en generación masiva")
    else:
        print("   - ¡Sistema listo para generar imágenes únicas!")
