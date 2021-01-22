import boto3
import json

class AWSSNS():
    def __init__(self,AccessKey,SecretKey):
        self.AccessKey = AccessKey
        self.SecretKey = SecretKey
    
    def AWSSNSAPICall(self,**Event):
        # #sets up the AWS SNS parameters
        #creating SNS client.
        EventPassed = {
            "summary": Event['summary'],
            "startOfEvent":Event['startOfEvent'],
            "endOfEvent":Event['endOfEvent']
        }
        Event_data = {
            "sms": "default",
            "EventPassed": json.dumps(EventPassed)
        }
        client = boto3.client("sns",aws_access_key_id = self.AccessKey, aws_secret_access_key = self.SecretKey,region_name = "us-east-1")
        client.publish(PhoneNumber = '+1347-399-1639',Message = json.dumps(Event_data),MessageStructure = 'json')