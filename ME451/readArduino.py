#!/usr/bin/env python

import serial
import time
import threading
import Queue
import multiprocessing


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
            try:
                destfile.write(queue.get())
            except:
                pass


def readArduino(queue, filename, baud, timeout):
    locations = ['/dev/ttyACM0', '/dev/ttyACM1']

    for device in locations:
        try:
            tempser = serial.Serial(device, baud)
            print "Successfully connected to", device
            portname = device
            tempser.close()
            break
        except:
            print "Failed to connect on", device

    serialdata = SerialThread(queue, portname, baud)
    serialdata.start()

    filethread = threading.Thread(target=writeFile, args=(filename, queue, timeout))
    filethread.start()

    serialdata.paused = True


if __name__ == '__main__':
    queue = Queue.Queue()
    filename = "piddelay5000.csv"
    baud = 9600
    timeout = 10
    readArduino(queue, filename, baud, timeout)
