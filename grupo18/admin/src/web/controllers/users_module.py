from src.models.user import User
from flask import render_template
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from src.web.helpers.auth import is_authorized
from src.web.helpers.users_validations import valid_email, validate_entry_data
from src.models.configs import Config

from src.models.institution import Institution

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@is_authorized('user_index')
def index() -> None:
    """
    Renders the users index page
    """
    page = request.args.get('page', 1, type=int)
    state = request.args.get('state', 'Todos')  # Asegúrate de tener un valor predeterminado
    users_pagination = User.query.paginate(page=page, per_page=Config.get_config().get('per_page'), error_out=False)

    return render_template('user_index.html', users=users_pagination.items,
                           permissions=User.get_permissions(session['user_id'], session['institution_id']),
                           users_pagination=users_pagination, state=state)


    
@users_bp.route('/users/showProfile/<int:user_id>', methods=['GET', 'POST'])
@is_authorized('user_profile')
def show_profile(user_id: int)->None:
    """
    Returns the profile of a given user
    """
    user = User.query.get(user_id)
    return render_template('user_profile.html', user=user)


@users_bp.route('/users', methods=['POST'])
@is_authorized('user_search')
def show_by_email()->None: 
    """
    Renders a user that match the search criteria
    """
    result = request.form.get('busqueda', None)
    users_pagination = None
    if result:
        user = User.query.filter_by(email = result).all()
    else:
        user = None
    return render_template('user_index.html', users=user,
                           permissions=User.get_permissions(session['user_id'], session['institution_id']), users_pagination=users_pagination)

@users_bp.route('/users/getUsersByState', methods=['POST', 'GET'])
@is_authorized('user_search')
def show_by_state() -> None:
    state = request.args.get('state', 'Todos')
    print(f"State: {state}")  # Agrega este mensaje de depuración
    users_query = User.user_get_by_state(state)

    page = request.args.get('page', 1, type=int)
    print(f"Page: {page}")  # Agrega este mensaje de depuración
    per_page = Config.get_config().get('per_page')

    users_pagination = users_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('user_index.html', users=users_pagination.items,
                           permissions=User.get_permissions(session['user_id'], session['institution_id']),
                           users_pagination=users_pagination, state=state)

@users_bp.route('/users/updateUser/<int:user_id>', methods=['GET'])
@is_authorized('user_update')
def show_update_form(user_id: int)->None: 
    """
    Shows the form to update a user
    """
    user = User.query.get(user_id)
    return render_template('user_update_form.html', user=user)

@users_bp.route('/users/updateUser', methods=['POST'])
@is_authorized('user_update') 
def update()->None:
    """
    Updates a user given the data from the form
    """
    if not validate_entry_data(request.form):
        flash('Los datos ingresados no son válidos')
        return redirect(url_for('users.show_update_form', user_id=request.form['id']))
    if not valid_email(request.form):
        flash('El correo electrónico ya existe. Por favor, elija otro.')
        return redirect(url_for('users.show_update_form', user_id=request.form['id']))
    User.update(request.form)
    return redirect(url_for('users.index'))

@users_bp.route('/users/blockUser/<int:user_id>', methods=['GET'])
@is_authorized('user_block')
def block(user_id: int)->None:
    """
    Blocks a user
    """
    if (User.is_super_admin(user_id)): 
        flash('No se puede bloquear a un super administrador')
        return redirect(url_for('users.index'))
    User.change_state(user_id)
    return redirect(url_for('users.index'))

@users_bp.route('/users/deleteUser/<int:user_id>', methods=['GET'])
@is_authorized('user_delete')
def delete(user_id: int)->None:
    """
    Deletes a user
    """
    if (User.is_super_admin(user_id)): 
        flash('No se puede eliminar a un super administrador')
        return redirect(url_for('users.index'))
    User.user_delete(user_id)
    return redirect(url_for('users.index'))
