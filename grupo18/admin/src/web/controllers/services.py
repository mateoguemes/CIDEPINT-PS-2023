#modulo 1.7
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from src.models.institution import Institution
from src.models.institution_service import Institution_Service
from src.models.keyword import Keyword
from src.models.service import Service
from src.models.service import ServiceType
from src.models.service_keyword import Service_Keyword
from src.models.database import db
from src.web.helpers.services_validations import validate_entry_data, validate_keywords
from src.web.helpers.auth import is_authorized
from src.models.configs import Config

services_bp= Blueprint('services', __name__)

from sqlalchemy.orm import joinedload

@services_bp.route('/services', methods=['GET', 'POST'])
@is_authorized("service_index")
def index():
    institution = Institution.query.get(session.get('institution_id', None))
    filter = "Todos" if request.method == 'GET' else request.form['criteria']

    page = request.args.get('page', 1, type=int)

    query = (
        Service.query
        .join(Institution_Service, Institution_Service.service_id == Service.id)
        .filter(Institution_Service.institution_id == institution.id)
    )

    if filter == "Activos":
        query = query.filter(Service.enable.is_(True))
    elif filter == "Inactivos":
        query = query.filter(Service.enable.is_(False))
    elif filter in ServiceType.get_all_values():
        query = query.filter(Service.type == filter)

    services_pagination = query.paginate(
        page=page,
        per_page=Config.get_config().get('per_page'),
        error_out=False
    )

    sorted_services = services_pagination.items
    service_types = ServiceType.get_all_values()

    return render_template('services.html', institution=institution, services=sorted_services,
                           services_pagination=services_pagination, selected_criteria=filter, service_types=service_types)


@services_bp.route('/services/show/<int:service_id>', methods=['GET'])
@is_authorized("service_show")
def show(service_id: int)->None:
    """Shows the specified service by id"""
    service = Service.query.get(service_id)

    if not service:
        flash("Ocurrió un error al mostrar un servicio", "error")
        return redirect(url_for("services.index"))

    keywords = service.get_keywords()
    sorted_keywords = sorted(keywords, key=lambda keyword: keyword.name)
    keywords_text = " ".join(keyword.name for keyword in sorted_keywords)

    institution_id = session.get('institution_id')
    institution = Institution.query.get(institution_id)

    return render_template("service_show.html", institution=institution, service=service, keywords=keywords_text)


@services_bp.route('/services/create', methods=['POST'])
@is_authorized("service_create")
def create()->None:
    """Creates the service specified for the institution and the respective keywords"""
    institution_id = session.get('institution_id',None)
    keywords = set(request.form['keywords'].split())#elimina palabras duplicadas 
    name = request.form['name']
    description = request.form['description']
    type = ServiceType.string_to_service_type(request.form['selected_type'])
    enable = request.form['enable']

    try:
        validate_entry_data(name,description,type,enable)
        validate_keywords(*keywords)
    except Exception as e:
        flash(f"{str(e)}","error")
        return redirect (url_for('services.show_create_form'))
    
    if(enable.lower() not in ["true","false"]):
        flash('Ha ocurrido un error al intentar crear el servicio','error')
        return redirect (url_for('services.index')) #esto sería por un error de un programador
    
    if not Service.is_this_name_unique_for(name,institution_id):
        flash(f"El servicio \"{name}\" ya existe en la institución, por favor, elija otro nombre",'error')
        return redirect (url_for('services.show_create_form'))
    
    #creo el servicio y le hago el commit así le asigna un id al que luego accedo
    enable = True if enable.lower() == "true" else False #ya validé que sea "true" o "false"
    new_service = Service(name,description,type,enable)
    db.session.add(new_service)
    db.session.commit() #es necesario para que cree debidamente el servicio

    for word in keywords:
        existing_keyword = Keyword.query.filter_by(name = word).first() #ve si ya existe esa palabra clave en la base da datos
        if not existing_keyword:
            existing_keyword = Keyword(word)
            db.session.add(existing_keyword)
            db.session.commit()#necesito hacer el commit para que la BD le otorgue un id
        db.session.add(Service_Keyword(new_service.id,existing_keyword.id))
        db.session.commit()

    db.session.add(Institution_Service(institution_id,new_service.id))
    db.session.commit()
    flash(f"El servicio \"{name}\" fue creado correctamente",'success')
    return redirect (url_for('services.index'))


