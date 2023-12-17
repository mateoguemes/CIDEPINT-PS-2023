from src.models.service import Service, ServiceType
from src.models.keyword import Keyword
import re

def validate_entry_data(name: str, description: str,
                         data_type: str, enable: bool)->None:
    """Validates the correctness of then data"""
    if not name or len(name) > 100:
        raise Exception("El nombre del servicio es obligatorio y no puede contener más de 100 caracteres")
    
    if not description or len(description) > 255:
        raise Exception("La descripción es obligatoria y no puede tener más de 255 caracteres")
    
    if not (data_type in ServiceType): #este método develve None si la palabra no es válida
        valid_values = ', '.join([f'"{member}"' for member in ServiceType.get_all_values()])
        raise Exception(f"El tipo de servicio es obligatorio y las opciones son: {valid_values}")

    if not enable:
        raise Exception("El estado del servicio es obligatorio")
    

def validate_keywords(*args) -> None:
    """Validates de length and the characters of the keywords"""
    for word in args:
        if len(word) > Keyword.max_length_name():
            raise Exception("Introdujiste palabras muy largas, recuerda que debes separarlas por espacios")
        # Si no cumple la expresión regular esperada
        if not re.match(r'^[\w\s]+$', word, re.UNICODE):
            raise Exception("Las palabras claves deben separarse por espacios en blanco. Solo se admiten letras y espacios")
