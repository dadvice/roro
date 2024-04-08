import boto3
import botocore
import roro_config.config as config
import roro_print.rprint as rprint

def get_session(json_config_file: dict, serial_number: str):
    
    print("[*] Iniciando sesion temporal. Duracion 1h")
    token_code = input("??? Token Code ")
    
    sts_client = boto3.Session(profile_name=json_config_file['aws_profile']).client("sts")
    response = sts_client.get_session_token(DurationSeconds=3600, SerialNumber=serial_number,TokenCode=token_code)
    
    json_config_file["sts"] = dict()
    json_config_file["sts"]["access_key_id"] = response["Credentials"]["AccessKeyId"]
    json_config_file["sts"]["secret_access_key"] = response["Credentials"]["SecretAccessKey"]
    json_config_file["sts"]["session_token"] = response["Credentials"]["SessionToken"]
    config.save_config(json_config_file)
    
    print("AWS_ACCESS_KEY_ID={0}".format(response["Credentials"]["AccessKeyId"]))
    print("AWS_SECRET_ACCESS_KEY={0}".format(response["Credentials"]["SecretAccessKey"]))
    print("AWS_SESSION_TOKEN={0}".format(response["Credentials"]["SessionToken"]))

def get_client_iam_profile(json_config_file: dict):
    return boto3.Session(profile_name=json_config_file['aws_profile']).client("iam")

def get_client_iam_session(json_config_file: dict):
    try:
        return boto3.Session(aws_access_key_id=json_config_file["sts"]["access_key_id"], 
                               aws_secret_access_key=json_config_file["sts"]["secret_access_key"],
                               aws_session_token=json_config_file["sts"]["session_token"]).client("iam")
    except botocore.exceptions.ClientError:
        rprint.print_denied_session()

def get_client_ssm_session(json_config_file: dict):
    try:
        return boto3.Session(aws_access_key_id=json_config_file["sts"]["access_key_id"], 
                               aws_secret_access_key=json_config_file["sts"]["secret_access_key"],
                               aws_session_token=json_config_file["sts"]["session_token"]).client("ssm")
    except botocore.exceptions.ClientError:
         rprint.print_denied_session()