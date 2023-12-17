from datetime import datetime
from src.models.database import db
from src.models.permission import Permission

class Role_Permission(db.Model):
    __tablename__ = "role_permissions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False) #FOREIGN KEY
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,role_id,permission_id):
        self.role_id=role_id
        self.permission_id=permission_id
        db.session.add(self)
        db.session.commit()

    def get_permissions(role_id: int)->list:
        """
        Returns a list of all the permissions of a role.
        """
        permissions_ids = [row.permission_id for row in Role_Permission.query.filter_by(role_id=role_id).all()] # me devuelve una lista de permissions_id
        return Permission.get_names(permissions_ids) # para obtener los nombres de esos permisos
