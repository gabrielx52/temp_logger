import os
from time import sleep
from datetime import datetime

#import gspread
#import json
#from oauth2client.service_account import ServiceAccountCredentials

#oauthfile = '/home/pi/temp_logger/palace temp logger-88911bdd605e.json'
#scope =['https://spreadshhets.google.com/feeds']
#json_key = json.load(open(oauthfile))
#credentials = SignedJwtAssertionCredentials(json_key['client_email'],
#                                            json_key['private_key'],
#                                            scope)

#gspreadclient = gspread.authorize(credentials)




os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


''' Six temp sensors hooked up to raspi, change temp_sensor_x[0] to change name'''
temp_sensor_1 = ['Sensor 1', '/sys/bus/w1/devices/28-0000072a6c7a/w1_slave']
temp_sensor_2 = ['Sensor 2', '/sys/bus/w1/devices/28-0115915062ff/w1_slave']
temp_sensor_3 = ['Sensor 3', '/sys/bus/w1/devices/28-041591204dff/w1_slave']
temp_sensor_4 = ['Sensor 4', '/sys/bus/w1/devices/28-0415911992ff/w1_slave']
temp_sensor_5 = ['Sensor 5', '/sys/bus/w1/devices/28-04159112cbff/w1_slave']
temp_sensor_6 = ['Sensor 6', '/sys/bus/w1/devices/28-04159123ccff/w1_slave']

all_sensors = [temp_sensor_1,
               temp_sensor_2,
               temp_sensor_3,
               temp_sensor_4,
               temp_sensor_5,
               temp_sensor_6]


def temp_writer(data_to_write):
    ''' writes data to daily txt file log '''
    with open('{}.txt'.format(datetime.now().strftime('%m.%d.%Y')), 'a+') as f:
        f.write(data_to_write)
    print(data_to_write)


def read_temp():
    ''' reads and converts temp from sensor, logs if disconnected '''
    for temp_sensor in all_sensors:
        if os.path.exists(temp_sensor[1]):
            try:
                with open(temp_sensor[1]) as raw_file:
                    lines = raw_file.readlines()
                    while lines[0].strip()[-3:] != 'YES':
                        sleep(0.2)
                        lines = raw_file.readlines()
                    temp_output = lines[1].find('t=')
                    if temp_output != -1:
                        temp_string = lines[1].strip()[temp_output+2:]
                        temp_c = float(temp_string) / 1000.0
                        temp_f = temp_c * 9.0 /5.0 + 32.0
                    if temp_f > 45.0:
                        # temp_writer('*** high temp alert *** ') add high temp text here.
                        temp_writer('{} {:.2f}\u00b0F {}\n'.format(temp_sensor[0], temp_f, datetime.now().strftime('%m/%d/%Y, %I:%M %p')))
                    else:
                        temp_writer('{} {:.2f}\u00b0F {}\n'.format(temp_sensor[0], temp_f, datetime.now().strftime('%m/%d/%Y, %I:%M %p')))
            except IndexError:
                temp_writer(str('{} is disconnected\n'.format(temp_sensor[0])))
        else:
            temp_writer(str('{} is disconnected\n'.format(temp_sensor[0])))



def temp_row_maker():
    ''' makes row out of temp '''
    row = []
    row.append(datetime.now().strftime('%I:%M %p'))
    for temp_sensor in all_sensors:
        if os.path.exists(temp_sensor[1]):
            try:
                with open(temp_sensor[1]) as raw_file:
                    lines = raw_file.readlines()
                    while lines[0].strip()[-3:] != 'YES':
                        sleep(0.2)
                        lines = raw_file.readlines()
                    temp_output = lines[1].find('t=')
                    if temp_output != -1:
                        temp_string = lines[1].strip()[temp_output+2:]
                        temp_c = float(temp_string) / 1000.0
                        temp_f = temp_c * 9.0 /5.0 + 32.0
                    row.append('{:.2f}\u00b0F'.format(temp_f))
            except IndexError:
                row.append('disconnected')
        else:
            row.append('disconnected')
    return row
            


#while True:
#    read_temp()
#    sleep(5)  # change sleep time to change cycle...

#temp_row_maker()

