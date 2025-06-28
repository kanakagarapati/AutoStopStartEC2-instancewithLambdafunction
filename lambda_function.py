import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-west-2')

    def get_instance_ids_by_action(action_value):
        response = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:ActionManoj', 'Values': [action_value]},
                {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
            ]
        )
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])
        return instance_ids

    # Auto-Stop
    stop_instances = get_instance_ids_by_action('Auto-Stop')
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped instances: {stop_instances}")
    else:
        print("No instances to stop.")

    # Auto-Start
    start_instances = get_instance_ids_by_action('Auto-Start')
    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started instances: {start_instances}")
    else:
        print("No instances to start.")