@services_bp.route('/services/update', methods=['POST'])
@is_authorized("service_update")
def update()->None:
    """Updates the specified service information"""
    institution = Institution.query.get(session.get('institution_id',None))
    service = Service.query.get(request.form['service_id'])
    
    if not (service and institution):
        flash("Ocurrió un eror al querer actualizar el sevicio","error")
        return redirect (url_for('services.show_update_form/', service = service))
    
    new_name=request.form['name']
    new_description=request.form['description']
    new_type=ServiceType.string_to_service_type(request.form['selected_type'])
    new_status=request.form['enable']
    keywords = set(request.form.get('keywords', '').split())  # sin duplicados

    try:  # valida keywords
        validate_keywords(*keywords)
    except Exception as e:
        flash(f"{str(e)}", "error")
        return redirect(url_for('services.update'))

    # crea keywords
    for word in keywords:
        existing_keyword = Keyword.query.filter_by(name=word).first()  # busca que no exista
        if not existing_keyword:
            existing_keyword = Keyword(word)
            db.session.add(existing_keyword)
            db.session.commit()  # necesita el id
            db.session.add(Service_Keyword(service.id, existing_keyword.id))
            db.session.commit()
        
    if(new_status.lower() not in ["true","false"]):
        flash('Ha ocurrido un error al intentar crear el servicio','error')
        return redirect (url_for('services.show_update_form', service = service)) #esto sería por un error de un programador

    if(not Service.can_update_name_to(new_name, institution.id, service.id)):
        flash(f"Ya existe un servicio en la institución llamado \"{new_name}\"")
        return redirect (url_for('services.show_update_form', service = service))
    
    new_status=True if new_status.lower() == "true" else False #ya validé que sea "true" o "false"
    service.update(new_name,new_description,new_type,new_status)
    db.session.commit()

    flash(f"El servicio \"{service.name}\" fue actualizado exitosamente","success")
    return redirect (url_for('services.index'))


@services_bp.route('/services/delete/<int:service_id>', methods=['POST'])
@is_authorized("service_destroy")
def destroy(service_id: int)->None:
    """Deletes the service and its relations with keywords"""
    institution_id = session.get('institution_id',None)
    service = Service.query.get(service_id)
    keywords = service.get_keywords()
    if service:
        for index, relation in enumerate(Service_Keyword.query.filter_by(service_id = service_id)):
            db.session.delete(relation)
            db.session.commit()
            keywords[index].if_alone_delete()

        #borro la relacion entre ese servicio y la institucion
        db.session.delete(Institution_Service.query.filter_by(service_id=service_id, institution_id = institution_id).first())
        db.session.delete(service)
        db.session.commit()
        flash("Se borró el servicio existosamente","success")
    return redirect(url_for("services.index"))


@services_bp.route('/services/create_form/', methods=['GET'])
@is_authorized("service_create")
def show_create_form()->None:
    """Shows the form to create a service"""
    institution = Institution.query.get(session.get('institution_id',None))
    return render_template ('service_create_form.html', institution = institution, service_types= ServiceType.get_all_values())
    

@services_bp.route('/services/update_form/<int:service_id>', methods=['GET'])
@is_authorized("service_update")
def show_update_form(service_id: int)->None:
    """Shows the form to update a service"""
    service = Service.query.get(service_id)
    institution = Institution.query.get(session.get('institution_id',None))
    if not (service and institution):
        flash("Ocurrió un error al querer modificar un servicio","error")
        return redirect(url_for('services.show', service_id=service_id))
    keywords = service.get_keywords()
    sorted_keywords = sorted(keywords, key=lambda keyword: keyword.name)
    #key se utiliza para especificar una función que se aplicará a cada elemento de la lista antes de ordenarlos
    keywords_text = " ".join(keyword.name for keyword in sorted_keywords)
    return render_template ('service_update_form.html', institution = institution, service= service, service_types= ServiceType.get_all_values(), keywords = keywords_text)