from src.models.user import User
from src.models.institution import Institution
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from src.web.helpers.auth import is_authorized

def valid_institution_name(form: dict) -> bool:
    name = form.get('name')
    
    if not name:
        return True  # Considera la validación exitosa si 'name' no está presente

    institution_with_name = Institution.name_exists(name)
    
    if institution_with_name:
        # Si el nombre está en uso, verifica si pertenece a la institución actual
        name_is_mine = institution_with_name.id == int(form.get('id', 0))
        return name_is_mine  # Devuelve True si el nombre pertenece a la institución actual

    return True  # Devuelve True si el nombre no está en uso

