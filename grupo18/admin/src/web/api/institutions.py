from flask import Blueprint, request
from flask import session
from src.web.helpers.auth import is_authorized
from src.models.institution import Institution
from flask import jsonify
from src.web.schemas.institution import institutions_schema, institution_schema
from src.web.schemas.service import services_schema
from src.models.service import Service

api_institutions_bp = Blueprint('institutions_api', __name__, url_prefix='/api/institutions')

@api_institutions_bp.get('/')
def index()->dict:
    """
    Returns a dict with all the institutions
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    institutions = Institution.query.paginate(page=page, per_page=per_page, error_out=False)

    if not institutions.items:
        return jsonify({'error': 'No se encontraron instituciones'}), 404

    data = {
        'data': institutions_schema.dump(institutions.items),
        'page': institutions.page,
        'per_page': institutions.per_page,
        'total': institutions.total
    }
    return data, 200

@api_institutions_bp.get('/<int:institution_id>/services')
def get_services(institution_id: int)-> list:
    """
    Returns a list of all services given an institution
    """
    institution = Institution.query.get(institution_id)

    if (not institution): 
        return jsonify({'error': 'parametros invalidos'}), 400

    services = institution.get_services()

    data = Service.api_get_services_for_form(services)
    return data,200
