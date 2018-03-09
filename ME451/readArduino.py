#!/usr/bin/env python

import serial
import time
import threading
import Queue
import sys
import glob


class SerialThread(threading.Thread):
    def __init__(self, queue, port, baud):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.baud = baud

    def run(self):
        s = serial.Serial(self.port, self.baud, timeout=0, writeTimeout=0)
        while True:
            if s.inWaiting():
                try:
                    self.queue.put(s.readline(s.inWaiting()))
                except ValueError:
                    pass


def writeFile(dest, queue, timeout):
    start = time.time()
    with open(dest, 'w') as destfile:
        while time.time() - start < timeout:
            print time.time() - start
            try:
                destfile.write(queue.get())
            except:
                pass
    destfile.close()


def saveFile(queue, filename, timeout):
    filethread = threading.Thread(target=writeFile, args=(filename, queue, timeout))
    filethread.start()


def listSerialPorts():
    # http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def readArduino(queue, baud):
    portname = listSerialPorts()
    # print portname[0]
    serialdata = SerialThread(queue, portname[0], baud)
    serialdata.start()
    while not serialdata.isAlive(): pass
    return serialdata

    # filethread = threading.Thread(target=writeFile, args=(filename, queue, timeout))
    # filethread.start()
    #
    # serialdata.paused = True


if __name__ == '__main__':
    queue = Queue.Queue()
    filename = "pidsin.csv"
    baud = 9600
    timeout = 30
    serialthread = readArduino(queue, baud)
    saveFile(queue, filename, timeout)
    serialthread.paused = True
