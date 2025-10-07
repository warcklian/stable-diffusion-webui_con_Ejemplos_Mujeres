"""
Módulo de Datos Étnicos

Este módulo contiene toda la información sobre poblaciones específicas,
incluyendo características físicas, variaciones regionales y datos
demográficos para la generación de diversidad étnica.
"""

from .ethnic_data import EthnicData, get_ethnic_variations
from .countries.cuba import CubaData
# from .countries.venezuela import VenezuelaData  # TODO: Implementar
# from .countries.haiti import HaitiData          # TODO: Implementar
# from .countries.republica_dominicana import RepublicaDominicanaData  # TODO: Implementar

__all__ = [
    "EthnicData",
    "get_ethnic_variations",
    "CubaData"
    # "VenezuelaData",  # TODO: Implementar
    # "HaitiData",      # TODO: Implementar
    # "RepublicaDominicanaData"  # TODO: Implementar
]
