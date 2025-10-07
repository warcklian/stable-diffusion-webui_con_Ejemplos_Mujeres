#!/usr/bin/env python3
"""
Sistema de Diversidad Regional para Venezuela
=============================================

Genera personas de todas las regiones de Venezuela de forma aleatoria
para maximizar la diversidad étnica y geográfica.
"""

import random
from typing import Dict, List, Any

class DiversidadRegional:
    """Sistema para generar diversidad regional venezolana."""
    
    def __init__(self):
        """Inicializa el sistema con todas las regiones de Venezuela."""
        self.regiones_venezuela = {
            # Región Capital
            "caracas": {
                "nombre": "Caracas",
                "caracteristicas": "urban, metropolitan, diverse ethnicity",
                "rasgos_tipicos": "mixed heritage, urban features"
            },
            
            # Región Central
            "valencia": {
                "nombre": "Valencia",
                "caracteristicas": "industrial, coastal influence",
                "rasgos_tipicos": "Mediterranean influence, mixed heritage"
            },
            "maracay": {
                "nombre": "Maracay",
                "caracteristicas": "agricultural, military influence",
                "rasgos_tipicos": "rural-urban mix, diverse features"
            },
            
            # Región Occidental
            "maracaibo": {
                "nombre": "Maracaibo",
                "caracteristicas": "oil industry, coastal",
                "rasgos_tipicos": "Caribbean influence, diverse ethnicity"
            },
            "barquisimeto": {
                "nombre": "Barquisimeto",
                "caracteristicas": "agricultural, commercial",
                "rasgos_tipicos": "mixed heritage, regional features"
            },
            
            # Región Oriental
            "ciudad_guayana": {
                "nombre": "Ciudad Guayana",
                "caracteristicas": "industrial, mining",
                "rasgos_tipicos": "diverse ethnicity, mixed heritage"
            },
            "cumana": {
                "nombre": "Cumaná",
                "caracteristicas": "coastal, historical",
                "rasgos_tipicos": "Caribbean influence, mixed heritage"
            },
            "maturin": {
                "nombre": "Maturín",
                "caracteristicas": "oil industry, agricultural",
                "rasgos_tipicos": "diverse ethnicity, regional features"
            },
            
            # Región Andina
            "merida": {
                "nombre": "Mérida",
                "caracteristicas": "mountainous, university town",
                "rasgos_tipicos": "Andean features, mixed heritage"
            },
            "san_cristobal": {
                "nombre": "San Cristóbal",
                "caracteristicas": "border city, commercial",
                "rasgos_tipicos": "diverse ethnicity, regional features"
            },
            
            # Región Llanera
            "san_fernando": {
                "nombre": "San Fernando de Apure",
                "caracteristicas": "llanos, agricultural",
                "rasgos_tipicos": "rural features, mixed heritage"
            },
            "barinas": {
                "nombre": "Barinas",
                "caracteristicas": "agricultural, oil",
                "rasgos_tipicos": "diverse ethnicity, regional features"
            },
            
            # Región Guayana
            "ciudad_bolivar": {
                "nombre": "Ciudad Bolívar",
                "caracteristicas": "historical, river port",
                "rasgos_tipicos": "mixed heritage, regional features"
            },
            "puerto_ayacucho": {
                "nombre": "Puerto Ayacucho",
                "caracteristicas": "Amazon region, indigenous influence",
                "rasgos_tipicos": "indigenous features, mixed heritage"
            }
        }
    
    def obtener_region_aleatoria(self) -> Dict[str, str]:
        """
        Obtiene una región aleatoria de Venezuela.
        
        Returns:
            Diccionario con información de la región
        """
        region_key = random.choice(list(self.regiones_venezuela.keys()))
        region_data = self.regiones_venezuela[region_key].copy()
        region_data['codigo'] = region_key
        return region_data
    
    def generar_prompt_regional(self, region_data: Dict[str, str]) -> str:
        """
        Genera prompt específico para la región.
        
        Args:
            region_data: Datos de la región seleccionada
            
        Returns:
            Prompt enriquecido con características regionales
        """
        nombre = region_data['nombre']
        caracteristicas = region_data['caracteristicas']
        rasgos = region_data['rasgos_tipicos']
        
        return f"venezuelan woman from {nombre} region, {caracteristicas}, {rasgos}"
    
    def generar_lote_diverso(self, cantidad: int = 10) -> List[Dict[str, Any]]:
        """
        Genera un lote diverso de perfiles regionales.
        
        Args:
            cantidad: Número de perfiles a generar
            
        Returns:
            Lista de perfiles con diversidad regional
        """
        perfiles = []
        
        for i in range(cantidad):
            region = self.obtener_region_aleatoria()
            
            perfil = {
                'id': f"diverso_{i+1:03d}",
                'region': region['codigo'],
                'region_nombre': region['nombre'],
                'prompt_regional': self.generar_prompt_regional(region),
                'caracteristicas': region['caracteristicas'],
                'rasgos_tipicos': region['rasgos_tipicos']
            }
            
            perfiles.append(perfil)
        
        return perfiles
    
    def mostrar_estadisticas_diversidad(self, perfiles: List[Dict[str, Any]]):
        """Muestra estadísticas de diversidad regional."""
        print(f"\n🌍 DIVERSIDAD REGIONAL GENERADA")
        print("=" * 50)
        
        regiones_usadas = {}
        for perfil in perfiles:
            region = perfil['region_nombre']
            regiones_usadas[region] = regiones_usadas.get(region, 0) + 1
        
        print(f"📊 Total de perfiles: {len(perfiles)}")
        print(f"🗺️  Regiones representadas: {len(regiones_usadas)}")
        
        print(f"\n📍 Distribución por región:")
        for region, count in sorted(regiones_usadas.items()):
            print(f"   {region}: {count} perfiles")

def main():
    """Función principal para probar el sistema."""
    print("🌍 SISTEMA DE DIVERSIDAD REGIONAL VENEZOLANA")
    print("=" * 60)
    
    # Crear sistema
    diversidad = DiversidadRegional()
    
    # Generar lote diverso
    print("🔄 Generando lote diverso...")
    perfiles = diversidad.generar_lote_diverso(15)
    
    # Mostrar resultados
    print(f"\n📋 PERFILES GENERADOS:")
    for i, perfil in enumerate(perfiles, 1):
        print(f"{i:2d}. {perfil['region_nombre']} - {perfil['prompt_regional']}")
    
    # Mostrar estadísticas
    diversidad.mostrar_estadisticas_diversidad(perfiles)
    
    print(f"\n✅ Sistema de diversidad regional listo para usar")

if __name__ == "__main__":
    main()
