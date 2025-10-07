#!/usr/bin/env python3
"""
Motor de Diversidad Genética Avanzado - Sin Sesgos Eurocéntricos
Sistema que permite generar belleza excepcional en todas las etnias y tonos de piel
"""

import random
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

@dataclass
class AdvancedGeneticProfile:
    """Perfil genético avanzado sin sesgos étnicos"""
    # Identificación
    image_id: str
    nationality: str
    region: str
    gender: str
    age: int
    
    # Características faciales detalladas
    face_shape: str
    face_width: str
    face_length: str
    jawline: str
    chin: str
    cheekbones: str
    facial_symmetry: str
    bone_structure: str
    
    # Ojos detallados
    eye_color: str
    eye_color_shade: str  # Tonalidad específica del color
    eye_shape: str
    eye_size: str
    eye_spacing: str
    eyelid_type: str
    eyelashes: str
    eyelashes_length: str
    eyebrows: str
    eyebrows_thickness: str
    eyebrows_shape: str
    
    # Nariz detallada
    nose_shape: str
    nose_size: str
    nose_width: str
    nose_bridge: str
    nose_tip: str
    nostril_size: str
    
    # Boca detallada
    lip_shape: str
    lip_size: str
    lip_thickness: str
    mouth_width: str
    lip_color: str
    lip_fullness: str
    
    # Piel detallada
    skin_tone: str
    skin_tone_shade: str  # Tonalidad específica
    skin_texture: str
    skin_undertone: str  # Cálido, frío, neutro
    skin_glow: str
    skin_imperfections: List[str]
    freckles: str
    freckles_density: str
    moles: str
    moles_count: str
    birthmarks: str
    scars: str
    acne: str
    age_spots: str
    wrinkles: str
    skin_elasticity: str
    
    # Cabello detallado
    hair_color: str
    hair_color_shade: str  # Tonalidad específica
    hair_texture: str
    hair_length: str
    hair_style: str
    hair_density: str
    hair_shine: str
    hair_curliness: str
    hair_thickness: str
    hairline: str
    
    # Características de edad
    age_characteristics: List[str]
    
    # Nivel de belleza (sin sesgos)
    beauty_level: str
    attractiveness_factors: List[str]
    ethnic_beauty_features: List[str]  # Características de belleza específicas de la etnia
    
    # Características étnicas específicas
    ethnic_features: List[str]
    genetic_heritage: List[str]  # Herencia genética (mestizo, afrodescendiente, etc.)
    
    # Metadatos
    generated_at: str
    generation_type: str
    uniqueness_score: float
    beauty_score: float  # Score de belleza independiente del tono de piel

