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