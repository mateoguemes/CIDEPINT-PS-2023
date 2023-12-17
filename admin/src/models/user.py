from datetime import datetime
from src.models.database import db
from src.models.user_institution_role import User_Institution_Role
from src.models.user_institution import User_Institution
from src.models.role import Role
from src.models.user_institution import User_Institution
from src.models.permission import Permission
import secrets
from werkzeug.security import generate_password_hash
from sqlalchemy.orm.query import Query as BaseQuery

class Token(db.Model):
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), nullable=False)
    token_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=True)
    password = db.Column(db.String(255), nullable=True) 
    username = db.Column(db.String(50), nullable=True) 
    email = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    tokens = db.relationship('Token', backref='user', lazy=True)
    user_institution = db.relationship('User_Institution', backref='user', cascade='all, delete-orphan')
    user_institution_role = db.relationship('User_Institution_Role', backref='user', cascade='all, delete-orphan')

    @classmethod
    def addUser(cls, name: str, last_name: str, email: str)->int:
        """
        Adds a user to the database and returns the id of the token created.
        """
        #Crea un nuevo usuario temporal y almacena el token de confirmación
        new_user = User(name=name, lastname=last_name, email=email, confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        # Genera un token único y aleatorio
        token_value = secrets.token_urlsafe(16) 
        # Crea un nuevo token con el valor generado
        token = Token(user_id=new_user.id, token=token_value, token_type='confirmation')
        db.session.add(token)
        db.session.commit()
        return token.id

    @classmethod
    def confirmUser(cls, token_obj: object, username: str, password: str)->None:
        """
        Confirms the user and updates its username and password.
        """
        #recupero el usuario
        user = User.query.get(token_obj.user_id)
        # Actualiza el usuario existente con el nombre de usuario y contraseña
        user.username = username
        user.password = generate_password_hash(password)
        # Marca al usuario como confirmado
        user.confirmed = True
        db.session.delete(token_obj)
        db.session.commit()
        
    def user_index()->list:
        """
        Returns a list of all users.
        """
        return User.query.order_by(User.name).all()

    def user_exists(mail: str)->object:
        """
        Return a user object if the email is in use by a user, None otherwise
        """
        return User.query.filter_by(email = mail).first()
    
    def user_delete(id: int)->None:
        """
        Deletes a user from the database.
        """
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

    def user_get_by_state(state: str) -> BaseQuery:
        """
        Returns a query of users filtered by state.
        """
        if state == "Todos":
            return User.query.order_by(User.email)
        elif state == "Activo":
            return User.query.filter_by(active=True).order_by(User.email)
        else:
            return User.query.filter_by(active=False).order_by(User.email)
        
    def change_state(id: int)->None:
        """
        Blocks or unblocks a user.
        """
        user = User.query.get(id)
        user.active = not user.active
        db.session.commit()

    def if_no_institution_block(self)->None:
        """
        Changes the state of the user to inactive if it has no institution.
        """
        institutions = User_Institution.query.filter(User_Institution.user_id == self.id).first()
        if not (institutions):
            self.change_state(self.id)

    def get_permissions(user_id: int, institution_id: int)->list:
        """
        Returns the permissions of the user in the institution.
        """
        if(User.is_super_admin(user_id)):
            permissions = [permission.name for permission in Permission.query.distinct().all()]
            return permissions
        role_in_institution = User_Institution_Role.search_role_id(user_id, institution_id) # me devuelve el id del rol
        user_permissions_list = Role.get_permissions(role_in_institution)
        return user_permissions_list
    
    def is_super_admin(user_id: int)->bool:
        """
        Returns True if the user is super admin, False otherwise.
        """
        roles_of_user = User_Institution_Role.get_roles(user_id)
        if (roles_of_user):
            names_of_roles = [Role.query.get(role_id).name for role_id in roles_of_user]
            return True if 'super admin' in names_of_roles else False
        else:
            return False
    
    def update(form: dict):
        """
        Updates a user given a form.
        """
        user = User.query.get(form['id'])
        user.name = form['name']
        user.lastname = form['lastname']
        user.username = form['username']
        user.email = form['email']
        db.session.commit()

    def get_role_in(self, institution_id: int)->object:
        """
        Returns the role of the user in the institution.
        """
        role_id = User_Institution_Role.search_role_id(self.id,institution_id)
        return Role.query.get(role_id) if role_id != None else None

    def if_alone_desactivate(self)->None:
        """
        Desactivates an user if it does not has institutions. 
        """
        relations_with_institutions = User_Institution.query.filter_by(user_id=self.id).first()
        self.active = False if not relations_with_institutions else True

    def activate(self):
        """
        Activates a user
        """
        if not self.active:
            self.active = True