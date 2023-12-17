from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from src.models.user import User
from src.models.user_institution import User_Institution
from src.models.institution import Institution
from src.web.helpers.auth import has_session
from src.web.oauth import oauth as Oauth

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login()->None:
    """
    Authenticates an user 
    and renders the home if it was successful.
    """
    if (has_session()):
        return redirect(url_for('home'))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first() 
        if user and user.confirmed and user.active:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                if User.is_super_admin(user.id):
                    session['institution_id'] = Institution.query.filter(Institution.name != "CIDEPINT").first().id
                else:
                    session['institution_id'] = User_Institution.query.filter_by(user_id = user.id).first().institution_id
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('home'))
            else:
                flash('Credenciales incorrectas. Intenta de nuevo.', 'error')
        elif user and not user.active:
            flash('Usuario inactivo', 'error')
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.', 'error')
    return render_template("login.html")

@login_bp.route("/change_institution/<int:institution_id>", methods=["POST"])
def change_institution(institution_id):
    session['institution_id'] = institution_id
    return redirect(url_for('home')) # no redirige al home ya que se ejecuta el ajax que recarga la pagina

@login_bp.route("/login/google")
def login_google()->None:
    """
    Authenticates an user with Google
    """
    redirect_uri = url_for('login.auth', _external=True)
    return Oauth.google.authorize_redirect(redirect_uri, prompt='select_account')

@login_bp.route('/login/google/callback')
def auth()->None:
    """
    Authenticates an user using google 
    and renders the home if it was successful.
    """
    token = Oauth.google.authorize_access_token()
    # Almacena la información del usuario en la sesión
    email = token['userinfo']['email']
    user = User.query.filter_by(email=email).first() 
    if user and user.active:
        session['user_id'] = user.id
        if User.is_super_admin(user.id):
            session['institution_id'] = Institution.query.filter(Institution.name != "CIDEPINT").first().id
        else:
            session['institution_id'] = User_Institution.query.filter_by(user_id = user.id).first().institution_id
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('home'))
    flash_message = 'Usuario inactivo' if user else f'El correo "{email}" no se encuentra registrado. Por favor regístrate para continuar.'
    flash(flash_message, 'error')
    return render_template("login.html")
