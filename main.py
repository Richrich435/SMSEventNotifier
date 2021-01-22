import GCalendar
import csv

def main():
    calendarName = input("Enter the calendar you want to read: ")
    gcalendar = GCalendar.GCalendar(calendarName)
    gcalendar.calendarAPICall()
    

if __name__=="__main__": 
    main() 