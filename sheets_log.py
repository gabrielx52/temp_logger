import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/temp_logger/palace temp logger-88911bdd605e.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("palace kitchen temp log").sheet1
wks.update_acell('A1', 'test')


#print(wks)
