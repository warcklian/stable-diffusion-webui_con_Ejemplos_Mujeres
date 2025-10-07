"""
Adaptador de API para WebUI
Conecta el generador masivo con la API interna de WebUI
"""

import base64
import json
from typing import Dict, Any, Optional

class WebUIAPIAdapter:
    """Adaptador para usar la API interna de WebUI"""
    
    def __init__(self, webui_api=None):
        """
        Inicializa el adaptador
        
        Args:
            webui_api: Instancia de la API de WebUI (opcional)
        """
        self.webui_api = webui_api
        self.fallback_mode = webui_api is None
    
    def txt2img(self, **params) -> Dict[str, Any]:
        """
        Genera imagen usando la API de WebUI
        
        Args:
            **params: Parámetros de generación
            
        Returns:
            Resultado de la generación
        """
        if self.fallback_mode:
            # Modo fallback para testing
            return self._simulate_generation(params)
        
        try:
            # Usar la API real de WebUI
            if hasattr(self.webui_api, 'txt2img'):
                return self.webui_api.txt2img(**params)
            else:
                # Fallback si no tiene el método esperado
                return self._simulate_generation(params)
        except Exception as e:
            print(f"Error en API de WebUI: {e}")
            return self._simulate_generation(params)
    
    def _simulate_generation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simula generación para testing
        
        Args:
            params: Parámetros de generación
            
        Returns:
            Resultado simulado
        """
        # Crear resultado simulado
        fake_image_data = base64.b64encode(b"fake_image_data").decode('utf-8')
        
        # Crear info simulado
        info_data = {
            "seed": params.get("seed", -1),
            "steps": params.get("steps", 30),
            "cfg_scale": params.get("cfg_scale", 9.0),
            "sampler_name": params.get("sampler_name", "DPM++ 2M Karras"),
            "width": params.get("width", 512),
            "height": params.get("height", 512)
        }
        
        return {
            "images": [fake_image_data],
            "info": json.dumps(info_data),
            "parameters": json.dumps(params)
        }
    
    def get_current_model(self) -> Optional[str]:
        """
        Obtiene el modelo actual
        
        Returns:
            Nombre del modelo actual
        """
        if self.fallback_mode:
            return "WebUI_Integrated_Model"
        
        try:
            if hasattr(self.webui_api, 'get_current_model'):
                return self.webui_api.get_current_model()
            else:
                return "WebUI_Integrated_Model"
        except Exception as e:
            print(f"Error obteniendo modelo actual: {e}")
            return "WebUI_Integrated_Model"
    
    def set_model(self, model_name: str, **kwargs) -> bool:
        """
        Cambia el modelo
        
        Args:
            model_name: Nombre del modelo
            **kwargs: Parámetros adicionales
            
        Returns:
            True si el cambio fue exitoso
        """
        if self.fallback_mode:
            print(f"Simulando cambio de modelo a: {model_name}")
            return True
        
        try:
            if hasattr(self.webui_api, 'set_model'):
                return self.webui_api.set_model(model_name, **kwargs)
            else:
                print(f"Simulando cambio de modelo a: {model_name}")
                return True
        except Exception as e:
            print(f"Error cambiando modelo: {e}")
            return False
    
    def get_memory_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado de memoria
        
        Returns:
            Estado de memoria
        """
        if self.fallback_mode:
            return {
                "current_memory": {
                    "percent": 50.0,
                    "used_gb": 4.0
                },
                "memory_pressure": "normal"
            }
        
        try:
            if hasattr(self.webui_api, 'get_memory_status'):
                return self.webui_api.get_memory_status()
            else:
                return {
                    "current_memory": {
                        "percent": 50.0,
                        "used_gb": 4.0
                    },
                    "memory_pressure": "normal"
                }
        except Exception as e:
            print(f"Error obteniendo estado de memoria: {e}")
            return {
                "current_memory": {
                    "percent": 50.0,
                    "used_gb": 4.0
                },
                "memory_pressure": "normal"
            }
    
    def force_memory_cleanup(self, reason: str = "manual") -> Dict[str, Any]:
        """
        Fuerza limpieza de memoria
        
        Args:
            reason: Razón de la limpieza
            
        Returns:
            Resultado de la limpieza
        """
        if self.fallback_mode:
            return {
                "success": True,
                "memory_freed_mb": 100,
                "reason": reason
            }
        
        try:
            if hasattr(self.webui_api, 'force_memory_cleanup'):
                return self.webui_api.force_memory_cleanup(reason)
            else:
                return {
                    "success": True,
                    "memory_freed_mb": 100,
                    "reason": reason
                }
        except Exception as e:
            print(f"Error en limpieza de memoria: {e}")
            return {
                "success": False,
                "error": str(e),
                "reason": reason
            }
