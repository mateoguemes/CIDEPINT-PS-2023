from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from src.models.user import User, Token
from src.models.database import db
from flask_mail import Mail, Message

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers an user and renders the login page.
    """
    register_from_portal = request.args.get('portal') == "True" #si portal es verdadero, redireccionará a la app pública
    google = request.args.get('google') == "True" #parámetro opcional que determina si es o no con google, recibirá un valor booleano
    if request.method == 'POST':
        login_url= url_for('login.login') if not register_from_portal else ("http://localhost:5173/login" if "5000" in request.base_url else "https://grupo18.proyecto2023.linti.unlp.edu.ar/login")
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        # Verifica si el correo electrónico ya está registrado
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash_message='Usted ya se encuentra registrado.'
        else:
            if(not google):
                flash_message='Se ha enviado un correo electrónico con instrucciones para confirmar su registro.'
                userToken = User.addUser(name, last_name, email)
                # Envía un correo de confirmación
                send_mail(userToken)
            else:
                flash_message='Su usuario fue registrado exitosamente.'
                new_user = User(name=name, lastname=last_name, email=email, confirmed=False, password = None)
                db.session.add(new_user)
                db.session.commit()
        flash(flash_message, 'success')
        return redirect(login_url)  # Redirige a la página de inicio de sesión correspondiente

    return render_template('register.html',google=google,portal=register_from_portal)

def send_mail(userToken: int)->None:
    """
    Send the confirmation email to the user.
    """
    app = current_app._get_current_object()
    tok = Token.query.get(userToken)
    user = User.query.get(tok.user_id)
    mail = Mail(app)

    confirm_link = url_for('confirm_registration.confirm_registration', token=tok.token, _external=True)

    subject = 'Confirmación de Registro'
    sender = app.config['MAIL_DEFAULT_SENDER']
    recipients = [user.email]
    message = f'¡Felicidades! Tu registro ha sido exitoso. Para confirmar tu registro, haz clic en el siguiente enlace: {confirm_link}'

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = message

    mail.send(msg)