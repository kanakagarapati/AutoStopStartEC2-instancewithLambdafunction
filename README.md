# AutoStopStartEC2-instancewithLambdafunction

# 🖥️ Automated EC2 Instance Start/Stop using AWS Lambda and Boto3

This project demonstrates how to use AWS Lambda with Python (Boto3) to automatically start and stop EC2 instances based on custom tags. It's useful for managing compute costs by automating resource usage schedules.

---

## 📌 Objective

Automatically start or stop EC2 instances based on their tags using a Lambda function triggered manually or on a schedule.

---

## ⚙️ Setup Instructions

### ✅ 1. Create Two EC2 Instances
- Launch two `t2.micro` instances in **us-west-2**
- Tag them as follows:

| Instance Name              | Tag Key       | Tag Value   |
|----------------------------|---------------|-------------|
| KanakaManoj-Instance1      | `ActionManoj` | `Auto-Stop` |
| KanakaManoj-Instance2      | `ActionManoj` | `Auto-Start` |
'KanakaManoj-Instance1' in start mode
![image](https://github.com/user-attachments/assets/de64e281-0d3a-42cf-9421-3d6fb548594b)
![image](https://github.com/user-attachments/assets/ca185da4-3e51-431f-9f36-4b2c15202244)

'KanakaManoj-Instance2' in stop mode
![image](https://github.com/user-attachments/assets/92801f12-92d0-491a-9795-50054e688161)
![image](https://github.com/user-attachments/assets/8a733226-852d-4673-8219-6dee930d7713)

![image](https://github.com/user-attachments/assets/a99f65b7-7201-4c31-908c-ddb8d73d5220)

Ensure:
- One instance is in `running` state (to stop)
- The other is in `stopped` state (to start)

---

### ✅ 2. IAM Role for Lambda

Create a new IAM role named: **KanakaManojLambdaEC2ManageRole**
![image](https://github.com/user-attachments/assets/e57f44f2-f62e-422e-ae53-b75ae017ed92)

Attach the following AWS-managed policy:
- `AmazonEC2FullAccess`
![image](https://github.com/user-attachments/assets/3853c533-d49c-494e-a64b-9b6aec8139d6)


This will grant Lambda full access to describe, start, and stop EC2 instances.

---

### ✅ 3. Lambda Function Configuration

- **Region**: Can be any region, but must point to `us-west-2` via code
- **Runtime**: Python 3.11
- **Handler**: `KanakaManoj-ManageEC2-Instances`
- **Deploy Code**: Use inline editor or upload ZIP
![image](https://github.com/user-attachments/assets/c6cd171a-d29b-4c50-a7ea-d7acaa52ce13)

![image](https://github.com/user-attachments/assets/f8daacf9-4e1b-44eb-ba22-cdbe90aea89b)


```python
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

    stop_instances = get_instance_ids_by_action('Auto-Stop')
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped instances: {stop_instances}")
    else:
        print("No instances to stop.")

    start_instances = get_instance_ids_by_action('Auto-Start')
    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started instances: {start_instances}")
    else:
        print("No instances to start.")
```

---

## 🧪 Testing

1. Go to the Lambda console
2. Click **Test** and create a new test event with `{}` as input
3. View logs:
   - Started/Stopped instance IDs
   - Or messages like: `No instances to stop`
![image](https://github.com/user-attachments/assets/f37da4ed-06dd-4652-8c86-44df9383d760)

after running function it auto stoped running instance and auto started stoped instance
![image](https://github.com/user-attachments/assets/90487ebd-3cc3-42b5-9d39-f58c331b0cea)

---



## 📂 Files

- `lambda_function.py` – Lambda function code
- `ManageEC2LambdaPackage_Updated.zip` – Uploadable zip
- IAM Role: `KanakaManojLambdaEC2ManageRole`
- IAM Policy: `AmazonEC2FullAccess` (attached to Lambda role)

---

## 👨‍💻 Author

**Kanaka Manoj Garapati**  
Feel free to fork and modify for your own automation needs!
