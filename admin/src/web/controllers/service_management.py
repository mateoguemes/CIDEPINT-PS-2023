from flask import Blueprint, render_template, request, session, redirect, url_for
from src.models.user import User
from src.models.state import State
from src.models.institution_service import Institution_Service
from src.models.service import Service, ServiceType
from src.models.requirement import Requirement
from src.models.requirement_state import Requirement_State
from datetime import datetime
from src.models.configs import Config

solicitudes_bp = Blueprint('solicitudes', __name__)

@solicitudes_bp.route('/service_management')
def index():
    # Obtén los parámetros de filtro de la URL
    service_type = request.args.get('status')
    serviceType = request.args.get('serviceType')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    user = request.args.get('user')
    if 'clear_filters' in request.args:
        return redirect(url_for('solicitudes.index'))
    # Realiza la consulta a la base de datos según los parámetros de filtro
    filtered_solicitudes = Requirement.query
    # Obtén el ID de la institución del usuario logueado desde la sesión
    institution_id = session.get('institution_id', None)
    if institution_id:
        # Obtén los IDs de los servicios asociados a la institución del usuario logueado
        matching_service_ids = Institution_Service.query.filter_by(institution_id=institution_id).with_entities(Institution_Service.service_id)
        matching_service_ids = [row[0] for row in matching_service_ids]
        # Filtra las solicitudes en base a los IDs de servicio obtenidos
        filtered_solicitudes = filtered_solicitudes.filter(Requirement.service_id.in_(matching_service_ids))

    if service_type:
        # Obtén los IDs de las solicitudes que tienen el estado de service_type
        matching_ids = Requirement_State.query.filter_by(state_id=service_type).with_entities(Requirement_State.requirement_id)
        matching_ids = [row[0] for row in matching_ids]
        # Filtra las solicitudes en base a los IDs obtenidos
        filtered_solicitudes = filtered_solicitudes.filter(Requirement.id.in_(matching_ids))

    if serviceType:
        # Obtén los IDs de los servicios que tienen el tipo seleccionado
        matching_service_ids = Service.query.filter_by(type=serviceType).with_entities(Service.id)
        matching_service_ids = [row[0] for row in matching_service_ids]
        # Filtra las solicitudes en base a los IDs de servicio obtenidos
        filtered_solicitudes = filtered_solicitudes.filter(Requirement.service_id.in_(matching_service_ids))

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_solicitudes = filtered_solicitudes.filter(Requirement.inserted_at >= start_date, Requirement.inserted_at <= end_date)

    if user:
        matching_users = User.query.filter_by(email=user).with_entities(User.id)
        matching_users = [row[0] for row in matching_users]
        filtered_solicitudes = filtered_solicitudes.filter(Requirement.user_id.in_(matching_users))

    # Ejecuta la consulta y obtén todas las solicitudes filtradas
    all_solicitudes = filtered_solicitudes.all()

    # Realiza el mismo procesamiento que tenías previamente para mostrar los resultados
    states = State.query.all()
    users = User.query.all()
    user_mapping = {user.id: user.email for user in users}
    services = Service.query.all()
    service_mapping = {service.id: service.name for service in services}
    estados = State.query.all()
    tipos_servicio = [service_type.value for service_type in ServiceType]

    for solicitud in all_solicitudes:
        user_id = solicitud.user_id
        user_email = user_mapping.get(user_id)
        if user_email:
            solicitud.user_email = user_email

        service_id = solicitud.service_id
        service_name = service_mapping.get(service_id)
        if service_name:
            solicitud.service_name = service_name

        latest_state = Requirement_State.query.filter_by(requirement_id=solicitud.id).order_by(Requirement_State.updated_at.desc()).first()
        if latest_state:
            solicitud.estado = latest_state.state.name
        else:
            solicitud.estado = "Sin estado"

    # Pagina las solicitudes después de realizar todas las filtraciones
    page = request.args.get('page', 1, type=int)
    solicitudes =  filtered_solicitudes.paginate(
        page=page,
        per_page=Config.get_config().get('per_page'),
        error_out=False
    )

    unique_users = list(set(solicitud.user_email for solicitud in all_solicitudes))
    # Obtén los tipos de servicio únicos de tus solicitudes
    unique_service_types = list(set(solicitud.service.type.name for solicitud in all_solicitudes))

    return render_template('service_management.html', solicitudes=solicitudes, unique_users=unique_users, estados=estados, tipos_servicio=tipos_servicio, states=states, unique_service_types=unique_service_types, pagination=solicitudes)