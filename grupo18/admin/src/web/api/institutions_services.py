from flask import Blueprint, jsonify
from src.models.institution_service import Institution_Service
from src.models.institution import Institution

institution_for_service_bp = Blueprint('institution_for_service', __name__)

@institution_for_service_bp.route('/api/institution-for-service/<int:service_id>', methods=['GET'])
def get_institution_for_service(service_id: int)->dict:
    """
    Returns the information of a institution given a service id.
    """
    try:
        # Buscar la relación en la tabla intermedia
        institution_service = Institution_Service.query.filter_by(service_id=service_id).first()

        if not institution_service:
            return jsonify({'error': 'No se encontró la relación servicio-institución'}), 404

        # Obtener información de la institución
        institution = Institution.query.get(institution_service.institution_id)

        if not institution:
            return jsonify({'error': 'No se encontró la institución correspondiente'}), 404

        # Devolver la información de la institución
        return jsonify({
            'name': institution.name,
            'information': institution.information,
            'address': institution.address,
            'location': institution.location,
            'web': institution.website,
            'days_and_opening_hours': institution.opening_hours,
            'email': institution.contact,
            'enabled': institution.enabled
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

