from flask_cors import CORS, cross_origin
from flask import Blueprint, session, request, jsonify, make_response
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies
from src.models.user import User
from werkzeug.security import check_password_hash
from google.oauth2 import id_token
from google.auth.transport import requests
from os import environ
import requests

api_auth_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')


# Añadir manejador para solicitudes OPTIONS
@api_auth_bp.route('/login_jwt_google', methods=['OPTIONS'])
@cross_origin()
def handle_preflight():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")  # Reemplaza con el origen correcto de tu aplicación frontend
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response


@api_auth_bp.route('/login_jwt_google', methods=['POST'])
@cross_origin()
def login_jwt_google():
    """
    Provee lógica de manejo para el inicio de sesión con Google.
    """
    try:
        if 'token' not in request.json:
            return jsonify({"error": "Token de Google no proporcionado"}), 400

        google_token = request.json['token']
        CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')  # Reemplaza con tu propio ID de cliente

        # Realizar una solicitud para verificar el token de acceso usando el módulo 'requests'
        response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_token}')
        token_info = response.json()

        # Verificar el resultado de la solicitud
        if 'error_description' in token_info:
            return jsonify({"error": "Invalid Google token"}), 401

        response = jsonify({"message": "Successfully logged in via Google."})
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        return response, 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500



@api_auth_bp.route('/verificar_registro', methods=['POST'])
@cross_origin()
def verificar_registro():
    try:
        # Verificar que el correo electrónico esté presente en la solicitud
        if 'email' not in request.json:
            return jsonify({"error": "Correo electrónico no proporcionado"}), 400
        email = request.json['email']
        # Verificar si el usuario ya está registrado en la base de datos
        user = User.query.filter_by(email=email).first()
        if user is not None:
            token = create_access_token(identity=user.id)
            response = jsonify({"token": token,"message": "Usuario registrado en la base de datos"})
            set_access_cookies(response, token)
            return response, 200 
        else:
            return jsonify({"error": "Usuario no registrado en la base de datos"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@api_auth_bp.post('/login_jwt')
@cross_origin()
def login_jwt():
    """
    Provee un login con la contraseña de la BD (NO sirve para entrar por Google)
    """
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    print(user)
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        data = {"token": access_token}
        response = jsonify(data)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify(message="Credenciales incorrectas. Intenta de nuevo."), 400


@api_auth_bp.route('/logout_jwt', methods=['GET', 'OPTIONS'])
@jwt_required()
def logout_jwt():
    try:    
        response = jsonify()
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        print(e)


#LOS CONTROLADORES DE LA API DEBERAN EXIGIR QUE HAYA UN TOKEN VALIDO, ESO QUIERE DECIR
#QUE USAN el decorador ya provisto "@jwt_required( )"