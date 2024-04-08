import argparse
import roro_config.config as config
import roro_user.basic as user_basic
import roro_user.master as user_master
import roro_user.common as user_common
import roro_print.rprint as rprint
import roro_logs.logs as logs
import sys

def get(options: dict, json_config_file: dict):  
    
    if  options.get("resource") != None:
        
        if options.get("resource") == "user" or options.get("resource") == "user-mfa":
        
            if options.get("username") == None:
                rprint.print_user_invalid_flags()
                
            if options.get("resource") == "user-mfa":
                user_basic.get_user_mfa(options.get("username"), json_config_file)
            else:
                user_basic.get_user_info(options.get("username"), json_config_file, True) 
                    
        elif options.get("resource") == "roles":
            
            if options.get("username") == None:
                rprint.print_user_invalid_flags()
            
            user_basic.get_name_roles(options.get("username"), json_config_file)
        
        elif options.get("resource") == "session":
            user_common.get_session(json_config_file, options.get("serial-number"))
            
def configure(options: dict, json_config_file: dict):
    if  options.get("resource") != None and options.get("resource") == "profile":
        if options.get("profile") == None and options.get("tags") == None:
            rprint.print_invalid_configure_flags()
        
        config.set_profile_aws(options.get("profile"), json_config_file)
        config.set_tags_project(options.get("profile-tags"), json_config_file)
        
        logs.create_log_group(json_config_file)

def set(options: dict, json_config_file: dict):
    if  options.get("resource") != None and options.get("resource") == "user-mfa":
        if options.get("username") == None or options.get("serial-number") == None or options.get("code1") == None or options.get("code2") == None:
            print("[*] Habilitando MFA Device.")
            print("!!! Utilice los flags para introducir los datos necesarios ")
            sys.exit(0) 
        
        user_basic.enable_mfa_device(options.get("username"), options.get("serial-number"), options.get("code1"), options.get("code2"), json_config_file)

def create(options: dict, json_config_file: dict):
    
    if options.get("resource") == "user":
        if options.get("username") == None or options.get("tags") == None:
            rprint.print_user_invalid_flags()
            
        user_master.create_user(json_config_file, options.get("username"), options.get("tags"))
        
def help_parser_args():
    
    parser = argparse.ArgumentParser(prog='roro')
    parser.add_argument("action", type=str, nargs='?', help="Realizamos acciones sobre objetos del sistema y AWS", choices=['create', 'get', 'configure', 'set'])
    parser.add_argument("resource", type=str, nargs='?', help="Recuperar informacion", choices=['session', 'user', 'user-mfa', 'roles', 'profile', 'tags'])
    parser.add_argument("--username", "-u", dest="username", help="Nombre de usuario", required=False)
    parser.add_argument("--tags", "-t", metavar="Key=a,Value=b;Key=c,Value=d", dest="tags", help="Tags para el usuario", required = False)
    parser.add_argument("--serial-number", "-sn", dest="serial-number", help="MFA Device", required=False)
    parser.add_argument("--profile-aws", "-pa", dest="profile", help="Perfil AWS CLI", required=False)
    parser.add_argument("--profile-tags", "-pt", dest="profile-tags", help="Tags proyecto de trabajo", required=False)
    
    try:
        args = parser.parse_args()
        options = vars(args)    
    except Exception as e:
        parser.print_help()
        sys.exit(0)
        
    return options
    
if __name__ == '__main__':
    
    options = help_parser_args()    
    json_config_file = config.prepare_config(options.get("action"))
               
    if options.get("action") == "get":
        get(options, json_config_file)
    elif options.get("action") == "configure":
        configure(options, json_config_file)
    elif options.get("action") == "set":
        set(options, json_config_file)
    elif options.get("action") == "create":
        create(options, json_config_file)