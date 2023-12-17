from werkzeug.security import generate_password_hash
import random
from src.models.database import db
from src.models.user import User
from src.models.role import Role
from src.models.institution import Institution
from src.models.user_institution import User_Institution
from src.models.user_institution_role import User_Institution_Role

def run(institutions, roles):
    # Debe recibir al menos 1 rol y al menos 1 institución
    create_super_user()  # Creo un superusuario con CIDEPINT
    users = create_users()
    for user in users:
        index_institution = random.randint(0, len(institutions) - 1)
        index_role = random.randint(0, len(roles) - 1)
        relationship_user_institution(user, institutions[index_institution], roles[index_role])

def create_super_user():
    super_admin = User(
        name="Jeremías",
        lastname="Pretto",
        confirmed=True,
        password=generate_password_hash("contra123"),
        username="jere",
        email="jere@gmail.com",
        active=True
    )
    db.session.add(super_admin)
    db.session.commit()
    super_admin_institution = Institution.query.filter_by(name="CIDEPINT").first()
    relation = User_Institution(super_admin.id, super_admin_institution.id)
    db.session.add(relation)
    db.session.commit()

    super_admin_role = Role.query.filter_by(name="super admin").first()
    relation_with_role = User_Institution_Role(super_admin.id, super_admin_institution.id, super_admin_role.id)
    db.session.add(relation_with_role)
    db.session.commit()

def create_users():
    users = []
    first = User(
        name="Rafael",
        lastname="Gomez",
        confirmed=True,
        password=generate_password_hash("rafa123"),
        username="rafa",
        email="rafa22nov@gmail.com",
        active=True
    )
    db.session.add(first)
    db.session.commit()

    second = User(
        name="Luciana",
        lastname="Lamella",
        confirmed=True,
        password=generate_password_hash("luciana123"),
        username="luli",
        email="luciana@gmail.com",
        active=True
    )
    db.session.add(second)
    db.session.commit()

    third = User(
        name="Mateo",
        lastname="Fachero",
        confirmed=True,
        password=generate_password_hash("mate123"),
        username="mate_dale_lobo",
        email="mate@gmail.com",
        active=True
    )
    db.session.add(third)
    db.session.commit()

    fourth = User(
        name="Catalina",
        lastname="Zuppa",
        confirmed=True,
        password=generate_password_hash("cata123"),
        username="catcuqui",
        email="cata@gmail.com",
        active=True
    )
    db.session.add(fourth)
    db.session.commit()

    users.append(User.query.filter_by(email="rafa22nov@gmail.com").first())
    users.append(User.query.filter_by(email="luciana@gmail.com").first())
    users.append(User.query.filter_by(email="cata@gmail.com").first())
    users.append(User.query.filter_by(email="mate@gmail.com").first())

    return users

def relationship_user_institution(user, institution, role):
    relation = User_Institution(user.id,institution.id)
    db.session.add(relation)
    db.session.commit()
    relation_with_role = User_Institution_Role(user.id, institution.id, role.id)
    db.session.add(relation_with_role)
    db.session.commit()