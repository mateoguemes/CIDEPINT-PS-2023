from flask import Flask, render_template, session, make_response, request
from os import environ
from src.models import database
from src.web.config import config
from src.web import routes
from src.web.helpers.auth import is_authenticated, check_authentication
from src.web.helpers.auth import get_institutions_of_user
from src.models.institution import Institution
from src.models.user import User
from src.models.configs import Config
from src.models.seeds import all_seeds
from src.web import error
from src.web import oauth
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app(env="development", static_folder="../../static"):
    """This is where the app is created"""

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)

    oauth.init_oauth(app)
    routes.register_routes(app)
    
    @app.context_processor
    def utility_processor():
        return dict(institutions_of_user=get_institutions_of_user,
                    actual_institution=Institution.get_name(session.get('institution_id')),
                    current_user=session.get('user_id'))

    @app.before_request
    def check_maintenance():
        maintenance_config = Config.get_config()
        maintenance_mode = maintenance_config.get('maintenance_mode')
        is_super_admin = User.is_super_admin(session.get('user_id'))

        # Permitir acceso a la vista de login durante el mantenimiento
        if request.endpoint == 'login':
            return

        if maintenance_mode and not check_authentication() and not is_super_admin:
            # Eliminar claves específicas de la sesión
            session.pop('user_id', None)
            session.pop('institution_id', None)
            # Redirigir directamente a la página de mantenimiento
            return render_template("maintenance.html", maintenance_message=maintenance_config.get('maintenance_message'))


    @app.route("/")
    @is_authenticated()
    def home():
        user = User.query.get(session.get('user_id'))
        permissions = User.get_permissions(session.get('user_id'), session.get('institution_id'))
        institution_id = session.get('institution_id')
        return render_template("home.html", user=user, permissions=permissions, institution_id=institution_id)

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        database.reset_db()
        all_seeds.run()

    @app.errorhandler(404)
    def not_found(e):
        return error.not_found_error(e)

    @app.errorhandler(401)
    def not_authorized(e):
        return error.not_authorized_error(e)

    @app.route('/<path:path>', methods=['OPTIONS'])
    def options_handler(path):
        return 'OK', 200

    
    cors = CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173","http://localhost:5000","https://accounts.google.com",
                        "https://localhost:5173","https://localhost:5000",
                        "https://admin-grupo18.proyecto2023.linti.unlp.edu.ar",
                        "https://grupo18.proyecto2023.linti.unlp.edu.ar"],
            "supports_credentials": True
        }
    })

    jwt = JWTManager(app)

    return app
