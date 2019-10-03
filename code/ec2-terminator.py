import boto3
import os
from datetime import datetime, timedelta


def get_session(region, access_id, secret_key):
    return boto3.session.Session(region_name=region,
                                aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key)

def calcDesiredInstanceCount(lbname):
    desiredCount=0
    session_ASG = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    asg_client = session_ASG.client('autoscaling')
    all_asg_groups = asg_client.describe_auto_scaling_groups()
    
    for asg_group in all_asg_groups['AutoScalingGroups']:
        if asg_group['LoadBalancerNames']:
            print("asg: ",asg_group['AutoScalingGroupName'], " assigned to loadbalancer: ",asg_group['LoadBalancerNames'][0], " with desired instance count of: ",asg_group['DesiredCapacity'])
            desiredCount+=asg_group['DesiredCapacity']

    return desiredCount

def lambda_handler(event, context):
    
    session = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    session_elb = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    session_ssm = get_session(os.getenv('AWS_DEFAULT_REGION'), os.getenv('ACCESS_KEY_ID'),os.getenv('SECRET_KEY'))
    
    dry_run_string = os.getenv('DRY_RUN',True)
    dry_run = True if dry_run_string.lower() == 'true' else False
    lb_name = os.getenv('LB_NAME','')
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dt_oldest = datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
    id2terminate = 0
    healthy_instances = 0
    ec2_client = session.client('ec2')
    elb_client = session_elb.client('elb')    
    
    desired_instance_count = calcDesiredInstanceCount(lb_name)
    print("desired instance count behind lb '",lb_name, "' is: ",desired_instance_count)

    instancehealthlist = elb_client.describe_instance_health(LoadBalancerName=lb_name)
    for instance in instancehealthlist['InstanceStates']:
        id = instance['InstanceId']
        state = instance['State']
        if 'InService' != state:
            print("WARNING: instance ",id," not 'InService', but in state: ",state," !")
        else:
            healthy_instances+=1
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
    
    ###
    # terminate oldest instance
    ###
    if healthy_instances >= desired_instance_count:
        instance2terminate = ec2_client.terminate_instances(InstanceIds=[id2terminate,],DryRun=dry_run)
        print("Terminating instance: ",instance2terminate)
        return "instance terminated"
    else:
        return "not enough healthy instances, instance termination skipped !"