from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import date
import pickle
import json

#this part connects the api to program
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
for event in range(len(getEvent['items'])):
    print("\nTHIS EVENT:")
    currentEvent = getEvent['items'][event]
    try:
        print(currentEvent['start'])
    except KeyError as keyError: 
        continue
    
