import json
import os
import sys

DIR_CONFIG = "C:\\Users\\{0}\\.roro".format(os.environ['USERNAME'])
TMP_CONFIG = "tmp"
FILE_CONFIG = "config.json"

PARAMETER_STORE_TEMPORARY = "/config/temporary/serial-number"
LOG_GROUP_USER_MASTER = "create-user-master-log-group"
LOG_STREAM_USER_MASTER = "create-user-master-log-stream"

def load_config():
    
    json_config_file = {}
    
    with open("{0}\\{1}".format(DIR_CONFIG, FILE_CONFIG), "r") as file:
        json_config_file = json.loads(file.read(), cls=json.JSONDecoder)
    
    return json_config_file

def create_config():
    
    with open("{0}\\{1}".format(DIR_CONFIG, FILE_CONFIG), "w") as outfile:
        outfile.write(json.dumps({}, cls=json.JSONEncoder))

def save_config(json_config_file: dict):
      
    with open("{0}\\{1}".format(DIR_CONFIG, FILE_CONFIG), "w") as outfile:
        outfile.write(json.dumps(json_config_file, cls=json.JSONEncoder))
        
def prepare_config(action: str):
    
    if os.path.exists("{0}\\{1}".format(DIR_CONFIG, FILE_CONFIG)):
        json_config_file = load_config()
    else:
        
        if action != "configure":
            print("[*] Preparando entorno de trabajo")
            print("!!! Utilice la opcion 'configure' con los flags de profile-aws y profile-tags")
            sys.exit(0)
        
        os.mkdir(DIR_CONFIG)
        os.mkdir("{0}\\{1}".format(DIR_CONFIG, TMP_CONFIG))
        create_config()
        json_config_file = load_config()
    
    return json_config_file

def set_profile_aws(profile: str, json_config_file: dict):
    
    print("[*] Tags definidos para el entorno de trabajo")
    print("--- AWS_PROFILE : {}".format(profile))
    
    json_config_file["aws_profile"] = profile
    save_config(json_config_file)

def set_tags_project(tags: str, json_config_file: dict):
    
    tags_project = {}
    arr_tag = tags.split(',')
    
    key = arr_tag[0].split('=')[1]
    value = arr_tag[1].split('=')[1]
    
    tags_project["Key"] = key
    tags_project["Value"] = value
    
    print("[*] Tags definidos para el entorno de trabajo")
    print("--- Key : {0}, Value : {1}".format(key, value))
     
    json_config_file['tags'] = tags_project
    save_config(json_config_file)