from flask import Blueprint
from flask import jsonify
from src.models.service import ServiceType

api_services_types_bp = Blueprint('services_type_api', __name__, url_prefix='/api/services-types')
 
@api_services_types_bp.get('/')
def get_service()->dict:
    """
    Returns a dictionary with all the services types
    """
    types = ServiceType.get_all_values()
    if (types):
        return jsonify({'data': types}), 200
    else:
        return jsonify({'error': 'Parámetros inválidos'}), 400