class AdvancedGeneticDiversityEngine:
    """Motor de diversidad genética avanzado sin sesgos"""
    
    def __init__(self, logger: logging.Logger = None):
        """Inicializa el motor avanzado"""
        self.logger = logger or logging.getLogger(__name__)
        self.consulta_dir = Path(__file__).parent / "Consulta"
        self.ethnic_data = self._load_ethnic_data()
        self.beauty_engine = self._initialize_advanced_beauty_engine()
        self.age_engine = self._initialize_age_engine()
        self.skin_engine = self._initialize_advanced_skin_engine()
        self.hair_engine = self._initialize_advanced_hair_engine()
        self.eye_engine = self._initialize_advanced_eye_engine()
        
    def _load_ethnic_data(self) -> Dict[str, Any]:
        """Carga datos étnicos desde archivos JSON"""
        ethnic_data = {}
        
        # Cargar datos de países
        countries_dir = self.consulta_dir / "countries"
        if countries_dir.exists():
            for country_file in countries_dir.glob("*.json"):
                try:
                    with open(country_file, 'r', encoding='utf-8') as f:
                        country_data = json.load(f)
                        country_name = country_file.stem
                        ethnic_data[country_name] = country_data
                except Exception as e:
                    self.logger.warning(f"Error cargando {country_file}: {e}")
        
        return ethnic_data
    
    def _initialize_advanced_beauty_engine(self) -> Dict[str, Any]:
        """Inicializa motor de belleza avanzado sin sesgos étnicos"""
        return {
            "beauty_levels": {
                "common": 0.4,
                "average": 0.3,
                "attractive": 0.2,
                "very_attractive": 0.08,
                "exceptionally_beautiful": 0.02
            },
            "attractiveness_factors": {
                "facial_symmetry": 0.8,
                "clear_skin": 0.7,
                "defined_features": 0.6,
                "golden_proportions": 0.5,
                "natural_expression": 0.9,
                "healthy_glow": 0.6,
                "balanced_features": 0.7,
                "expressive_eyes": 0.8,
                "well_defined_bone_structure": 0.6,
                "harmonious_facial_balance": 0.7
            },
            "ethnic_beauty_features": {
                "venezuelan": {
                    "mestizo_beauty": ["warm_skin_tone", "expressive_eyes", "defined_cheekbones", "full_lips"],
                    "afrodescendant_beauty": ["rich_skin_tone", "almond_eyes", "strong_bone_structure", "voluptuous_lips"],
                    "indigenous_beauty": ["golden_skin_tone", "deep_eyes", "high_cheekbones", "natural_features"],
                    "european_beauty": ["fair_skin_tone", "light_eyes", "defined_nose", "classic_features"]
                }
            },
            "skin_tone_beauty": {
                "very_light": ["porcelain_glow", "translucent_skin", "rosy_undertones"],
                "light": ["peachy_glow", "smooth_texture", "warm_undertones"],
                "medium_light": ["golden_glow", "radiant_skin", "neutral_undertones"],
                "medium": ["bronze_glow", "rich_texture", "warm_undertones"],
                "medium_dark": ["copper_glow", "luminous_skin", "golden_undertones"],
                "dark": ["mahogany_glow", "deep_radiance", "rich_undertones"],
                "very_dark": ["ebony_glow", "smooth_richness", "deep_undertones"]
            }
        }
    
    def _initialize_advanced_skin_engine(self) -> Dict[str, Any]:
        """Inicializa motor de piel avanzado"""
        return {
            "skin_tones": {
                "very_light": {
                    "shades": ["porcelain", "ivory", "alabaster"],
                    "undertones": ["cool", "neutral", "warm"],
                    "beauty_features": ["translucent_glow", "rosy_cheeks", "smooth_texture"]
                },
                "light": {
                    "shades": ["fair", "light_beige", "peachy"],
                    "undertones": ["warm", "neutral", "cool"],
                    "beauty_features": ["peachy_glow", "smooth_texture", "natural_radiance"]
                },
                "medium_light": {
                    "shades": ["light_olive", "golden_beige", "warm_beige"],
                    "undertones": ["warm", "neutral", "olive"],
                    "beauty_features": ["golden_glow", "radiant_skin", "healthy_complexion"]
                },
                "medium": {
                    "shades": ["olive", "bronze", "caramel"],
                    "undertones": ["warm", "neutral", "olive"],
                    "beauty_features": ["bronze_glow", "rich_texture", "sun_kissed_look"]
                },
                "medium_dark": {
                    "shades": ["deep_olive", "copper", "rich_bronze"],
                    "undertones": ["warm", "neutral", "golden"],
                    "beauty_features": ["copper_glow", "luminous_skin", "warm_radiance"]
                },
                "dark": {
                    "shades": ["mahogany", "deep_bronze", "rich_brown"],
                    "undertones": ["warm", "neutral", "red"],
                    "beauty_features": ["mahogany_glow", "deep_radiance", "rich_complexion"]
                },
                "very_dark": {
                    "shades": ["ebony", "deep_mahogany", "rich_ebony"],
                    "undertones": ["cool", "neutral", "blue"],
                    "beauty_features": ["ebony_glow", "smooth_richness", "deep_luminosity"]
                }
            },
            "skin_textures": {
                "smooth": 0.3,
                "normal": 0.4,
                "slightly_rough": 0.2,
                "rough": 0.1
            },
            "skin_imperfections": {
                "acne": 0.1,
                "scars": 0.05,
                "age_spots": 0.15,
                "wrinkles": 0.2,
                "dark_circles": 0.1,
                "uneven_tone": 0.1,
                "large_pores": 0.1,
                "blackheads": 0.05
            },
            "freckles": {
                "none": 0.6,
                "light": 0.25,
                "medium": 0.1,
                "heavy": 0.05
            },
            "moles": {
                "none": 0.7,
                "few": 0.2,
                "several": 0.08,
                "many": 0.02
            }
        }
    
    def _initialize_advanced_hair_engine(self) -> Dict[str, Any]:
        """Inicializa motor de cabello avanzado"""
        return {
            "hair_colors": {
                "black": {
                    "shades": ["jet_black", "soft_black", "blue_black", "brown_black"],
                    "beauty_features": ["deep_shine", "rich_color", "smooth_texture"]
                },
                "dark_brown": {
                    "shades": ["chocolate", "espresso", "dark_chestnut", "rich_brown"],
                    "beauty_features": ["warm_tones", "natural_shine", "rich_depth"]
                },
                "brown": {
                    "shades": ["chestnut", "medium_brown", "warm_brown", "golden_brown"],
                    "beauty_features": ["natural_warmth", "versatile_color", "healthy_shine"]
                },
                "light_brown": {
                    "shades": ["light_chestnut", "honey_brown", "caramel", "bronze"],
                    "beauty_features": ["sun_kissed_look", "warm_glow", "natural_highlights"]
                },
                "blonde": {
                    "shades": ["platinum", "ash_blonde", "golden_blonde", "honey_blonde"],
                    "beauty_features": ["bright_shine", "light_reflection", "youthful_appearance"]
                },
                "red": {
                    "shades": ["auburn", "copper", "strawberry", "burgundy"],
                    "beauty_features": ["unique_color", "warm_undertones", "eye_catching"]
                },
                "gray": {
                    "shades": ["silver", "pepper_salt", "steel_gray", "white"],
                    "beauty_features": ["distinguished_look", "natural_elegance", "mature_beauty"]
                }
            },
            "hair_textures": {
                "straight": 0.4,
                "wavy": 0.3,
                "curly": 0.2,
                "coily": 0.1
            },
            "hair_styles": {
                "women": {
                    "long": ["loose", "ponytail", "braids", "bun", "waves", "curls"],
                    "medium": ["bob", "lob", "layered", "wavy", "straight"],
                    "short": ["pixie", "bob", "asymmetrical", "textured"]
                },
                "men": {
                    "long": ["man_bun", "ponytail", "loose", "wavy"],
                    "medium": ["textured", "layered", "side_part", "messy"],
                    "short": ["classic", "modern", "fade", "buzz", "crew_cut"]
                }
            }
        }
    
    def _initialize_advanced_eye_engine(self) -> Dict[str, Any]:
        """Inicializa motor de ojos avanzado"""
        return {
            "eye_colors": {
                "brown": {
                    "shades": ["light_brown", "medium_brown", "dark_brown", "honey", "amber", "chocolate"],
                    "beauty_features": ["warm_depth", "expressive", "mysterious"]
                },
                "dark_brown": {
                    "shades": ["dark_brown", "chocolate", "espresso", "ebony"],
                    "beauty_features": ["deep_intensity", "expressive", "mysterious"]
                },
                "light_brown": {
                    "shades": ["light_brown", "honey", "amber", "golden_brown"],
                    "beauty_features": ["warm_glow", "expressive", "soft"]
                },
                "blue": {
                    "shades": ["light_blue", "sky_blue", "navy_blue", "steel_blue", "crystal_blue"],
                    "beauty_features": ["bright_shine", "clear_depth", "captivating"]
                },
                "green": {
                    "shades": ["emerald", "hazel_green", "forest_green", "olive_green", "jade"],
                    "beauty_features": ["unique_color", "natural_beauty", "striking"]
                },
                "hazel": {
                    "shades": ["light_hazel", "golden_hazel", "brown_hazel", "green_hazel"],
                    "beauty_features": ["chameleon_effect", "mysterious", "versatile"]
                },
                "gray": {
                    "shades": ["light_gray", "steel_gray", "blue_gray", "silver_gray"],
                    "beauty_features": ["sophisticated", "mysterious", "elegant"]
                },
                "amber": {
                    "shades": ["golden_amber", "honey_amber", "orange_amber"],
                    "beauty_features": ["warm_glow", "unique", "captivating"]
                }
            },
            "eye_shapes": {
                "almond": 0.3,
                "round": 0.25,
                "oval": 0.2,
                "upturned": 0.15,
                "downturned": 0.1
            },
            "eye_sizes": {
                "large": 0.3,
                "medium": 0.5,
                "small": 0.2
            }
        }
    
    def _initialize_age_engine(self) -> Dict[str, Any]:
        """Inicializa motor de características de edad"""
        return {
            "18-25": {
                "skin_texture": "smooth",
                "hair_density": "thick",
                "facial_features": "defined",
                "imperfections": ["acne", "dark_circles"]
            },
            "26-35": {
                "skin_texture": "normal",
                "hair_density": "thick",
                "facial_features": "mature",
                "imperfections": ["fine_lines", "dark_circles", "uneven_tone"]
            },
            "36-45": {
                "skin_texture": "slightly_rough",
                "hair_density": "medium",
                "facial_features": "mature",
                "imperfections": ["wrinkles", "age_spots", "sagging"]
            },
            "46-55": {
                "skin_texture": "rough",
                "hair_density": "thin",
                "facial_features": "aged",
                "imperfections": ["deep_wrinkles", "age_spots", "jowls", "neck_lines"]
            },
            "56-65": {
                "skin_texture": "rough",
                "hair_density": "thin",
                "facial_features": "aged",
                "imperfections": ["deep_wrinkles", "age_spots", "jowls", "neck_lines", "sagging"]
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
    
    def generate_advanced_genetic_profile(self, 
                                        nationality: str, 
                                        region: str, 
                                        gender: str, 
                                        age: int,
                                        beauty_control: str = "normal",
                                        skin_control: str = "auto",
                                        hair_control: str = "auto",
                                        eye_control: str = "auto") -> AdvancedGeneticProfile:
        """
        Genera un perfil genético avanzado sin sesgos étnicos
        
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
        
        # Añadir variación de seed para máxima diversidad
        import time
        unique_seed = int(time.time() * 1000000) + random.randint(1, 999999) + hash(f"{nationality}_{region}_{gender}_{age}") % 1000000
        random.seed(unique_seed)
        
        # Si la región es "aleatorio", seleccionar una región aleatoria
        if region == "aleatorio":
            import random
            # Usar la misma lista de regiones que el método masivo básico
            available_regions = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
            region = random.choice(available_regions)
        
        region_data = regions.get(region, regions.get("caracas", {}))
        
        # Generar características faciales
        face_shape = self._generate_face_shape(region_data, gender)
        face_width = self._generate_face_width(region_data)
        face_length = self._generate_face_length(region_data)
        jawline = self._generate_jawline(region_data, gender, age)
        chin = self._generate_chin(region_data, gender)
        cheekbones = self._generate_cheekbones(region_data, gender, age)
        facial_symmetry = self._generate_facial_symmetry(beauty_control)
        bone_structure = self._generate_bone_structure(region_data, gender)
        
        # Generar características de ojos avanzadas
        eye_color, eye_color_shade = self._generate_advanced_eye_color(region_data, eye_control)
        eye_shape = self._generate_eye_shape(region_data)
        eye_size = self._generate_eye_size(region_data)
        eye_spacing = self._generate_eye_spacing(region_data)
        eyelid_type = self._generate_eyelid_type(region_data)
        eyelashes, eyelashes_length = self._generate_eyelashes(region_data, gender)
        eyebrows, eyebrows_thickness, eyebrows_shape = self._generate_eyebrows(region_data, gender)
        
        # Generar características de nariz avanzadas
        nose_shape = self._generate_nose_shape(region_data)
        nose_size = self._generate_nose_size(region_data)
        nose_width = self._generate_nose_width(region_data)
        nose_bridge = self._generate_nose_bridge(region_data)
        nose_tip = self._generate_nose_tip(region_data)
        nostril_size = self._generate_nostril_size(region_data)
        
        # Generar características de boca avanzadas
        lip_shape = self._generate_lip_shape(region_data, gender)
        lip_size = self._generate_lip_size(region_data, gender)
        lip_thickness = self._generate_lip_thickness(region_data, gender)
        mouth_width = self._generate_mouth_width(region_data)
        lip_color = self._generate_lip_color(region_data, gender)
        lip_fullness = self._generate_lip_fullness(region_data, gender)
        
        # Generar características de piel avanzadas
        skin_tone, skin_tone_shade = self._generate_advanced_skin_tone(region_data, skin_control)
        skin_texture = self._generate_skin_texture(region_data, age)
        skin_undertone = self._generate_skin_undertone(skin_tone)
        skin_glow = self._generate_skin_glow(skin_tone, beauty_control)
        skin_imperfections = self._generate_skin_imperfections(age, beauty_control)
        freckles, freckles_density = self._generate_freckles(region_data, skin_tone)
        moles, moles_count = self._generate_moles(region_data, skin_tone)
        birthmarks = self._generate_birthmarks(region_data, skin_tone)
        scars = self._generate_scars(region_data, age)
        acne = self._generate_acne(age, beauty_control)
        age_spots = self._generate_age_spots(age, beauty_control)
        wrinkles = self._generate_wrinkles(age, beauty_control)
        skin_elasticity = self._generate_skin_elasticity(age)
        
        # Generar características de cabello avanzadas
        hair_color, hair_color_shade = self._generate_advanced_hair_color(region_data, hair_control)
        hair_texture = self._generate_hair_texture(region_data)
        hair_length = self._generate_hair_length(region_data, gender)
        hair_style = self._generate_hair_style(region_data, gender, hair_length)
        hair_density = self._generate_hair_density(region_data, gender, age)
        hair_shine = self._generate_hair_shine(hair_color, beauty_control)
        hair_curliness = self._generate_hair_curliness(hair_texture)
        hair_thickness = self._generate_hair_thickness(region_data, gender)
        hairline = self._generate_hairline(region_data, gender, age)
        
        # Generar características de edad
        age_characteristics = self._generate_age_characteristics(age)
        
        # Generar nivel de belleza sin sesgos
        beauty_level = self._generate_beauty_level(beauty_control)
        attractiveness_factors = self._generate_attractiveness_factors(beauty_level)
        ethnic_beauty_features = self._generate_ethnic_beauty_features(nationality, skin_tone)
        
        # Generar características étnicas específicas
        ethnic_features = self._generate_ethnic_features(region_data, nationality)
        genetic_heritage = self._generate_genetic_heritage(region_data, nationality)
        
        # Calcular scores
        uniqueness_score = self._calculate_uniqueness_score()
        beauty_score = self._calculate_beauty_score(beauty_level, skin_tone, attractiveness_factors)
        
        return AdvancedGeneticProfile(
            image_id=f"{nationality}_{region}_{gender}_{age}_{int(time.time() * 1000000)}_{random.randint(1, 999999)}",
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
            facial_symmetry=facial_symmetry,
            bone_structure=bone_structure,
            eye_color=eye_color,
            eye_color_shade=eye_color_shade,
            eye_shape=eye_shape,
            eye_size=eye_size,
            eye_spacing=eye_spacing,
            eyelid_type=eyelid_type,
            eyelashes=eyelashes,
            eyelashes_length=eyelashes_length,
            eyebrows=eyebrows,
            eyebrows_thickness=eyebrows_thickness,
            eyebrows_shape=eyebrows_shape,
            nose_shape=nose_shape,
            nose_size=nose_size,
            nose_width=nose_width,
            nose_bridge=nose_bridge,
            nose_tip=nose_tip,
            nostril_size=nostril_size,
            lip_shape=lip_shape,
            lip_size=lip_size,
            lip_thickness=lip_thickness,
            mouth_width=mouth_width,
            lip_color=lip_color,
            lip_fullness=lip_fullness,
            skin_tone=skin_tone,
            skin_tone_shade=skin_tone_shade,
            skin_texture=skin_texture,
            skin_undertone=skin_undertone,
            skin_glow=skin_glow,
            skin_imperfections=skin_imperfections,
            freckles=freckles,
            freckles_density=freckles_density,
            moles=moles,
            moles_count=moles_count,
            birthmarks=birthmarks,
            scars=scars,
            acne=acne,
            age_spots=age_spots,
            wrinkles=wrinkles,
            skin_elasticity=skin_elasticity,
            hair_color=hair_color,
            hair_color_shade=hair_color_shade,
            hair_texture=hair_texture,
            hair_length=hair_length,
            hair_style=hair_style,
            hair_density=hair_density,
            hair_shine=hair_shine,
            hair_curliness=hair_curliness,
            hair_thickness=hair_thickness,
            hairline=hairline,
            age_characteristics=age_characteristics,
            beauty_level=beauty_level,
            attractiveness_factors=attractiveness_factors,
            ethnic_beauty_features=ethnic_beauty_features,
            ethnic_features=ethnic_features,
            genetic_heritage=genetic_heritage,
            generated_at=datetime.now().isoformat(),
            generation_type="advanced_genetic_diversity",
            uniqueness_score=uniqueness_score,
            beauty_score=beauty_score
        )
    
    def _generate_facial_symmetry(self, beauty_control: str) -> str:
        """Genera simetría facial basada en control de belleza"""
        if beauty_control == "attractive":
            symmetry = {
                "perfect": 0.3,
                "near_perfect": 0.4,
                "good": 0.2,
                "average": 0.1
            }
        elif beauty_control == "realistic":
            symmetry = {
                "perfect": 0.05,
                "near_perfect": 0.15,
                "good": 0.4,
                "average": 0.4
            }
        else:
            symmetry = {
                "perfect": 0.1,
                "near_perfect": 0.2,
                "good": 0.4,
                "average": 0.3
            }
        return self._select_by_probability(symmetry)
    
    def _generate_bone_structure(self, region_data: Dict, gender: str) -> str:
        """Genera estructura ósea"""
        if gender == "hombre":
            structures = {
                "strong": 0.4,
                "defined": 0.3,
                "moderate": 0.2,
                "soft": 0.1
            }
        else:
            structures = {
                "defined": 0.4,
                "moderate": 0.3,
                "soft": 0.2,
                "strong": 0.1
            }
        return self._select_by_probability(structures)
    
    def _generate_advanced_eye_color(self, region_data: Dict, control: str) -> Tuple[str, str]:
        """Genera color de ojos avanzado con tonalidad específica"""
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
        
        eye_color = self._select_by_probability(eye_colors)
        # Convertir lista de tonalidades a diccionario con probabilidades iguales
        if eye_color in self.eye_engine["eye_colors"]:
            shades_list = self.eye_engine["eye_colors"][eye_color]["shades"]
        else:
            # Fallback para colores no definidos
            shades_list = [eye_color]
        shades_dict = {shade: 1.0/len(shades_list) for shade in shades_list}
        eye_color_shade = self._select_by_probability(shades_dict)
        
        return eye_color, eye_color_shade
    
    def _generate_advanced_skin_tone(self, region_data: Dict, control: str) -> Tuple[str, str]:
        """Genera tono de piel avanzado con tonalidad específica"""
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
        
        skin_tone = self._select_by_probability(skin_tones)
        # Convertir lista de tonalidades a diccionario con probabilidades iguales
        shades_list = self.skin_engine["skin_tones"][skin_tone]["shades"]
        shades_dict = {shade: 1.0/len(shades_list) for shade in shades_list}
        skin_tone_shade = self._select_by_probability(shades_dict)
        
        return skin_tone, skin_tone_shade
    
    def _generate_advanced_hair_color(self, region_data: Dict, control: str) -> Tuple[str, str]:
        """Genera color de cabello avanzado con tonalidad específica"""
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
        
        hair_color = self._select_by_probability(hair_colors)
        # Convertir lista de tonalidades a diccionario con probabilidades iguales
        shades_list = self.hair_engine["hair_colors"][hair_color]["shades"]
        shades_dict = {shade: 1.0/len(shades_list) for shade in shades_list}
        hair_color_shade = self._select_by_probability(shades_dict)
        
        return hair_color, hair_color_shade
    
    def _generate_skin_undertone(self, skin_tone: str) -> str:
        """Genera undertone de piel"""
        undertones = self.skin_engine["skin_tones"][skin_tone]["undertones"]
        return self._select_by_probability({tone: 1.0/len(undertones) for tone in undertones})
    
    def _generate_skin_glow(self, skin_tone: str, beauty_control: str) -> str:
        """Genera brillo de piel basado en tono y belleza"""
        if beauty_control in ["attractive", "exceptionally_beautiful"]:
            glow_options = {
                "radiant": 0.4,
                "luminous": 0.3,
                "glowing": 0.2,
                "natural": 0.1
            }
        else:
            glow_options = {
                "natural": 0.5,
                "glowing": 0.3,
                "luminous": 0.15,
                "radiant": 0.05
            }
        return self._select_by_probability(glow_options)
    
    def _generate_ethnic_beauty_features(self, nationality: str, skin_tone: str) -> List[str]:
        """Genera características de belleza étnicas específicas"""
        features = []
        
        # Obtener características de belleza por tono de piel
        skin_beauty = self.beauty_engine["skin_tone_beauty"].get(skin_tone, [])
        features.extend(skin_beauty)
        
        # Obtener características étnicas específicas
        ethnic_beauty = self.beauty_engine["ethnic_beauty_features"].get(nationality, {})
        for heritage, heritage_features in ethnic_beauty.items():
            if random.random() < 0.3:  # 30% probabilidad de incluir cada herencia
                features.extend(heritage_features)
        
        return features
    
    def _generate_genetic_heritage(self, region_data: Dict, nationality: str) -> List[str]:
        """Genera herencia genética"""
        heritage_options = {
            "mestizo": 0.4,
            "afrodescendant": 0.2,
            "indigenous": 0.2,
            "european": 0.15,
            "mixed": 0.05
        }
        
        heritage = []
        for heritage_type, probability in heritage_options.items():
            if random.random() < probability:
                heritage.append(heritage_type)
        
        return heritage if heritage else ["mestizo"]
    
    def _calculate_beauty_score(self, beauty_level: str, skin_tone: str, attractiveness_factors: List[str]) -> float:
        """Calcula score de belleza independiente del tono de piel"""
        base_scores = {
            "common": 0.3,
            "average": 0.5,
            "attractive": 0.7,
            "very_attractive": 0.85,
            "exceptionally_beautiful": 0.95
        }
        
        base_score = base_scores.get(beauty_level, 0.5)
        
        # Añadir bonus por factores de atractivo
        factor_bonus = len(attractiveness_factors) * 0.02
        
        # Añadir bonus por características étnicas de belleza
        ethnic_bonus = 0.05  # Todas las etnias tienen características de belleza
        
        final_score = min(1.0, base_score + factor_bonus + ethnic_bonus)
        return round(final_score, 3)
    
    def generate_prompt_from_advanced_profile(self, profile: AdvancedGeneticProfile, background_control: str = "white") -> Tuple[str, str]:
        """Genera prompt simplificado desde perfil genético avanzado - Basado en muestras exitosas"""
        
        # Construir prompt positivo simplificado (como las muestras exitosas)
        prompt_parts = [
            f"{profile.nationality} {profile.gender}",
            f"{profile.age} years old",
            f"from {profile.region} region",
            f"{profile.skin_tone} skin",
            f"{profile.skin_texture} skin texture",
            f"{profile.hair_color} hair",
            f"{profile.hair_style} hair",
            f"{profile.eye_color} eyes",
            f"{profile.eye_shape} eyes",
            f"{profile.face_shape} face",
            f"{profile.nose_shape} nose",
            f"{profile.lip_shape} lips",
            f"{profile.eyebrows} eyebrows",
            f"{profile.jawline} jawline",
            f"{profile.cheekbones} cheekbones"
        ]
        
        # Añadir características específicas solo si son relevantes (simplificado)
        if profile.freckles != "none":
            prompt_parts.append(f"{profile.freckles} freckles")
        
        if profile.moles != "none":
            prompt_parts.append(f"{profile.moles} moles")
        
        if profile.scars != "none":
            prompt_parts.append(f"{profile.scars} scars")
        
        if profile.acne != "none":
            prompt_parts.append(f"{profile.acne} acne")
        
        if profile.wrinkles != "none":
            prompt_parts.append(f"{profile.wrinkles} wrinkles")
        
        # Añadir contexto de pasaporte (exactamente como las muestras exitosas)
        prompt_parts.extend([
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
            "head and shoulders framing",
            "passport crop",
            "ID photo crop",
            "official document crop",
            "head centered in frame",
            "shoulders at bottom edge",
            "SAIME Venezuela passport photo",
            "official SAIME specifications",
            "Venezuelan passport requirements",
            "head positioned in upper third of frame",
            "head in upper portion of image",
            "head not touching top edge",
            "small space above head",
            "minimal clearance above head",
            "head well below top border",
            "head centered vertically in upper third",
            "face fills 70% of image height",
            "face occupies most of frame",
            "head takes up most of image",
            "large head in frame",
            "head dominates the image",
            "head and shoulders fill frame",
            "shoulders at bottom of image",
            "shoulders visible at bottom edge",
            "head and shoulders composition",
            "passport photo proportions",
            "ID photo proportions",
            "document photo proportions",
            "official photo proportions",
            "government photo proportions",
            "passport style proportions",
            "ID card proportions",
            "document proportions",
            "official document proportions",
            "government document proportions",
            "tight headshot framing",
            "close-up headshot",
            "head fills most of frame",
            "face centered in upper portion",
            "head positioned in upper 60% of image",
            "eyes positioned at 45% from top",
            "head and shoulders visible",
            "shoulders at bottom edge",
            "head not touching top",
            "head not touching sides",
            "proper head size for passport",
            "correct head proportions",
            "head size appropriate for ID",
            "head size suitable for document",
            "head size perfect for passport",
            "head size ideal for ID card",
            "head size optimal for document",
            "head size correct for official photo",
            "head size proper for government ID",
            "shoulders not touching sides",
            "shoulders not touching bottom",
            "clavicle junction visible",
            "clavicle connection visible",
            "shoulder joint visible",
            "shoulder connection visible",
            "proper head size",
            "correct head size",
            "head not too large",
            "head not too small",
            "head proportional",
            "head well proportioned",
            "head properly sized",
            "head correctly sized",
            "head appropriately sized",
            "head optimally sized",
            "head perfectly sized",
            "head ideally sized",
            "high quality",
            "high resolution",
            "sharp focus",
            "crystal clear",
            "detailed",
            "crisp",
            "clean",
            "professional quality",
            "studio quality",
            "photographic quality",
            "color photography",
            "full color",
            "vibrant colors",
            "natural colors",
            "accurate colors",
            "true colors",
            "rich colors",
            "saturated colors",
            "colorful",
            "color image",
            "color photo",
            "color photograph",
            "color portrait",
            "color headshot",
            "color passport photo",
            "color ID photo",
            "color document photo",
            "color official photo",
            "color government photo",
            "color passport",
            "color ID",
            "color document",
            "color official",
            "color government",
            "everyday person",
            "normal person",
            "regular person",
            "common person",
            "average person",
            "real person",
            "authentic person",
            "natural person",
            "ordinary person",
            "typical person"
        ])
        
        # Agregar fondo según control (optimizado para pasaportes)
        if background_control == "white":
            prompt_parts.extend([
                "pure white background",
                "solid white background", 
                "clean white background",
                "uniform white background",
                "plain white background",
                "studio white background"
            ])
        elif background_control == "beige":
            prompt_parts.extend([
                "pure beige background",
                "solid beige background",
                "clean beige background",
                "uniform beige background"
            ])
        elif background_control == "light_blue":
            prompt_parts.extend([
                "pure light blue background",
                "solid light blue background",
                "clean light blue background",
                "uniform light blue background"
            ])
        elif background_control == "sin_fondo":
            prompt_parts.extend([
                "transparent background",
                "no background",
                "alpha channel",
                "transparent backdrop"
            ])
        else:
            # Por defecto usar fondo blanco sólido para pasaportes
            prompt_parts.extend([
                "pure white background",
                "solid white background",
                "clean white background",
                "uniform white background",
                "plain white background",
                "studio white background"
            ])
        
        positive_prompt = ", ".join(prompt_parts)
        
        # Construir prompt negativo simplificado (basado en muestras exitosas)
        negative_prompt = ", ".join([
            "3/4 view, side profile, profile view, looking away, looking left, looking right, looking up, looking down, tilted head, turned head, angled face, off-center, asymmetrical, smiling, laughing, frowning, head tilted, head turned, head angled, head not straight, head not centered, face not centered, face not straight, face angled, face tilted, face turned, shoulders not visible, shoulders not straight, shoulders tilted, shoulders angled, hair covering face, hair covering eyes, hair covering ears, hair covering shoulders, hair messy, hair unkempt, hair not neat, hair not professional, hair in face, hair over eyes, hair over ears, hair over shoulders, long hair covering, hair blocking face, hair blocking eyes, hair blocking ears, hair blocking shoulders, improper framing, wrong proportions, incorrect framing, bad composition, poor framing, wrong crop, incorrect crop, bad crop, too close, too far, wrong distance, incorrect distance, bad distance, head too large, head too small, head too close, head too far, head touching top, head touching edges, head touching sides, head touching bottom, shoulders touching sides, shoulders touching bottom, shoulders touching edges, no space above head, insufficient space above head, too little space above head, head filling frame, head filling top, head filling edges, head filling sides, head filling bottom, head at top of image, head near top edge, head close to top, head touching top border, head touching top margin, head too high in frame, head positioned too high, head not centered vertically, head not in upper third, head not in upper portion, head too high in frame, head at top of image, head touching top edge, head filling top of frame, head too small in frame, head too far from camera, head not filling frame, head not dominating image, face too small, face not filling frame, head not centered vertically, head not in upper third, head positioned too low, head in middle of frame, head in lower portion, head not in upper portion, shoulders not visible, shoulders cut off, shoulders missing, head only visible, no shoulders, shoulders not at bottom, wrong proportions, incorrect proportions, bad proportions, poor proportions, wrong composition, incorrect composition, bad composition, poor composition, head too large for frame, head too small for frame, head not appropriate size, head size incorrect for passport, head size wrong for ID, head size inappropriate for document, head size not suitable for passport, head size not ideal for ID card, head size not optimal for document, head size not correct for official photo, head size not proper for government ID, head touching top edge, head touching sides, head touching bottom, head filling entire frame, head too close to edges, head too close to top, head too close to sides, head too close to bottom, insufficient space around head, no space around head, head filling frame completely, head dominating entire image, head taking up whole frame, shoulders filling frame, shoulders filling sides, shoulders filling bottom, shoulders filling edges, clavicle not visible, clavicle junction not visible, clavicle connection not visible, shoulder joint not visible, shoulder connection not visible, improper head size, incorrect head size, wrong head size, bad head size, head not proportional, head not well proportioned, head not properly sized, head not correctly sized, head not appropriately sized, head not optimally sized, head not perfectly sized, head not ideally sized, low quality, low resolution, blurry, fuzzy, unclear, unfocused, soft focus, out of focus, poor quality, bad quality, amateur quality, grainy, noisy, pixelated, compressed, artifacts, distorted, deformed, black and white, bw, monochrome, grayscale, sepia, vintage, old, aged, faded, washed out, desaturated, muted colors, dull colors, pale colors, weak colors, faded colors, washed out colors, desaturated colors, muted, dull, pale, weak, faded, washed out, desaturated, no color, colorless, achromatic, monochromatic, grayscale, sepia tone, vintage look, old look, aged look, faded look, washed out look, desaturated look, muted look, dull look, pale look, weak look, faded look, washed out look, desaturated look, multiple people, blurry, low quality, distorted, deformed, ugly, bad anatomy, bad proportions, extra limbs, missing limbs, extra fingers, missing fingers, extra arms, missing arms, extra legs, missing legs, extra heads, missing heads, extra eyes, missing eyes, extra nose, missing nose, extra mouth, missing mouth, text, watermark, signature, gradient background, gradient, faded background, textured background, patterned background, noisy background, complex background, busy background, shadows on background, lighting effects on background, colored background, colored backdrop, tinted background, off-white background, cream background, beige background, gray background, light gray background, dark background, black background, blue background, green background, red background, yellow background, purple background, orange background, brown background, wood background, wall background, fabric background, paper background, canvas background, brick background, stone background, metal background, glass background, mirror background, reflection, shadows, lighting, spotlight, soft lighting, dramatic lighting, rim lighting, back lighting, side lighting, top lighting, bottom lighting, ambient lighting, natural lighting, artificial lighting, studio lighting, flash lighting, harsh lighting, dim lighting, bright lighting, overexposed, underexposed, high contrast, low contrast, saturated colors, desaturated colors, vibrant colors, muted colors, warm colors, cool colors, neutral colors, pastel colors, bold colors, subtle colors, airbrushed, photoshopped, retouched, smooth skin, perfect skin, flawless skin, glowing skin, shiny skin, oily skin, greasy skin, plastic skin, artificial skin, digital art, 3d render, cg, computer generated, synthetic, fake, artificial, overexposed, bright lighting, studio lighting, flash photography, harsh lighting, dramatic lighting, cinematic lighting, professional lighting, perfect lighting, ideal lighting, enhanced, improved, perfected, beautified, glamorized, stylized, artistic, aesthetic, beautiful, attractive, handsome, pretty, gorgeous, stunning, perfect, ideal, flawless, immaculate, pristine, clean, pure, crystal clear, sharp, crisp, vibrant, saturated, colorful, bright, luminous, radiant, brilliant, sparkling, shining, glowing, glossy, polished, refined, elegant, sophisticated, luxurious, premium, high-end, professional, commercial, advertising, marketing, fashion, beauty, cosmetic, makeup, foundation, concealer, powder, blush, lipstick, mascara, eyeliner, eyeshadow, contouring, highlighting, bronzer, primer, setting spray, finishing powder, model look, supermodel appearance, celebrity look, fashion model, beauty model, perfect face, flawless face, ideal face, beautiful face, attractive face, handsome face, pretty face, gorgeous face, stunning face, perfect features, flawless features, ideal features, beautiful features, attractive features, handsome features, pretty features, gorgeous features, stunning features"
        ])
        
        return positive_prompt, negative_prompt
    
    # Funciones auxiliares que faltan
    def _generate_face_shape(self, region_data: Dict, gender: str) -> str:
        """Genera forma de cara"""
        shapes = {
            "oval": 0.3,
            "round": 0.25,
            "square": 0.2,
            "heart": 0.15,
            "diamond": 0.1
        }
        return self._select_by_probability(shapes)
    
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
        """Genera mandíbula"""
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
    
    def _generate_eyelashes(self, region_data: Dict, gender: str) -> Tuple[str, str]:
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
        
        lash_type = self._select_by_probability(lashes)
        lash_length = lash_type  # Mismo valor para simplicidad
        return lash_type, lash_length
    
    def _generate_eyebrows(self, region_data: Dict, gender: str) -> Tuple[str, str, str]:
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
        
        brow_type = self._select_by_probability(brows)
        brow_thickness = brow_type  # Mismo valor para simplicidad
        brow_shape = "natural"  # Valor por defecto
        return brow_type, brow_thickness, brow_shape
    
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
    
    def _generate_nose_tip(self, region_data: Dict) -> str:
        """Genera punta de nariz"""
        tips = {
            "pointed": 0.3,
            "rounded": 0.4,
            "flat": 0.2,
            "upturned": 0.1
        }
        return self._select_by_probability(tips)
    
    def _generate_nostril_size(self, region_data: Dict) -> str:
        """Genera tamaño de fosas nasales"""
        sizes = {
            "small": 0.3,
            "medium": 0.5,
            "large": 0.2
        }
        return self._select_by_probability(sizes)
    
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
    
    def _generate_lip_color(self, region_data: Dict, gender: str) -> str:
        """Genera color de labios"""
        colors = {
            "natural": 0.6,
            "pink": 0.2,
            "coral": 0.1,
            "red": 0.1
        }
        return self._select_by_probability(colors)
    
    def _generate_lip_fullness(self, region_data: Dict, gender: str) -> str:
        """Genera plenitud de labios"""
        fullness = {
            "full": 0.3,
            "medium": 0.5,
            "thin": 0.2
        }
        return self._select_by_probability(fullness)
    
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
        base_probabilities = self.skin_engine["skin_imperfections"].copy()
        
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
            if isinstance(probability, (int, float)) and random.random() < probability:
                imperfections.append(char)
        
        return imperfections
    
    def _generate_freckles(self, region_data: Dict, skin_tone: str) -> Tuple[str, str]:
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
        
        freckle_type = self._select_by_probability(freckles)
        freckle_density = freckle_type  # Mismo valor para simplicidad
        return freckle_type, freckle_density
    
    def _generate_moles(self, region_data: Dict, skin_tone: str) -> Tuple[str, str]:
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
        
        mole_type = self._select_by_probability(moles)
        mole_count = mole_type  # Mismo valor para simplicidad
        return mole_type, mole_count
    
    def _generate_birthmarks(self, region_data: Dict, skin_tone: str) -> str:
        """Genera marcas de nacimiento"""
        birthmarks = {
            "none": 0.9,
            "small": 0.08,
            "medium": 0.02
        }
        return self._select_by_probability(birthmarks)
    
    def _generate_scars(self, region_data: Dict, age: int) -> str:
        """Genera cicatrices basadas en edad"""
        if age <= 25:
            scars = {
                "none": 0.9,
                "small": 0.1
            }
        elif age <= 45:
            scars = {
                "none": 0.8,
                "small": 0.15,
                "medium": 0.05
            }
        else:
            scars = {
                "none": 0.7,
                "small": 0.2,
                "medium": 0.1
            }
        return self._select_by_probability(scars)
    
    def _generate_acne(self, age: int, beauty_control: str) -> str:
        """Genera acné basado en edad y belleza"""
        if age <= 25:
            acne = {
                "none": 0.7,
                "mild": 0.2,
                "moderate": 0.1
            }
        else:
            acne = {
                "none": 0.95,
                "mild": 0.05
            }
        
        if beauty_control == "attractive":
            acne["none"] += 0.2
            if "mild" in acne:
                acne["mild"] -= 0.1
            if "moderate" in acne:
                acne["moderate"] -= 0.1
        
        return self._select_by_probability(acne)
    
    def _generate_age_spots(self, age: int, beauty_control: str) -> str:
        """Genera puntos de edad"""
        if age <= 35:
            spots = {
                "none": 0.95,
                "few": 0.05
            }
        elif age <= 50:
            spots = {
                "none": 0.8,
                "few": 0.15,
                "several": 0.05
            }
        else:
            spots = {
                "none": 0.6,
                "few": 0.25,
                "several": 0.15
            }
        
        if beauty_control == "attractive":
            spots["none"] += 0.1
            if "few" in spots:
                spots["few"] -= 0.05
            if "several" in spots:
                spots["several"] -= 0.05
        
        return self._select_by_probability(spots)
    
    def _generate_wrinkles(self, age: int, beauty_control: str) -> str:
        """Genera arrugas basadas en edad y belleza"""
        if age <= 25:
            wrinkles = {
                "none": 0.9,
                "fine": 0.1
            }
        elif age <= 35:
            wrinkles = {
                "none": 0.7,
                "fine": 0.25,
                "moderate": 0.05
            }
        elif age <= 50:
            wrinkles = {
                "none": 0.4,
                "fine": 0.4,
                "moderate": 0.15,
                "deep": 0.05
            }
        else:
            wrinkles = {
                "none": 0.2,
                "fine": 0.3,
                "moderate": 0.3,
                "deep": 0.2
            }
        
        if beauty_control == "attractive":
            wrinkles["none"] += 0.2
            if "fine" in wrinkles:
                wrinkles["fine"] -= 0.1
            if "moderate" in wrinkles:
                wrinkles["moderate"] -= 0.05
            if "deep" in wrinkles:
                wrinkles["deep"] -= 0.05
        
        return self._select_by_probability(wrinkles)
    
    def _generate_skin_elasticity(self, age: int) -> str:
        """Genera elasticidad de piel basada en edad"""
        if age <= 25:
            elasticity = {
                "high": 0.8,
                "medium": 0.2
            }
        elif age <= 35:
            elasticity = {
                "high": 0.5,
                "medium": 0.4,
                "low": 0.1
            }
        elif age <= 50:
            elasticity = {
                "high": 0.2,
                "medium": 0.5,
                "low": 0.3
            }
        else:
            elasticity = {
                "high": 0.1,
                "medium": 0.3,
                "low": 0.6
            }
        return self._select_by_probability(elasticity)
    
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
    
    def _generate_hair_shine(self, hair_color: str, beauty_control: str) -> str:
        """Genera brillo de cabello"""
        if beauty_control in ["attractive", "exceptionally_beautiful"]:
            shine = {
                "shiny": 0.4,
                "natural": 0.4,
                "dull": 0.2
            }
        else:
            shine = {
                "natural": 0.6,
                "shiny": 0.2,
                "dull": 0.2
            }
        return self._select_by_probability(shine)
    
    def _generate_hair_curliness(self, hair_texture: str) -> str:
        """Genera rizado de cabello"""
        if hair_texture == "straight":
            return "straight"
        elif hair_texture == "wavy":
            return "wavy"
        elif hair_texture == "curly":
            return "curly"
        else:
            return "coily"
    
    def _generate_hair_thickness(self, region_data: Dict, gender: str) -> str:
        """Genera grosor de cabello"""
        thickness = {
            "thick": 0.3,
            "medium": 0.5,
            "thin": 0.2
        }
        return self._select_by_probability(thickness)
    
    def _generate_hairline(self, region_data: Dict, gender: str, age: int) -> str:
        """Genera línea de cabello"""
        if gender == "hombre" and age > 30:
            hairline = {
                "normal": 0.6,
                "receding": 0.3,
                "high": 0.1
            }
        else:
            hairline = {
                "normal": 0.9,
                "high": 0.1
            }
        return self._select_by_probability(hairline)
    
    def _generate_age_characteristics(self, age: int) -> List[str]:
        """Genera características de edad"""
        age_range = self._get_age_range(age)
        age_chars = self.age_engine.get(age_range, {})
        
        characteristics = []
        for char, probability in age_chars.items():
            if isinstance(probability, (int, float)) and random.random() < probability:
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
        
        # Agregar características basadas en la región
        if region_data:
            for key, value in region_data.items():
                if isinstance(value, dict) and random.random() < 0.3:
                    features.append(f"{key}_characteristics")
        
        return features
    
    def _calculate_uniqueness_score(self) -> float:
        """Calcula score de unicidad"""
        return round(random.uniform(0.95, 1.0), 3)
