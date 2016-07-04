from datetime import datetime
from time import sleep

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from temp_logger import temp_row_maker 

# scope = ['https://spreadsheets.google.com/feeds']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/temp_logger/palace temp logger-88911bdd605e.json', scope)
# gc = gspread.authorize(credentials)
# sh = gc.open("palace kitchen temp log")

#wks = gc.open("palace kitchen temp log").sheet1
#wks.update_acell('A1', 'test')


#print(wks)

def sheets_logger():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/temp_logger/palace temp logger-88911bdd605e.json', scope)
    gc = gspread.authorize(credentials)
    sh = gc.open("palace kitchen temp log")
    try:
        worksheet = sh.worksheet(datetime.now().strftime('%m.%d.%Y'))
        worksheet.append_row(temp_row_maker())
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(datetime.now().strftime('%m.%d.%Y'),
                                     rows='1',
                                     cols='7')
        worksheet.append_row(['time',
                              'sensor 1',
                              'sensor 2',
                              'sensor 3',
                              'sensor 4',
                              'sensor 5',
                              'sensor 6'])
        worksheet.append_row(temp_row_maker())
    except Exception as e:
        with open('error_log.txt','a+') as er_log:
            er_log.write('ERROR: {} at {:.2f}\u00b0F \n'.format(str(e), datetime.now().strftime('%m/%d/%Y, %I:%M %p')))


while True:
    sheets_logger()
    sleep(60)
