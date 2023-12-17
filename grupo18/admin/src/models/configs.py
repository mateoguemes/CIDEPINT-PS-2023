# src/models/configs.py
from src.models.database import db

class Config(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    per_page = db.Column(db.Integer, nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
    maintenance_mode = db.Column(db.Boolean, nullable=False, default=False)
    maintenance_message = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_config(cls):
        """
        Returns the config data.
        """
        config = cls.query.first()
        if config:
            return {
                'per_page': config.per_page,
                'contact_info': str(config.contact_info),
                'maintenance_mode': config.maintenance_mode,
                'maintenance_message': config.maintenance_message,
            }


    @classmethod
    def update_config(cls, data: dict):
        """
        Updates the web config given the form.
        """
        config = cls.query.first()
        config.per_page = data.get('per_page', config.per_page)
        config.contact_info = data.get('contact_info', config.contact_info)
        config.maintenance_mode = data.get('maintenance_mode', config.maintenance_mode)
        config.maintenance_message = data.get('maintenance_message', config.maintenance_message)
        db.session.commit()

