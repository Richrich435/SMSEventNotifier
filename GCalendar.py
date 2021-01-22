from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import date
import pickle
import json
import csv
import AWSSNSApi

class GCalendar():
    def __init__(self,calendarName):
        self.calendarName = calendarName
        
    def calendarAPICall(self):
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
        calendarID = ""
        #parses each calendar 
        for i in range(len(returnedCalendars)):
            if returnedCalendars['items'][i]['summary'] == self.calendarName:
                calendarID = returnedCalendars['items'][i]['id']
            else:
                continue
            
        #returns each event within the calendar
        getEvent = service.events().list(calendarId = calendarID, showDeleted = False,orderBy = 'updated').execute() # pylint: disable=maybe-no-member
        print("THIS IS THE EVENT LIST")
        print(json.dumps(getEvent, indent = 2))
        #Extracts events of that day
        presentDate = date.today()
        currentDate = presentDate.strftime("%Y-%m-%d")
        startdateOfEvent = ""
        summary = ""
        Event = {}
        for event in range(len(getEvent['items'])):
            currentEvent = getEvent['items'][event]
            try:
                print("\nTHIS EVENT:")
                print(currentEvent)
                startdateOfEvent = currentEvent['start']['dateTime'].split('T')[0]
                summary = currentEvent['summary']
                startTime = currentEvent['start']['dateTime'].split('T')[1]
                endTime = currentEvent['end']['dateTime'].split('T')[1]
                Event = {
                    "summary": summary,
                    "startOfEvent": startTime,
                    "endOfEvent": endTime
                }
            except KeyError as keyError: 
                continue

        if(currentDate == startdateOfEvent):
            #send the SMS message
                with open('rootkey.csv', newline = '') as csvFile:
                    reader = csv.DictReader(csvFile)
                    for row in reader: 
                        if(row['AccessKey'] == "AWSAccessKeyId"):
                            AccessKey = row['Info']
                            #print(AccessKey)
                        if(row['AccessKey'] == "AWSSecretKey"):
                            SecretKey = row['Info']
                AWSapi = AWSSNSApi.AWSSNS(AccessKey,SecretKey)
                AWSapi.AWSSNSAPICall(**Event)
        else: 
                print("Cant find date")