from datetime import datetime
from src.models.database import db

class User_Institution_Role(db.Model):
    __tablename__ = "user_institution_roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #FOREIGN KEY
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"), nullable=False) #FOREIGN KEY
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,user_id,institution_id,role_id):
        self.user_id=user_id
        self.institution_id=institution_id
        self.role_id=role_id

    @classmethod
    def search_role_id(cls, user_id: int, institution_id: int)->int:
        """
        Returns the role_id of the user in the institution
        """
        user_institution_role = User_Institution_Role.query.filter_by(user_id=user_id, institution_id=institution_id).first()
        return user_institution_role.role_id if user_institution_role else None
    
    
    def get_roles(user_id: int)->list:
        """
        Returns a list with the id of the roles of the user
        """
        roles = User_Institution_Role.query.filter_by(user_id=user_id).all()
        role_ids = [role.role_id for role in roles]
        return role_ids

    def change_role(self, new_role_id: int):
        """
        Changes the role of the user in the institution
        """
        self.role_id = new_role_id