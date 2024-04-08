import boto3
import roro_config.config as config
import time

seq_token_code = ""

def create_log_group(json_config_file: dict):
    
    logs_client = boto3.Session(profile_name=json_config_file["aws_profile"]).client("logs")
    
    try:
        logs_client.create_log_group(logGroupName=config.LOG_GROUP_USER_MASTER)
        logs_client.create_log_stream(logGroupName=config.LOG_GROUP_USER_MASTER, logStreamName=config.LOG_STREAM_USER_MASTER)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        print("!!! Log Group [{0}] ya existe".format(config.LOG_GROUP_USER_MASTER))

def put_log_event(json_config_file: dict, message: str):
    
    event = dict()
    event["timestamp"] = int(time.time() * 1000)
    event["message"] = message
    
    print(event)
    
    logs_client = boto3.Session(profile_name=json_config_file["aws_profile"]).client("logs")
    if len(seq_token_code) == 0:   
        response = logs_client.put_log_events(logGroupName=config.LOG_GROUP_USER_MASTER, logStreamName=config.LOG_STREAM_USER_MASTER, logEvents=[event])
        print(response)
    else:
        response = logs_client.put_log_events(logGroupName=config.LOG_GROUP_USER_MASTER, logStreamName=config.LOG_STREAM_USER_MASTER, logEvents=[event], seq_token_code=json_config_file['seq_token_code_user_master'])
        
    json_config_file['seq_token_code_user_master'] = response['nextSequenceToken']
    config.save_config(json_config_file)