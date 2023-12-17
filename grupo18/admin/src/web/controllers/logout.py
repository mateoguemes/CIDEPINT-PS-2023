from flask import Blueprint, redirect, url_for, flash, session
from src.web.helpers.auth import is_authenticated
import requests

logout_bp = Blueprint('logout', __name__)

@logout_bp.route("/logout", methods=['GET','POST'])
@is_authenticated()
def logout()->None:
    """
    Logs out an user and redirects to the login page
    """
    if 'user_id' in session:
        session.pop('user_id', None)
        flash('Has cerrado sesión con éxito', 'success')
    else:
        flash('No hay sesión activa para cerrar', 'info')

    return redirect(url_for('login.login'))
    