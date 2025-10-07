#!/usr/bin/env python3
"""
Utilidad para agregar nuevos países al sistema modular
"""

import json
import sys
from pathlib import Path

def create_country_template(country_code: str, country_name: str, regions: list) -> dict:
    """Crea un template para un nuevo país"""
    template = {
        "metadata": {
            "country_code": country_code,
            "country_name": country_name,
            "version": "1.0",
            "description": f"{country_name} - Diversidad regional basada en datos demográficos reales",
            "created": "2025-01-12",
            "based_on": "Datos demográficos reales y características regionales específicas"
        },
        "regions": {}
    }
    
    for region in regions:
        template["regions"][region["code"]] = {
            "name": region["name"],
            "description": region["description"],
            "demographics": {
                "european_heritage": 0.3,
                "mestizo": 0.4,
                "indigenous": 0.2,
                "african_heritage": 0.1
            },
            "skin_tones": {
                "very_light": 0.1,
                "light": 0.2,
                "medium_light": 0.3,
                "medium": 0.25,
                "medium_dark": 0.12,
                "dark": 0.03
            },
            "hair_colors": {
                "blonde": 0.05,
                "light_brown": 0.2,
                "medium_brown": 0.4,
                "dark_brown": 0.3,
                "black": 0.05
            },
            "hair_styles": {
                "straight": 0.4,
                "wavy": 0.35,
                "curly": 0.2,
                "afro": 0.05
            },
            "eye_colors": {
                "blue": 0.1,
                "green": 0.05,
                "hazel": 0.1,
                "brown": 0.6,
                "dark_brown": 0.15
            },
            "facial_structures": {
                "oval": 0.35,
                "round": 0.3,
                "square": 0.2,
                "heart_shaped": 0.15
            },
            "height_tendency": "average",
            "body_type": "mixed",
            "ethnic_characteristics": [
                f"{region['code']} {country_code} features",
                f"{region['name']} heritage",
                f"{region['code']} mixed ancestry",
                f"{region['code']} characteristics"
            ]
        }
    
    return template

def update_index(country_code: str, country_name: str, regions: list):
    """Actualiza el archivo de índice"""
    index_file = Path("index.json")
    
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
    else:
        index_data = {
            "metadata": {
                "version": "1.0",
                "description": "Índice de países con datos regionales disponibles",
                "created": "2025-01-12",
                "system": "modular_country_data"
            },
            "countries": {},
            "fallback_countries": []
        }
    
    # Agregar nuevo país al índice
    index_data["countries"][country_code] = {
        "file": f"{country_code}.json",
        "name": country_name,
        "regions_count": len(regions),
        "regions": [region["code"] for region in regions],
        "description": f"Diversidad regional basada en datos demográficos reales"
    }
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Índice actualizado con {country_name}")

def main():
    """Función principal"""
    if len(sys.argv) < 3:
        print("Uso: python add_country.py <country_code> <country_name> [region1,region2,...]")
        print("Ejemplo: python add_country.py colombiana Colombia norte,centro,sur")
        return
    
    country_code = sys.argv[1]
    country_name = sys.argv[2]
    
    if len(sys.argv) > 3:
        region_codes = sys.argv[3].split(',')
        regions = []
        for i, code in enumerate(region_codes):
            regions.append({
                "code": code.strip(),
                "name": f"Región {code.strip().title()}",
                "description": f"Descripción de la región {code.strip()}"
            })
    else:
        # Regiones por defecto
        regions = [
            {"code": "norte", "name": "Región Norte", "description": "Región norte del país"},
            {"code": "centro", "name": "Región Centro", "description": "Región central del país"},
            {"code": "sur", "name": "Región Sur", "description": "Región sur del país"}
        ]
    
    # Crear archivo del país
    country_data = create_country_template(country_code, country_name, regions)
    country_file = Path(f"{country_code}.json")
    
    with open(country_file, 'w', encoding='utf-8') as f:
        json.dump(country_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Archivo creado: {country_file}")
    
    # Actualizar índice
    update_index(country_code, country_name, regions)
    
    print(f"🎉 País {country_name} agregado exitosamente!")
    print(f"📁 Archivo: {country_file}")
    print(f"📊 Regiones: {len(regions)}")
    print(f"🔧 Edita el archivo para personalizar las características regionales")

if __name__ == "__main__":
    main()
