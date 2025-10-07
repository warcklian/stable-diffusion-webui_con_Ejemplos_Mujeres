#!/usr/bin/env python3
"""
Generador de Imágenes de Pasaportes Venezolanos
===============================================

Este script utiliza las configuraciones de la carpeta Consulta para generar
imágenes de pasaportes venezolanos con diversidad étnica masiva.

Características:
- Fotos de pasaporte con estándares ICAO/SAIME
- Fondo transparente (PNG con canal alfa)
- Diversidad étnica auténtica
- Configuraciones optimizadas para cada nacionalidad
- Generación en lotes automatizada

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import json
import os
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

class GeneradorPasaportes:
    """Generador de imágenes de pasaportes venezolanos con diversidad étnica."""
    
    def __init__(self, consulta_dir: str = "Consulta"):
        """
        Inicializa el generador con las configuraciones de la carpeta Consulta.
        
        Args:
            consulta_dir: Ruta a la carpeta Consulta con las configuraciones
        """
        self.consulta_dir = Path(consulta_dir)
        self.config = self._cargar_configuracion()
        self.prompts = self._cargar_prompts()
        self.datos_etnicos = self._cargar_datos_etnicos()
        
    def _cargar_configuracion(self) -> Dict[str, Any]:
        """Carga la configuración principal desde gui_config.json."""
        config_path = self.consulta_dir / "gui_config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"No se encontró {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _cargar_prompts(self) -> Dict[str, Any]:
        """Carga los prompts optimizados desde optimized_prompts.json."""
        prompts_path = self.consulta_dir / "optimized_prompts.json"
        if not prompts_path.exists():
            raise FileNotFoundError(f"No se encontró {prompts_path}")
        
        with open(prompts_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _cargar_datos_etnicos(self) -> Dict[str, Any]:
        """Carga los datos étnicos desde intelligent_ethnic_data.json."""
        datos_path = self.consulta_dir / "intelligent_ethnic_data.json"
        if not datos_path.exists():
            raise FileNotFoundError(f"No se encontró {datos_path}")
        
        with open(datos_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generar_caracteristicas_etnicas(self, nacionalidad: str) -> Dict[str, str]:
        """
        Genera características étnicas aleatorias basadas en los datos demográficos.
        
        Args:
            nacionalidad: Nacionalidad para la cual generar características
            
        Returns:
            Diccionario con las características generadas
        """
        if nacionalidad not in self.datos_etnicos:
            raise ValueError(f"Nacionalidad '{nacionalidad}' no encontrada en los datos étnicos")
        
        datos = self.datos_etnicos[nacionalidad]
        caracteristicas = {}
        
        # Generar tono de piel
        skin_tones = datos.get('skin_tones', {})
        caracteristicas['skin_tone'] = self._seleccionar_por_probabilidad(skin_tones)
        
        # Generar color de cabello
        hair_colors = datos.get('hair_colors', {})
        caracteristicas['hair_color'] = self._seleccionar_por_probabilidad(hair_colors)
        
        # Generar estilo de cabello
        hair_styles = datos.get('hair_styles', {})
        caracteristicas['hair_style'] = self._seleccionar_por_probabilidad(hair_styles)
        
        # Generar color de ojos
        eye_colors = datos.get('eye_colors', {})
        caracteristicas['eye_color'] = self._seleccionar_por_probabilidad(eye_colors)
        
        # Generar estructura facial
        facial_structures = datos.get('facial_structures', {})
        caracteristicas['facial_structure'] = self._seleccionar_por_probabilidad(facial_structures)
        
        # Generar características étnicas
        ethnic_characteristics = datos.get('ethnic_characteristics', {})
        caracteristicas['ethnic_characteristics'] = self._seleccionar_por_probabilidad(ethnic_characteristics)
        
        return caracteristicas
    
    def _seleccionar_por_probabilidad(self, opciones: Dict[str, float]) -> str:
        """
        Selecciona una opción basada en sus probabilidades.
        
        Args:
            opciones: Diccionario con opciones y sus probabilidades
            
        Returns:
            Opción seleccionada
        """
        rand = random.random()
        acumulado = 0.0
        
        for opcion, probabilidad in opciones.items():
            acumulado += probabilidad
            if rand <= acumulado:
                return opcion
        
        # Fallback: devolver la primera opción
        return list(opciones.keys())[0]
    
    def generar_prompt_completo(self, nacionalidad: str, genero: str = "mujer", 
                              edad_min: int = 18, edad_max: int = 60) -> tuple:
        """
        Genera un prompt completo para la generación de imágenes.
        
        Args:
            nacionalidad: Nacionalidad de la persona
            genero: Género (mujer/hombre)
            edad_min: Edad mínima
            edad_max: Edad máxima
            
        Returns:
            Tupla con (prompt_positivo, prompt_negativo)
        """
        # Obtener características étnicas
        caracteristicas = self.generar_caracteristicas_etnicas(nacionalidad)
        
        # Usar el template de passport_photography
        template = self.prompts.get('passport_photography', {})
        base_prompt = template.get('base_prompt', '')
        negative_prompt = template.get('negative_prompt', '')
        
        # Reemplazar variables en el prompt
        replacements = {
            '{gender}': genero,
            '{nationality}': nacionalidad,
            '{age_range}': f"{edad_min}-{edad_max} years old",
            '{skin_tone}': caracteristicas.get('skin_tone', 'natural skin tone'),
            '{hair_color}': caracteristicas.get('hair_color', 'natural hair color'),
            '{hair_style}': caracteristicas.get('hair_style', 'natural hair style'),
            '{eye_color}': caracteristicas.get('eye_color', 'natural eye color'),
            '{facial_structure}': caracteristicas.get('facial_structure', 'natural facial structure'),
            '{ethnic_characteristics}': caracteristicas.get('ethnic_characteristics', 'natural ethnic characteristics'),
            '{facial_wrinkles}': 'natural facial wrinkles',
            '{expression_lines}': 'natural expression lines',
            '{eye_bags}': 'natural eye area',
            '{skin_texture}': 'natural skin texture',
            '{age_spots}': 'natural age spots',
            '{pores_texture}': 'natural pores',
            '{acne_scars}': 'natural skin variations',
            '{moles_freckles}': 'natural moles and freckles',
            '{facial_asymmetry}': 'natural facial asymmetry',
            '{skin_imperfections}': 'natural skin imperfections',
            '{unique_features}': 'natural unique features',
            '{hair_graying}': 'natural hair graying',
            '{hair_texture_age}': 'natural hair texture for age',
            '{hair_density}': 'natural hair density',
            '{hair_loss}': 'natural hair variations'
        }
        
        # Aplicar reemplazos
        prompt_positivo = base_prompt
        for placeholder, valor in replacements.items():
            prompt_positivo = prompt_positivo.replace(placeholder, valor)
        
        return prompt_positivo, negative_prompt
    
    def generar_lote_imagenes(self, nacionalidades: List[str], cantidad_por_nacionalidad: int = 5,
                            genero: str = "mujer", edad_min: int = 18, edad_max: int = 60) -> List[Dict]:
        """
        Genera un lote de configuraciones para múltiples imágenes.
        
        Args:
            nacionalidades: Lista de nacionalidades a generar
            cantidad_por_nacionalidad: Cantidad de imágenes por nacionalidad
            genero: Género de las personas
            edad_min: Edad mínima
            edad_max: Edad máxima
            
        Returns:
            Lista de configuraciones para generar imágenes
        """
        configuraciones = []
        
        for nacionalidad in nacionalidades:
            for i in range(cantidad_por_nacionalidad):
                prompt_positivo, prompt_negativo = self.generar_prompt_completo(
                    nacionalidad, genero, edad_min, edad_max
                )
                
                configuracion = {
                    'id': f"{nacionalidad}_{i+1:03d}",
                    'nacionalidad': nacionalidad,
                    'genero': genero,
                    'edad_min': edad_min,
                    'edad_max': edad_max,
                    'prompt_positivo': prompt_positivo,
                    'prompt_negativo': prompt_negativo,
                    'configuracion_tecnica': {
                        'width': self.config.get('width', 1024),
                        'height': self.config.get('height', 1024),
                        'steps': self.config.get('steps', 30),
                        'cfg_scale': self.config.get('cfg_scale', 8.0),
                        'sampler': self.config.get('sampler', 'DPM++ 2M Karras'),
                        'model': self.config.get('model', 'aidmaRealisticPeoplePhotograph-FLUX-V0.2.safetensors [a6e3441be6]')
                    }
                }
                
                configuraciones.append(configuracion)
        
        return configuraciones
    
    def guardar_configuracion_lote(self, configuraciones: List[Dict], 
                                 archivo_salida: str = "lote_pasaportes.json"):
        """
        Guarda las configuraciones del lote en un archivo JSON.
        
        Args:
            configuraciones: Lista de configuraciones
            archivo_salida: Nombre del archivo de salida
        """
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_imagenes': len(configuraciones),
                    'nacionalidades': list(set(c['nacionalidad'] for c in configuraciones)),
                    'genero': configuraciones[0]['genero'] if configuraciones else 'N/A',
                    'rango_edad': f"{configuraciones[0]['edad_min']}-{configuraciones[0]['edad_max']}" if configuraciones else 'N/A',
                    'fecha_generacion': '2025-01-12',
                    'descripcion': 'Lote de configuraciones para generación de pasaportes venezolanos con diversidad étnica'
                },
                'configuraciones': configuraciones
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuraciones guardadas en: {archivo_salida}")
        print(f"📊 Total de imágenes: {len(configuraciones)}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de las nacionalidades disponibles."""
        print("\n📊 ESTADÍSTICAS DE NACIONALIDADES DISPONIBLES")
        print("=" * 50)
        
        for nacionalidad, datos in self.datos_etnicos.items():
            descripcion = datos.get('description', 'Sin descripción')
            print(f"\n🌍 {nacionalidad.upper()}")
            print(f"   Descripción: {descripcion}")
            
            # Mostrar distribución de tonos de piel
            skin_tones = datos.get('skin_tones', {})
            if skin_tones:
                print("   Tonos de piel:")
                for tono, prob in skin_tones.items():
                    print(f"     - {tono}: {prob*100:.1f}%")
        
        print(f"\n📈 Total de nacionalidades: {len(self.datos_etnicos)}")

