import sys

def print_valid_roles_user(roles: dict):
    print("[*] -> Roles disponibles para tu perfil")
    for role in roles['Roles']:
        print("--- Role : {0}".format(role['RoleName']))
        
def print_user_info(user_info: dict):
    user_info = user_info['User']
    
    print("[*] Informacion de usuario")
    print("--- UserName : {0}, UserId : {1}".format(user_info['UserName'], user_info['UserId']))
    print("--- ARN : {0}".format(user_info['Arn']))
    print("[*] Tags : ")
    for tag in user_info['Tags']:
        print("-- Key : {0}, Value = {1}".format(tag['Key'], tag['Value']))    

def print_user_invalid_flags():
    print("[*] Recuperando informacion del usuario")
    print("!!! Debe especificar flags validos para recuperar informacion del usuario")
    sys.exit(0)

def print_invalid_configure_flags():
    print("[*] Configurando profile y tags para entorno de trabajo")
    print("!!! Utilice los flags para introducir los datos necesarios ")
    sys.exit(0)
    
def print_denied_session():
    print("[*] Comprobando sesion temporal")
    print("!!! Sesion caducada. Vuelva a solicitar una sesion valida")
    sys.exit(0)

def print_invalid_user():
    print("[*] Creando claves de acesso")
    print("!!! Es necesario indicar un usuario")
    sys.exit(0)