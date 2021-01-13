from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import date
import pickle
import json

scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json",scopes = scopes)

credentialsflow = flow.run_console()
pickle.dump(credentialsflow, open("token.pkl","wb"))
credentials = pickle.load(open("token.pkl","rb"))
print(credentials)

service = build("calendar","v3",credentials = credentials)
returnedCalendars = service.calendarList().list().execute() # pylint: disable=maybe-no-member
print(json.dumps(returnedCalendars, indent= 2))

print(json.dumps(returnedCalendars['items'][2],indent = 2 ))

calendar_id = returnedCalendars['items'][2]['id']
print(calendar_id)

presentDate = date.today()
dateTime = presentDate.strftime("%m/%d/%Y, %H:%M:%S")
getEvent = service.events().list(calendarId = calendar_id, showDeleted = False , singleEvents = True).execute() # pylint: disable=maybe-no-member
print(json.dumps(getEvent, indent = 2))