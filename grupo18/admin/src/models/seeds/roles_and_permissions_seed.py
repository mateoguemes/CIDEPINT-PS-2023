from src.models.permission import Permission
from src.models.role import Role
from src.models.role_permission import Role_Permission

def run():
    create_permissions()
    roles = create_roles()
    relationship_role_permission(roles)
    return roles

def create_permissions():
    permission_names = [
        "user_index", "user_update", "user_destroy", "user_show", "user_search", "user_block",
        "institution_index", "institution_create", "institution_update", "institution_destroy", "institution_show", "institution_activate",
        "user_institution_index", "user_institution_create", "user_institution_update", "user_institution_destroy",
        "service_index", "service_create", "service_update", "service_destroy", "service_show",
        "requirement_index", "requirement_update", "requirement_destroy", "requirement_show",
        "configuration_show", "configuration_update"
    ]
    # Se crean en la BD
    permissions = []
    for name in permission_names:
        permission = Permission(name)
        permissions.append(permission)
    return permissions

def create_roles():
    Role("super admin")
    role_names = ["Operador", "Administrador", "Dueño"]
    # Se crean en la BD
    roles = []
    for name in role_names:
        role = Role(name)
        roles.append(role)
    return roles

def relationship_role_permission(roles):
    # No le agrego permisos al super dado que algorítmicamente, si el rol es super admin, el usuario puede hacer todo
    operator = Role.query.filter_by(name="Operador").first()
    admin = Role.query.filter_by(name="Administrador").first()
    owner = Role.query.filter_by(name="Dueño").first()

    for role in roles:
        Role_Permission(operator.id, Permission.query.filter_by(name="user_show").first().id)  # Todos ven su perfil
        Role_Permission(operator.id, Permission.query.filter_by(name="institution_show").first().id)  # Todos ven la info de la institucion
        
    # Es tedioso y manual, pero me parece más personalizable definir cada permiso específico de cada rol. Si
    # el día de mañana los permisos en común cambian y toda la asignación la hice en un for que recorre
    # los roles preguntando por su nombre, puede ser muy difícil ajustarlo. De esta manera es más claro

    # OPERATOR
    # Services
    Role_Permission(operator.id, Permission.query.filter_by(name="service_index").first().id)
    Role_Permission(operator.id, Permission.query.filter_by(name="service_create").first().id)
    Role_Permission(operator.id, Permission.query.filter_by(name="service_update").first().id)
    Role_Permission(operator.id, Permission.query.filter_by(name="service_show").first().id)
    # Requirements
    Role_Permission(operator.id, Permission.query.filter_by(name="requirement_index").first().id)
    Role_Permission(operator.id, Permission.query.filter_by(name="requirement_update").first().id)
    Role_Permission(operator.id, Permission.query.filter_by(name="requirement_show").first().id)

    # ADMIN
    # Users of the institution
    Role_Permission(admin.id, Permission.query.filter_by(name="user_institution_index").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="user_institution_update").first().id)
    # Services
    Role_Permission(admin.id, Permission.query.filter_by(name="service_index").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="service_create").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="service_update").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="service_show").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="service_destroy").first().id)
    # Requirements
    Role_Permission(admin.id, Permission.query.filter_by(name="requirement_index").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="requirement_update").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="requirement_destroy").first().id)
    Role_Permission(admin.id, Permission.query.filter_by(name="requirement_show").first().id)

    # OWNER
    # Users of the institution
    Role_Permission(owner.id, Permission.query.filter_by(name="user_institution_index").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="user_institution_create").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="user_institution_destroy").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="user_institution_update").first().id)
    # Services
    Role_Permission(owner.id, Permission.query.filter_by(name="service_index").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="service_create").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="service_update").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="service_show").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="service_destroy").first().id)
    # Requirements
    Role_Permission(owner.id, Permission.query.filter_by(name="requirement_index").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="requirement_update").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="requirement_destroy").first().id)
    Role_Permission(owner.id, Permission.query.filter_by(name="requirement_show").first().id)