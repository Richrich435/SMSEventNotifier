from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import date
import pickle
import json
import boto3
import csv

#this part connects the google calendar api to program
scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
flow = InstalledAppFlow.from_client_secrets_file("credentials.json",scopes = scopes)
credentialsflow = flow.run_console()

#this part is suppose to save the credentials of the Oauth method without having the sign in again. 
pickle.dump(credentialsflow, open("token.pkl","wb"))
credentials = pickle.load(open("token.pkl","rb"))
print(credentials)
#obtains the calendar object from the provided credentials and returns a list of calendars
service = build("calendar","v3",credentials = credentials)
returnedCalendars = service.calendarList().list().execute() # pylint: disable=maybe-no-member
print(json.dumps(returnedCalendars, indent= 2))

calendarName = input("Enter the name of the calendar you want to be notified with ")

calendarID = ""
for i in range(len(returnedCalendars)):
    if returnedCalendars['items'][i]['summary'] == calendarName:
        calendarID = returnedCalendars['items'][i]['id']
    else:
        continue
    
print(calendarID)

getEvent = service.events().list(calendarId = calendarID, showDeleted = False,orderBy = 'updated').execute() # pylint: disable=maybe-no-member
print("THIS IS THE EVENT LIST")
print(json.dumps(getEvent, indent = 2))

currentDate = date.today()
startdateOfEvent = ""
enddateOfEvent = ""
for event in range(len(getEvent['items'])):
    currentEvent = getEvent['items'][event]
    try:
        print("\nTHIS EVENT:")
        print(currentEvent['start']['dateTime'].split('T')[0])
        startdateOfEvent = currentEvent['start']['dateTime'].split('T')[0]
        enddateOfEvent = currentEvent['end']['dateTime'].split('T')[0]
    except KeyError as keyError: 
        continue

if(currentDate == startdateOfEvent):
    #send the SMS message
    print("Great")
else: 
    print("Cant find date")

#sets up the AWS SNS parameters
AccessKey = " "
SecretKey = " "
with open('rootkey.csv', newline = '') as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader: 
        print(row['AccessKey'] + " = " + row['Info'])
        if(row['AccessKey'] == "AWSAccessKeyId"):
            AccessKey = row['Info']
            #print(AccessKey)
        if(row['AccessKey'] == "AWSSecretKey"):
            SecretKey = row['Info']
            #print(SecretKey)        

#creating SNS client
client = boto3.client("sns",aws_access_key_id = AccessKey, aws_secret_access_key = SecretKey,region_name = "us-east-1")

client.publish(PhoneNumber = "347-399-1639",Message = "")