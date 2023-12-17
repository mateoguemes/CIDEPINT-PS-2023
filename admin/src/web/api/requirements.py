from flask import Blueprint, request
from src.models.requirement import Requirement
from flask import jsonify
from src.web.schemas.requirement import requirements_schema, requirement_schema, status_quantities_schema, status_quantity_schema
from sqlalchemy import func

api_requirements_bp = Blueprint('requirements_api', __name__, url_prefix='/api/requirements')

@api_requirements_bp.get('/groupedByState')
def groupedByState()->dict:
    """
    Returns a json with the quantities of requirements per state
    """
    states_quant = Requirement.grouped_and_counted_by_state()

    return jsonify({'data': states_quant}), 200

@api_requirements_bp.get('/servicesQuantities')
def servicesQuantities()->dict:
    """
    Returns a json with the quantities of requirements per service
    """
    req_quant = Requirement.grouped_and_counted_by_service()

    return jsonify({'data': req_quant}), 200

@api_requirements_bp.get('/top10')
def top10()->dict:
    """
    Returns a json with the top 10 institutions with best resolution time
    """
    top10 = Requirement.top10()

    return jsonify({'data': top10}), 200