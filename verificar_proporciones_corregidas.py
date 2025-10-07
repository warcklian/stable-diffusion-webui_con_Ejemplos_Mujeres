#!/usr/bin/env python3
"""
Script de Verificación de Proporciones Corregidas
================================================

Este script verifica que las configuraciones han sido corregidas correctamente
para solucionar el problema de estiramiento en las imágenes de pasaportes.

Verifica:
- Resolución cambiada de 512x512 a 512x640 (formato 4:5)
- Prompts actualizados con instrucciones anti-estiramiento
- Configuraciones SAIME estándar implementadas

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

class VerificadorProporciones:
    """Verificador de correcciones de proporciones en configuraciones de pasaportes."""
    
    def __init__(self, consulta_dir: str = "Consulta"):
        """
        Inicializa el verificador.
        
        Args:
            consulta_dir: Directorio con las configuraciones
        """
        self.consulta_dir = Path(consulta_dir)
        self.correcciones_aplicadas = []
        self.problemas_encontrados = []
        
    def verificar_resolucion_corregida(self, config: Dict[str, Any], archivo: str) -> bool:
        """
        Verifica que la resolución esté corregida a formato rectangular.
        
        Args:
            config: Configuración a verificar
            archivo: Nombre del archivo
            
        Returns:
            True si está corregida, False en caso contrario
        """
        try:
            # Verificar configuración de generación (para plantillas)
            generation = config.get('config', {}).get('generation', {})
            width = generation.get('width', 0)
            height = generation.get('height', 0)
            
            # Si no hay configuración de generación, verificar estructura directa (para gui_config.json)
            if width == 0 and height == 0:
                width = config.get('width', 0)
                height = config.get('height', 0)
            
            # Verificar que no sea cuadrado
            if width == height:
                self.problemas_encontrados.append(f"❌ {archivo}: Resolución cuadrada {width}x{height}")
                return False
            
            # Verificar formato 4:5 (512x640)
            if width == 512 and height == 640:
                self.correcciones_aplicadas.append(f"✅ {archivo}: Resolución corregida {width}x{height} (4:5)")
                return True
            elif width == 512 and height > 512:
                self.correcciones_aplicadas.append(f"✅ {archivo}: Resolución rectangular {width}x{height}")
                return True
            else:
                self.problemas_encontrados.append(f"⚠️ {archivo}: Resolución inusual {width}x{height}")
                return False
                
        except Exception as e:
            self.problemas_encontrados.append(f"❌ {archivo}: Error verificando resolución: {e}")
            return False
    
    def verificar_prompts_anti_estiramiento(self, config: Dict[str, Any], archivo: str) -> bool:
        """
        Verifica que los prompts contengan instrucciones anti-estiramiento.
        
        Args:
            config: Configuración a verificar
            archivo: Nombre del archivo
            
        Returns:
            True si tiene instrucciones anti-estiramiento, False en caso contrario
        """
        try:
            # Buscar en base_prompt o prompts (para plantillas)
            base_prompt = config.get('config', {}).get('base_prompt', '')
            prompts = config.get('config', {}).get('prompts', {})
            base_prompt_prompts = prompts.get('base_prompt', '') if isinstance(prompts, dict) else ''
            
            # Si no hay configuración de prompts, verificar estructura directa (para gui_config.json)
            if not base_prompt and not base_prompt_prompts:
                base_prompt = config.get('base_prompt', '')
            
            prompt_completo = f"{base_prompt} {base_prompt_prompts}".lower()
            
            # Instrucciones anti-estiramiento que deben estar presentes
            instrucciones_requeridas = [
                'rectangular',
                '4:5',
                'natural head proportions',
                'no vertical stretching',
                'no head stretching',
                'proper head positioning'
            ]
            
            instrucciones_encontradas = []
            for instruccion in instrucciones_requeridas:
                if instruccion in prompt_completo:
                    instrucciones_encontradas.append(instruccion)
            
            if len(instrucciones_encontradas) >= 3:
                self.correcciones_aplicadas.append(f"✅ {archivo}: Prompts anti-estiramiento encontrados ({len(instrucciones_encontradas)}/6)")
                return True
            else:
                self.problemas_encontrados.append(f"⚠️ {archivo}: Faltan instrucciones anti-estiramiento ({len(instrucciones_encontradas)}/6)")
                return False
                
        except Exception as e:
            self.problemas_encontrados.append(f"❌ {archivo}: Error verificando prompts: {e}")
            return False
    
    def verificar_estandares_saime(self, config: Dict[str, Any], archivo: str) -> bool:
        """
        Verifica que se implementen estándares SAIME.
        
        Args:
            config: Configuración a verificar
            archivo: Nombre del archivo
            
        Returns:
            True si tiene estándares SAIME, False en caso contrario
        """
        try:
            # Buscar estándares SAIME (para plantillas)
            saime_standards = config.get('config', {}).get('saime_standards', {})
            base_prompt = config.get('config', {}).get('base_prompt', '')
            
            # Si no hay configuración de prompts, verificar estructura directa (para gui_config.json)
            if not base_prompt:
                base_prompt = config.get('base_prompt', '')
            
            # Verificar estándares SAIME
            if saime_standards:
                self.correcciones_aplicadas.append(f"✅ {archivo}: Estándares SAIME implementados")
                return True
            elif 'saime' in base_prompt.lower():
                self.correcciones_aplicadas.append(f"✅ {archivo}: Referencias SAIME en prompt")
                return True
            else:
                self.problemas_encontrados.append(f"⚠️ {archivo}: No se encontraron estándares SAIME")
                return False
                
        except Exception as e:
            self.problemas_encontrados.append(f"❌ {archivo}: Error verificando estándares SAIME: {e}")
            return False
    
    def verificar_archivo_configuracion(self, archivo_path: Path) -> Dict[str, bool]:
        """
        Verifica un archivo de configuración específico.
        
        Args:
            archivo_path: Ruta al archivo de configuración
            
        Returns:
            Diccionario con resultados de verificación
        """
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            archivo_nombre = archivo_path.name
            
            resultados = {
                'archivo': archivo_nombre,
                'resolucion_corregida': self.verificar_resolucion_corregida(config, archivo_nombre),
                'prompts_anti_estiramiento': self.verificar_prompts_anti_estiramiento(config, archivo_nombre),
                'estandares_saime': self.verificar_estandares_saime(config, archivo_nombre)
            }
            
            return resultados
            
        except Exception as e:
            self.problemas_encontrados.append(f"❌ {archivo_path.name}: Error cargando archivo: {e}")
            return {
                'archivo': archivo_path.name,
                'resolucion_corregida': False,
                'prompts_anti_estiramiento': False,
                'estandares_saime': False,
                'error': str(e)
            }
    
    def verificar_todas_configuraciones(self) -> Dict[str, Any]:
        """
        Verifica todas las configuraciones del sistema.
        
        Returns:
            Diccionario con resultados completos
        """
        print("🔍 Verificando correcciones de proporciones...")
        print("=" * 60)
        
        resultados = {
            'archivos_verificados': [],
            'correcciones_aplicadas': [],
            'problemas_encontrados': [],
            'resumen': {}
        }
        
        # Verificar archivo principal
        gui_config_path = self.consulta_dir / "gui_config.json"
        if gui_config_path.exists():
            resultado = self.verificar_archivo_configuracion(gui_config_path)
            resultados['archivos_verificados'].append(resultado)
        
        # Verificar plantillas
        templates_dir = self.consulta_dir / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.json"):
                resultado = self.verificar_archivo_configuracion(template_file)
                resultados['archivos_verificados'].append(resultado)
        
        # Agregar correcciones y problemas encontrados
        resultados['correcciones_aplicadas'] = self.correcciones_aplicadas
        resultados['problemas_encontrados'] = self.problemas_encontrados
        
        # Calcular resumen
        total_archivos = len(resultados['archivos_verificados'])
        archivos_corregidos = sum(1 for r in resultados['archivos_verificados'] 
                                if r.get('resolucion_corregida', False))
        
        resultados['resumen'] = {
            'total_archivos': total_archivos,
            'archivos_corregidos': archivos_corregidos,
            'porcentaje_corregido': (archivos_corregidos / total_archivos * 100) if total_archivos > 0 else 0,
            'correcciones_aplicadas': len(self.correcciones_aplicadas),
            'problemas_encontrados': len(self.problemas_encontrados)
        }
        
        return resultados
    
    def mostrar_reporte_verificacion(self, resultados: Dict[str, Any]):
        """
        Muestra un reporte detallado de la verificación.
        
        Args:
            resultados: Resultados de la verificación
        """
        print("\n📊 REPORTE DE VERIFICACIÓN DE PROPORCIONES")
        print("=" * 60)
        
        # Resumen general
        resumen = resultados['resumen']
        print(f"\n📈 RESUMEN GENERAL:")
        print(f"   📁 Archivos verificados: {resumen['total_archivos']}")
        print(f"   ✅ Archivos corregidos: {resumen['archivos_corregidos']}")
        print(f"   📊 Porcentaje corregido: {resumen['porcentaje_corregido']:.1f}%")
        print(f"   🔧 Correcciones aplicadas: {resumen['correcciones_aplicadas']}")
        print(f"   ⚠️ Problemas encontrados: {resumen['problemas_encontrados']}")
        
        # Detalles por archivo
        print(f"\n📋 DETALLES POR ARCHIVO:")
        for archivo in resultados['archivos_verificados']:
            print(f"\n   📄 {archivo['archivo']}:")
            print(f"      🔧 Resolución corregida: {'✅' if archivo.get('resolucion_corregida') else '❌'}")
            print(f"      📝 Prompts anti-estiramiento: {'✅' if archivo.get('prompts_anti_estiramiento') else '❌'}")
            print(f"      🏛️ Estándares SAIME: {'✅' if archivo.get('estandares_saime') else '❌'}")
            if 'error' in archivo:
                print(f"      ❌ Error: {archivo['error']}")
        
        # Correcciones aplicadas
        if resultados['correcciones_aplicadas']:
            print(f"\n✅ CORRECCIONES APLICADAS:")
            for correccion in resultados['correcciones_aplicadas']:
                print(f"   {correccion}")
        
        # Problemas encontrados
        if resultados['problemas_encontrados']:
            print(f"\n⚠️ PROBLEMAS ENCONTRADOS:")
            for problema in resultados['problemas_encontrados']:
                print(f"   {problema}")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        if resumen['porcentaje_corregido'] >= 80:
            print("   🎉 ¡Excelente! La mayoría de configuraciones están corregidas.")
            print("   🚀 Puedes proceder con la generación de imágenes.")
        elif resumen['porcentaje_corregido'] >= 50:
            print("   ⚠️ Progreso bueno, pero algunas configuraciones necesitan corrección.")
            print("   🔧 Revisa los problemas encontrados y aplica las correcciones faltantes.")
        else:
            print("   ❌ Muchas configuraciones necesitan corrección.")
            print("   🛠️ Aplica las correcciones sugeridas antes de generar imágenes.")
        
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print("   1. Revisa los problemas encontrados")
        print("   2. Aplica las correcciones faltantes")
        print("   3. Ejecuta este script nuevamente para verificar")
        print("   4. Genera imágenes de prueba para validar las correcciones")

def main():
    """Función principal del script de verificación."""
    print("🔍 Verificador de Correcciones de Proporciones")
    print("=" * 50)
    
    try:
        # Inicializar verificador
        verificador = VerificadorProporciones()
        
        # Verificar todas las configuraciones
        resultados = verificador.verificar_todas_configuraciones()
        
        # Mostrar reporte
        verificador.mostrar_reporte_verificacion(resultados)
        
        # Guardar reporte
        reporte_path = "reporte_verificacion_proporciones.json"
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte detallado guardado en: {reporte_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
