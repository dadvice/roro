import boto3
import botocore
import roro_config.config as config
import roro_logs.logs as logs
import roro_user.common as user_common
import roro_print.rprint as rprint
import sys

def create_user(json_config_file: dict, username: str, tags: list):
    
    try:
        aws_tags = []
        arr_tags = tags.split(";")
        for tag in arr_tags:
            aws_tag = tag.split(",")
            object = {}
            for tag_key_value in aws_tag:
                key_value = tag_key_value.split("=")
                object[key_value[0]] = key_value[1]
            aws_tags.append(object)
    except Exception as e:
        rprint.print_user_invalid_flags()
          
    iam_client = user_common.get_client_iam_session(json_config_file)
    response = iam_client.create_user(UserName=username, Tags=aws_tags)
    print("[*] Creando usuario")
    print("--- Usuario creado")
            
    serial_number = create_mfa_device(json_config_file, username)
    
    try:
        put_paramter_serial_number(json_config_file, username, serial_number)
        logs.put_log_event(json_config_file, "Usuario {0} creado con MFA temporal".format(username))
        
    except botocore.exceptions.ClientError:
        print("!!! Error producido en uno de los pasos de la creacion del usuario")
        print("!!! Eliminando el usuario ...")
        rollback_create_user(json_config_file, username, serial_number)
        
def create_mfa_device(json_config_file: dict, username: str):
    
    iam_client = user_common.get_client_iam_session(json_config_file)
    response = iam_client.create_virtual_mfa_device(VirtualMFADeviceName=username)
    print("--- Serial Number : {0}".format(response['VirtualMFADevice']['SerialNumber']))
    
    qr_username = "QRImage-{0}.png".format(username)
    qr_path = "{0}\\{1}\\{2}".format(config.DIR_CONFIG, config.TMP_CONFIG, qr_username)
    with open(qr_path, "wb") as outfile:
        outfile.write(response['VirtualMFADevice']['QRCodePNG'])
        
    print("--- QR Image exportado : {0}", qr_path)
    
    return response['VirtualMFADevice']['SerialNumber']

def put_paramter_serial_number(json_config_file: dict, username: str, serial_number: str):
    ssm_client = user_common.get_client_ssm_session(json_config_file)
    ssm_client.put_parameter(Name="{0}/{1}".format(config.PARAMETER_STORE_TEMPORARY, username), Value=serial_number,Type="SecureString",Tier="Standard")

def delete_mfa_device(json_config_file: dict, serial_number: str):
    iam_client = user_common.get_client_iam_session(json_config_file)
    iam_client.delete_virtual_mfa_device(SerialNumber=serial_number)

def delete_user(json_config_file: dict, username: str):
     iam_client = user_common.get_client_iam_session(json_config_file)
     iam_client.delete_user(UserName=username)

def delete_parameter_serial_number(json_config_file: dict, username: str):
    ssm_client = user_common.get_client_ssm_session(json_config_file)
    ssm_client.delete_parameter(Name="{0}/{1}".format(config.PARAMETER_STORE_TEMPORARY, username))

def rollback_create_user(json_config_file: dict, username: str, serial_number: str):
    delete_parameter_serial_number(json_config_file, username)
    delete_mfa_device(json_config_file, serial_number)
    delete_user(json_config_file, username)
    logs.put_log_event(json_config_file, "Usuario {0} creado con MFA temporal, eliminado".format(username))
    print("!!! Usuario eliminado")
    sys.exit(0) 