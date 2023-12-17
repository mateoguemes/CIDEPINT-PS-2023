from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.models.user import User
from src.models.institution import Institution
from src.models.user_institution import User_Institution
from src.models.user_institution_role import User_Institution_Role
from src.models.role import Role
from src.models.configs import Config
from src.models.keyword import Keyword
from src.models.institution_keyword import Institution_Keyword
from src.models.role_permission import Role_Permission
from src.models.database import db
from src.web.controllers.validations import valid_institution_name
from src.web.helpers.auth import is_authorized, has_permission
from src.web.helpers.services_validations import validate_keywords
from sqlalchemy.orm import Query

institutions_bp = Blueprint('institutions', __name__)

@institutions_bp.route('/institutions', methods=['GET'])
@is_authorized("institution_index")
def index()->None:
    """
    Renders the institutions index page
    """
    page = request.args.get('page', 1, type=int)
    institutions_pagination = Institution.query.paginate(page=page, per_page=Config.get_config().get('per_page'), error_out=False)

    return render_template('institutions_index.html', institutions=institutions_pagination)

@institutions_bp.route('/institutions/add', methods=['GET', 'POST'])
@is_authorized("institution_create")
def register()->None:
    """
    Adds a new institution to the database
    and renders the institutions index page
    """
    if request.method == 'POST':
        existing_name = Institution.name_exists(request.form['name'])
        keywords = set(request.form['keywords'].split()) #sin duplicados
        if existing_name:
            flash('El nombre de institución ya existe. Por favor, elija otro.')
            return redirect(url_for('institutions.add'))
            
        try:  # valida keywords
            validate_keywords(*keywords)
        except Exception as e:
            flash(f"{str(e)}", "error")
            return redirect(url_for('institutions.add'))

        Institution.add_institution(request.form)
        new_institution = Institution.query.filter_by(name=request.form['name']).first()

        # crea keywords
        for word in keywords:
            existing_keyword = Keyword.query.filter_by(name=word).first()  # busca que no exista
            if not existing_keyword:
                existing_keyword = Keyword(word)
                db.session.add(existing_keyword)
                db.session.commit()  # necesita el id
                db.session.add(Institution_Keyword(new_institution.id, existing_keyword.id))
                db.session.commit()

        flash(f"La institución \"{new_institution.name}\" fue creada exitosamente", "success")
        return redirect(url_for('institutions.index'))
    
    return render_template('institution_add.html')

@institutions_bp.route('/institutions/updateInstitution/<int:institution_id>', methods=['GET'])
@is_authorized("institution_update")
def show_update_form(institution_id)->None:
    """
    Renders the update institution form
    """
    institution = Institution.query.get(institution_id)
    keywords = institution.get_keywords()
    sorted_keywords = sorted(keywords, key=lambda keyword: keyword.name)
    text = " ".join(keyword.name for keyword in sorted_keywords)
   
    return render_template('institution_update_form.html', institution=institution, keywords=text)

@institutions_bp.route('/institutions/updateInstitution/<int:institution_id>', methods=['GET', 'POST'])
@is_authorized("institution_update")
def update(institution_id):
    """
    Updates an institution and renders the corresponding institution page
    """
    institution = Institution.query.get(institution_id)
    
    if not valid_institution_name(request.form):
        flash('El nombre de institución ingresado ya está en uso. Por favor, elija otro.')
        return redirect(url_for('institutions.show_update_form', institution_id=institution_id))

    keywords = set(request.form.get('keywords', '').split())  # sin duplicados

    try:  # valida keywords
        validate_keywords(*keywords)
    except Exception as e:
        flash(f"{str(e)}", "error")
        return redirect(url_for('institutions.update', institution_id=institution_id))

    # crea keywords
    for word in keywords:
        existing_keyword = Keyword.query.filter_by(name=word).first()  # busca que no exista
        if not existing_keyword:
            existing_keyword = Keyword(word)
            db.session.add(existing_keyword)
            db.session.commit()  # necesita el id
            db.session.add(Institution_Keyword(institution.id, existing_keyword.id))
            db.session.commit()

    if institution:
        institution.update(request.form)
        flash(f"La institución \"{institution.name}\" fue editada exitosamente", "success")
        return redirect(url_for('institutions.show', institution_id=institution.id))
    else:
        # Manejar el caso en el que la institución no existe
        flash('La institución no existe', 'error')
        # Puedes redirigir a alguna página de error o a donde sea necesario
        return redirect(url_for('institutions.index'))

@institutions_bp.route('/institutions/disableInstitution/<int:institution_id>', methods=['GET'])
@is_authorized("institution_deactivate")
def disable(institution_id: int)->None:
    """
    Disables an institution and renders the institutions index page.
    """
    institution = Institution.query.filter(Institution.id == institution_id).first()
    institution.disable()
    flash(f"La institución \"{institution.name}\" fue deshabilitada exitosamente", "success")
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/institutions/enableInstitution/<int:institution_id>', methods=['GET'])
@is_authorized("institution_activate")
def enable(institution_id: int)->None:
    """
    Disables an institution and renders the institutions index page.
    """
    institution = Institution.query.filter(Institution.id == institution_id).first()
    institution.enable()
    flash(f"La institución \"{institution.name}\" fue habilitada exitosamente", "success")
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/institutions/deleteInstitution/<int:institution_id>', methods=['GET'])
@is_authorized("institution_destroy")
def delete(institution_id: int)->None:
    """
    Deletes an institution and renders the institutions index page
    """
    institution = Institution.query.get(institution_id)  # NO SE AGARRA DE LA SESSION
    institution.delete()
    flash(f"La institución \"{institution.name}\" fue eliminada exitosamente", "success")
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/institutions/show/<int:institution_id>', methods=['GET'])
@is_authorized("institution_show")
def show(institution_id: int)->None:
    """
    Renders a given institution
    """
    institution = Institution.query.filter(Institution.id == institution_id).first()
    super_admin = User.is_super_admin(session.get('user_id'))
    auth = has_permission("user_institution_index")
    keywords = institution.get_keywords()
    sorted_keywords = sorted(keywords, key=lambda keyword: keyword.name)
    text = " ".join(keyword.name for keyword in sorted_keywords)
    permissions=User.get_permissions(session.get('user_id'), session.get('institution_id'))
    return render_template('institution_show.html', institution=institution, super=super_admin, auth=auth, keywords=text, permissions= permissions)
