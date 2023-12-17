from src.web.controllers.login import login_bp
from src.web.controllers.logout import logout_bp
from src.web.controllers.service_management import solicitudes_bp
from src.web.controllers.service_detail import service_detail_bp
from src.web.controllers.register import register_bp 
from src.web.controllers.confirm_registration import confirm_registration_bp
from src.web.controllers.users_module import users_bp
from src.web.controllers.users_of_institution import users_of_institution_bp
from src.web.controllers.services import services_bp
from src.web.controllers.institutions_module import institutions_bp
from src.web.api.users import api_users_bp
from src.web.api.institutions import api_institutions_bp
from src.web.api.auth import api_auth_bp
from src.web.api.services import api_services_bp
from src.web.api.services_types import api_services_types_bp
from src.web.api.institutions_services import institution_for_service_bp
from src.web.api.requirements import api_requirements_bp
from src.web.controllers.configs_module import config_module_bp
from src.web.controllers.maintenance import maintenance_bp
from src.web.api.config import api_config_bp

def register_routes(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(users_of_institution_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(confirm_registration_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(service_detail_bp)
    app.register_blueprint(institutions_bp)
    app.register_blueprint(api_users_bp)
    app.register_blueprint(api_institutions_bp)
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(api_services_bp)
    app.register_blueprint(api_services_types_bp)
    app.register_blueprint(institution_for_service_bp)
    app.register_blueprint(config_module_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(api_requirements_bp)
    app.register_blueprint(api_config_bp)