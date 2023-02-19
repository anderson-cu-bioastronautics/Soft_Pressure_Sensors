import atexit
import serial
import numpy as np 
import pyqtgraph as pg
from pyqtgraph.ptime import time
from pyqtgraph.Qt import QtGui, QtCore
import win32api, win32con
import os

def serialSetup():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM3'
    ser.open()
    return ser

def serialPrint(ser):

    while True:
        print(ser.readline())

def exit_handler(ser, button,name):
    print("Exiting")
    directory = 'Data/'+name
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.savetxt('Data/'+name+'/data.txt',serialGraph.data)
    np.savetxt('Data/'+name+'/time.txt',serialGraph.time)
    if button is True:
        click(163,414)
    ser.close()

    
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


class serialGraph:
    def __init__(self, ser):
        self.app = QtGui.QApplication([])
        p = pg.plot(title="Pressure Sensor Output")
        self.curve = p.plot()
        self.ser = ser
        serialGraph.data = [0]
        serialGraph.time = [0]
    def update(self):
        while True:
            line = self.ser.readline()
            line = line.decode("utf-8")
            
            try:
                [time,value] = line.split("|")
                ip = np.float(value)
                time = np.float(time)
                time = time/1000
                print(time)
                print('|')
                print(ip)
                print('\n')
                serialGraph.data.append(ip)
                serialGraph.time.append(time)
            except:
                pass
            
            xdata = np.array(serialGraph.data, dtype='float64')
            self.curve.setData(xdata)
            self.app.processEvents()



if __name__=="__main__":
    ser = serialSetup()
    #serialPrint(ser)
    g = serialGraph(ser)
    click(64,413)
    g.update()
