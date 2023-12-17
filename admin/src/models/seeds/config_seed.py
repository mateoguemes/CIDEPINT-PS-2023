from src.models.configs import Config
from src.models.database import db

def run():
    config = Config(
        per_page=10,
        contact_info="CIDEPINT@MAINTANCE.COM.AR",
        maintenance_mode=False,
        maintenance_message="El sitio no está en mantenimiento"
    )
    db.session.add(config)
    db.session.commit()