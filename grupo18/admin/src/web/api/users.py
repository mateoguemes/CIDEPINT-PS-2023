from src.models.user import User
from src.models.requirement import Requirement
from flask import Blueprint
from flask import session
from flask import jsonify
from flask import request as req
from src.web.helpers.api_validations import valid_data, can_see_data
from src.web.schemas.user import user_schema
from src.web.schemas.requirement import requirements_schema, requirement_schema
from src.models.note import Note
from src.web.schemas.note import notes_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.configs import Config

api_users_bp = Blueprint('users_api', __name__, url_prefix='/api/me')
    
@api_users_bp.get('/profile')
@jwt_required()
def profile()->dict:
    """
    Returns a the information for the user profile
    """
    if (not get_jwt_identity()): 
        return jsonify({'error': 'parametros invalidos'}), 400
    
    user = User.query.get(session.get('user_id'))
    data = user_schema.dump(user) 
    return data, 200

@api_users_bp.get('/requests')
@jwt_required()
def requests()->dict:
    """
    Returns a list of all requirements given a user
    """
    sort_criteria = req.args.get('sort') 
    order = req.args.get('order') if req.args.get('order') else 'desc'
    page = req.args.get('page', 1, type=int)
    user_id = get_jwt_identity()
    try:
        query = Requirement.get_requirements_of_user(user_id, order, sort_criteria, page) 
    except Exception as e:
        print(e)
        return jsonify({'error': 'parametros invalidos'}), 400
    
    data = {}
    if (query):
        result = requirements_schema.dump(query)
        print(result)
        data = {
            "data": result,
            "page":page,
            "per_page": Config.get_config().get('per_page'),
            "total_pages": Requirement.get_total_pages(user_id)
            }
    return jsonify(data), 200
    
@api_users_bp.post('/requests') 
@jwt_required() 
def create_request():
    """
    Stores the received request in the database 
    """
    try:
        data = req.get_json()
        data['user_id'] = get_jwt_identity()
        valid_data(data)
        Requirement.add_requirement(data)
        return jsonify({'message': 'Solicitud recibida correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error al procesar la solicitud'}), 400

@api_users_bp.get('/requests/<request_id>')
@jwt_required()
def get_request(request_id: int)->dict:
    """
    Returns a requirement given an id
    """
    if (not can_see_data(get_jwt_identity(), request_id)):
        return jsonify({'error': 'No estas autorizado'}), 401
    
    query = Requirement.get_requirement(request_id)
    if (query):
        result = requirement_schema.dump(query)
        data = {
            "data": result,
            "page":1,
            "per_page": 10,
            }	
        return jsonify(data), 200
    else:
        return jsonify({'error': 'parametros invalidos'}), 400
    
@api_users_bp.get('/requests/<request_id>/notes')
@jwt_required()
def get_notes(request_id: int)->dict:
    """
    Returns a list of the notes of a requirement.
    """
    if (not can_see_data(get_jwt_identity(), request_id)):
        return jsonify({'error': 'No estas autorizado'}), 401
    
    query = Note.query.filter_by(requirement_id=request_id).all()
    result = notes_schema.dump(query)
    return jsonify(result), 200

@api_users_bp.post('/requests/addNote') 
@jwt_required()
def create_note()->dict:
    """
    Creates a note for a request given a form.
    """
    try:
        data = req.get_json()
        if (not can_see_data(get_jwt_identity(), data['requirement_id'])):
            return jsonify({'error': 'No estas autorizado'}), 401
        Note.add_note(data)
        return jsonify({'message': 'Solicitud recibida correctamente'}), 201
    except Exception as e:
        return jsonify({'error': 'error'}), 400
    


    

