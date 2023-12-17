#modulo 1.6 de la consigna
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.models.user import User
from src.models.configs import Config
from src.models.institution import Institution
from src.models.user_institution import User_Institution
from src.models.user_institution_role import User_Institution_Role
from src.models.role import Role
from src.models.database import db
from src.web.helpers.auth import is_authorized
from sqlalchemy.orm import Query

users_of_institution_bp = Blueprint('users_of_institution', __name__)
@users_of_institution_bp.route('/users_of_institution', methods=['GET'])
@is_authorized("user_institution_index")
def index()->None:
    """
    Renders the users of institution page
    """
    page = request.args.get('page', 1, type=int)
    
    institution = Institution.query.get(session.get('institution_id', None))
    
    # Utiliza el método paginate para obtener los resultados paginados
    users_pagination = User.query.join(User_Institution).join(Institution).filter(Institution.id == institution.id).paginate(page=page, per_page=Config.get_config().get('per_page'), error_out=False)
    users = users_pagination.items

    roles = []
    for user in users_pagination.items:
        roles.append(user.get_role_in(institution.id))

    all_roles = Role.get_all_posibilities()

    return render_template('users_of_institution.html', institution=institution, users=users, roles=roles, institution_roles=all_roles, permissions=User.get_permissions(session['user_id'], session['institution_id']), pagination=users_pagination)


@users_of_institution_bp.route('/users_of_institution/create', methods=['POST'])
@is_authorized("user_institution_create")
def create()->None:
    """This function gives the selected role to the selected user"""

    institution_id=session.get('institution_id',None)
    role_id=request.form['role']
    user = User.query.filter_by(email = request.form['email']).first()
    if not user:
        flash('No se ha encontrado un usuario con ese email', 'error')
        return redirect(url_for('users_of_institution.index'))
    else:
        user_institution_role = User_Institution.query.filter_by(user_id=user.id, institution_id=institution_id).first()

        if user_institution_role:
            flash('Ese usuario ya cuenta con un rol', 'error')
            return redirect(url_for('users_of_institution.index'))
        else:
            user.activate()
            db.session.add(User_Institution(user.id, institution_id))
            db.session.add(User_Institution_Role(user.id, institution_id, role_id))
            db.session.commit()
            flash('El usuario fue agregado exitosamente a la institución', 'success')
            return redirect(url_for('users_of_institution.index'))


@users_of_institution_bp.route('/users_of_institution/delete_role', methods=['POST'])
@is_authorized("user_institution_destroy")
def destroy()->None:
    """This function deletes the role of the selected user in that institution"""

    user_id = request.form['user_id']
    institution_id = session.get('institution_id',None)
    user_institution_role = User_Institution_Role.query.filter_by(user_id=user_id, institution_id=institution_id).first()
    user_institution = User_Institution.query.filter_by(user_id=user_id, institution_id=institution_id).first()

    if (not user_institution_role or not user_institution):
        flash('Ha ocurrido un error al intentar quitarle el rol','error')
        return redirect (url_for('users_of_institution.index'))
    
    db.session.delete(user_institution_role)
    db.session.delete(user_institution)
    user = User.query.get(user_id)
    user.if_alone_desactivate()

    db.session.commit()
    flash('El usuario ya no cuenta con un rol en la institución', 'success')
    return redirect (url_for('users_of_institution.index'))


@users_of_institution_bp.route('/users_of_institution/update_role', methods=['POST'])
@is_authorized("user_institution_update")
def update_role()->None:
    """This function changes the role of the user in that institution if it is not the previous one"""

    user_id = request.form['user_id']
    institution_id = session.get('institution_id',None)
    old_role_id = request.form['old_role_id']
    new_role_id = request.form['new_role_id']

    if(old_role_id != new_role_id):
        user_institution_role = User_Institution_Role.query.filter_by(user_id=user_id, institution_id=institution_id).first()
        if(user_institution_role):
            user_institution_role.change_role(new_role_id)
            db.session.commit()
            flash(f'El rol se ha actualizado con éxito', 'success')
    
    return redirect (url_for('users_of_institution.index'))