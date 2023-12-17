from flask import Blueprint
from src.models.configs import Config
from flask import jsonify

api_config_bp = Blueprint('config_api', __name__, url_prefix='/api/config')

@api_config_bp.get('/contactMail')
def contactMail()->dict:
    """
    Returns a json with the registered contact mail
    """

    config = Config.get_config()

    return jsonify({'mail': config['contact_info']}), 200