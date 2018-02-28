#!/usr/bin/env python

import serial
import Tkinter as tk
import threading
import Queue
from collections import deque
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo


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
        self.parent = parent
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.geometry("1360x750")
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.X, padx=40, pady=40)
        self.queue = Queue.Queue()
        self.thread = SerialThread(self.queue, 100)
        self.thread.start()
        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.line = self.ax1.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=4, padx=20, pady=20)

        self.widgets()


    def widgets(self):
        self.avgtxt = tk.Label(self.frame, text="", font='TimesNewRoman 37', bg=self.cget('bg'), relief='flat')
        self.stdtxt = tk.Label(self.frame, text="", font='TimesNewRoman 37', bg=self.cget('bg'), relief='flat')
        self.exitbutton = tk.Button(self.frame, text='Close', command=lambda: self.closeall(), width=10, height=3)
        self.dequescale = tk.Entry(self.frame)
        self.dequescalebutton = tk.Button(self.frame, text="Filter Size:", command=lambda: self.changedequesize())

        #self.canvas = tk.Canvas(self.frame, width=100, height=100)


        self.exitbutton.grid(row=0, column=0)
        self.avgtxt.grid(row=1, column=0)
        self.stdtxt.grid(row=2, column=0)
        self.dequescale.grid(row=0, column=2)
        self.dequescalebutton.grid(row=0, column=1)
        #self.canvas.grid(row=3, column=3)
        self.process_serial()


    def changedequesize(self):
        try:
            val = int(self.dequescale.get())
            self.thread.deque = deque([], val)
        except ValueError:
            pass
        print self.thread.deque.maxlen

    def closeall(self):
        self.parent.destroy()
        quit()

    def process_serial(self):
        while self.queue.qsize():
            try:
                self.avgtxt["text"] = "Average: {0:.2f}".format(self.thread.getaverage())
                self.stdtxt["text"] = "Deviation: {0:.2f}".format(self.thread.getstd())
                self.queue.get()
                #self.canvas.
                #self.fig = mpl.figure.Figure(figsize=(2, 1))
                #self.ax = self.fig.add_axes([0, 0, 1, 1])

                #ax.plot(xrange(len(self.thread.deque)), list(self.thread.deque))
                fig_x, fig_y = 100, 100
                #fig_photo = draw_figure(self.canvas, fig, loc=(fig_x, fig_y))
                #fig_w, fig_h = fig_photo.width(), fig_photo.height()
            except Queue.Empty:
                pass
        self.after(10, self.process_serial)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
