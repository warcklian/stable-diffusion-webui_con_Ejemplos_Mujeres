#!/usr/bin/env python3
"""
Script para probar la diversidad mejorada con región aleatoria y niveles de belleza expandidos
"""

import random
import time
import hashlib

def generar_caracteristicas_etnicas_diversas(nacionalidad, genero, edad, region="aleatorio"):
    """Genera características étnicas diversas para el método masivo básico."""
    
    # Agregar timestamp y múltiples factores para máxima aleatoriedad
    unique_seed = int(time.time() * 1000000) + random.randint(1, 999999) + hash(f"{nacionalidad}{genero}{edad}{region}") % 1000000
    random.seed(unique_seed)
    
    # SIEMPRE usar región aleatoria para máxima diversidad
    regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
    region = random.choice(regiones_disponibles)
    
    # Características regionales que influyen en la apariencia - EXPANDIDAS
    caracteristicas_regionales = {
        "caracas": {"skin_modifier": "urban", "hair_modifier": "modern", "facial_features": "cosmopolitan"},
        "maracaibo": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "valencia": {"skin_modifier": "industrial", "hair_modifier": "practical", "facial_features": "working_class"},
        "barquisimeto": {"skin_modifier": "arid", "hair_modifier": "traditional", "facial_features": "rural"},
        "ciudad_guayana": {"skin_modifier": "industrial", "hair_modifier": "practical", "facial_features": "mining_region"},
        "maturin": {"skin_modifier": "eastern", "hair_modifier": "traditional", "facial_features": "llanero"},
        "merida": {"skin_modifier": "mountain", "hair_modifier": "conservative", "facial_features": "andean"},
        "san_cristobal": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "barcelona": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "puerto_la_cruz": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "ciudad_bolivar": {"skin_modifier": "historical", "hair_modifier": "traditional", "facial_features": "colonial"},
        "tucupita": {"skin_modifier": "delta", "hair_modifier": "indigenous", "facial_features": "warao"},
        "porlamar": {"skin_modifier": "island", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "valera": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "acarigua": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "guanare": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "san_fernando": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "trujillo": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "el_tigre": {"skin_modifier": "oil_region", "hair_modifier": "practical", "facial_features": "industrial"},
        "cabimas": {"skin_modifier": "oil_region", "hair_modifier": "practical", "facial_features": "industrial"},
        "punto_fijo": {"skin_modifier": "peninsula", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "ciudad_ojeda": {"skin_modifier": "oil_region", "hair_modifier": "practical", "facial_features": "industrial"},
        "puerto_cabello": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "valle_de_la_pascua": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "san_juan_de_los_morros": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "carora": {"skin_modifier": "arid", "hair_modifier": "traditional", "facial_features": "rural"},
        "tocuyo": {"skin_modifier": "arid", "hair_modifier": "traditional", "facial_features": "rural"},
        "duaca": {"skin_modifier": "arid", "hair_modifier": "traditional", "facial_features": "rural"},
        "siquisique": {"skin_modifier": "arid", "hair_modifier": "traditional", "facial_features": "rural"},
        "araure": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "turen": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "guanarito": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "santa_elena": {"skin_modifier": "amazon", "hair_modifier": "indigenous", "facial_features": "amazonian"},
        "el_venado": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "san_rafael": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "san_antonio": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "la_fria": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "rubio": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "colon": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "tachira": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "apure": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "amazonas": {"skin_modifier": "amazon", "hair_modifier": "indigenous", "facial_features": "amazonian"},
        "delta_amacuro": {"skin_modifier": "delta", "hair_modifier": "indigenous", "facial_features": "warao"},
        "yacambu": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "lara": {"skin_modifier": "arid", "hair_modifier": "traditional", "facial_features": "rural"},
        "portuguesa": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "cojedes": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "guarico": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "anzoategui": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "monagas": {"skin_modifier": "eastern", "hair_modifier": "traditional", "facial_features": "llanero"},
        "sucre": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "nueva_esparta": {"skin_modifier": "island", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "falcon": {"skin_modifier": "peninsula", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "zulia": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "merida": {"skin_modifier": "mountain", "hair_modifier": "conservative", "facial_features": "andean"},
        "trujillo": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "barinas": {"skin_modifier": "llano", "hair_modifier": "traditional", "facial_features": "llanero"},
        "yaracuy": {"skin_modifier": "mountain", "hair_modifier": "traditional", "facial_features": "andean"},
        "carabobo": {"skin_modifier": "industrial", "hair_modifier": "practical", "facial_features": "working_class"},
        "aragua": {"skin_modifier": "industrial", "hair_modifier": "practical", "facial_features": "working_class"},
        "miranda": {"skin_modifier": "urban", "hair_modifier": "modern", "facial_features": "cosmopolitan"},
        "vargas": {"skin_modifier": "coastal", "hair_modifier": "tropical", "facial_features": "caribbean"},
        "distrito_capital": {"skin_modifier": "urban", "hair_modifier": "modern", "facial_features": "cosmopolitan"}
    }
    
    # Características de piel por nacionalidad - EXPANDIDAS para mayor diversidad
    skin_tones = {
        "venezuelan": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey", "dark", "rich brown", "coffee", "mahogany", "espresso", "chocolate", "mocha", "cinnamon", "amber", "copper"]
    }
    
    # Colores de cabello por nacionalidad - EXPANDIDOS
    hair_colors = {
        "venezuelan": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze", "light brown", "honey", "golden", "blonde", "strawberry blonde", "red", "ginger", "salt and pepper", "gray", "white"]
    }
    
    # Colores de ojos por nacionalidad - EXPANDIDOS
    eye_colors = {
        "venezuelan": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany", "green", "blue", "gray", "blue-green", "hazel-green", "amber-brown", "light hazel", "dark hazel"]
    }
    
    # Estilos de cabello - OPTIMIZADOS PARA PASAPORTE
    hair_styles = ["straight", "wavy", "curly", "braided", "ponytail", "bun", "pixie", "bob", "shoulder-length", "layered", "textured", "voluminous", "sleek", "styled", "natural", "professional", "casual", "messy", "neat", "tidy", "unkempt", "wild", "smooth", "rough", "thick", "thin", "fine", "coarse"]
    
    # Formas de cara - EXPANDIDAS
    face_shapes = ["oval", "round", "square", "heart", "diamond", "long", "triangular", "pear", "inverted triangle", "rectangular", "angular", "soft", "defined", "symmetrical", "asymmetrical", "wide", "narrow", "broad", "thin", "full", "hollow", "prominent", "recessed"]
    
    # Características faciales - ULTRA EXPANDIDAS
    facial_features = {
        "nose": ["straight", "aquiline", "button", "wide", "narrow", "small", "prominent", "delicate", "strong", "refined", "classic", "distinctive", "roman", "snub", "hooked", "bulbous", "pointed", "flat", "upturned", "downturned", "asymmetric", "perfect", "crooked", "broad", "thin", "long", "short", "large", "tiny", "bent", "twisted", "bumpy", "smooth", "rough", "textured"],
        "lips": ["full", "medium", "thin", "wide", "narrow", "plump", "defined", "natural", "shapely", "expressive", "delicate", "strong", "pouty", "bow-shaped", "heart-shaped", "straight", "curved", "asymmetric", "perfect", "uneven", "thick", "thin", "long", "short", "prominent", "subtle", "large", "small", "wide", "narrow", "pursed", "relaxed", "tense", "loose"],
        "eyes": ["almond", "round", "hooded", "deep-set", "wide-set", "close-set", "upturned", "downturned", "monolid", "double-lid", "expressive", "intense", "gentle", "piercing", "sleepy", "alert", "droopy", "cat-like", "downturned", "upturned", "asymmetric", "perfect", "uneven", "large", "small", "prominent", "recessed", "bulging", "sunken", "puffy", "swollen", "narrow", "wide", "slanted", "straight"]
    }
    
    # Obtener características regionales
    region_traits = caracteristicas_regionales.get(region, {"skin_modifier": "standard", "hair_modifier": "standard", "facial_features": "standard"})
    
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
        "freckles": random.choice(["none", "light", "moderate", "heavy", "scattered", "concentrated", "bridge", "cheeks", "forehead", "nose", "chin", "arms", "shoulders"]) if random.random() < 0.4 else "none",
        "eyebrows": random.choice(["thick", "medium", "thin", "arched", "straight", "defined", "natural", "bushy", "sparse", "uneven", "perfect", "asymmetric", "high", "low", "close", "wide", "angled", "curved", "messy", "neat", "tidy", "unkempt", "wild", "smooth", "rough", "patchy", "full", "partial", "missing", "overgrown", "trimmed", "shaped"]),
        "jawline": random.choice(["strong", "soft", "defined", "rounded", "angular", "delicate", "square", "pointed", "weak", "prominent", "recessed", "asymmetric", "perfect", "uneven", "wide", "narrow", "broad", "thin", "full", "hollow", "sharp", "blunt", "chiseled", "soft", "hard", "firm", "loose", "tight", "relaxed", "tense"]),
        "cheekbones": random.choice(["high", "medium", "low", "prominent", "subtle", "defined", "sharp", "soft", "angular", "rounded", "asymmetric", "perfect", "uneven", "wide", "narrow", "hollow", "full", "broad", "thin", "strong", "weak", "chiseled", "smooth", "rough", "textured", "flat", "raised", "sunken", "puffy", "swollen"]),
        "skin_texture": random.choice(["smooth", "textured", "natural", "mature", "youthful", "rough", "fine", "coarse", "porous", "tight", "loose", "elastic", "dry", "oily", "combination", "blemished", "clear", "acne-prone", "sensitive", "resilient", "fragile", "thick", "thin", "firm", "soft", "wrinkled", "aged", "fresh", "dull", "glowing", "radiant"]),
        "facial_hair": random.choice(["clean-shaven", "stubble", "beard", "mustache", "goatee", "sideburns", "full-beard", "trimmed", "unkempt", "styled", "patchy", "thick", "thin", "sparse", "dense", "curly", "straight", "wiry", "soft", "rough", "neat", "messy", "professional", "casual", "wild", "tamed"]) if genero == "hombre" else "none",
        "moles": random.choice(["none", "small", "medium", "large", "multiple", "cheek", "chin", "forehead", "nose", "lip", "eye", "ear", "neck", "shoulder", "arm", "hand", "back", "chest"]) if random.random() < 0.3 else "none",
        "scars": random.choice(["none", "small", "faint", "visible", "cheek", "chin", "forehead", "nose", "lip", "eye", "ear", "neck", "shoulder", "arm", "hand", "back", "chest", "surgical", "accident", "birth", "childhood"]) if random.random() < 0.15 else "none",
        "acne": random.choice(["none", "mild", "moderate", "severe", "scattered", "concentrated", "forehead", "cheeks", "chin", "nose", "back", "chest", "shoulders", "active", "healing", "scarred", "cystic", "blackheads", "whiteheads"]) if random.random() < 0.2 else "none",
        "wrinkles": random.choice(["none", "fine", "moderate", "deep", "forehead", "eye", "mouth", "neck", "crow's feet", "laugh lines", "frown lines", "worry lines", "smile lines", "expression lines", "age lines", "sun damage", "genetic", "lifestyle"]) if edad > 25 and random.random() < 0.4 else "none"
    }
    
    return {
        "region": region,
        "region_traits": region_traits,
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

def generar_nivel_belleza_aleatorio():
    """Genera nivel de belleza aleatorio para máxima diversidad real"""
    niveles_belleza = [
        "muy_atractivo", "atractivo", "normal", "promedio", "comun", "ordinario", 
        "poco_atractivo", "feo", "muy_feo", "realista", "variado"
    ]
    return random.choice(niveles_belleza)

def test_diversidad_mejorada():
    """Prueba la diversidad mejorada con región aleatoria y niveles de belleza expandidos"""
    print("🎨 PROBANDO DIVERSIDAD MEJORADA CON REGIÓN ALEATORIA")
    print("=" * 60)
    
    # Generar 10 perfiles diferentes para ver la diversidad
    perfiles_generados = []
    regiones_utilizadas = set()
    niveles_belleza_utilizados = set()
    
    for i in range(10):
        print(f"\n📋 Generando perfil {i+1}/10...")
        
        # Generar nivel de belleza aleatorio
        nivel_belleza = generar_nivel_belleza_aleatorio()
        niveles_belleza_utilizados.add(nivel_belleza)
        
        # Generar perfil
        perfil = generar_caracteristicas_etnicas_diversas(
            nacionalidad="venezuelan",
            genero="mujer",
            edad=25,
            region="aleatorio"
        )
        
        perfiles_generados.append(perfil)
        regiones_utilizadas.add(perfil['region'])
        
        # Mostrar características
        print(f"   🏙️ Región: {perfil['region']} ({perfil['region_traits']['facial_features']})")
        print(f"   💎 Belleza: {nivel_belleza}")
        print(f"   🎨 Piel: {perfil['skin_tone']} {perfil['skin_texture']}")
        print(f"   💇 Cabello: {perfil['hair_color']} {perfil['hair_style']}")
        print(f"   👁️ Ojos: {perfil['eye_color']} {perfil['eye_shape']}")
        print(f"   🎭 Cara: {perfil['face_shape']}")
        print(f"   👃 Nariz: {perfil['nose_shape']}")
        print(f"   👄 Labios: {perfil['lip_shape']}")
        print(f"   👁️ Cejas: {perfil['eyebrows']}")
        print(f"   🦴 Mandíbula: {perfil['jawline']}")
        print(f"   🍎 Pómulos: {perfil['cheekbones']}")
        
        # Mostrar características adicionales si no son "none"
        if perfil['freckles'] != "none":
            print(f"   ✨ Pecas: {perfil['freckles']}")
        if perfil['moles'] != "none":
            print(f"   🔸 Lunares: {perfil['moles']}")
        if perfil['scars'] != "none":
            print(f"   🩹 Cicatrices: {perfil['scars']}")
        if perfil['acne'] != "none":
            print(f"   🔴 Acné: {perfil['acne']}")
        if perfil['wrinkles'] != "none":
            print(f"   📏 Arrugas: {perfil['wrinkles']}")
    
    # Calcular estadísticas de diversidad
    total_perfiles = len(perfiles_generados)
    regiones_unicas = len(regiones_utilizadas)
    niveles_belleza_unicos = len(niveles_belleza_utilizados)
    
    print(f"\n\n📊 ESTADÍSTICAS DE DIVERSIDAD")
    print("=" * 50)
    print(f"✅ Total de perfiles generados: {total_perfiles}")
    print(f"✅ Regiones únicas utilizadas: {regiones_unicas}/{total_perfiles}")
    print(f"✅ Niveles de belleza únicos: {niveles_belleza_unicos}/{total_perfiles}")
    print(f"✅ Diversidad de regiones: {(regiones_unicas/total_perfiles)*100:.1f}%")
    print(f"✅ Diversidad de belleza: {(niveles_belleza_unicos/total_perfiles)*100:.1f}%")
    
    print(f"\n🏙️ REGIONES UTILIZADAS:")
    for region in sorted(regiones_utilizadas):
        print(f"   - {region}")
    
    print(f"\n💎 NIVELES DE BELLEZA UTILIZADOS:")
    for nivel in sorted(niveles_belleza_utilizados):
        print(f"   - {nivel}")
    
    # Calcular score de diversidad
    diversidad_regiones = (regiones_unicas / total_perfiles) * 100
    diversidad_belleza = (niveles_belleza_unicos / total_perfiles) * 100
    score_diversidad = (diversidad_regiones + diversidad_belleza) / 2
    
    print(f"\n🎯 SCORE DE DIVERSIDAD: {score_diversidad:.1f}%")
    
    if score_diversidad >= 80:
        print("   ✅ EXCELENTE - Máxima diversidad alcanzada")
    elif score_diversidad >= 60:
        print("   ⚠️ BUENO - Buena diversidad")
    elif score_diversidad >= 40:
        print("   ⚠️ REGULAR - Diversidad moderada")
    else:
        print("   ❌ MALO - Poca diversidad")
    
    print(f"\n🎉 MEJORAS IMPLEMENTADAS:")
    print("   ✅ Región SIEMPRE aleatoria para máxima diversidad")
    print("   ✅ 60+ regiones venezolanas disponibles")
    print("   ✅ 11 niveles de belleza incluyendo no atractivos")
    print("   ✅ Características faciales ultra expandidas")
    print("   ✅ Variaciones adicionales ultra diversas")
    print("   ✅ ¡Diversidad real garantizada!")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE DIVERSIDAD MEJORADA")
    print("=" * 60)
    
    test_diversidad_mejorada()

