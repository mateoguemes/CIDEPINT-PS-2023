from src.models.institution import Institution
from src.models.institution_service import Institution_Service
from src.models.institution_keyword import Institution_Keyword
from src.models.service import Service
from src.models.service import ServiceType
from src.models.service_keyword import Service_Keyword
from src.models.keyword import Keyword
from src.models.database import db

def run():
    institutions = create_institutions()
    services = create_services()
    institution_keywords = create_keywords("pintura", "experiencia", "investigación", "consultoría")
    service_keyword = create_keywords("pintura", "rápido", "cuotas", "consultoría", "investigación")
    relationship_institution_services(institutions[0], services)  # aquí es el error
    relationship_institution_keywords(institutions[1], institution_keywords)
    relationship_service_keywords(services[0], service_keyword)
    return institutions

def create_institutions():
    institutions = []
    # la institución del super admin
    super = Institution(
        name ="CIDEPINT",
        information ="super admin",
        address ="super admin",
        location ="super admin",
        website = "super admin",
        opening_hours = "super admin",
        contact = "super admin"
    )
    # una habilitada con servicios y sin palabras clave
    first = Institution(
        name = "Laboratorios FEMEBA",
        information = "Laboratorio privado con 50 años de experiencia",
        address = "7 y 50 n° 226",
        location = "-34.9137405,-57.9493383",
        website = "www.laboratorio_femeba.com.ar",
        opening_hours = "de lunes a viernes, 8:00 a 17:00",
        contact = "femeba@gmail.com"
    )
    # otra habilitada sin servicios y con palabras clave
    second = Institution(
        name ="Pinturas Leónidas",
        information = "Somos el centro de investigación, fabricación e innovación en pinturas número 1 de Córdoba Capital",
        address = "Schiaretti al 1925",
        location = "-31.4067058,-64.222794",
        website ="www.leonidas_pinturas.com.ar",
        opening_hours = "de lunes a lunes, 7:00 a 22:00",
        contact = "leonidas_pinta@gmail.com"
    )
    db.session.add(super)
    db.session.commit()
    db.session.add(first)
    db.session.commit()
    db.session.add(second)
    db.session.commit()

    institutions.append(Institution.query.filter_by(name="Laboratorios FEMEBA").first())
    institutions.append(Institution.query.filter_by(name="Pinturas Leónidas").first())
    return institutions

def create_services():
    services = []
    first = Service(
        "Nuevo color personalizado",
        "Se realiza a pedido un color especificado por el cliente si este no se encuentra en nuestro catálogo",
        ServiceType.DEVELOPMENT, True
    )
    second = Service(
        "Análisis de la calidad de una pintura",
        "Se provee un análisis detallado del insumo que provee el cliente (duración, adhesión, resistencia a condiciones climáticas extremas, etc)",
        ServiceType.ANALYSIS, False
    )
    db.session.add(first)
    db.session.commit()
    db.session.add(second)
    db.session.commit()
    services.append(Service.query.filter_by(name="Nuevo color personalizado").first())
    services.append(Service.query.filter_by(name="Análisis de la calidad de una pintura").first())
    return services

def relationship_institution_services(institution, services):
    for service in services:
        db.session.add(Institution_Service(institution.id, service.id))
        db.session.commit()

def relationship_institution_keywords(institution, keywords):
    for keyword in keywords:
        db.session.add(Institution_Keyword(institution.id, keyword.id))
        db.session.commit()

def relationship_service_keywords(service, keywords):
    for keyword in keywords:
        db.session.add(Service_Keyword(service.id, keyword.id))
        db.session.commit()

def create_keywords(*args):
    keywords = []
    for arg in args:
        was_created = Keyword.query.filter_by(name=arg).first()
        if not was_created:
            was_created = Keyword(arg)
        db.session.add(was_created)
        db.session.commit()
        keywords.append(was_created)
    return keywords
