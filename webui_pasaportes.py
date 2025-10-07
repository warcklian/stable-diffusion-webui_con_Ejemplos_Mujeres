#!/usr/bin/env python3
"""
Integración con Stable Diffusion WebUI para Generación de Pasaportes
====================================================================

Este script se integra con la API de Stable Diffusion WebUI para generar
imágenes de pasaportes venezolanos usando las configuraciones de la carpeta Consulta.

Características:
- Integración directa con la API de WebUI
- Generación en lotes automatizada
- Procesamiento de configuraciones JSON
- Guardado automático con nombres descriptivos
- Monitoreo de progreso

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import json
import os
import time
import requests
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
from PIL import Image
import io

class WebUIPasaportes:
    """Cliente para generar imágenes de pasaportes usando Stable Diffusion WebUI."""
    
    def __init__(self, webui_url: str = "http://localhost:7860"):
        """
        Inicializa el cliente de WebUI.
        
        Args:
            webui_url: URL del servidor de Stable Diffusion WebUI
        """
        self.webui_url = webui_url.rstrip('/')
        self.api_url = f"{self.webui_url}/sdapi/v1"
        self.session = requests.Session()
        
    def verificar_conexion(self) -> bool:
        """
        Verifica si WebUI está disponible.
        
        Returns:
            True si WebUI está disponible, False en caso contrario
        """
        try:
            response = self.session.get(f"{self.webui_url}/", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def obtener_modelos_disponibles(self) -> List[str]:
        """
        Obtiene la lista de modelos disponibles en WebUI.
        
        Returns:
            Lista de nombres de modelos
        """
        try:
            response = self.session.get(f"{self.api_url}/sd-models")
            if response.status_code == 200:
                modelos = response.json()
                return [modelo['title'] for modelo in modelos]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def cambiar_modelo(self, nombre_modelo: str) -> bool:
        """
        Cambia el modelo activo en WebUI.
        
        Args:
            nombre_modelo: Nombre del modelo a cargar
            
        Returns:
            True si el cambio fue exitoso, False en caso contrario
        """
        try:
            payload = {"sd_model_checkpoint": nombre_modelo}
            response = self.session.post(f"{self.api_url}/options", json=payload)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def generar_imagen(self, configuracion: Dict[str, Any]) -> Optional[bytes]:
        """
        Genera una imagen usando la configuración proporcionada.
        
        Args:
            configuracion: Configuración de generación
            
        Returns:
            Datos de la imagen en bytes, o None si falló
        """
        try:
            # Preparar payload para la API
            payload = {
                "prompt": configuracion['prompt_positivo'],
                "negative_prompt": configuracion['prompt_negativo'],
                "width": configuracion['configuracion_tecnica']['width'],
                "height": configuracion['configuracion_tecnica']['height'],
                "steps": configuracion['configuracion_tecnica']['steps'],
                "cfg_scale": configuracion['configuracion_tecnica']['cfg_scale'],
                "sampler_name": configuracion['configuracion_tecnica']['sampler'],
                "batch_size": 1,
                "n_iter": 1,
                "save_images": False,
                "send_images": True
            }
            
            # Enviar solicitud a la API
            response = self.session.post(f"{self.api_url}/txt2img", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if 'images' in result and result['images']:
                    # Decodificar imagen base64
                    image_data = base64.b64decode(result['images'][0])
                    return image_data
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la solicitud: {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None
    
    def guardar_imagen(self, image_data: bytes, configuracion: Dict[str, Any], 
                      directorio_salida: str = "outputs/pasaportes") -> str:
        """
        Guarda la imagen generada con un nombre descriptivo.
        
        Args:
            image_data: Datos de la imagen en bytes
            configuracion: Configuración usada para generar la imagen
            directorio_salida: Directorio donde guardar la imagen
            
        Returns:
            Ruta del archivo guardado
        """
        # Crear directorio si no existe
        output_dir = Path(directorio_salida)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre de archivo descriptivo
        nacionalidad = configuracion['nacionalidad']
        genero = configuracion['genero']
        edad = f"{configuracion['edad_min']}-{configuracion['edad_max']}"
        id_imagen = configuracion['id']
        
        nombre_archivo = f"pasaporte_{nacionalidad}_{genero}_{edad}_{id_imagen}.png"
        ruta_archivo = output_dir / nombre_archivo
        
        # Guardar imagen
        with open(ruta_archivo, 'wb') as f:
            f.write(image_data)
        
        return str(ruta_archivo)
    
    def procesar_lote(self, archivo_configuraciones: str, 
                     directorio_salida: str = "outputs/pasaportes",
                     modelo_preferido: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesa un lote completo de configuraciones.
        
        Args:
            archivo_configuraciones: Ruta al archivo JSON con configuraciones
            directorio_salida: Directorio donde guardar las imágenes
            modelo_preferido: Modelo específico a usar (opcional)
            
        Returns:
            Diccionario con estadísticas del procesamiento
        """
        # Cargar configuraciones
        with open(archivo_configuraciones, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        configuraciones = datos['configuraciones']
        metadata = datos['metadata']
        
        print(f"🚀 Iniciando procesamiento de lote...")
        print(f"📊 Total de imágenes: {len(configuraciones)}")
        print(f"🌍 Nacionalidades: {', '.join(metadata['nacionalidades'])}")
        
        # Verificar conexión
        if not self.verificar_conexion():
            raise ConnectionError("No se puede conectar a Stable Diffusion WebUI")
        
        # Cambiar modelo si se especifica
        if modelo_preferido:
            print(f"🔄 Cambiando a modelo: {modelo_preferido}")
            if not self.cambiar_modelo(modelo_preferido):
                print(f"⚠️  No se pudo cambiar al modelo {modelo_preferido}, continuando con el actual")
        
        # Estadísticas
        estadisticas = {
            'total': len(configuraciones),
            'exitosas': 0,
            'fallidas': 0,
            'archivos_generados': [],
            'errores': []
        }
        
        # Procesar cada configuración
        for i, configuracion in enumerate(configuraciones, 1):
            print(f"\n📸 Procesando imagen {i}/{len(configuraciones)}: {configuracion['id']}")
            print(f"   🌍 Nacionalidad: {configuracion['nacionalidad']}")
            print(f"   👤 Género: {configuracion['genero']}")
            
            try:
                # Generar imagen
                image_data = self.generar_imagen(configuracion)
                
                if image_data:
                    # Guardar imagen
                    ruta_archivo = self.guardar_imagen(image_data, configuracion, directorio_salida)
                    estadisticas['archivos_generados'].append(ruta_archivo)
                    estadisticas['exitosas'] += 1
                    print(f"   ✅ Imagen guardada: {ruta_archivo}")
                else:
                    estadisticas['fallidas'] += 1
                    error_msg = f"Error al generar imagen {configuracion['id']}"
                    estadisticas['errores'].append(error_msg)
                    print(f"   ❌ {error_msg}")
                
                # Pausa pequeña entre generaciones
                time.sleep(1)
                
            except Exception as e:
                estadisticas['fallidas'] += 1
                error_msg = f"Error inesperado en {configuracion['id']}: {e}"
                estadisticas['errores'].append(error_msg)
                print(f"   ❌ {error_msg}")
        
        return estadisticas
    
    def mostrar_estadisticas_finales(self, estadisticas: Dict[str, Any]):
        """Muestra las estadísticas finales del procesamiento."""
        print(f"\n📊 ESTADÍSTICAS FINALES")
        print("=" * 40)
        print(f"✅ Imágenes exitosas: {estadisticas['exitosas']}")
        print(f"❌ Imágenes fallidas: {estadisticas['fallidas']}")
        print(f"📈 Tasa de éxito: {(estadisticas['exitosas']/estadisticas['total']*100):.1f}%")
        
        if estadisticas['errores']:
            print(f"\n❌ Errores encontrados:")
            for error in estadisticas['errores']:
                print(f"   - {error}")
        
        if estadisticas['archivos_generados']:
            print(f"\n📁 Archivos generados:")
            for archivo in estadisticas['archivos_generados']:
                print(f"   - {archivo}")

def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Generador de Pasaportes con Stable Diffusion WebUI')
    parser.add_argument('--config', required=True,
                       help='Archivo JSON con configuraciones de imágenes')
    parser.add_argument('--output', default='outputs/pasaportes',
                       help='Directorio de salida (por defecto: outputs/pasaportes)')
    parser.add_argument('--webui-url', default='http://localhost:7860',
                       help='URL de Stable Diffusion WebUI (por defecto: http://localhost:7860)')
    parser.add_argument('--modelo', 
                       help='Modelo específico a usar (opcional)')
    parser.add_argument('--listar-modelos', action='store_true',
                       help='Listar modelos disponibles en WebUI')
    
    args = parser.parse_args()
    
    try:
        # Inicializar cliente
        webui = WebUIPasaportes(args.webui_url)
        
        if args.listar_modelos:
            print("🔄 Obteniendo modelos disponibles...")
            modelos = webui.obtener_modelos_disponibles()
            if modelos:
                print(f"\n📋 Modelos disponibles ({len(modelos)}):")
                for modelo in modelos:
                    print(f"   - {modelo}")
            else:
                print("❌ No se pudieron obtener los modelos")
            return
        
        # Verificar conexión
        print(f"🔍 Verificando conexión con WebUI en {args.webui_url}...")
        if not webui.verificar_conexion():
            print(f"❌ Error: No se puede conectar a Stable Diffusion WebUI en {args.webui_url}")
            print("💡 Asegúrate de que WebUI esté ejecutándose y accesible")
            return
        
        print("✅ Conexión establecida con WebUI")
        
        # Verificar archivo de configuraciones
        if not os.path.exists(args.config):
            print(f"❌ Error: No se encontró el archivo {args.config}")
            return
        
        # Procesar lote
        estadisticas = webui.procesar_lote(args.config, args.output, args.modelo)
        
        # Mostrar estadísticas finales
        webui.mostrar_estadisticas_finales(estadisticas)
        
        print(f"\n🎉 ¡Procesamiento completado!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
