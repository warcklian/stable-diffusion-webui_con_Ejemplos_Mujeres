#!/usr/bin/env python3
"""
Motor de Diversidad Genética Dinámica
Sistema avanzado para generar características únicas con control granular
"""

import random
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

@dataclass
class GeneticProfile:
    """Perfil genético completo de una persona"""
    # Identificación
    image_id: str
    nationality: str
    region: str
    gender: str
    age: int
    
    # Características faciales
    face_shape: str
    face_width: str
    face_length: str
    jawline: str
    chin: str
    cheekbones: str
    
    # Ojos
    eye_color: str
    eye_shape: str
    eye_size: str
    eye_spacing: str
    eyelid_type: str
    eyelashes: str
    eyebrows: str
    
    # Nariz
    nose_shape: str
    nose_size: str
    nose_width: str
    nose_bridge: str
    
    # Boca
    lip_shape: str
    lip_size: str
    lip_thickness: str
    mouth_width: str
    
    # Piel
    skin_tone: str
    skin_texture: str
    skin_imperfections: List[str]
    freckles: str
    moles: str
    
    # Cabello
    hair_color: str
    hair_texture: str
    hair_length: str
    hair_style: str
    hair_density: str
    
    # Características de edad
    age_characteristics: List[str]
    
    # Nivel de belleza
    beauty_level: str
    attractiveness_factors: List[str]
    
    # Características étnicas específicas
    ethnic_features: List[str]
    
    # Metadatos
    generated_at: str
    generation_type: str
    uniqueness_score: float

