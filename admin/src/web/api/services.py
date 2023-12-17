from flask import Blueprint
from flask import jsonify
from src.models.service import Service
from src.models.institution_service import Institution_Service
from src.models.service_keyword import Service_Keyword
from src.models.institution import Institution
from src.models.keyword import Keyword
from src.models.service import ServiceType
from sqlalchemy import or_
from src.models.configs import Config
from flask import request

api_services_bp = Blueprint('services_api', __name__, url_prefix='/api/services')

@api_services_bp.get('/search') 
def search()->dict:
    """
    Search services by name and type.
    """
    service_name = request.args.get('q') 
    service_type = request.args.get('serviceType').upper()

    try:
        if (service_type):
            services = Service.query.filter(Service.name.ilike(f'{service_name}%'),
                                            Service.type == service_type,
                                            Service.enable).all()
        else:
            services = Service.query.filter(Service.name.ilike(f'{service_name}%'),
                                            Service.enable).all()
    except:
        return jsonify({'error': 'Parámetros inválidos'}), 400
        
    data = {'data': []}
    if (services):
        result = Service.api_services_search(services)
        data = {'data': result}
    
    return jsonify(data), 200
 
@api_services_bp.get('/<int:service_id>')
def get_service(service_id: int)->dict:
    """
    Returns a service given an id.
    """
    service = Service.query.get(service_id)
        
    if (service):
        result = service.api_get_service()
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Parámetros inválidos'}), 400

@api_services_bp.get('/index')
def index() -> dict:
    """
    Returns all the services paginated
    """
    per_page = Config.get_config().get('per_page')
    actual_page = request.args.get('page', default=1, type=int)
    services = Service.query.paginate(page=actual_page, per_page=per_page, error_out=False)
    data = {'data': [],
            "page": actual_page,
            "per_page": per_page,
            "total": services.total
    }
    for service in services.items:
        data['data'].append({'service': service.api_get_service()[0], 'match': None}) #en la vista se espera un campo match

    return jsonify(data), 200


@api_services_bp.get('/search_advanced')
def search_advanced() -> dict:
    """
    Advanced search for services by title, description, institution name, and keywords.
    """
    type_param = request.args.get('type')
    per_page = Config.get_config().get('per_page')
    actual_page = request.args.get('page', default=1, type=int)
    search_string = request.args.get('q')

    if (search_string is None or search_string == "") and (type_param is None or type_param == ""):
        #no hice un 400 porque seria deseable que si quieren filtrar sin datos, simplemente devuelva la pagina actual sin filtrado alguno
        services = Service.query.paginate(page=actual_page, per_page=per_page, error_out=False)
        data = {'data': [],
                "page": actual_page,
                "per_page": per_page,
                "total": services.total
        }
        for service in services.items:
            data['data'].append({'service': service.api_get_service()[0], 'match': None}) #en la vista se espera un campo match
        #perdon por esto, no me anime a refactorizar estando tan cerca la entrega
        return jsonify(data), 200

    services_by_name = Service.query.filter(
            Service.name.ilike(f'%{search_string}%'),
            Service.enable)
    
    services_by_description = Service.query.filter(
            Service.description.ilike(f'%{search_string}%'),
            Service.enable)

    # Búsqueda por nombre de institución con paginación
    institutions_by_name = [institution.id for institution in Institution.query.filter(Institution.name.ilike(f'%{search_string}%')).all()]
    services_of_this_institutions = [Service.query.get(relation.service_id) for relation in Institution_Service.query.filter(Institution_Service.institution_id in institutions_by_name)]
    services_by_institution_name = Service.query.filter(Service.id in services_of_this_institutions)

    keywords_that_matched = [key.id for key in Keyword.query.filter(Keyword.name.ilike(f'%{search_string}%')).all()]
    services_of_that_keywords = [Service.query.get(relation.service_id) for relation in Service_Keyword.query.filter(Service_Keyword.service_id in keywords_that_matched)]
    services_by_keywords = Service.query.filter(Service.id in services_of_that_keywords)

    # Aplicar filtro por tipo si type_param tiene un valor <> de None
    if type_param:
        service_type = ServiceType.string_to_service_type(type_param)
        if service_type:
            services_by_name = services_by_name.filter_by(type=service_type)
            services_by_description = services_by_description.filter_by(type=service_type)
            services_by_institution_name = services_by_institution_name.filter_by(type=service_type)
            services_by_keywords = services_by_keywords.filter_by(type=service_type)

    #Obtener resultados paginados y contar el total de elementos
    all_services = (
        services_by_name.union(services_by_description)
        .union(services_by_institution_name)
        .union(services_by_keywords)
        .all()
    )

    total_elements = len(all_services)
    all_services = list(all_services)[(actual_page -1)*per_page:actual_page*per_page] if total_elements > 0 else []
    #va del elemento 0 al 19 por ejemplo, si la paginacion es de 20 elementos

    # Construir la respuesta con los motivos de coincidencia
    data = {'data': [],
            "page": actual_page,
            "per_page": per_page,
            "total": total_elements}

    for service in all_services:
        match = ""
        if service in services_by_name:
            match += "nombre"
        if service in services_by_description:
            match += "descripción" if (match == "") else ", descripción"
        if service in services_by_institution_name:
            match += "institución" if (match == "") else ", institución"
        if service in services_by_keywords:
            match += "palabras clave" if (match == "") else " y palabras clave"

        data['data'].append({'service': service.api_get_service()[0], 'match': match})

    print(data)
    return jsonify(data), 200

@api_services_bp.get('/search_by_type')
def search_by_type() -> dict:
    per_page = Config.get_config().get('per_page')
    actual_page = request.args.get('page', default=1, type=int)

    if request.args.get('q') is None:
        return jsonify({'error': 'Parámetros inválidos'}), 400
    else:
        type = ServiceType.string_to_service_type(request.args.get('q'))
        if type is None:
            return jsonify({'error': 'Parámetros inválidos'}), 400
    
    all_services = Service.query.filter(Service.type == type).all()
    if not all_services:
        return jsonify({'data': [], "page": actual_page, "per_page": per_page, "total": 0}), 200

    data = {'data': [],
            "page": actual_page,
            "per_page": per_page,
            "total": len(all_services)
    }

    for service in all_services:
        data['data'].append({'service': service.api_get_service()[0], 'match': ""})
    
    return jsonify(data), 200