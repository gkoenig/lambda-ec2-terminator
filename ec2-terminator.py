import boto3
import os
from datetime import datetime, timedelta


def get_session(region, access_id, secret_key):
    return boto3.session.Session(region_name=region,
                                aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key)

def lambda_handler(event, context):
    
    session = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    session_elb = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    session_ssm = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dt_oldest = datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
    id2terminate = 0
    ec2_client = session.client('ec2')
    elb_client = session_elb.client('elb')    
    
    instancehealthlist = elb_client.describe_instance_health(LoadBalancerName=os.getenv('LB_NAME'))
    for instance in instancehealthlist['InstanceStates']:
        id = instance['InstanceId']
        state = instance['State']
        if 'InService' != state:
            return "WARNING: not all instances behind ELB are up !"
        
        ec2 = ec2_client.describe_instances(InstanceIds=[id,])
        for reservation in ec2['Reservations']:
            for instance_description in reservation['Instances']:
                launch_time = instance_description['LaunchTime']
                
        tmp_launch_time = launch_time.strftime('%Y-%m-%d %H:%M:%S')
        dt_launch_time = datetime.strptime(tmp_launch_time,'%Y-%m-%d %H:%M:%S')
        print("oldest timestamp: ",dt_oldest)
        print(f"InstanceId: ",id,", State: ",state,", launchedAt: ",dt_launch_time,".")
        if dt_launch_time < dt_oldest:
            dt_oldest = dt_launch_time
            id2terminate = id
            print("oldest timestamp has changed, now : ",dt_oldest, " of instance: ", id2terminate)
    print("all instances behind ELB are up !")
    
    ###
    # terminate oldest instance
    ###
    
    instance2terminate = ec2_client.terminate_instances(InstanceIds=[id2terminate,])
    return "instance terminated: ",instance2terminate