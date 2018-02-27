#!/usr/bin/env python

import serial
import time

def readArduino(filename, baud, timeout):

    locations = ['/dev/ttyACM0','/dev/ttyACM1']
    connected = False

    for device in locations:
        try:
            print "Trying...", device
            ser = serial.Serial(device, baud)
            break
        except:
            print "Failed to connect on", device

    while not connected:
        serin = ser.read()
        connected = True

    text_file = open(filename, 'w')

    start = time.time()
    while time.time() - start < timeout:
        line = ser.readline().decode('utf-8')
        text_file.write(line)
        text_file.flush()

    # close the serial connection and text file
    text_file.close()
    ser.close()
