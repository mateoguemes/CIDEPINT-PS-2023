from datetime import datetime
from src.models.database import db
from src.models.role_permission import Role_Permission

class Role(db.Model):
    __tablename__="roles"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    name = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,name):
        self.name=name
        db.session.add(self)
        db.session.commit()

    def get_permissions(role_in_institution_id:int)->list:
        """
        Returns a list of permissions of the role with the given id.
        """
        permissions = []
        permissions = Role_Permission.get_permissions(role_in_institution_id)
        return permissions
    
    @classmethod
    def get_all_posibilities(cls)->list:
        """
        Returns a list of all the possible roles
        """
        return Role.query.filter(Role.name != "super admin").distinct(Role.name).all()