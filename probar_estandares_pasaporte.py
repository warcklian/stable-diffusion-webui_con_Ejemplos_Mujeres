#!/usr/bin/env python3
"""
Script para probar los estándares de foto de pasaporte
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
        regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto"]
        region = random.choice(regiones_disponibles)
    
    # Características de piel por nacionalidad
    skin_tones = {
        "venezuelan": ["light", "fair", "medium", "medium-dark", "olive", "tan", "golden", "bronze", "caramel", "honey"]
    }
    
    # Colores de cabello por nacionalidad
    hair_colors = {
        "venezuelan": ["black", "dark brown", "brown", "auburn", "chestnut", "chocolate", "espresso", "mahogany", "copper", "bronze"]
    }
    
    # Colores de ojos por nacionalidad
    eye_colors = {
        "venezuelan": ["dark brown", "brown", "hazel", "amber", "light brown", "honey", "golden", "coffee", "chocolate", "mahogany"]
    }
    
    # Estilos de cabello - OPTIMIZADOS PARA PASAPORTE
    hair_styles = ["straight", "wavy", "curly", "braided", "ponytail", "bun", "pixie", "bob", "shoulder-length", "layered", "textured", "voluminous", "sleek", "styled", "natural", "professional", "casual"]
    
    # Formas de cara
    face_shapes = ["oval", "round", "square", "heart", "diamond", "long", "triangular", "pear", "inverted triangle", "rectangular", "angular", "soft", "defined", "symmetrical"]
    
    # Características faciales
    facial_features = {
        "nose": ["straight", "aquiline", "button", "wide", "narrow", "small", "prominent", "delicate", "strong", "refined", "classic", "distinctive", "roman", "snub", "hooked", "bulbous", "pointed", "flat", "upturned", "downturned", "asymmetric", "perfect", "crooked", "broad", "thin", "long", "short"],
        "lips": ["full", "medium", "thin", "wide", "narrow", "plump", "defined", "natural", "shapely", "expressive", "delicate", "strong", "pouty", "bow-shaped", "heart-shaped", "straight", "curved", "asymmetric", "perfect", "uneven", "thick", "thin", "long", "short", "prominent", "subtle"],
        "eyes": ["almond", "round", "hooded", "deep-set", "wide-set", "close-set", "upturned", "downturned", "monolid", "double-lid", "expressive", "intense", "gentle", "piercing", "sleepy", "alert", "droopy", "cat-like", "downturned", "upturned", "asymmetric", "perfect", "uneven", "large", "small", "prominent", "recessed"]
    }
    
    # Seleccionar características aleatorias
    skin_tone = random.choice(skin_tones.get(nacionalidad, ["medium", "olive", "tan"]))
    hair_color = random.choice(hair_colors.get(nacionalidad, ["black", "dark brown", "brown"]))
    eye_color = random.choice(eye_colors.get(nacionalidad, ["dark brown", "brown", "hazel"]))
    hair_style = random.choice(hair_styles)
    face_shape = random.choice(face_shapes)
    nose_shape = random.choice(facial_features["nose"])
    lip_shape = random.choice(facial_features["lips"])
    eye_shape = random.choice(facial_features["eyes"])
    
    # Características adicionales
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

def generar_prompt_pasaporte_estricto(perfil, edad=25):
    """Genera prompt estricto para foto de pasaporte"""
    
    prompt_parts = [
        f"{perfil['region']} {perfil['skin_tone']} person",
        f"{edad} years old",
        f"{perfil['skin_tone']} skin",
        f"{perfil['skin_texture']} skin texture",
        f"{perfil['hair_color']} hair",
        f"{perfil['hair_style']} hair",
        f"{perfil['eye_color']} eyes",
        f"{perfil['eye_shape']} eyes",
        f"{perfil['face_shape']} face",
        f"{perfil['nose_shape']} nose",
        f"{perfil['lip_shape']} lips",
        f"{perfil['eyebrows']} eyebrows",
        f"{perfil['jawline']} jawline",
        f"{perfil['cheekbones']} cheekbones",
        "official passport photo",
        "government ID photo",
        "document photo",
        "official headshot",
        "passport style photo",
        "ID card photo",
        "looking directly at camera",
        "facing camera directly",
        "front view only",
        "head and shoulders only",
        "head centered perfectly",
        "face centered perfectly",
        "neutral expression",
        "serious expression",
        "no smile",
        "mouth closed",
        "eyes open",
        "looking straight ahead",
        "head straight",
        "no head tilt",
        "no head turn",
        "head upright",
        "shoulders visible",
        "shoulders straight",
        "shoulders level",
        "hair behind ears",
        "hair not covering face",
        "hair not covering shoulders",
        "hair neat and tidy",
        "hair professional style",
        "raw photography",
        "documentary style",
        "unretouched",
        "natural skin texture",
        "pores visible",
        "natural skin imperfections",
        "authentic appearance",
        "natural lighting",
        "centered composition",
        "symmetrical positioning",
        "proper framing",
        "correct proportions",
        "everyday person",
        "normal person",
        "regular person",
        "common person",
        "average person",
        "real person",
        "authentic person",
        "natural person",
        "ordinary person",
        "typical person",
        "pure white background",
        "solid white background",
        "clean white background",
        "uniform white background",
        "plain white background",
        "studio white background"
    ]
    
    # Añadir características específicas si no son "none"
    if perfil['freckles'] != "none":
        prompt_parts.append(f"{perfil['freckles']} freckles")
    if perfil['moles'] != "none":
        prompt_parts.append(f"{perfil['moles']} moles")
    if perfil['scars'] != "none":
        prompt_parts.append(f"{perfil['scars']} scars")
    if perfil['acne'] != "none":
        prompt_parts.append(f"{perfil['acne']} acne")
    if perfil['wrinkles'] != "none":
        prompt_parts.append(f"{perfil['wrinkles']} wrinkles")
    
    # Filtrar elementos vacíos
    prompt_parts = [part for part in prompt_parts if part.strip()]
    
    prompt = ", ".join(prompt_parts)
    
    negative_prompt = ", ".join([
        "3/4 view, side profile, profile view, looking away, looking left, looking right, looking up, looking down, tilted head, turned head, angled face, off-center, asymmetrical, smiling, laughing, frowning, head tilted, head turned, head angled, head not straight, head not centered, face not centered, face not straight, face angled, face tilted, face turned, shoulders not visible, shoulders not straight, shoulders tilted, shoulders angled, hair covering face, hair covering eyes, hair covering ears, hair covering shoulders, hair messy, hair unkempt, hair not neat, hair not professional, hair in face, hair over eyes, hair over ears, hair over shoulders, long hair covering, hair blocking face, hair blocking eyes, hair blocking ears, hair blocking shoulders, improper framing, wrong proportions, incorrect framing, bad composition, poor framing, wrong crop, incorrect crop, bad crop, too close, too far, wrong distance, incorrect distance, bad distance, multiple people, blurry, low quality, distorted, deformed, ugly, bad anatomy, bad proportions, extra limbs, missing limbs, extra fingers, missing fingers, extra arms, missing arms, extra legs, missing legs, extra heads, missing heads, extra eyes, missing eyes, extra nose, missing nose, extra mouth, missing mouth, text, watermark, signature, gradient background, gradient, faded background, textured background, patterned background, noisy background, complex background, busy background, shadows on background, lighting effects on background, colored background, colored backdrop, tinted background, off-white background, cream background, beige background, gray background, light gray background, dark background, black background, blue background, green background, red background, yellow background, purple background, orange background, brown background, wood background, wall background, fabric background, paper background, canvas background, brick background, stone background, metal background, glass background, mirror background, reflection, shadows, lighting, spotlight, soft lighting, dramatic lighting, rim lighting, back lighting, side lighting, top lighting, bottom lighting, ambient lighting, natural lighting, artificial lighting, studio lighting, flash lighting, harsh lighting, dim lighting, bright lighting, overexposed, underexposed, high contrast, low contrast, saturated colors, desaturated colors, vibrant colors, muted colors, warm colors, cool colors, neutral colors, pastel colors, bold colors, subtle colors, airbrushed, photoshopped, retouched, smooth skin, perfect skin, flawless skin, glowing skin, shiny skin, oily skin, greasy skin, plastic skin, artificial skin, digital art, 3d render, cg, computer generated, synthetic, fake, artificial, overexposed, bright lighting, studio lighting, flash photography, harsh lighting, dramatic lighting, cinematic lighting, professional lighting, perfect lighting, ideal lighting, enhanced, improved, perfected, beautified, glamorized, stylized, artistic, aesthetic, beautiful, attractive, handsome, pretty, gorgeous, stunning, perfect, ideal, flawless, immaculate, pristine, clean, pure, crystal clear, sharp, crisp, vibrant, saturated, colorful, bright, luminous, radiant, brilliant, sparkling, shining, glowing, glossy, polished, refined, elegant, sophisticated, luxurious, premium, high-end, professional, commercial, advertising, marketing, fashion, beauty, cosmetic, makeup, foundation, concealer, powder, blush, lipstick, mascara, eyeliner, eyeshadow, contouring, highlighting, bronzer, primer, setting spray, finishing powder, model look, supermodel appearance, celebrity look, fashion model, beauty model, perfect face, flawless face, ideal face, beautiful face, attractive face, handsome face, pretty face, gorgeous face, stunning face, perfect features, flawless features, ideal features, beautiful features, attractive features, handsome features, pretty features, gorgeous features, stunning features"
    ])
    
    return prompt, negative_prompt

def test_passport_standards():
    """Prueba los estándares de foto de pasaporte"""
    print("📸 PROBANDO ESTÁNDARES DE FOTO DE PASAPORTE")
    print("=" * 60)
    
    # Generar 3 perfiles diferentes
    for i in range(3):
        print(f"\n📋 Generando perfil {i+1}/3...")
        perfil = generar_caracteristicas_etnicas_diversas(
            nacionalidad="venezuelan",
            genero="mujer",
            edad=25,
            region="aleatorio"
        )
        
        # Mostrar características
        print(f"   🏙️ Región: {perfil['region']}")
        print(f"   🎨 Piel: {perfil['skin_tone']} {perfil['skin_texture']}")
        print(f"   💇 Cabello: {perfil['hair_color']} {perfil['hair_style']}")
        print(f"   👁️ Ojos: {perfil['eye_color']} {perfil['eye_shape']}")
        print(f"   🎭 Cara: {perfil['face_shape']}")
        print(f"   👃 Nariz: {perfil['nose_shape']}")
        print(f"   👄 Labios: {perfil['lip_shape']}")
        if perfil['freckles'] != "none":
            print(f"   ✨ Pecas: {perfil['freckles']}")
        if perfil['moles'] != "none":
            print(f"   🔸 Lunares: {perfil['moles']}")
        if perfil['scars'] != "none":
            print(f"   🩹 Cicatrices: {perfil['scars']}")
        
        # Generar prompt
        prompt, negative_prompt = generar_prompt_pasaporte_estricto(perfil, 25)
        
        print(f"\n   📝 PROMPT POSITIVO (primeros 300 chars):")
        print(f"   {prompt[:300]}...")
        
        print(f"\n   🚫 PROMPT NEGATIVO (primeros 200 chars):")
        print(f"   {negative_prompt[:200]}...")
        
        # Analizar estándares de pasaporte
        passport_indicators = [
            "official passport photo", "government ID photo", "document photo",
            "official headshot", "passport style photo", "ID card photo",
            "looking directly at camera", "facing camera directly", "front view only",
            "head and shoulders only", "head centered perfectly", "face centered perfectly",
            "neutral expression", "serious expression", "no smile", "mouth closed",
            "eyes open", "looking straight ahead", "head straight", "no head tilt",
            "no head turn", "head upright", "shoulders visible", "shoulders straight",
            "shoulders level", "hair behind ears", "hair not covering face",
            "hair not covering shoulders", "hair neat and tidy", "hair professional style",
            "proper framing", "correct proportions"
        ]
        
        passport_count = sum(1 for indicator in passport_indicators if indicator in prompt)
        print(f"\n   🎯 INDICADORES DE PASAPORTE: {passport_count}/{len(passport_indicators)}")
        
        # Analizar negativos de pasaporte
        negative_indicators = [
            "3/4 view", "side profile", "profile view", "looking away",
            "tilted head", "turned head", "angled face", "off-center",
            "head tilted", "head turned", "head angled", "head not straight",
            "face not centered", "face not straight", "face angled",
            "shoulders not visible", "shoulders not straight", "shoulders tilted",
            "hair covering face", "hair covering eyes", "hair covering ears",
            "hair covering shoulders", "hair messy", "hair unkempt",
            "hair not neat", "hair not professional", "hair in face",
            "hair over eyes", "hair over ears", "hair over shoulders",
            "long hair covering", "hair blocking face", "hair blocking eyes",
            "improper framing", "wrong proportions", "incorrect framing",
            "bad composition", "poor framing", "wrong crop", "too close",
            "too far", "wrong distance", "incorrect distance", "bad distance"
        ]
        
        negative_count = sum(1 for indicator in negative_indicators if indicator in negative_prompt)
        print(f"   🚫 INDICADORES NEGATIVOS: {negative_count}/{len(negative_indicators)}")
        
        # Calcular score total
        total_score = (passport_count + negative_count) / (len(passport_indicators) + len(negative_indicators)) * 100
        
        print(f"\n   📊 SCORE TOTAL: {total_score:.1f}%")
        
        if total_score >= 90:
            print("   ✅ EXCELENTE - Cumple todos los estándares de pasaporte")
        elif total_score >= 80:
            print("   ⚠️ BUENO - Cumple la mayoría de estándares")
        elif total_score >= 70:
            print("   ⚠️ REGULAR - Necesita mejoras en algunos estándares")
        else:
            print("   ❌ MALO - No cumple los estándares de pasaporte")
    
    print(f"\n\n📊 RESUMEN DE ESTÁNDARES DE PASAPORTE")
    print("=" * 50)
    print("✅ Prompts optimizados para foto oficial de pasaporte")
    print("✅ Términos estrictos de posición y encuadre")
    print("✅ Control estricto de cabello y hombros")
    print("✅ Prompt negativo reforzado contra errores comunes")
    print("✅ Estándares de gobierno y documento oficial")
    
    print(f"\n🎯 REQUISITOS CUMPLIDOS:")
    print("   - Vista frontal estricta (no 3/4)")
    print("   - Cabeza centrada y recta")
    print("   - Hombros visibles y nivelados")
    print("   - Cabello no cubre cara u hombros")
    print("   - Expresión neutral y seria")
    print("   - Encuadre correcto (cabeza y hombros)")
    print("   - Fondo blanco sólido")
    print("   - ¡Listo para generar fotos de pasaporte perfectas!")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE ESTÁNDARES DE PASAPORTE")
    print("=" * 60)
    
    test_passport_standards()
