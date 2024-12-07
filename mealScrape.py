from pprint import pprint
import os.path
import datetime
from datetime import date

import requests
from bs4 import BeautifulSoup

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'

SCOPES = ['https://www.googleapis.com/auth/calendar']

def calCreate(summary, description, eventBegin, eventEnd): #need to pass in variables
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    
    
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary' : summary,
        'description' : description,

        'start' : {
            'dateTime' : eventBegin,
            'timeZone' : 'America/Chicago',
        },

        'end' : {
            'dateTime' : eventEnd,
            'timeZone' : 'America/Chicago',
        },
        'guestsCanInviteOthers' : False,
    }

    event = service.events().insert(calendarId="9346f4711fd2044ddc0e63942e533838afabb8054142516344b1d3ac76b5e71b@group.calendar.google.com", body=event).execute()



#function to scrape data from school's website per bsoup (day):
def scrape(day, note, start, end):
     #print(webData)
    for meal in day.find_all("div", class_= "fsCalendarDaybox fsStateHasEvents"):
        print('day loop:')
        #print(day)
        description = note
    
        for info in meal.find_all(class_="fsCalendarEventTitle fsCalendarEventLink"):
            eventDetail = info['title'].rstrip()        
            
            #print(eventDetail + "BFAST MOFO")

        for info in meal.find_all(class_="fsCalendarDate"):
            eventMonth = str(int(info['data-month'])+1)
            eventDay = str(int(info['data-day']))
            eventYear = str(int(info['data-year']))
            #print(str(eventMonth) + '/' + str(eventDay)+'/'+str(eventYear))
            
            
            #print('detail loop:')
            #print(info)
        
        
        if eventDetail == "No School":
            break        

        if len(eventDay) == 1:
            eventDay = '0'+ eventDay

        #eventDate = str(eventYear)+ str(eventMonth) + str(eventDay)
        eventStart = eventYear + '-' + eventMonth + '-' + eventDay + start
        eventEnd = eventYear + '-' + eventMonth + '-' + eventDay + end
        print(eventDetail)
        print(eventStart)
        print(eventEnd)
        
        print('next')
        #calCreate(eventDetail, description, eventStart, eventEnd)
        print('cal event would be created right here')


#IDs for parent divs for relative calendar
bfastID = '#fsEl_77141'
lunchID = '#fsEl_77149'
schoolCalID = '#fsEl_16091'

#bfast time will be set to 7:30 - 8
bStart = 'T07:30:00-06:00'
bEnd = 'T08:00:00-06:00'

#lunch time span at BEE is 10:45a - 12:05p
lStart = 'T10:45:00-06:00'
lEnd = 'T12:05:00-06:00'



url = 'https://bonneecoleelementary.stpsb.org/our-school/school-meals'
urlCal = 'https://bonneecoleelementary.stpsb.org/connect/calendar'

r = requests.get(url)

rCal = requests.get(urlCal)

soup = BeautifulSoup(r.content, 'html.parser')
soupCal = BeautifulSoup(rCal.content, 'html.parser')
print(soupCal)

#pull breakfast data
bfast = soup.select_one(bfastID)

#pull lunch data
lunch = soup.select_one(lunchID)

#pull school cal data
school = soupCal.select_one(schoolCalID)
#print(school)


bNote = "Fruit, fruit juice, cereal with toast and choice of milk offered daily."
lNote = "Vegetarian option, vegetable, fruit and choice of milk offered daily."

print('breakfast')
#scrape(bfast, bNote, bStart, bEnd)
print('end breakfast')

print('lunch')
#scrape(lunch, lNote, lStart, lEnd)
print('end lunch')

print('calendar')
#scrape(school)

print('done')


#working bfast
'''
for day in bfast.find_all("div", class_= "fsCalendarDaybox fsStateHasEvents"):
    print('day loop:')
    #print(day)
    
    for info in day.find_all(class_="fsCalendarEventTitle fsCalendarEventLink"):
        eventDetail = info['title'].rstrip()        
        
        #print(eventDetail + "BFAST MOFO")

    for info in day.find_all(class_="fsCalendarDate"):
        eventMonth = int(info['data-month'])+1
        eventDay = int(info['data-day'])
        eventYear = int(info['data-year'])
        #print(str(eventMonth) + '/' + str(eventDay)+'/'+str(eventYear))
        
        
        #print('detail loop:')
        #print(info)

    
    if eventDetail == "No School":
            break
    print(eventDetail)
    print(str(eventMonth) + '/' + str(eventDay)+'/'+str(eventYear))
    print('next')
'''


#this currently pulls meals from both calendars. Do not alter!!!!
'''
for day in soup.find_all("div", class_= "fsCalendarDaybox fsStateHasEvents"):
    print('day loop:')
    #print(day)
    
    for info in day.find_all(class_="fsCalendarDate"):
        eventMonth = int(info['data-month'])+1
        eventDay = int(info['data-day'])
        eventYear = int(info['data-year'])
        #print(str(eventMonth) + '/' + str(eventDay)+'/'+str(eventYear))
        
        
        #print('detail loop:')
        #print(info)

    for info in day.find_all(class_="fsCalendarEventTitle fsCalendarEventLink"):
        eventDetail = info['title']
        #print(eventDetail + "BFAST MOFO")

    print(eventDetail)
    print(str(eventMonth) + '/' + str(eventDay)+'/'+str(eventYear))
    print('next')
'''