def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Generador de Imágenes de Pasaportes Venezolanos')
    parser.add_argument('--nacionalidades', nargs='+', 
                       default=['venezuelan', 'cuban', 'haitian', 'dominican', 'mexican'],
                       help='Nacionalidades a generar (por defecto: venezuelan cuban haitian dominican mexican)')
    parser.add_argument('--cantidad', type=int, default=5,
                       help='Cantidad de imágenes por nacionalidad (por defecto: 5)')
    parser.add_argument('--genero', choices=['mujer', 'hombre'], default='mujer',
                       help='Género de las personas (por defecto: mujer)')
    parser.add_argument('--edad-min', type=int, default=18,
                       help='Edad mínima (por defecto: 18)')
    parser.add_argument('--edad-max', type=int, default=60,
                       help='Edad máxima (por defecto: 60)')
    parser.add_argument('--output', default='lote_pasaportes.json',
                       help='Archivo de salida (por defecto: lote_pasaportes.json)')
    parser.add_argument('--estadisticas', action='store_true',
                       help='Mostrar estadísticas de nacionalidades disponibles')
    
    args = parser.parse_args()
    
    try:
        # Inicializar generador
        print("🚀 Iniciando Generador de Pasaportes Venezolanos...")
        generador = GeneradorPasaportes()
        
        if args.estadisticas:
            generador.mostrar_estadisticas()
            return
        
        # Validar nacionalidades
        nacionalidades_validas = list(generador.datos_etnicos.keys())
        nacionalidades_invalidas = [n for n in args.nacionalidades if n not in nacionalidades_validas]
        
        if nacionalidades_invalidas:
            print(f"❌ Error: Nacionalidades no válidas: {nacionalidades_invalidas}")
            print(f"✅ Nacionalidades disponibles: {', '.join(nacionalidades_validas)}")
            return
        
        # Generar configuraciones
        print(f"\n🎯 Generando configuraciones para:")
        print(f"   📍 Nacionalidades: {', '.join(args.nacionalidades)}")
        print(f"   👤 Género: {args.genero}")
        print(f"   🎂 Edad: {args.edad_min}-{args.edad_max} años")
        print(f"   📊 Cantidad por nacionalidad: {args.cantidad}")
        
        configuraciones = generador.generar_lote_imagenes(
            args.nacionalidades, args.cantidad, args.genero, 
            args.edad_min, args.edad_max
        )
        
        # Guardar configuraciones
        generador.guardar_configuracion_lote(configuraciones, args.output)
        
        print(f"\n✅ ¡Generación completada exitosamente!")
        print(f"📁 Archivo generado: {args.output}")
        print(f"🔧 Próximo paso: Usar este archivo con Stable Diffusion WebUI")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
