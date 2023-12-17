from flask import Blueprint, redirect, url_for, flash, render_template, request 
from src.models.user import User, Token
from src.models.database import db

confirm_registration_bp = Blueprint('confirm_registration', __name__)

@confirm_registration_bp.route('/confirm/<token>', methods=['GET' , 'POST'])
def confirm_registration(token: int)-> None:
    """
    Confirms the registration of a user 
    and renders the registration form.
    """
    # Verifica si el token de confirmación es válido
    token_obj = Token.query.filter_by(token=token, token_type='confirmation').first()
    
    if token_obj:
        if request.method == "POST":
            usern = request.form['username']
            password = request.form['password']
            # Verifica si el nombre de usuario ya existe en la base de datos
            existing_user = User.query.filter_by(username=usern).first()
            if existing_user:
                flash('El nombre de usuario ya está en uso', 'error')
                return render_template('register_user_pass.html')
            else:
                User.confirmUser(token_obj, usern, password)
                flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login.login'))  # Redirige a la página de inicio de sesión 
        else:
            flash('¡Registro confirmado! Ahora puedes establecer tu nombre de usuario y contraseña.', 'success')
            return render_template('register_user_pass.html')

    else:
        flash('Token de confirmación inválido.', 'error')
        return redirect(url_for('login.login'))
