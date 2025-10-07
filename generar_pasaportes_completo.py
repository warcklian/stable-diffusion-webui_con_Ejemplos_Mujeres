#!/usr/bin/env python3
"""
Sistema Completo de Generación de Pasaportes Venezolanos
========================================================

Este script integra todo el sistema para generar imágenes de pasaportes
venezolanos con diversidad étnica masiva usando Stable Diffusion WebUI.

Flujo completo:
1. Generar configuraciones basadas en datos étnicos
2. Conectar con Stable Diffusion WebUI
3. Generar imágenes en lotes
4. Guardar con nombres descriptivos
5. Generar reporte de resultados

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path

# Importar nuestros módulos
try:
    from generar_pasaportes import GeneradorPasaportes
    from webui_pasaportes import WebUIPasaportes
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("💡 Asegúrate de que los archivos generar_pasaportes.py y webui_pasaportes.py estén en el mismo directorio")
    sys.exit(1)

class SistemaPasaportesCompleto:
    """Sistema completo para generar pasaportes venezolanos."""
    
    def __init__(self, consulta_dir: str = "Consulta", webui_url: str = "http://localhost:7860"):
        """
        Inicializa el sistema completo.
        
        Args:
            consulta_dir: Directorio con las configuraciones
            webui_url: URL de Stable Diffusion WebUI
        """
        self.generador = GeneradorPasaportes(consulta_dir)
        self.webui = WebUIPasaportes(webui_url)
        self.webui_url = webui_url
        
    def verificar_prerequisitos(self) -> bool:
        """
        Verifica que todos los prerequisitos estén cumplidos.
        
        Returns:
            True si todo está listo, False en caso contrario
        """
        print("🔍 Verificando prerequisitos...")
        
        # Verificar archivos de configuración
        if not Path(self.generador.consulta_dir).exists():
            print(f"❌ No se encontró el directorio {self.generador.consulta_dir}")
            return False
        
        # Verificar conexión con WebUI
        if not self.webui.verificar_conexion():
            print(f"❌ No se puede conectar a Stable Diffusion WebUI en {self.webui_url}")
            print("💡 Asegúrate de que WebUI esté ejecutándose:")
            print("   ./webui.sh")
            return False
        
        print("✅ Todos los prerequisitos están cumplidos")
        return True
    
    def generar_y_procesar_lote(self, nacionalidades: list, cantidad_por_nacionalidad: int = 5,
                              genero: str = "mujer", edad_min: int = 18, edad_max: int = 60,
                              directorio_salida: str = "outputs/pasaportes",
                              modelo_preferido: str = None) -> dict:
        """
        Genera configuraciones y procesa el lote completo.
        
        Args:
            nacionalidades: Lista de nacionalidades
            cantidad_por_nacionalidad: Cantidad por nacionalidad
            genero: Género de las personas
            edad_min: Edad mínima
            edad_max: Edad máxima
            directorio_salida: Directorio de salida
            modelo_preferido: Modelo específico a usar
            
        Returns:
            Diccionario con estadísticas completas
        """
        print("🚀 Iniciando generación y procesamiento completo...")
        
        # Paso 1: Generar configuraciones
        print("\n📝 Paso 1: Generando configuraciones...")
        configuraciones = self.generador.generar_lote_imagenes(
            nacionalidades, cantidad_por_nacionalidad, genero, edad_min, edad_max
        )
        
        # Guardar configuraciones temporalmente
        archivo_temp = "temp_configuraciones.json"
        self.generador.guardar_configuracion_lote(configuraciones, archivo_temp)
        
        # Paso 2: Procesar con WebUI
        print("\n🎨 Paso 2: Generando imágenes con WebUI...")
        estadisticas = self.webui.procesar_lote(archivo_temp, directorio_salida, modelo_preferido)
        
        # Limpiar archivo temporal
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)
        
        # Agregar información adicional a las estadísticas
        estadisticas['configuracion'] = {
            'nacionalidades': nacionalidades,
            'cantidad_por_nacionalidad': cantidad_por_nacionalidad,
            'genero': genero,
            'edad_min': edad_min,
            'edad_max': edad_max,
            'directorio_salida': directorio_salida,
            'modelo_usado': modelo_preferido
        }
        
        return estadisticas
    
    def generar_reporte(self, estadisticas: dict, archivo_reporte: str = "reporte_pasaportes.json"):
        """
        Genera un reporte detallado del procesamiento.
        
        Args:
            estadisticas: Estadísticas del procesamiento
            archivo_reporte: Archivo donde guardar el reporte
        """
        reporte = {
            'metadata': {
                'fecha_generacion': time.strftime('%Y-%m-%d %H:%M:%S'),
                'sistema': 'Generador de Pasaportes Venezolanos',
                'version': '1.0',
                'webui_url': self.webui_url
            },
            'configuracion': estadisticas.get('configuracion', {}),
            'estadisticas': {
                'total_imagenes': estadisticas['total'],
                'exitosas': estadisticas['exitosas'],
                'fallidas': estadisticas['fallidas'],
                'tasa_exito': (estadisticas['exitosas'] / estadisticas['total'] * 100) if estadisticas['total'] > 0 else 0
            },
            'archivos_generados': estadisticas.get('archivos_generados', []),
            'errores': estadisticas.get('errores', [])
        }
        
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Reporte guardado en: {archivo_reporte}")
    
    def mostrar_resumen_final(self, estadisticas: dict):
        """Muestra un resumen final del procesamiento."""
        print(f"\n🎉 RESUMEN FINAL DEL PROCESAMIENTO")
        print("=" * 50)
        
        config = estadisticas.get('configuracion', {})
        print(f"🌍 Nacionalidades procesadas: {', '.join(config.get('nacionalidades', []))}")
        print(f"👤 Género: {config.get('genero', 'N/A')}")
        print(f"🎂 Rango de edad: {config.get('edad_min', 'N/A')}-{config.get('edad_max', 'N/A')} años")
        print(f"📁 Directorio de salida: {config.get('directorio_salida', 'N/A')}")
        
        print(f"\n📊 Estadísticas:")
        print(f"   ✅ Imágenes exitosas: {estadisticas['exitosas']}")
        print(f"   ❌ Imágenes fallidas: {estadisticas['fallidas']}")
        print(f"   📈 Tasa de éxito: {(estadisticas['exitosas']/estadisticas['total']*100):.1f}%")
        
        if estadisticas.get('archivos_generados'):
            print(f"\n📁 Archivos generados ({len(estadisticas['archivos_generados'])}):")
            for archivo in estadisticas['archivos_generados'][:5]:  # Mostrar solo los primeros 5
                print(f"   - {archivo}")
            if len(estadisticas['archivos_generados']) > 5:
                print(f"   ... y {len(estadisticas['archivos_generados']) - 5} más")

def main():
    """Función principal del sistema completo."""
    parser = argparse.ArgumentParser(description='Sistema Completo de Generación de Pasaportes Venezolanos')
    
    # Argumentos de configuración
    parser.add_argument('--nacionalidades', nargs='+', 
                       default=['venezuelan', 'cuban', 'haitian'],
                       help='Nacionalidades a generar (por defecto: venezuelan cuban haitian)')
    parser.add_argument('--cantidad', type=int, default=3,
                       help='Cantidad de imágenes por nacionalidad (por defecto: 3)')
    parser.add_argument('--genero', choices=['mujer', 'hombre'], default='mujer',
                       help='Género de las personas (por defecto: mujer)')
    parser.add_argument('--edad-min', type=int, default=18,
                       help='Edad mínima (por defecto: 18)')
    parser.add_argument('--edad-max', type=int, default=60,
                       help='Edad máxima (por defecto: 60)')
    
    # Argumentos de sistema
    parser.add_argument('--webui-url', default='http://localhost:7860',
                       help='URL de Stable Diffusion WebUI (por defecto: http://localhost:7860)')
    parser.add_argument('--output', default='outputs/pasaportes',
                       help='Directorio de salida (por defecto: outputs/pasaportes)')
    parser.add_argument('--modelo', 
                       help='Modelo específico a usar (opcional)')
    parser.add_argument('--consulta-dir', default='Consulta',
                       help='Directorio con configuraciones (por defecto: Consulta)')
    parser.add_argument('--reporte', default='reporte_pasaportes.json',
                       help='Archivo de reporte (por defecto: reporte_pasaportes.json)')
    
    # Argumentos de utilidad
    parser.add_argument('--estadisticas', action='store_true',
                       help='Mostrar estadísticas de nacionalidades disponibles')
    parser.add_argument('--listar-modelos', action='store_true',
                       help='Listar modelos disponibles en WebUI')
    parser.add_argument('--solo-configuraciones', action='store_true',
                       help='Solo generar configuraciones, no procesar imágenes')
    
    args = parser.parse_args()
    
    try:
        # Inicializar sistema
        print("🚀 Sistema Completo de Generación de Pasaportes Venezolanos")
        print("=" * 60)
        
        sistema = SistemaPasaportesCompleto(args.consulta_dir, args.webui_url)
        
        # Mostrar estadísticas si se solicita
        if args.estadisticas:
            sistema.generador.mostrar_estadisticas()
            return 0
        
        # Listar modelos si se solicita
        if args.listar_modelos:
            print("🔄 Obteniendo modelos disponibles...")
            modelos = sistema.webui.obtener_modelos_disponibles()
            if modelos:
                print(f"\n📋 Modelos disponibles ({len(modelos)}):")
                for modelo in modelos:
                    print(f"   - {modelo}")
            else:
                print("❌ No se pudieron obtener los modelos")
            return 0
        
        # Solo generar configuraciones si se solicita
        if args.solo_configuraciones:
            print("📝 Generando solo configuraciones...")
            configuraciones = sistema.generador.generar_lote_imagenes(
                args.nacionalidades, args.cantidad, args.genero, 
                args.edad_min, args.edad_max
            )
            sistema.generador.guardar_configuracion_lote(configuraciones, "configuraciones_pasaportes.json")
            return 0
        
        # Verificar prerequisitos
        if not sistema.verificar_prerequisitos():
            return 1
        
        # Procesar lote completo
        estadisticas = sistema.generar_y_procesar_lote(
            args.nacionalidades, args.cantidad, args.genero,
            args.edad_min, args.edad_max, args.output, args.modelo
        )
        
        # Generar reporte
        sistema.generar_reporte(estadisticas, args.reporte)
        
        # Mostrar resumen final
        sistema.mostrar_resumen_final(estadisticas)
        
        print(f"\n🎉 ¡Procesamiento completado exitosamente!")
        print(f"📊 Reporte detallado: {args.reporte}")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Procesamiento interrumpido por el usuario")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
