from flask import abort, session, flash, render_template, request
from src.models.user import User
from src.models.configs import Config
from src.models.institution import Institution
from functools import wraps

def get_institutions_of_user()->list:
    """
    Returns the institutions of the logued user.
    """
    if ('institution_id' in session) != None:
        return Institution.get_institutions_of_user(session.get('user_id'))
    else:
        return []

def has_session()->bool:
    """
    Returns if theres a session.
    """
    return session.get('user_id') is not None

def check_authentication()->bool:
    """
    Gives authorization to use the app if its under maintenance.
    """
    maintenance_config = Config.get_config()
    maintenance_mode = maintenance_config.get('maintenance_mode')

    # Permitir acceso a la vista de login durante el mantenimiento
    if request.endpoint == 'login':
        return True

    if maintenance_mode:
        # Si no hay sesión, habilitar la vista de login durante el mantenimiento
        if not has_session():
            return True

        user_id = session.get('user_id')
        # Permitir acceso a superadmins durante el mantenimiento
        if User.is_super_admin(user_id):
            return True

        # Si llegamos aquí, la sesión existe pero no es un superadmin, denegar el acceso
        flash('Acceso denegado, solo superadmins pueden acceder durante el mantenimiento', 'error')
        return False

    # Si no estamos en mantenimiento, verificar la autenticación normalmente
    if not has_session():
        return False

    user_id = session.get('user_id')
    return True

def has_permission(required_permission: str)->bool:
    """
    Returns if a user has a permission.
    """
    if User.is_super_admin(session.get('user_id')):
        return True
    user_permission_list = User.get_permissions(session.get('user_id'), session.get('institution_id'))
    has_permission = True if required_permission in user_permission_list else False
    return has_permission

def is_authorized(required_permission: str)->bool:
    """
    Returns if a user is authorized.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not has_session():
                flash('Acceso denegado, debes estar logueado para continuar', 'error')
                return render_template("login.html")
            if not has_permission(required_permission):
                abort(401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def is_authenticated()->bool:
    """
    Returns if a user is authenticated.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not has_session():
                flash('Acceso denegado, debes estar logueado para continuar', 'error')
                return render_template("login.html")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def is_super_admin(f):
    """
    Returns if a user is super admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not has_session():
            flash('Acceso denegado, debes estar logueado para continuar', 'error')
            return render_template("login.html")
        if not User.is_super_admin(session.get('user_id')):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
