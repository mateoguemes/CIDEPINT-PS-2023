from datetime import datetime
from src.models.database import db
from src.models.user_institution import User_Institution
from src.models.user_institution_role import User_Institution_Role
from src.models.institution_service import Institution_Service
from src.models.user import User
from src.models.role import Role
from src.models.service import Service
from src.models.institution_keyword import Institution_Keyword
from src.models.keyword import Keyword
from flask import flash

class Institution(db.Model):
    __tablename__ = "institutions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    information = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    opening_hours = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_institution = db.relationship('User_Institution', backref='institution',
                                       cascade='all, delete-orphan')
    user_institution_role = db.relationship('User_Institution_Role', backref='institution',
                                            cascade='all, delete-orphan')
    institution_service = db.relationship('Institution_Service', backref='institution',
                                         cascade='all, delete-orphan')
    institution_keyword = db.relationship('Institution_Keyword', backref='institution',
                                         cascade='all, delete-orphan')

    @classmethod
    def add_institution(cls, form: dict):
        """
        Adds an institution to the database given a form.
        """
        # Verificar si 'name' ya existe
        existing_name = cls.name_exists(form.get('name'))

        if existing_name:
            flash('El nombre de institución ya existe. Por favor, elija otro.')
            return

        # Obtén la dirección y las coordenadas desde el formulario
        address = form.get('formatted_address')
        latitude = form.get('latitude')
        longitude = form.get('longitude')

        # Concatena la latitud y longitud en el formato deseado
        location2 = f"{latitude},{longitude}"

        new_institution = Institution(
            name=form.get('name'),
            information=form.get('information'),
            address=address,  # Cambiado a 'location'
            location=location2,
            website=form.get('website'),
            opening_hours=form.get('opening_hours'),
            contact=form.get('contact'),
            enabled=True
        )

        db.session.add(new_institution)
        db.session.commit()

    @classmethod
    def name_exists(cls,name)->any:
        """
        Returns an institution if it exists, otherwise returns None.
        """
        return Institution.query.filter_by(name = name).first()

    def get_users(self) -> list:
        """
        Returns the users of a institution.
        """
        user_ids = [user_institution.user_id for user_institution in 
                    User_Institution.query.filter_by(institution_id=self.id).all()]
        users = User.query.filter(User.id.in_(user_ids)).all()
        return users

    def get_roles(self) -> list:
        """
        Returns the ids of the roles of a institution.
        """
        role_ids = [user_institution_role.role_id for user_institution_role in 
                    User_Institution_Role.query.filter_by(institution_id = self.id)]
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        return roles
    
    @classmethod
    def institutions_index(cls)->list:
        """
        Returns all the institutions except CIDEPINT.
        """
        return Institution.query.filter(Institution.name != "CIDEPINT").all()
    
    @classmethod
    def get_by_name(cls,name) -> object:
        """
        Returns an institution by its name.
        """
        return Institution.query.filter(Institution.name == name).first()
    
    def disable(self)->None:
        """
        Disables an institution.
        """
        self.enabled = False
        db.session.commit()

    def enable(self)->None:
        """
        Enables an institution.
        """
        self.enabled = True
        db.session.commit()

    def delete(self)->None:
        """
        Deletes an institution.
        """
        users_institutions = User_Institution.query.filter(
            User_Institution.institution_id == self.id).all()
        users = []
        for u_i in users_institutions:
            users.append(u_i.user_id)
            db.session.delete(u_i)
            db.session.commit()
        
        institutions_keywords = Institution_Keyword.query.filter(
            Institution_Keyword.institution_id == self.id).all()
        keywords = []
        for i_k in institutions_keywords:
            keywords.append(i_k.keyword_id)
            db.session.delete(i_k)
            db.session.commit()
                
        db.session.delete(self)

        for u_id in users:
            user = User.query.get(u_id)
            user.if_no_institution_block()
        for k_id in keywords:
            keyword = Keyword.query.get(k_id)
            keyword.if_alone_delete()

        db.session.commit()

    def update(self,form: dict)->None:
        """
        Updates an institution given the form.
        """
        self.name = form['name']
        self.information = form['information']
        self.address = form['address']
        latitude = form.get('latitude')
        longitude = form.get('longitude')
        location2 = f"{latitude},{longitude}"
        self.location = location2
        self.website = form['website']
        self.opening_hours = form['opening_hours']
        self.contact = form['contact']
        db.session.commit()

    def get_institutions_of_user(user_id: int)->list:
        """
        Returns the institutions a given user is part of.
        """
        institutions = []
        if (User.is_super_admin(user_id)):
            institutions = Institution.query.filter(Institution.name != 'CIDEPINT').all()
        else:
            for institution in User_Institution.query.filter_by(user_id=user_id).all():
                institutions.append(Institution.query.get(institution.institution_id)) 
        return institutions
    
    def get_services(self) -> list:
        """
        Returns the services of a institution.
        """
        services_ids = [institution_service.service_id for institution_service in Institution_Service.query.filter_by(institution_id = self.id)]
        services = Service.query.filter(Service.id.in_(services_ids)).all()
        return services
    
    def get_name(id: int):
        """
        Returns the name of an institution given its id.
        """
        return Institution.query.get(id).name if Institution.query.get(id) != None else None
    
    def get_keywords(self) -> list:
        """
        Returns the keywords of a institution.
        """
        keyword_ids = [relation.keyword_id for relation in Institution_Keyword.query.filter_by(institution_id=self.id).all()]
        keywords = Keyword.query.filter(Keyword.id.in_(keyword_ids)).all() 
        return keywords if keywords else []
