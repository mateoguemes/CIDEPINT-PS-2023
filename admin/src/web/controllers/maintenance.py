# En tu archivo de rutas, por ejemplo, maintenance.py
from flask import Blueprint, render_template
from src.models.configs import Config
from src.web.helpers.auth import is_authorized

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@maintenance_bp.route('/')
@is_authorized("configuration_update")
def maintenance_page()->None:
    """
    Renders the maintenance page
    """
    maintenance_message = Config.get_config().get('maintenance_message')
    return render_template('maintenance.html', maintenance_message=maintenance_message)