class GeneticDiversityEngine:
    """Motor de diversidad genética con control granular"""
    
    def __init__(self, logger: logging.Logger = None):
        """Inicializa el motor de diversidad genética"""
        self.logger = logger or logging.getLogger(__name__)
        self.consulta_dir = Path(__file__).parent / "Consulta"
        self.ethnic_data = self._load_ethnic_data()
        self.beauty_engine = self._initialize_beauty_engine()
        self.age_engine = self._initialize_age_engine()
        
    def _load_ethnic_data(self) -> Dict[str, Any]:
        """Carga datos étnicos desde archivos JSON"""
        ethnic_data = {}
        
        # Cargar datos de países
        countries_dir = self.consulta_dir / "countries"
        if countries_dir.exists():
            for json_file in countries_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        country_name = json_file.stem
                        ethnic_data[country_name] = data
                except Exception as e:
                    self.logger.warning(f"Error cargando {json_file}: {e}")
        
        return ethnic_data
    
    def _initialize_beauty_engine(self) -> Dict[str, Any]:
        """Inicializa el motor de belleza realista"""
        return {
            "beauty_levels": {
                "common": 0.50,           # 50% - Apariencia común
                "average": 0.30,          # 30% - Apariencia promedio  
                "attractive": 0.15,       # 15% - Apariencia atractiva
                "very_attractive": 0.04,  # 4% - Muy atractivo
                "exceptionally_beautiful": 0.01  # 1% - Excepcionalmente bello
            },
            "attractiveness_factors": {
                "symmetrical_features": 0.30,
                "clear_skin": 0.25,
                "expressive_eyes": 0.20,
                "well_proportioned": 0.15,
                "natural_beauty": 0.10
            },
            "imperfections": {
                "natural_skin_texture": 0.80,
                "slight_asymmetry": 0.60,
                "minor_blemishes": 0.40,
                "freckles": 0.25,
                "moles": 0.20,
                "scars": 0.10,
                "acne_marks": 0.15,
                "age_spots": 0.05,
                "dark_circles": 0.30,
                "visible_pores": 0.70
            }
        }
    
    def _initialize_age_engine(self) -> Dict[str, Any]:
        """Inicializa el motor de características por edad"""
        return {
            "18-25": {
                "smooth_skin": 0.90,
                "youthful_appearance": 0.95,
                "fresh_complexion": 0.85,
                "minor_acne": 0.20,
                "oily_skin": 0.30,
                "full_cheeks": 0.80,
                "tight_skin": 0.90
            },
            "26-35": {
                "smooth_skin": 0.70,
                "youthful_appearance": 0.80,
                "fresh_complexion": 0.60,
                "fine_lines": 0.30,
                "crow_feet": 0.20,
                "mature_features": 0.40,
                "full_cheeks": 0.60,
                "tight_skin": 0.70
            },
            "36-45": {
                "smooth_skin": 0.40,
                "youthful_appearance": 0.50,
                "fresh_complexion": 0.30,
                "fine_lines": 0.60,
                "crow_feet": 0.50,
                "forehead_lines": 0.30,
                "mature_features": 0.80,
                "nasolabial_folds": 0.20,
                "full_cheeks": 0.40,
                "tight_skin": 0.40
            },
            "46-55": {
                "smooth_skin": 0.20,
                "youthful_appearance": 0.30,
                "fresh_complexion": 0.15,
                "fine_lines": 0.80,
                "crow_feet": 0.70,
                "forehead_lines": 0.50,
                "mature_features": 0.95,
                "nasolabial_folds": 0.50,
                "marionette_lines": 0.30,
                "neck_lines": 0.40,
                "full_cheeks": 0.20,
                "tight_skin": 0.20
            },
            "56-65": {
                "smooth_skin": 0.10,
                "youthful_appearance": 0.15,
                "fresh_complexion": 0.05,
                "fine_lines": 0.90,
                "crow_feet": 0.80,
                "forehead_lines": 0.70,
                "mature_features": 0.98,
                "nasolabial_folds": 0.70,
                "marionette_lines": 0.50,
                "neck_lines": 0.60,
                "jowls": 0.30,
                "full_cheeks": 0.10,
                "tight_skin": 0.10
            }
        }
    
    def _select_by_probability(self, options: Dict[str, float]) -> str:
        """Selecciona una opción basada en probabilidades"""
        rand = random.random()
        acumulado = 0.0
        
        for option, probability in options.items():
            acumulado += probability
            if rand <= acumulado:
                return option
        
        return list(options.keys())[0]
    
    def _get_age_range(self, age: int) -> str:
        """Obtiene el rango de edad para características"""
        if 18 <= age <= 25:
            return "18-25"
        elif 26 <= age <= 35:
            return "26-35"
        elif 36 <= age <= 45:
            return "36-45"
        elif 46 <= age <= 55:
            return "46-55"
        elif 56 <= age <= 65:
            return "56-65"
        else:
            return "18-25"
    
    def generate_genetic_profile(self, 
                               nationality: str, 
                               region: str, 
                               gender: str, 
                               age: int,
                               beauty_control: str = "normal",
                               skin_control: str = "auto",
                               hair_control: str = "auto",
                               eye_control: str = "auto") -> GeneticProfile:
        """
        Genera un perfil genético completo con control granular
        
        Args:
            nationality: Nacionalidad
            region: Región específica
            gender: Género
            age: Edad específica
            beauty_control: Control de belleza (normal, attractive, realistic, random)
            skin_control: Control de piel (auto, light, medium, dark, mixed)
            hair_control: Control de cabello (auto, dark, light, mixed)
            eye_control: Control de ojos (auto, dark, light, mixed)
        """
        
        # Obtener datos étnicos de la nacionalidad y región
        ethnic_data = self.ethnic_data.get(nationality, {})
        regions = ethnic_data.get("regions", {})
        region_data = regions.get(region, regions.get("caracas", {}))  # Fallback a caracas
        
        # Generar características faciales
        face_shape = self._generate_face_shape(region_data, gender)
        face_width = self._generate_face_width(region_data)
        face_length = self._generate_face_length(region_data)
        jawline = self._generate_jawline(region_data, gender, age)
        chin = self._generate_chin(region_data, gender)
        cheekbones = self._generate_cheekbones(region_data, gender, age)
        
        # Generar características de ojos
        eye_color = self._generate_eye_color(region_data, eye_control)
        eye_shape = self._generate_eye_shape(region_data)
        eye_size = self._generate_eye_size(region_data)
        eye_spacing = self._generate_eye_spacing(region_data)
        eyelid_type = self._generate_eyelid_type(region_data)
        eyelashes = self._generate_eyelashes(region_data, gender)
        eyebrows = self._generate_eyebrows(region_data, gender)
        
        # Generar características de nariz
        nose_shape = self._generate_nose_shape(region_data)
        nose_size = self._generate_nose_size(region_data)
        nose_width = self._generate_nose_width(region_data)
        nose_bridge = self._generate_nose_bridge(region_data)
        
        # Generar características de boca
        lip_shape = self._generate_lip_shape(region_data, gender)
        lip_size = self._generate_lip_size(region_data, gender)
        lip_thickness = self._generate_lip_thickness(region_data, gender)
        mouth_width = self._generate_mouth_width(region_data)
        
        # Generar características de piel
        skin_tone = self._generate_skin_tone(region_data, skin_control)
        skin_texture = self._generate_skin_texture(region_data, age)
        skin_imperfections = self._generate_skin_imperfections(age, beauty_control)
        freckles = self._generate_freckles(region_data, skin_tone)
        moles = self._generate_moles(region_data, skin_tone)
        
        # Generar características de cabello
        hair_color = self._generate_hair_color(region_data, hair_control)
        hair_texture = self._generate_hair_texture(region_data)
        hair_length = self._generate_hair_length(region_data, gender)
        hair_style = self._generate_hair_style(region_data, gender, hair_length)
        hair_density = self._generate_hair_density(region_data, gender, age)
        
        # Generar características de edad
        age_characteristics = self._generate_age_characteristics(age)
        
        # Generar nivel de belleza
        beauty_level = self._generate_beauty_level(beauty_control)
        attractiveness_factors = self._generate_attractiveness_factors(beauty_level)
        
        # Generar características étnicas específicas
        ethnic_features = self._generate_ethnic_features(region_data, nationality)
        
        # Calcular score de unicidad
        uniqueness_score = self._calculate_uniqueness_score()
        
        return GeneticProfile(
            image_id=f"{nationality}_{region}_{gender}_{age}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}",
            nationality=nationality,
            region=region,
            gender=gender,
            age=age,
            face_shape=face_shape,
            face_width=face_width,
            face_length=face_length,
            jawline=jawline,
            chin=chin,
            cheekbones=cheekbones,
            eye_color=eye_color,
            eye_shape=eye_shape,
            eye_size=eye_size,
            eye_spacing=eye_spacing,
            eyelid_type=eyelid_type,
            eyelashes=eyelashes,
            eyebrows=eyebrows,
            nose_shape=nose_shape,
            nose_size=nose_size,
            nose_width=nose_width,
            nose_bridge=nose_bridge,
            lip_shape=lip_shape,
            lip_size=lip_size,
            lip_thickness=lip_thickness,
            mouth_width=mouth_width,
            skin_tone=skin_tone,
            skin_texture=skin_texture,
            skin_imperfections=skin_imperfections,
            freckles=freckles,
            moles=moles,
            hair_color=hair_color,
            hair_texture=hair_texture,
            hair_length=hair_length,
            hair_style=hair_style,
            hair_density=hair_density,
            age_characteristics=age_characteristics,
            beauty_level=beauty_level,
            attractiveness_factors=attractiveness_factors,
            ethnic_features=ethnic_features,
            generated_at=datetime.now().isoformat(),
            generation_type="genetic_diversity_engine",
            uniqueness_score=uniqueness_score
        )
    
    def _generate_face_shape(self, region_data: Dict, gender: str) -> str:
        """Genera forma de cara basada en datos étnicos"""
        face_shapes = region_data.get("facial_structures", {
            "oval": 0.4,
            "round": 0.25,
            "square": 0.15,
            "heart": 0.1,
            "diamond": 0.05,
            "oblong": 0.05
        })
        return self._select_by_probability(face_shapes)
    
    def _generate_face_width(self, region_data: Dict) -> str:
        """Genera ancho de cara"""
        widths = {
            "narrow": 0.2,
            "medium": 0.6,
            "wide": 0.2
        }
        return self._select_by_probability(widths)
    
    def _generate_face_length(self, region_data: Dict) -> str:
        """Genera largo de cara"""
        lengths = {
            "short": 0.2,
            "medium": 0.6,
            "long": 0.2
        }
        return self._select_by_probability(lengths)
    
    def _generate_jawline(self, region_data: Dict, gender: str, age: int) -> str:
        """Genera línea de mandíbula"""
        if gender == "hombre":
            jawlines = {
                "strong": 0.4,
                "defined": 0.3,
                "soft": 0.2,
                "weak": 0.1
            }
        else:
            jawlines = {
                "soft": 0.4,
                "defined": 0.3,
                "strong": 0.2,
                "weak": 0.1
            }
        
        # Ajustar por edad
        if age > 40:
            jawlines["soft"] += 0.2
            jawlines["strong"] -= 0.1
            jawlines["defined"] -= 0.1
        
        return self._select_by_probability(jawlines)
    
    def _generate_chin(self, region_data: Dict, gender: str) -> str:
        """Genera características de barbilla"""
        if gender == "hombre":
            chins = {
                "strong": 0.3,
                "defined": 0.4,
                "soft": 0.2,
                "weak": 0.1
            }
        else:
            chins = {
                "soft": 0.4,
                "defined": 0.3,
                "strong": 0.2,
                "weak": 0.1
            }
        return self._select_by_probability(chins)
    
    def _generate_cheekbones(self, region_data: Dict, gender: str, age: int) -> str:
        """Genera pómulos"""
        if gender == "hombre":
            cheekbones = {
                "prominent": 0.3,
                "defined": 0.4,
                "soft": 0.2,
                "flat": 0.1
            }
        else:
            cheekbones = {
                "soft": 0.4,
                "defined": 0.3,
                "prominent": 0.2,
                "flat": 0.1
            }
        
        # Ajustar por edad
        if age > 35:
            cheekbones["soft"] += 0.2
            cheekbones["prominent"] -= 0.1
            cheekbones["defined"] -= 0.1
        
        return self._select_by_probability(cheekbones)
    
    def _generate_eye_color(self, region_data: Dict, control: str) -> str:
        """Genera color de ojos con control"""
        if control == "auto":
            eye_colors = region_data.get("eye_colors", {
                "brown": 0.6,
                "dark_brown": 0.2,
                "light_brown": 0.1,
                "green": 0.05,
                "blue": 0.03,
                "gray": 0.01,
                "hazel": 0.01
            })
        elif control == "dark":
            eye_colors = {
                "brown": 0.7,
                "dark_brown": 0.3
            }
        elif control == "light":
            eye_colors = {
                "blue": 0.4,
                "green": 0.3,
                "hazel": 0.2,
                "light_brown": 0.1
            }
        else:  # mixed
            eye_colors = {
                "brown": 0.4,
                "dark_brown": 0.2,
                "light_brown": 0.15,
                "green": 0.1,
                "blue": 0.1,
                "hazel": 0.05
            }
        
        return self._select_by_probability(eye_colors)
    
    def _generate_eye_shape(self, region_data: Dict) -> str:
        """Genera forma de ojos"""
        eye_shapes = region_data.get("eye_shapes", {
            "almond": 0.4,
            "round": 0.3,
            "large": 0.15,
            "small": 0.1,
            "deep_set": 0.05
        })
        return self._select_by_probability(eye_shapes)
    
    def _generate_eye_size(self, region_data: Dict) -> str:
        """Genera tamaño de ojos"""
        sizes = {
            "large": 0.3,
            "medium": 0.5,
            "small": 0.2
        }
        return self._select_by_probability(sizes)
    
    def _generate_eye_spacing(self, region_data: Dict) -> str:
        """Genera espaciado de ojos"""
        spacing = {
            "close": 0.2,
            "normal": 0.6,
            "wide": 0.2
        }
        return self._select_by_probability(spacing)
    
    def _generate_eyelid_type(self, region_data: Dict) -> str:
        """Genera tipo de párpados"""
        eyelids = region_data.get("eyelids", {
            "double": 0.6,
            "single": 0.35,
            "hooded": 0.05
        })
        return self._select_by_probability(eyelids)
    
    def _generate_eyelashes(self, region_data: Dict, gender: str) -> str:
        """Genera pestañas"""
        if gender == "mujer":
            lashes = {
                "long": 0.4,
                "medium": 0.4,
                "short": 0.2
            }
        else:
            lashes = {
                "medium": 0.5,
                "short": 0.4,
                "long": 0.1
            }
        return self._select_by_probability(lashes)
    
    def _generate_eyebrows(self, region_data: Dict, gender: str) -> str:
        """Genera cejas"""
        if gender == "mujer":
            brows = {
                "thick": 0.3,
                "medium": 0.4,
                "thin": 0.2,
                "arched": 0.1
            }
        else:
            brows = {
                "thick": 0.5,
                "medium": 0.3,
                "thin": 0.1,
                "bushy": 0.1
            }
        return self._select_by_probability(brows)
    
    def _generate_nose_shape(self, region_data: Dict) -> str:
        """Genera forma de nariz"""
        nose_shapes = {
            "straight": 0.4,
            "aquiline": 0.2,
            "button": 0.2,
            "roman": 0.1,
            "snub": 0.1
        }
        return self._select_by_probability(nose_shapes)
    
    def _generate_nose_size(self, region_data: Dict) -> str:
        """Genera tamaño de nariz"""
        sizes = {
            "small": 0.2,
            "medium": 0.6,
            "large": 0.2
        }
        return self._select_by_probability(sizes)
    
    def _generate_nose_width(self, region_data: Dict) -> str:
        """Genera ancho de nariz"""
        widths = {
            "narrow": 0.3,
            "medium": 0.5,
            "wide": 0.2
        }
        return self._select_by_probability(widths)
    
    def _generate_nose_bridge(self, region_data: Dict) -> str:
        """Genera puente nasal"""
        bridges = {
            "high": 0.2,
            "medium": 0.6,
            "low": 0.2
        }
        return self._select_by_probability(bridges)
    
    def _generate_lip_shape(self, region_data: Dict, gender: str) -> str:
        """Genera forma de labios"""
        if gender == "mujer":
            lips = {
                "full": 0.3,
                "medium": 0.4,
                "thin": 0.2,
                "bow_shaped": 0.1
            }
        else:
            lips = {
                "medium": 0.5,
                "thin": 0.3,
                "full": 0.2
            }
        return self._select_by_probability(lips)
    
    def _generate_lip_size(self, region_data: Dict, gender: str) -> str:
        """Genera tamaño de labios"""
        if gender == "mujer":
            sizes = {
                "large": 0.3,
                "medium": 0.5,
                "small": 0.2
            }
        else:
            sizes = {
                "medium": 0.6,
                "small": 0.3,
                "large": 0.1
            }
        return self._select_by_probability(sizes)
    
    def _generate_lip_thickness(self, region_data: Dict, gender: str) -> str:
        """Genera grosor de labios"""
        if gender == "mujer":
            thickness = {
                "thick": 0.3,
                "medium": 0.5,
                "thin": 0.2
            }
        else:
            thickness = {
                "medium": 0.6,
                "thin": 0.3,
                "thick": 0.1
            }
        return self._select_by_probability(thickness)
    
    def _generate_mouth_width(self, region_data: Dict) -> str:
        """Genera ancho de boca"""
        widths = {
            "narrow": 0.2,
            "medium": 0.6,
            "wide": 0.2
        }
        return self._select_by_probability(widths)
    
    def _generate_skin_tone(self, region_data: Dict, control: str) -> str:
        """Genera tono de piel con control"""
        if control == "auto":
            skin_tones = region_data.get("skin_tones", {
                "very_light": 0.15,
                "light": 0.25,
                "medium_light": 0.3,
                "medium": 0.2,
                "medium_dark": 0.08,
                "dark": 0.02
            })
        elif control == "light":
            skin_tones = {
                "very_light": 0.4,
                "light": 0.4,
                "medium_light": 0.2
            }
        elif control == "medium":
            skin_tones = {
                "medium_light": 0.3,
                "medium": 0.4,
                "medium_dark": 0.3
            }
        elif control == "dark":
            skin_tones = {
                "medium_dark": 0.4,
                "dark": 0.6
            }
        else:  # mixed
            skin_tones = {
                "light": 0.2,
                "medium_light": 0.3,
                "medium": 0.3,
                "medium_dark": 0.2
            }
        
        return self._select_by_probability(skin_tones)
    
    def _generate_skin_texture(self, region_data: Dict, age: int) -> str:
        """Genera textura de piel basada en edad"""
        if age <= 25:
            textures = {
                "smooth": 0.8,
                "normal": 0.2
            }
        elif age <= 35:
            textures = {
                "smooth": 0.5,
                "normal": 0.4,
                "slightly_rough": 0.1
            }
        elif age <= 45:
            textures = {
                "smooth": 0.2,
                "normal": 0.5,
                "slightly_rough": 0.3
            }
        else:
            textures = {
                "normal": 0.3,
                "slightly_rough": 0.5,
                "rough": 0.2
            }
        
        return self._select_by_probability(textures)
    
    def _generate_skin_imperfections(self, age: int, beauty_control: str) -> List[str]:
        """Genera imperfecciones de piel basadas en edad y control de belleza"""
        imperfections = []
        
        # Obtener características de edad
        age_range = self._get_age_range(age)
        age_chars = self.age_engine.get(age_range, {})
        
        # Ajustar probabilidades según control de belleza
        base_probabilities = self.beauty_engine["imperfections"].copy()
        
        if beauty_control == "attractive":
            # Reducir imperfecciones
            for key in base_probabilities:
                base_probabilities[key] *= 0.5
        elif beauty_control == "realistic":
            # Mantener probabilidades normales
            pass
        elif beauty_control == "random":
            # Aumentar variación
            for key in base_probabilities:
                base_probabilities[key] *= random.uniform(0.5, 1.5)
        
        # Agregar imperfecciones basadas en probabilidades
        for imperfection, probability in base_probabilities.items():
            if random.random() < probability:
                imperfections.append(imperfection)
        
        # Agregar características de edad
        for char, probability in age_chars.items():
            if random.random() < probability:
                imperfections.append(char)
        
        return imperfections
    
    def _generate_freckles(self, region_data: Dict, skin_tone: str) -> str:
        """Genera pecas basadas en tono de piel"""
        if skin_tone in ["very_light", "light"]:
            freckles = {
                "none": 0.4,
                "light": 0.4,
                "medium": 0.2
            }
        elif skin_tone in ["medium_light", "medium"]:
            freckles = {
                "none": 0.7,
                "light": 0.3
            }
        else:
            freckles = {
                "none": 0.9,
                "light": 0.1
            }
        
        return self._select_by_probability(freckles)
    
    def _generate_moles(self, region_data: Dict, skin_tone: str) -> str:
        """Genera lunares basados en tono de piel"""
        if skin_tone in ["very_light", "light"]:
            moles = {
                "none": 0.6,
                "few": 0.3,
                "several": 0.1
            }
        else:
            moles = {
                "none": 0.8,
                "few": 0.2
            }
        
        return self._select_by_probability(moles)
    
    def _generate_hair_color(self, region_data: Dict, control: str) -> str:
        """Genera color de cabello con control"""
        if control == "auto":
            hair_colors = region_data.get("hair_colors", {
                "brown": 0.35,
                "dark_brown": 0.25,
                "black": 0.2,
                "light_brown": 0.1,
                "blonde": 0.05,
                "dark_blonde": 0.03,
                "red": 0.01,
                "auburn": 0.01
            })
        elif control == "dark":
            hair_colors = {
                "black": 0.4,
                "dark_brown": 0.4,
                "brown": 0.2
            }
        elif control == "light":
            hair_colors = {
                "blonde": 0.4,
                "light_brown": 0.3,
                "dark_blonde": 0.2,
                "brown": 0.1
            }
        else:  # mixed
            hair_colors = {
                "brown": 0.3,
                "dark_brown": 0.2,
                "black": 0.2,
                "light_brown": 0.15,
                "blonde": 0.1,
                "dark_blonde": 0.05
            }
        
        return self._select_by_probability(hair_colors)
    
    def _generate_hair_texture(self, region_data: Dict) -> str:
        """Genera textura de cabello"""
        textures = region_data.get("hair_styles", {
            "straight": 0.45,
            "wavy": 0.35,
            "curly": 0.15,
            "afro": 0.05
        })
        return self._select_by_probability(textures)
    
    def _generate_hair_length(self, region_data: Dict, gender: str) -> str:
        """Genera largo de cabello"""
        if gender == "mujer":
            lengths = {
                "long": 0.4,
                "medium": 0.35,
                "short": 0.2,
                "very_short": 0.05
            }
        else:
            lengths = {
                "short": 0.6,
                "very_short": 0.25,
                "medium": 0.1,
                "long": 0.05
            }
        return self._select_by_probability(lengths)
    
    def _generate_hair_style(self, region_data: Dict, gender: str, length: str) -> str:
        """Genera estilo de cabello"""
        if gender == "mujer":
            if length == "long":
                styles = {
                    "loose": 0.4,
                    "ponytail": 0.2,
                    "braids": 0.15,
                    "bun": 0.15,
                    "waves": 0.1
                }
            elif length == "medium":
                styles = {
                    "loose": 0.5,
                    "waves": 0.2,
                    "ponytail": 0.15,
                    "bob": 0.15
                }
            else:
                styles = {
                    "loose": 0.6,
                    "bob": 0.2,
                    "pixie": 0.2
                }
        else:
            styles = {
                "classic": 0.3,
                "modern": 0.25,
                "messy": 0.2,
                "styled": 0.15,
                "natural": 0.1
            }
        
        return self._select_by_probability(styles)
    
    def _generate_hair_density(self, region_data: Dict, gender: str, age: int) -> str:
        """Genera densidad de cabello"""
        if gender == "mujer":
            density = {
                "thick": 0.4,
                "medium": 0.4,
                "thin": 0.2
            }
        else:
            density = {
                "thick": 0.3,
                "medium": 0.5,
                "thin": 0.2
            }
        
        # Ajustar por edad
        if age > 40:
            density["thin"] += 0.2
            density["thick"] -= 0.1
            density["medium"] -= 0.1
        
        return self._select_by_probability(density)
    
    def _generate_age_characteristics(self, age: int) -> List[str]:
        """Genera características de edad"""
        age_range = self._get_age_range(age)
        age_chars = self.age_engine.get(age_range, {})
        
        characteristics = []
        for char, probability in age_chars.items():
            if random.random() < probability:
                characteristics.append(char)
        
        return characteristics
    
    def _generate_beauty_level(self, control: str) -> str:
        """Genera nivel de belleza con control"""
        if control == "normal":
            beauty_levels = self.beauty_engine["beauty_levels"]
        elif control == "attractive":
            beauty_levels = {
                "common": 0.2,
                "average": 0.3,
                "attractive": 0.3,
                "very_attractive": 0.15,
                "exceptionally_beautiful": 0.05
            }
        elif control == "realistic":
            beauty_levels = {
                "common": 0.6,
                "average": 0.3,
                "attractive": 0.08,
                "very_attractive": 0.02,
                "exceptionally_beautiful": 0.0
            }
        else:  # random
            beauty_levels = {
                "common": random.uniform(0.2, 0.6),
                "average": random.uniform(0.2, 0.4),
                "attractive": random.uniform(0.1, 0.3),
                "very_attractive": random.uniform(0.02, 0.1),
                "exceptionally_beautiful": random.uniform(0.0, 0.05)
            }
            # Normalizar
            total = sum(beauty_levels.values())
            beauty_levels = {k: v/total for k, v in beauty_levels.items()}
        
        return self._select_by_probability(beauty_levels)
    
    def _generate_attractiveness_factors(self, beauty_level: str) -> List[str]:
        """Genera factores de atractivo basados en nivel de belleza"""
        factors = []
        
        if beauty_level in ["very_attractive", "exceptionally_beautiful"]:
            # Más factores de atractivo
            for factor, probability in self.beauty_engine["attractiveness_factors"].items():
                if random.random() < probability * 1.5:
                    factors.append(factor)
        elif beauty_level == "attractive":
            # Factores normales
            for factor, probability in self.beauty_engine["attractiveness_factors"].items():
                if random.random() < probability:
                    factors.append(factor)
        else:
            # Menos factores de atractivo
            for factor, probability in self.beauty_engine["attractiveness_factors"].items():
                if random.random() < probability * 0.5:
                    factors.append(factor)
        
        return factors
    
    def _generate_ethnic_features(self, region_data: Dict, nationality: str) -> List[str]:
        """Genera características étnicas específicas"""
        features = []
        
        # Características específicas por nacionalidad
        if nationality == "venezuelan":
            features.extend([
                "mixed_heritage",
                "caribbean_influence",
                "european_features",
                "indigenous_traits"
            ])
        elif nationality == "cuban":
            features.extend([
                "caribbean_heritage",
                "african_influence",
                "spanish_features"
            ])
        elif nationality == "haitian":
            features.extend([
                "african_heritage",
                "caribbean_influence"
            ])
        
        # Agregar características regionales
        if region_data:
            features.append(f"{nationality}_{region_data.get('name', 'regional')}_traits")
        
        return features
    
    def _calculate_uniqueness_score(self) -> float:
        """Calcula score de unicidad de 0 a 1"""
        # Combinación de múltiples factores aleatorios
        factors = [
            random.random(),  # Factor base
            random.random(),  # Factor étnico
            random.random(),  # Factor de edad
            random.random(),  # Factor de belleza
        ]
        
        return sum(factors) / len(factors)
    
    def generate_prompt_from_profile(self, profile: GeneticProfile) -> Tuple[str, str]:
        """Genera prompt completo basado en perfil genético"""
        
        # Prompt positivo
        positive_prompt = f"passport photo, ICAO standards, official document photo, government ID photo, {profile.gender} {profile.nationality}, {profile.age} years old, "
        
        # Características faciales
        positive_prompt += f"{profile.face_shape} face, {profile.face_width} face width, {profile.face_length} face length, "
        positive_prompt += f"{profile.jawline} jawline, {profile.chin} chin, {profile.cheekbones} cheekbones, "
        
        # Ojos
        positive_prompt += f"{profile.eye_color} eyes, {profile.eye_shape} eye shape, {profile.eye_size} eyes, "
        positive_prompt += f"{profile.eye_spacing} eye spacing, {profile.eyelid_type} eyelids, {profile.eyelashes} eyelashes, {profile.eyebrows} eyebrows, "
        
        # Nariz
        positive_prompt += f"{profile.nose_shape} nose, {profile.nose_size} nose size, {profile.nose_width} nose width, {profile.nose_bridge} nose bridge, "
        
        # Boca
        positive_prompt += f"{profile.lip_shape} lips, {profile.lip_size} lip size, {profile.lip_thickness} lip thickness, {profile.mouth_width} mouth width, "
        
        # Piel
        positive_prompt += f"{profile.skin_tone} skin tone, {profile.skin_texture} skin texture, "
        if profile.freckles != "none":
            positive_prompt += f"{profile.freckles} freckles, "
        if profile.moles != "none":
            positive_prompt += f"{profile.moles} moles, "
        
        # Cabello
        positive_prompt += f"{profile.hair_color} hair, {profile.hair_texture} hair texture, {profile.hair_length} hair length, "
        positive_prompt += f"{profile.hair_style} hair style, {profile.hair_density} hair density, "
        
        # Características de edad
        if profile.age_characteristics:
            positive_prompt += f"{', '.join(profile.age_characteristics[:3])}, "
        
        # Nivel de belleza
        positive_prompt += f"{profile.beauty_level}, "
        
        # Factores de atractivo
        if profile.attractiveness_factors:
            positive_prompt += f"{', '.join(profile.attractiveness_factors[:2])}, "
        
        # Características étnicas
        if profile.ethnic_features:
            positive_prompt += f"{', '.join(profile.ethnic_features[:2])}, "
        
        # Imperfecciones de piel (para realismo)
        if profile.skin_imperfections:
            positive_prompt += f"{', '.join(profile.skin_imperfections[:3])}, "
        
        # Finalizar prompt
        positive_prompt += "professional headshot photography, direct portrait photography, pure white background, strictly frontal view, no three quarter view, head and shoulders visible, shoulders must be visible, sufficient head space, no head crop, full head visible, head positioned in upper 60%, eyes positioned at 45%, perfectly centered composition, professional studio lighting, even lighting, no shadows, clean background, high quality, detailed, realistic"
        
        # Prompt negativo
        negative_prompt = "3/4 view, side profile, looking away, smiling, laughing, multiple people, double exposure, passport document visible, photo of photo, magazine model, overly perfect, artificial lighting, shadows, background objects, jewelry, glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, beauty contest, professional headshot, studio lighting, dramatic lighting, soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, duplicate, watermark, text, signature, date, stamp, border, frame, perfect skin, flawless skin, airbrushed, photoshopped, model look, supermodel appearance, celebrity look, fashion model, beauty model, perfect features, flawless features, extreme beauty, perfect beauty, perfect symmetry, flawless symmetry, perfect proportions, flawless proportions, WHITE BACKGROUND, COLORED BACKGROUND, SOLID BACKGROUND, TEXTURED BACKGROUND, GRADIENT BACKGROUND, PATTERN BACKGROUND, BACKGROUND, BACKDROP, WALL, SURFACE, FLOOR, CEILING, ENVIRONMENT, SCENE, SETTING, LOCATION, PLACE, ROOM, INTERIOR, EXTERIOR, OUTDOOR, INDOOR, STUDIO BACKGROUND, PHOTO STUDIO, BACKGROUND WALL, BACKGROUND SURFACE"
        
        return positive_prompt, negative_prompt
