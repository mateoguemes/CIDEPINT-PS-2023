from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.models.requirement import Requirement  # Asegúrate de importar el modelo de Solicitud
from src.models.user import User
from src.models.state import State
from src.models.requirement_state import Requirement_State
from src.models.note import Note
from typing import Union
from src.web.helpers.api_validations import valid_data

service_detail_bp = Blueprint('service_detail', __name__)

@service_detail_bp.route('/service_detail/<int:request_id>', methods=['GET' ,'POST'])
def show_request(request_id: int)->Union[None, str]:
    """
    Shows a request detail and 
    renders the service_detail page if it was successful,
    else sends a feedback
    """
    # Carga los datos de la solicitud según el 'request_id'
    solicitud = Requirement.query.get(request_id)  # Recupera la solicitud de la base de datos
    if solicitud is not None:
        requirement_state = Requirement_State.query.filter_by(requirement_id=request_id).first()
        if request.method == 'POST' and request.form['new-status']:
            new_status = request.form['new-status']
            observation = request.form['observation']
            Requirement_State.update_requirement_state(requirement_state, new_status , observation)
            flash('Se actualizo el estado de la solicitud.', 'success')
            return redirect(url_for('solicitudes.index'))
        else:
            # Cargar los estados desde la base de datos
            user_id = User.query.get(solicitud.user_id)
            if requirement_state is not None:
                state = State.query.get(requirement_state.state_id)
                states = State.query.all()
                # Obtenemos los detalles de la solicitud
                customer_name = f"{user_id.name} {user_id.lastname}"
                customer_email = user_id.email # Correo electrónico del cliente
                service_name = solicitud.service.name  # Nombre del servicio
                service_description = solicitud.service.description  # Descripción del servicio
                service_state = state.name
                service_observation = requirement_state.observation
                requirement_detail = solicitud.detail
                # Puedes cargar los archivos adjuntos, estado, observaciones y comentarios aquí también si son parte de tu modelo

                # Renderiza la plantilla y pasa los datos a la misma
                return render_template('service_detail.html', customer_name=customer_name, 
                                    customer_email=customer_email, service_name=service_name,
                                        service_description=service_description,
                                    solicitud=solicitud, service_state=service_state,
                                    service_observation= service_observation, states=states,
                                    requirement_id = request_id, requirement_detail=requirement_detail)   
            else:
                 return "Solicitud no encontrada", 404              
    else:
        return "Solicitud no encontrada", 404
    
@service_detail_bp.route('/showNotes/<int:request_id>', methods=['GET'])
def show_notes(request_id: int)->None:
    """
    Renders the notes of a request.
    """
    notes = Note.query.filter_by(requirement_id=request_id).all()
    return render_template('notes.html', notes=notes, requirement_id=request_id)

@service_detail_bp.get('/addNotes/<int:request_id>')
def show_note_form(request_id: int)->None:
    """
    Renders the form to add a note.
    """
    return render_template('note_add.html', requirement_id=request_id)

@service_detail_bp.post('/addNotes/<int:request_id>')
def add_notes(request_id: int)->None:
    """
    Adds a note to a request.
    """
    if request.method == 'POST': 
        data = {"text": request.form['text'], "requirement_id": request_id,
                "from_laboratory": True}
        
        if (not data['text']):
            flash('No se puede agregar una nota vacía.', 'danger')
            return redirect(url_for('service_detail.show_note_form', request_id=request_id))
        
        if (len(data['text']) > 255):
            flash('La nota no puede tener más de 255 caracteres.', 'danger')
            return redirect(url_for('service_detail.show_note_form', request_id=request_id))

        Note.add_note(data)
        return redirect(url_for('service_detail.show_notes', request_id=request_id))
    else:
        return "Solicitud no encontrada", 404