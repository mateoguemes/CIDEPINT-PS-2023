from datetime import datetime
from src.models.institution_service import Institution_Service
from src.models.institution import Institution
from src.models.database import db
from src.models.requirement_state import Requirement_State
from src.models.service import Service
from src.models.state import State
from sqlalchemy import case, desc, func, asc, label, extract
from sqlalchemy.sql.expression import select
from src.models.configs import Config
from math import ceil

class Requirement(db.Model):
    __tablename__ = "requirements"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    detail = db.Column(db.String(255), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False) #FOREIGN KEY
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow) #this is the date of creation
    service = db.relationship('Service', back_populates='requirements')
    states = db.relationship('Requirement_State', backref='requirement', lazy=True)

    @classmethod
    def add_requirement(cls, data: dict)->None:
        """
        Adds a requirement to the database given a form.
        """
        creation_date_str = data['creation_date']
        creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        new_requirement = Requirement(
            detail = data['description'],
            service_id = data['service_id'],
            user_id = data['user_id'], 
            inserted_at = creation_date,
            updated_at = None,
        )
        db.session.add(new_requirement) 
        db.session.commit()

        new_requirement_id = new_requirement.id
        
        new_requirement_state = Requirement_State(
            requirement_id = new_requirement_id,
            observation = "Se ha creado la solicitud",
        )
        db.session.add(new_requirement_state)
        db.session.commit()

    @classmethod
    def get_requirements_of_user(cls, user_id: int, 
                                 order_of_elements: str, sort_criteria: str,
                                 page: int)->list:
        """
        Returns a list of all the requirements of a user 
        following the order and sort criteria 
        """

        allowed_criteria = ['creation_date', 'service_name', 'current_status']
        
        if sort_criteria and sort_criteria not in allowed_criteria:
            raise ValueError("Parametros invalidos.")
        
        if order_of_elements.lower() not in ['asc', 'desc']:
            raise ValueError("Parametros invalidos.")

        query = (
            db.session.query(
                Service.name.label("service_name"),
                Requirement.inserted_at.label("creation_date"),
                State.name.label("current_status"),
                Service.description,
                Requirement.id.label("requirement_id"),
                )
            .add_columns(
                case(
                    (State.name == "Cancelado", Requirement.updated_at),
                    else_=None
                ).label("close_date")
            )
            .join(Service, Requirement.service_id == Service.id)
            .join(Requirement_State, Requirement.id == Requirement_State.requirement_id)
            .join(State, Requirement_State.state_id == State.id)
            .filter(Requirement.user_id == user_id)
        )

        print(query.all())
        if sort_criteria:
            if sort_criteria == 'creation_date':
                query = query.order_by(desc (Requirement.inserted_at) 
                                       if order_of_elements == 'desc' 
                                       else Requirement.inserted_at)
            elif sort_criteria == 'service_name':
                query = query.order_by(desc(Service.name) 
                                       if order_of_elements == 'desc' 
                                       else Service.name)
            elif sort_criteria == 'current_status':
                query = query.order_by(desc(State.name) 
                                       if order_of_elements == 'desc'
                                        else State.name)
                
                
        paginated_query = query.paginate(page=page,per_page=Config.get_config()['per_page'], error_out=False)
        return paginated_query
    
    @classmethod
    def grouped_and_counted_by_state(cls)->dict:
        """
        Returns a dict with the form of status_name: quantity_of_requirements
        """
        
        states = (db.session.query(State.name, func.count(Requirement.id))
                            .join(Requirement_State, Requirement.id == Requirement_State.requirement_id)
                            .join(State, Requirement_State.state_id == State.id)
                            .group_by(State.name)
        )        
        
        result = states.all()

        dictionary = {}
        dictionary = dict((x, y) for x, y in result)

        return dictionary
    
    @classmethod
    def grouped_and_counted_by_service(cls)->dict:
        """
        Returns a dict with the form of service_name: quantity_of_requirements
        """
        
        services = (db.session.query(Service.name, func.count(Requirement.id))
                        .join(Service, Requirement.service_id == Service.id)
                        .group_by(Service.name)
        )        
        
        result = services.limit(10)

        dictionary = {}
        dictionary = dict((x, y) for x, y in result)

        return dictionary
    
    @classmethod
    def top10(cls)->dict:
        """
        Returns a dict with the form of institution_name: avg_resolution_time
        """

        institutions_avr = (
            db.session.query(Institution.name,
                func.avg(func.extract('epoch',
                    Requirement_State.updated_at - Requirement.inserted_at
                    )
                )
                .label('avg_resolution_time')
            )
            .select_from(Requirement)
            .join(Service, Requirement.service_id == Service.id)
            .join(Institution_Service, Service.id == Institution_Service.service_id)
            .join(Institution, Institution_Service.institution_id == Institution.id)
            .join(Requirement_State, Requirement_State.requirement_id == Requirement.id)
            .join(State, Requirement_State.state_id == State.id)
            .filter(State.name == 'Finalizado')
            .group_by(Institution.name)
        )
        
        result = institutions_avr.limit(10)

        dictionary = {}
        dictionary = dict((x, y) for x, y in result)

        return dictionary

    @classmethod
    def get_requirement(cls,requirement_id: int)->list:
        """
        Returns the selected requirement 
        """
        query = (
            db.session.query(
                Service.name.label("service_name"),
                Requirement.inserted_at.label("creation_date"),
                State.name.label("current_status"),
                Service.description,
                Requirement.detail.label("client_description"),
                Requirement_State.observation.label("observation"),
                Service.id.label("service_id"),
                )
            .add_columns(
                case(
                    ((State.name == "Finalizado"),
                      Requirement_State.updated_at),
                    else_=None
                ).label("close_date")
            )
            .join(Service, Requirement.service_id == Service.id)
            .join(Requirement_State, Requirement.id == Requirement_State.requirement_id)
            .join(State, Requirement_State.state_id == State.id)
            .filter(Requirement.id == requirement_id)
            .first()
        )
        return query

    @classmethod
    def get_total_pages(cls, user_id: int)->int:
        """
        Returns the total number of pages
        """
        total_pages = (
            db.session.query(
                db.func.count(Requirement.id)
            )
            .filter(Requirement.user_id == user_id)
            .scalar()
        )
        return ceil(total_pages/Config.get_config()['per_page'])