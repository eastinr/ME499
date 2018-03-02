#!/usr/bin/env python

import serial
import threading
import Queue
from collections import deque
import numpy as np
import Tkinter as tk
import Tkconstants
import tkFileDialog
import ttk
import time
import matplotlib
import sys
import os
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


LARGE_FONT = ("Verdana", 35)
style.use("ggplot")


class SerialThread(threading.Thread):
    def __init__(self, queue, size):
        threading.Thread.__init__(self)
        self.queue = queue
        self.deque = deque([], size)
        self.avg = 0
        self.val = 0

    def getaverage(self):
        return np.mean(list(self.deque))

    def getstd(self):
        return np.std(list(self.deque))

    def getinstant(self):
        return self.val

    def getlen(self):
        return len(list(self.deque))

    def run(self):
        s = serial.Serial('/dev/ttyACM0', 9600, timeout=0, writeTimeout=0)
        while True:
            if s.inWaiting():
                try:
                    text = s.readline(s.inWaiting())
                    self.queue.put(text)
                    self.val = int(text)
                    self.deque.appendleft(self.val)
                except ValueError:
                    pass


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.running = False
        self.ani = None
        self.traces = dict()
        self.parent = parent

        #self.parent.grid_rowconfigure(0, weight=1)
        #self.parent.grid_columnconfigure(0, weight=1)
        self.parent.geometry("1360x750")
        self.frame = ttk.Frame(self.parent)
        #self.frame.grid(row=0, column=0, padx=40, pady=40)
        self.frame.pack(side=tk.TOP, anchor='nw', padx=40, pady=40)
        self.frame2 = ttk.Frame(self.parent)
        self.frame2.pack(side=tk.TOP, anchor='w', padx=40)
        self.frame3 = ttk.Frame(self.parent)
        self.frame3.pack(side=tk.TOP, anchor='w', padx=40)
        self.queue = Queue.Queue()
        self.thread = SerialThread(self.queue, 100)
        self.thread.start()

        self.widgets()

    def get_data(self):
        y = list(self.thread.deque)
        y += [0] * (self.thread.deque.maxlen - len(y))
        x = xrange(len(y))
        return x, y

    def savefile(self):
        try:
            path = self.savedirinput.get()
            os.lstat(path)
            self.savedata(path, 5)
        except OSError:
            file = tkFileDialog.asksaveasfilename(initialdir = "/home/robert",title = "Select file")
            self.savedirinput['text'] = file
            self.savedata(file, 5)
            print (file)

    def savedata(self, filename, savetime):
        now = time.time()
        while (time.time() - now) < savetime:
            with open(filename, 'w') as f:
                f.write(str(time.time() - now) + ',' + self.thread.queue.get() + '\n')
                f.flush()

    def widgets(self):
        self.avgtxt = tk.Label(self.frame2, text="", font=LARGE_FONT, anchor='w')
        self.stdtxt = tk.Label(self.frame2, text="", font=LARGE_FONT, anchor='w')
        self.instxt = tk.Label(self.frame2, text="", font=LARGE_FONT, anchor='w')
        self.exitbutton = tk.Button(self.frame, text='Close', command=lambda: self.closeall(), width=10, height=3)
        self.dequescale = tk.Entry(self.frame)
        self.dequescalebutton = tk.Button(self.frame, text="Filter Size:", command=lambda: self.changedequesize())
        self.savebutton = tk.Button(self.frame3, text="Save", command=lambda: self.savefile())
        self.savedirinput = tk.Entry(self.frame3)

        self.exitbutton.pack(side=tk.LEFT, padx=10, anchor='nw')
        self.dequescalebutton.pack(side=tk.LEFT)
        self.dequescale.pack(side=tk.LEFT)

        self.instxt.pack(side=tk.TOP, anchor='w')
        self.avgtxt.pack(side=tk.TOP, anchor='w')
        self.stdtxt.pack(side=tk.TOP, anchor='w')
        self.savebutton.pack(side=tk.LEFT)
        self.savedirinput.pack(side=tk.LEFT)

        # self.exitbutton.grid(row=0, column=0, columnspan=2, sticky='w')
        # self.instxt.grid(row=1, column=0, sticky='w', columnspan=4)
        # self.avgtxt.grid(row=2, column=0, sticky='w', columnspan=3)
        # self.stdtxt.grid(row=3, column=0, sticky='w', columnspan=3)
        # self.dequescale.grid(row=0, column=2, sticky='W', columnspan=1)
        # self.dequescalebutton.grid(row=0, column=1, sticky='E')
        # self.savebutton.grid(row=4, column=0, sticky='W')
        # self.savedirinput.grid(row=4, column=1, columnspan=2, sticky='W')
        #self.graph()

        self.process_serial()

    def graph(self):
        self.fig = Figure(dpi=100)
        self.subplt = self.fig.add_subplot(111)
        self.line, = self.subplt.plot([],[])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        #self.canvas.get_tk_widget().grid(row=3, column=1)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        self.canvas.show()
        self.process_serial()

    def animate(self, name, dataset_x, dataset_y):
        if name in self.traces:
            self.line.set_data(dataset_x, dataset_y)
        else:
            self.traces[name] = True
            self.line, = self.subplt.plot(dataset_x, dataset_y)
        self.canvas.draw()

    def changedequesize(self):
        try:
            val = int(self.dequescale.get())
            self.thread.deque = deque([], val)
        except ValueError:
            pass

    def closeall(self):
        self.after_cancel(self.parent)
        self.parent.destroy()

    def process_serial(self):
        while self.queue.qsize():
            try:
                self.instxt["text"] = "Instantaneous: {0:.2f}".format(self.thread.getinstant())
                self.avgtxt["text"] = "Average: {0:.2f}".format(self.thread.getaverage())
                self.stdtxt["text"] = "Deviation: {0:.2f}".format(self.thread.getstd())
                self.queue.get()
            except Queue.Empty:
                pass
        #self.animate("data", *self.get_data())
        self.after(10, self.process_serial)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    #app.animate("data", *app.get_data())
    app.mainloop()
