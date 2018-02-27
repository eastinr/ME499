#!/usr/bin/env python

import serial
import threading
import Queue
import Tkinter as tk
from collections import deque
import numpy as np


def close():
    quit()

if __name__ == '__main__':
    top = tk.Tk()
    button = tk.Button(top, text="Close", command=close)
    txt = tk.
    button.pack()
    top.mainloop()
