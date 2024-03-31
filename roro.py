import argparse
import roro_config.config as config
import roro_user.basic as user_basic
import sys

def get(options: dict, json_config_file: dict):  
    
    if  options.get("resource") != None:
        
        if options.get("resource") == "user" or options.get("resource") == "user-mfa":
        
            if options.get("username") == None:
                print("*** Debe especificar flags validos para recuperar informacion del usuario")
                sys.exit(0)
                
            if options.get("resource") == "user-mfa":
                user_basic.get_user_mfa(options.get("username"), json_config_file)
            else:
                user_basic.get_user_info(options.get("username"), json_config_file, True) 
                    
        elif options.get("resource") == "roles":
            
            if options.get("username") == None:
                print("*** Debe especificar flags validos para recuperar informacion del usuario")
                sys.exit(0)
            
            user_basic.get_name_roles(options.get("username"), json_config_file)
            
def configure(options: dict, json_config_file: dict):
    if  options.get("resource") != None and options.get("resource") == "profile":
        if options.get("profile") == None and options.get("tags") == None:
            print("[*] Configurando profile y tags para entorno de trabajo")
            print("!!! Utilice los flags para introducir los datos necesarios ")
            sys.exit(0) 
        
        config.set_profile_aws(options.get("profile"), json_config_file)
        config.set_tags_project(options.get("tags"), json_config_file)

def set(options: dict, json_config_file: dict):
    if  options.get("resource") != None and options.get("resource") == "user-mfa":
        if options.get("username") == None or options.get("serial-number") == None or options.get("code1") == None or options.get("code2") == None:
            print("[*] Habilitando MFA Device.")
            print("!!! Utilice los flags para introducir los datos necesarios ")
            sys.exit(0) 
        
        user_basic.enable_mfa_device(options.get("username"), options.get("serial-number"), options.get("code1"), options.get("code2"), json_config_file)
         
def help_parser_args():
    
    parser = argparse.ArgumentParser(prog='roro')
    parser.add_argument("action", type=str, nargs='?', help="Realizamos acciones sobre objetos del sistema y AWS", choices=['get', 'configure', 'set'])
    parser.add_argument("resource", type=str, nargs='?', help="Recuperar informacion", choices=['user', 'user-mfa', 'roles', 'profile', 'tags'])
    parser.add_argument("--username", "-u", dest="username", help="Nombre de usuario", required=False)
    parser.add_argument("--serial-number", "-sn", dest="serial-number", help="MFA Device", required=False)
    parser.add_argument("--token-code1", "-code1", dest="code1", help="Token Code App", required=False)
    parser.add_argument("--token-code2", "-code2", dest="code2", help="Token Code App", required=False)
    parser.add_argument("--profile-aws", "-p", dest="profile", help="Perfil AWS CLI", required=False)
    parser.add_argument("--profile-tags", "-t", dest="tags", help="Tags proyecto de trabajo", required=False)
    args = parser.parse_args()
    options = vars(args)
    
    return options
    
if __name__ == '__main__':
    
    options = help_parser_args()    
    json_config_file = config.prepare_config(options.get("action"))
           
    if options.get("action") != None and options.get("action") == "get":
        get(options, json_config_file)
    elif options.get("action") != None and options.get("action") == "configure":
        configure(options, json_config_file)
    elif options.get("action") != None and options.get("action") == "set":
        set(options, json_config_file)