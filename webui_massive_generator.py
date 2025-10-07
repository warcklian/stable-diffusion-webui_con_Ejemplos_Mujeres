"""
Generador Masivo Integrado para WebUI
Sistema completo de generación masiva con diversidad étnica y prompts JSON únicos
Integrado desde SD_Automatizador para uso en navegador
"""

import base64
import time
import gc
import threading
import queue
import random
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class WebUIMassiveGenerator:
    """Generador masivo integrado para WebUI con todas las funcionalidades avanzadas"""
    
    def __init__(self, api_client=None, output_dir="outputs/pasaportes_masivos"):
        """
        Inicializa el generador masivo integrado
        
        Args:
            api_client: Cliente API de WebUI
            output_dir: Directorio de salida
        """
        # Importar y configurar el adaptador de API
        try:
            from webui_api_adapter import WebUIAPIAdapter
            self.api = WebUIAPIAdapter(api_client)
        except ImportError:
            self.api = api_client
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración de optimización
        self.batch_size = 4  # Tamaño óptimo de lote
        self.max_workers = 2  # Número de workers paralelos
        self.memory_threshold = 0.8  # Umbral de memoria (80%)
        
        # Estadísticas
        self.stats = {
            'total_generated': 0,
            'total_failed': 0,
            'total_time': 0,
            'memory_cleanups': 0
        }
        
        # Datos de diversidad étnica
        self.diversity_data = self._load_diversity_data()
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    def _load_diversity_data(self) -> Dict[str, Any]:
        """Carga datos de diversidad étnica"""
        diversity_data = {
            "age_ranges": [
                "18-25 years old", "26-35 years old", "36-45 years old", 
                "46-55 years old", "56-65 years old", "66-75 years old"
            ],
            "facial_structures": [
                "oval face", "round face", "square face", "heart-shaped face",
                "diamond face", "oblong face", "triangular face", "pear-shaped face"
            ],
            "skin_tones": [
                "light skin tone", "medium-light skin tone", "medium skin tone",
                "medium-dark skin tone", "dark skin tone", "very dark skin tone",
                "olive skin tone", "tan skin tone", "fair skin tone", "bronze skin tone"
            ],
            "hair_colors": [
                "black hair", "dark brown hair", "medium brown hair", "light brown hair",
                "blonde hair", "red hair", "auburn hair", "gray hair", "white hair",
                "salt and pepper hair", "strawberry blonde hair", "chestnut hair"
            ],
            "hair_styles": [
                "short hair", "medium length hair", "long hair", "curly hair",
                "wavy hair", "straight hair", "afro hair", "braided hair",
                "ponytail", "bun", "bob cut", "pixie cut", "buzz cut", "bald"
            ],
            "eye_colors": [
                "brown eyes", "dark brown eyes", "light brown eyes", "hazel eyes",
                "green eyes", "blue eyes", "gray eyes", "amber eyes", "black eyes"
            ],
            "facial_features": [
                "high cheekbones", "prominent cheekbones", "soft cheekbones",
                "strong jawline", "defined jawline", "soft jawline", "round jawline",
                "pointed chin", "round chin", "square chin", "cleft chin",
                "broad nose", "narrow nose", "straight nose", "aquiline nose",
                "button nose", "wide nose", "thin lips", "full lips", "medium lips"
            ],
            "ethnic_characteristics": [
                "mixed ethnicity features", "indigenous features", "european features",
                "african features", "asian features", "middle eastern features",
                "latin american features", "caribbean features", "mediterranean features"
            ],
            "natural_imperfections": [
                "natural skin texture", "subtle skin blemishes", "natural skin pores",
                "freckles", "moles", "natural skin variations", "age spots",
                "fine lines", "natural wrinkles", "realistic skin texture"
            ]
        }
        return diversity_data
    
    def generate_massive_diversity(self, 
                                 nationality: str,
                                 gender: str,
                                 age_min: int = 18,
                                 age_max: int = 80,
                                 quantity: int = 10,
                                 progress_callback: Callable = None) -> Dict[str, Any]:
        """
        Genera múltiples imágenes con diversidad étnica real
        
        Args:
            nationality: Nacionalidad (venezuelan, cuban, haitian, etc.)
            gender: Género (mujer, hombre)
            age_min: Edad mínima
            age_max: Edad máxima
            quantity: Cantidad de imágenes a generar
            progress_callback: Callback de progreso
            
        Returns:
            Diccionario con resultados y estadísticas
        """
        start_time = time.time()
        self.logger.info(f"🚀 Iniciando generación masiva de {quantity} imágenes para {nationality}")
        
        # Crear directorio de salida con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_dir = self.output_dir / f"batch_{nationality}_{gender}_{timestamp}"
        batch_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar perfiles únicos de diversidad
        diversity_profiles = self._generate_diversity_profiles(
            nationality, gender, age_min, age_max, quantity
        )
        
        # Generar imágenes por lotes
        results = self._process_diversity_batch(
            diversity_profiles, 
            batch_dir, 
            progress_callback
        )
        
        # Calcular estadísticas finales
        total_time = time.time() - start_time
        self.stats['total_time'] = total_time
        
        # Limpieza final de memoria
        self._perform_final_cleanup()
        
        self.logger.info(f"✅ Generación masiva completada en {total_time:.2f}s")
        self.logger.info(f"📊 Estadísticas: {self.stats}")
        
        return {
            'success': True,
            'generated_count': results['generated'],
            'failed_count': results['failed'],
            'total_time': total_time,
            'stats': self.stats.copy(),
            'output_directory': str(batch_dir)
        }
    
    def _generate_diversity_profiles(self, 
                                   nationality: str,
                                   gender: str,
                                   age_min: int,
                                   age_max: int,
                                   quantity: int) -> List[Dict[str, Any]]:
        """
        Genera perfiles únicos de diversidad para cada imagen
        
        Args:
            nationality: Nacionalidad
            gender: Género
            age_min: Edad mínima
            age_max: Edad máxima
            quantity: Cantidad de perfiles
            
        Returns:
            Lista de perfiles de diversidad únicos
        """
        profiles = []
        used_combinations = set()
        
        for i in range(quantity):
            # Generar combinación única
            attempts = 0
            while attempts < 100:  # Evitar bucle infinito
                age = random.randint(age_min, age_max)
                age_range = self._get_age_range(age)
                skin_tone = random.choice(self.diversity_data["skin_tones"])
                hair_color = random.choice(self.diversity_data["hair_colors"])
                hair_style = random.choice(self.diversity_data["hair_styles"])
                eye_color = random.choice(self.diversity_data["eye_colors"])
                facial_structure = random.choice(self.diversity_data["facial_structures"])
                facial_features = random.choice(self.diversity_data["facial_features"])
                ethnic_characteristics = random.choice(self.diversity_data["ethnic_characteristics"])
                natural_imperfections = random.choice(self.diversity_data["natural_imperfections"])
                
                # Crear combinación única
                combination = f"{age}_{skin_tone}_{hair_color}_{eye_color}_{facial_structure}"
                
                if combination not in used_combinations:
                    used_combinations.add(combination)
                    break
                attempts += 1
            
            # Crear perfil único
            profile = {
                "nationality": nationality,
                "gender": gender,
                "age": age,
                "age_range": age_range,
                "skin_tone": skin_tone,
                "hair_color": hair_color,
                "hair_style": hair_style,
                "eye_color": eye_color,
                "facial_structure": facial_structure,
                "facial_features": facial_features,
                "ethnic_characteristics": ethnic_characteristics,
                "natural_imperfections": natural_imperfections,
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            }
            
            profiles.append(profile)
        
        return profiles
    
    def _get_age_range(self, age: int) -> str:
        """Convierte edad numérica a rango de edad"""
        if age <= 25:
            return "18-25 years old"
        elif age <= 35:
            return "26-35 years old"
        elif age <= 45:
            return "36-45 years old"
        elif age <= 55:
            return "46-55 years old"
        elif age <= 65:
            return "56-65 years old"
        else:
            return "66-75 years old"
    
    def _process_diversity_batch(self, 
                               profiles: List[Dict[str, Any]], 
                               output_dir: Path,
                               progress_callback: Callable = None) -> Dict[str, int]:
        """
        Procesa lotes de perfiles de diversidad
        
        Args:
            profiles: Lista de perfiles de diversidad
            output_dir: Directorio de salida
            progress_callback: Callback de progreso
            
        Returns:
            Diccionario con conteos de éxito y fallos
        """
        generated_count = 0
        failed_count = 0
        total_profiles = len(profiles)
        
        # Dividir en lotes para optimización de memoria
        batch_size = min(self.batch_size, total_profiles)
        batches = [profiles[i:i + batch_size] for i in range(0, total_profiles, batch_size)]
        
        for batch_idx, batch in enumerate(batches):
            self.logger.info(f"🔄 Procesando lote {batch_idx + 1}/{len(batches)} ({len(batch)} perfiles)")
            
            # Verificar memoria antes del lote
            if self._should_cleanup_memory():
                self._perform_memory_cleanup()
            
            # Procesar lote
            batch_results = self._process_single_batch(batch, output_dir)
            
            # Actualizar contadores
            generated_count += batch_results['generated']
            failed_count += batch_results['failed']
            
            # Actualizar estadísticas
            self.stats['total_generated'] = generated_count
            self.stats['total_failed'] = failed_count
            
            # Callback de progreso
            if progress_callback:
                processed = (batch_idx + 1) * len(batch)
                progress_callback(
                    processed, 
                    total_profiles, 
                    f"Lote {batch_idx + 1}/{len(batches)} completado"
                )
            
            # Pausa entre lotes para liberar memoria
            if batch_idx < len(batches) - 1:
                time.sleep(0.5)
        
        return {
            'generated': generated_count,
            'failed': failed_count
        }
    
    def _process_single_batch(self, 
                            batch: List[Dict[str, Any]], 
                            output_dir: Path) -> Dict[str, int]:
        """
        Procesa un solo lote de perfiles
        
        Args:
            batch: Lote de perfiles
            output_dir: Directorio de salida
            
        Returns:
            Diccionario con conteos de éxito y fallos
        """
        generated = 0
        failed = 0
        
        # Usar ThreadPoolExecutor para procesamiento paralelo limitado
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Crear tareas
            future_to_profile = {
                executor.submit(
                    self._generate_single_diversity_image, 
                    profile, 
                    output_dir
                ): profile for profile in batch
            }
            
            # Procesar resultados
            for future in as_completed(future_to_profile):
                profile = future_to_profile[future]
                try:
                    result = future.result()
                    if result:
                        generated += 1
                    else:
                        failed += 1
                except Exception as e:
                    self.logger.error(f"Error procesando perfil: {e}")
                    failed += 1
        
        return {'generated': generated, 'failed': failed}
    
    def _generate_single_diversity_image(self, 
                                       profile: Dict[str, Any], 
                                       output_dir: Path) -> bool:
        """
        Genera una sola imagen con diversidad étnica
        
        Args:
            profile: Perfil de diversidad
            output_dir: Directorio de salida
            
        Returns:
            True si la generación fue exitosa
        """
        try:
            # Generar prompt único basado en el perfil
            prompt, negative_prompt = self._generate_unique_prompt(profile)
            
            # Parámetros homogéneos (misma cámara, misma distancia)
            params = {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'width': 512,  # Resolución homogénea
                'height': 512,  # Como misma cámara
                'steps': 30,
                'cfg_scale': 9.0,  # CFG alto para seguir instrucciones
                'sampler_name': 'DPM++ 2M Karras',
                'seed': -1,
                'batch_size': 1,
                'n_iter': 1,
                'save_images': False,
                'send_images': True
            }
            
            # Generar imagen usando la API de WebUI
            if self.api:
                result = self.api.txt2img(**params)
            else:
                # Fallback: simular resultado para testing
                result = {'images': ['fake_image_data']}
            
            if result and result.get('images'):
                # Generar nombre de archivo único
                filename = self._generate_unique_filename(profile)
                filepath = output_dir / filename
                
                # Decodificar y guardar imagen
                if self.api:
                    image_data = base64.b64decode(result['images'][0])
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                else:
                    # Fallback: crear archivo vacío para testing
                    filepath.touch()
                
                # Guardar configuración JSON única
                self._save_unique_json_config(profile, params, result, filepath)
                
                return True
            else:
                self.logger.warning(f"⚠️ No se generó imagen para perfil: {profile['nationality']}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error generando imagen: {e}")
            return False
    
    def _generate_unique_prompt(self, profile: Dict[str, Any]) -> tuple:
        """
        Genera prompt único basado en el perfil de diversidad
        
        Args:
            profile: Perfil de diversidad
            
        Returns:
            Tupla (prompt, negative_prompt)
        """
        nationality = profile['nationality']
        gender = profile['gender']
        age_range = profile['age_range']  # Usar age_range para generación masiva
        region = profile['region']
        skin_tone = profile['skin_tone']
        skin_texture = profile['skin_texture']
        hair_color = profile['hair_color']
        hair_style = profile['hair_style']
        eye_color = profile['eye_color']
        eye_shape = profile['eye_shape']
        facial_structure = profile['facial_structure']
        nose_shape = profile['nose_shape']
        lip_shape = profile['lip_shape']
        eyebrows = profile['eyebrows']
        jawline = profile['jawline']
        cheekbones = profile['cheekbones']
        
        # Prompt positivo simplificado (basado en muestras exitosas)
        prompt = f"{nationality} {gender}, {age_range}, from {region} region, {skin_tone} skin, {skin_texture} skin texture, {hair_color} hair, {hair_style} hair, {eye_color} eyes, {eye_shape} eyes, {facial_structure} face, {nose_shape} nose, {lip_shape} lips, {eyebrows} eyebrows, {jawline} jawline, {cheekbones} cheekbones, passport photo, professional headshot, looking directly at camera, facing camera directly, front view, head centered, face centered, neutral expression, raw photography, documentary style, unretouched, natural skin texture, pores visible, natural skin imperfections, authentic appearance, candid photography, natural lighting, centered composition, symmetrical positioning, pure white background, solid white background, clean white background, uniform white background, plain white background, studio white background"
        
        # Prompt negativo simplificado (basado en muestras exitosas)
        negative_prompt = "3/4 view, side profile, profile view, looking away, looking left, looking right, looking up, looking down, tilted head, turned head, angled face, off-center, asymmetrical, smiling, laughing, frowning, multiple people, blurry, low quality, distorted, deformed, ugly, bad anatomy, bad proportions, extra limbs, missing limbs, extra fingers, missing fingers, extra arms, missing arms, extra legs, missing legs, extra heads, missing heads, extra eyes, missing eyes, extra nose, missing nose, extra mouth, missing mouth, text, watermark, signature, gradient background, gradient, faded background, textured background, patterned background, noisy background, complex background, busy background, shadows on background, lighting effects on background, colored background, colored backdrop, tinted background, off-white background, cream background, beige background, gray background, light gray background, dark background, black background, blue background, green background, red background, yellow background, purple background, orange background, brown background, wood background, wall background, fabric background, paper background, canvas background, brick background, stone background, metal background, glass background, mirror background, reflection, shadows, lighting, spotlight, soft lighting, dramatic lighting, rim lighting, back lighting, side lighting, top lighting, bottom lighting, ambient lighting, natural lighting, artificial lighting, studio lighting, flash lighting, harsh lighting, dim lighting, bright lighting, overexposed, underexposed, high contrast, low contrast, saturated colors, desaturated colors, vibrant colors, muted colors, warm colors, cool colors, neutral colors, pastel colors, bold colors, subtle colors, airbrushed, photoshopped, retouched, smooth skin, perfect skin, flawless skin, glowing skin, shiny skin, oily skin, greasy skin, plastic skin, artificial skin, digital art, 3d render, cg, computer generated, synthetic, fake, artificial, overexposed, bright lighting, studio lighting, flash photography, harsh lighting, dramatic lighting, cinematic lighting, professional lighting, perfect lighting, ideal lighting, enhanced, improved, perfected, beautified, glamorized, stylized, artistic, aesthetic, beautiful, attractive, handsome, pretty, gorgeous, stunning, perfect, ideal, flawless, immaculate, pristine, clean, pure, crystal clear, sharp, crisp, vibrant, saturated, colorful, bright, luminous, radiant, brilliant, sparkling, shining, glowing, glossy, polished, refined, elegant, sophisticated, luxurious, premium, high-end, professional, commercial, advertising, marketing, fashion, beauty, cosmetic, makeup, foundation, concealer, powder, blush, lipstick, mascara, eyeliner, eyeshadow, contouring, highlighting, bronzer, primer, setting spray, finishing powder, model look, supermodel appearance, celebrity look, fashion model, beauty model"
        
        return prompt, negative_prompt
    
    def _generate_unique_filename(self, profile: Dict[str, Any]) -> str:
        """
        Genera nombre de archivo único para la imagen
        
        Args:
            profile: Perfil de diversidad
            
        Returns:
            Nombre de archivo único
        """
        nationality = profile['nationality']
        gender = profile['gender']
        age = profile['age']
        timestamp = profile['timestamp']
        
        return f"massive_{gender}_{age}_{nationality}_{timestamp}.png"
    
    def _get_current_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información del modelo actual en WebUI
        
        Returns:
            Diccionario con información del modelo actual
        """
        try:
            # Intentar obtener información del modelo actual desde WebUI
            import sys
            if 'modules' in sys.modules:
                try:
                    from modules import shared, sd_models
                    
                    # Obtener modelo actual
                    current_model = shared.sd_model
                    if current_model and hasattr(current_model, 'sd_checkpoint_info'):
                        checkpoint_info = current_model.sd_checkpoint_info
                        return {
                            "model_name": checkpoint_info.name_for_extra,
                            "model_title": checkpoint_info.title,
                            "model_filename": checkpoint_info.filename,
                            "model_hash": getattr(current_model, 'sd_model_hash', 'unknown'),
                            "model_type": "Stable Diffusion",
                            "is_sdxl": getattr(current_model, 'is_sdxl', False),
                            "is_sd1": getattr(current_model, 'is_sd1', False),
                            "is_sd2": getattr(current_model, 'is_sd2', False),
                            "is_sd3": getattr(current_model, 'is_sd3', False)
                        }
                    else:
                        # Fallback: obtener desde configuración
                        selected_model = shared.opts.sd_model_checkpoint
                        if selected_model:
                            return {
                                "model_name": selected_model,
                                "model_title": selected_model,
                                "model_filename": "unknown",
                                "model_hash": "unknown",
                                "model_type": "Stable Diffusion",
                                "is_sdxl": False,
                                "is_sd1": True,
                                "is_sd2": False,
                                "is_sd3": False
                            }
                except Exception as e:
                    self.logger.warning(f"⚠️ Error obteniendo modelo actual: {e}")
            
            # Fallback por defecto
            return {
                "model_name": "WebUI_Integrated_Model",
                "model_title": "WebUI Integrated Model",
                "model_filename": "unknown",
                "model_hash": "unknown",
                "model_type": "Stable Diffusion",
                "is_sdxl": False,
                "is_sd1": True,
                "is_sd2": False,
                "is_sd3": False
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo información del modelo: {e}")
            return {
                "model_name": "Unknown_Model",
                "model_title": "Unknown Model",
                "model_filename": "unknown",
                "model_hash": "unknown",
                "model_type": "Stable Diffusion",
                "is_sdxl": False,
                "is_sd1": True,
                "is_sd2": False,
                "is_sd3": False
            }
    
    def _save_unique_json_config(self, 
                               profile: Dict[str, Any], 
                               params: Dict[str, Any], 
                               result: Dict[str, Any], 
                               image_filepath: Path):
        """
        Guarda configuración JSON única para replicar la imagen
        
        Args:
            profile: Perfil de diversidad
            params: Parámetros de generación
            result: Resultado de la API
            image_filepath: Ruta del archivo de imagen
        """
        try:
            # Extraer seed real de la respuesta
            real_seed = -1
            if isinstance(result, dict):
                info_data = result.get("info", {})
                if isinstance(info_data, str):
                    try:
                        info_data = json.loads(info_data)
                    except json.JSONDecodeError:
                        info_data = {}
                real_seed = info_data.get("seed", params.get("seed", -1))
            
            # Obtener información del modelo actual
            model_info = self._get_current_model_info()
            
            # Crear configuración completa
            config_data = {
                "image_info": {
                    "filename": image_filepath.name,
                    "generated_at": datetime.now().isoformat(),
                    "generation_time_seconds": 0  # Se puede calcular si es necesario
                },
                "prompt_data": {
                    "prompt": params.get("prompt", ""),
                    "negative_prompt": params.get("negative_prompt", ""),
                    "width": params.get("width", 512),
                    "height": params.get("height", 512),
                    "steps": params.get("steps", 30),
                    "cfg_scale": params.get("cfg_scale", 9.0),
                    "sampler_name": params.get("sampler_name", "DPM++ 2M Karras"),
                    "batch_size": params.get("batch_size", 1),
                    "n_iter": params.get("n_iter", 1),
                    "seed": real_seed if real_seed != -1 else params.get("seed", -1),
                    "nationality": profile.get("nationality"),
                    "gender": profile.get("gender"),
                    "age": profile.get("age"),
                    "age_range": profile.get("age_range"),
                    "skin_tone": profile.get("skin_tone"),
                    "hair_color": profile.get("hair_color"),
                    "hair_style": profile.get("hair_style"),
                    "eye_color": profile.get("eye_color"),
                    "facial_structure": profile.get("facial_structure"),
                    "facial_features": profile.get("facial_features"),
                    "ethnic_characteristics": profile.get("ethnic_characteristics"),
                    "natural_imperfections": profile.get("natural_imperfections"),
                    "template_used": False,
                    "generation_type": "massive_diversity"
                },
                "ethnic_info": {
                    "ethnic_origin": None,
                    "ethnic_group_name": None,
                    "ethnic_subgroup": None,
                    "ethnic_subgroup_description": None
                },
                "generation_parameters": {
                    "width": params.get("width", 512),
                    "height": params.get("height", 512),
                    "steps": params.get("steps", 30),
                    "cfg_scale": params.get("cfg_scale", 9.0),
                    "sampler_name": params.get("sampler_name", "DPM++ 2M Karras"),
                    "seed": real_seed if real_seed != -1 else params.get("seed", -1),
                    "batch_size": params.get("batch_size", 1),
                    "n_iter": params.get("n_iter", 1)
                },
                "model_info": model_info,
                "replication_instructions": {
                    "description": "Configuración completa para replicar esta imagen exacta",
                    "usage": "Usar estos parámetros en cualquier interfaz de Stable Diffusion para generar la misma imagen",
                    "note": "El prompt y negative_prompt son específicos para esta imagen única con diversidad étnica",
                    "model_verification": f"Modelo utilizado: {model_info['model_name']} ({model_info['model_title']})"
                }
            }
            
            # Guardar archivo JSON
            json_filepath = image_filepath.with_suffix('.json')
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Configuración JSON guardada: {json_filepath.name}")
            self.logger.info(f"📋 Modelo utilizado: {model_info['model_name']} ({model_info['model_title']})")
            
        except Exception as e:
            self.logger.error(f"❌ Error guardando configuración JSON: {e}")
    
    def _should_cleanup_memory(self) -> bool:
        """Determina si se debe realizar limpieza de memoria"""
        # Implementación simple - se puede mejorar con psutil
        return self.stats['memory_cleanups'] < 10  # Límite de limpiezas
    
    def _perform_memory_cleanup(self):
        """Realiza limpieza de memoria"""
        self.logger.info("🧹 Realizando limpieza de memoria...")
        
        # Forzar recolección de basura
        gc.collect()
        
        self.stats['memory_cleanups'] += 1
        self.logger.info("✅ Limpieza de memoria completada")
    
    def _perform_final_cleanup(self):
        """Realiza limpieza final completa de memoria"""
        try:
            self.logger.info("🧹 Iniciando limpieza final de memoria...")
            
            # Limpieza básica de Python
            objects_before = len(gc.get_objects())
            for i in range(3):
                collected = gc.collect()
                if collected == 0:
                    break
                time.sleep(0.1)
            objects_after = len(gc.get_objects())
            objects_cleaned = objects_before - objects_after
            
            self.logger.info(f"✅ Limpieza final completada: {objects_cleaned} objetos limpiados")
            
        except Exception as e:
            self.logger.error(f"❌ Error en limpieza final: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de generación
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'batch_size': self.batch_size,
            'max_workers': self.max_workers,
            'stats': self.stats.copy()
        }
