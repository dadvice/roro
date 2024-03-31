import boto3
from pprint import pprint
import roro_print.rprint as rprint

PARAMETER_STORE_TEMPORARY = "/config/temporary/serial-number"

def get_user_info(username: str, json_config_file: dict, pretty_print: bool):
    print("[*] -> Recuperando informacion del usuario : {0}".format(username))
    
    iamClient = boto3.Session(profile_name = json_config_file.get("aws_profile")).client("iam")
    response = iamClient.get_user(UserName=username)
    
    if pretty_print:
        rprint.print_user_info(response)
    
    return response

def get_user_mfa(username: str, json_config_file: dict):
    session = boto3.Session(profile_name = json_config_file.get("aws_profile"))
    
    print("[*] -> Recuperando dispositivos mfa")
    iam_client = session.client("iam")
    response = iam_client.list_mfa_devices(UserName=username)
    
    if len(response['MFADevices']) > 0:
        for mfa in response['MFADevices']:
            print("--- Arn Serial Number : {}".format(mfa['SerialNumber']))
    else:
        print("[*] -> Recuperando dispositivo mfa temporal. No asociado a ningun usuario")
        ssm_client = session.client("ssm")
        response = ssm_client.get_parameter(Name="{0}/{1}".format(PARAMETER_STORE_TEMPORARY, username), WithDecryption=True)
        print("--- Arn Serial Number : {}".format(response['Parameter']['Value']))
   
def get_name_roles(username: str, json_config_file: dict):
    print("[*] -> Recuperando roles disponibles")
             
    user_info = get_user_info(username, json_config_file, False)
    arn_user = user_info['User']['Arn']
     
    iam_client = boto3.Session(profile_name = json_config_file.get("aws_profile")).client("iam")
    response = iam_client.list_roles()
    
    roles_print = {'Roles': []}
    for role in response['Roles']:
        assume_role_policy = str(role['AssumeRolePolicyDocument'])
         
        if assume_role_policy.__contains__(arn_user) == False:
            continue
         
        role_name = role['RoleName']
        role_tags = iam_client.list_role_tags(RoleName = role_name)
                  
        role_tags = list(map(lambda e: "{0}={1}".format(e['Key'], e['Value']), role_tags['Tags']))
        tag_profile = "{0}={1}".format(json_config_file['tags']['Key'], json_config_file['tags']['Value']) 
                         
        if role_tags.__contains__(tag_profile) == False:
             continue
         
        roles_print['Roles'].append(role)
         
    rprint.print_valid_roles_user(roles_print)
    
def enable_mfa_device(username: str, serial_number: str, token_code_one: int, token_code_two: int, json_config_file: dict):
    print("[*] -> Asociando MFA device al usuario {0}".format(username))
   
    iam_client = boto3.Session(profile_name = json_config_file.get("aws_profile")).client("iam")
    response = iam_client.enable_mfa_device(UserName=username, SerialNumber=serial_number, AuthenticationCode1=token_code_one, AuthenticationCode2=token_code_two)
    print(response)