#!/usr/bin/env python

import serial
import threading
import Queue
from collections import deque
import numpy as np
import Tkinter as tk
import ttk
import matplotlib
import sys
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
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

    def getaverage(self):
        return np.mean(list(self.deque))

    def getstd(self):
        return np.std(list(self.deque))

    def run(self):
        s = serial.Serial('/dev/ttyACM0', 9600, timeout=0, writeTimeout=0)
        while True:
            if s.inWaiting():
                text = s.readline(s.inWaiting())
                self.queue.put(text)
                try:
                    val = int(text)
                    self.deque.appendleft(val)
                except ValueError:
                    pass


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.running = False
        self.ani = None
        self.parent = parent
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.geometry("1360x750")
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, padx=40, pady=40)
        self.queue = Queue.Queue()
        self.thread = SerialThread(self.queue, 100)
        self.thread.start()

        self.widgets()

    def get_data(self):
        x = list(self.thread.deque)
        y = xrange(len(x))
        return x,y

    def widgets(self):
        self.avgtxt = tk.Label(self.frame, text="", font=LARGE_FONT, bg=self.cget('bg'), relief='flat')
        self.stdtxt = tk.Label(self.frame, text="", font=LARGE_FONT, bg=self.cget('bg'), relief='flat')
        self.exitbutton = tk.Button(self.frame, text='Close', command=lambda: self.closeall(), width=10, height=3)
        self.dequescale = tk.Entry(self.frame)
        self.dequescalebutton = tk.Button(self.frame, text="Filter Size:", command=lambda: self.changedequesize())

        self.exitbutton.grid(row=0, column=0)
        self.avgtxt.grid(row=1, column=0)
        self.stdtxt.grid(row=2, column=0)
        self.dequescale.grid(row=0, column=2, sticky='W')
        self.dequescalebutton.grid(row=0, column=1)
        #self.startgraph()

        self.process_serial()

    def graph(self):
        if self.ani is None:
            return self.start()
        if self.running:
            self.ani.event_source.stop()
        else:

            self.ani.event_source.start()
        self.running = not self.running

    def start(self):
        self.ani = animation.FuncAnimation(
            self.fig,
            self.animate,
            interval=100,
            repeat=False
        )
        self.running = True
        self.ani._start()

    def startgraph(self):
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.subplt = self.fig.add_subplot(111)
        #self.ax = self.fig.add_axes((0.15, .1, .8, .80), frameon=False)
        #self.ax.set_xlabel('Points')
        #self.ax.set_ylabel('Value')
        self.line, = self.subplt.plot([],[])
        #self.ax.plot(np.max(np.random.rand(100, 10) * 10, axis=1), "r-")
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().grid(row=3, column=2)
        self.canvas.show()
        #self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        #self.toolbar.grid(row=3, column=4)
        #self.toolbar.update()
        self.graph()

    def animate(self):
        self.line.set_data(*self.get_data())
        self.canvas.show()

    def changedequesize(self):
        try:
            val = int(self.dequescale.get())
            self.thread.deque = deque([], val)
        except ValueError:
            pass

    def closeall(self):
        self.parent.destroy()

    def process_serial(self):
        while self.queue.qsize():
            try:
                self.avgtxt["text"] = "Average: {0:.2f}".format(self.thread.getaverage())
                self.stdtxt["text"] = "Deviation: {0:.2f}".format(self.thread.getstd())
                self.queue.get()
                self.animate()
            except Queue.Empty:
                pass
        print len(list(self.thread.deque))
        self.after(10, self.process_serial)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    #root.update()
    #root.deiconify()
    app.mainloop()
