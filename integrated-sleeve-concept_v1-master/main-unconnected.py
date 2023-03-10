import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
import readSPI
import raw2Ohms
import time
import numpy as np
import csv
import pyqtgraph as pg

qtCreatorFile = "Sleeve_UI.ui" # Ui file generated by QtDesigner to outline GUI
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class IntegratedSleeveUi(Ui_MainWindow): 
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog) #initiates UI
        
        #setup variables
        self.sampRate=int(self.rateSamp.value())
        self.sensors = {} #dictionary which holds the progress bars of the sensors
        self.sensorNum = int(self.numSensors.value())
        self.sensorData = {}
        self.spiInstances = {} #dictionary which holds each SPI interface object

        #setup function to convert from raw 0-1 value to Ohms, inputs are voltage in and resistor resistance
        self.convert = raw2Ohms.converter(4,10).convert

        #connect buttons from UI to the appropriate function
        self.connectButton.clicked.connect(self.connect)
        self.startButton.clicked.connect(self.startData)
        self.stopButton.setEnabled(False)

    def connect(self): #this function will attempt to connect to the RPi and also generate the bars showing each sensor's output. 
        numInstances = int(np.ceil(self.sensorNum / 8))
        #self.spiInstances[i] = np.random.rand(1)#
        #try:
        self.plot = pg.PlotWidget()
        self.sensorBars = pg.PlotWidget()
        self.sensorBox.addWidget(self.sensorBars)
        self.graphBox.addWidget(self.plot)
        yvalues = np.empty((16,))
        xvalues = np.arange(1,self.sensorNum+1,1,dtype='int')
        self.bg = pg.BarGraphItem(x=xvalues, y1=yvalues, width = 0.6)
        self.sensorBars.setRange(yRange=[0,50])
        
        xax = self.sensorBars.getAxis('bottom')
        dx = [(value, str(value)) for value in xvalues]
        xax.setTicks([dx,[]])

        yax = self.sensorBars.getAxis('left')
        dy = [(value, str(value)) for value in np.arange(0,50,5,dtype='int')]
        yax.setTicks([dy,[]])
        self.sensorBars.showGrid(x=False, y=True, alpha=.5)

        self.sensorBars.addItem(self.bg)
        
        self.curve = self.plot.plotItem
        self.curve.setLabels(left='Ohms')
        
        self.SensorCurve = self.curve.plot()
        self.SensorCurve.setPen(pg.mkPen(color='#ff0000',width=2))
        self.sensorSelect.setMaximum(self.sensorNum)

        self.sensorSelect.setMaximum(self.sensorNum)
        self.plotData = []
        self.currentPlot = self.sensorSelect.value()
        
        '''
        for i in range(0,numInstances):
            self.spiInstances[i] = readSPI.mcp(self.ipAddress.text(),0,i)
        for i in range(1,self.sensorNum+1): #setup progress bars for sensors
            progBar = QProgressBar()
            sName = 'sensor'+str(i)
            progBar.setObjectName(sName)
            progBar.setMaximum(1000)
            progBar.setTextVisible(True)
            progBar.setFormat('%v')
            progBar.setValue(0)
            self.sensorBox.addWidget(progBar)
            _dict = {sName:progBar}
            self.sensors.update(_dict)
        '''
        self.statusBox.setText("Connected!")
        '''
        except:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Could not connect!') #error message to show
            error_dialog.setWindowTitle("IP Address Error") 
            self.statusBox.setText("Connection Error!")
        '''
                
    def startData(self):
        IPaddress = self.ipAddress.text()
        self.data_thread = spiThread()
        self.data_thread.output.connect(self.dispData)
        self.data_thread.finished.connect(self.doneData)
        self.stopButton.setEnabled(True)
        self.stopButton.clicked.connect(self.data_thread.stop)
        self.startButton.setEnabled(False)
        self.data_thread.start()
        
    def dispData(self,output):
        self.statusBox.setText("Running...")
        values = [output[key] for key in output.keys()][0]
        valuesConverted = self.convert(values)
        for key in output.keys():
            outputConverted = {key:valuesConverted}
        self.sensorData.update(outputConverted)
        self.bg.setOpts(y1=np.concatenate(list(outputConverted.values())))
        
        
        
        if self.sensorSelect.value() != self.currentPlot:
            self.plotData = []
            self.currentPlot = self.sensorSelect.value()

        plotPoint = np.concatenate(list(outputConverted.values()))[self.currentPlot]

        if len(self.plotData) < 50:
            self.plotData.append(plotPoint)
        else:
            self.plotData = self.plotData[1:] + [plotPoint]

        self.SensorCurve.setData(self.plotData)
        
        #print(values[0], valuesConverted[0])
        print(outputConverted.values())

        

    def doneData(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        #np.savetxt('dataOutput.txt', np.zeros((16,)))
        fname = str(self.saveName.text())
        with open(fname, 'w') as f:
            dataWriter = csv.writer(f,delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for key in self.sensorData.keys():
                values = self.sensorData[key].flatten().tolist()
                toWrite = np.append(key,values)
                dataWriter.writerow(toWrite)
        self.statusBox.setText("Data saved!")


class spiThread(QThread):
    output = pyqtSignal(dict)
    finished = pyqtSignal()
    _isRunning = True
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()
    
    '''
    def getData(self,IPaddress):
        data = np.random.rand(16,1)
        return data
    '''

    def run(self):
        self._isRunning = True
        #data = {}
        while self._isRunning == True:
            #led.on()
            data={}
            
            sensorData_temp=np.empty((0,))
            for i in range(0,2):
                spi_chip=np.random.rand(1,8)
                sensorData_temp = np.append(sensorData_temp,spi_chip)
            data[time.time()]=sensorData_temp
            '''
            data[time.time()] = self.getData(self.IPaddress)
            '''
            self.output.emit(data)
            #led.off()
            time.sleep(1/4)
        self.finished.emit()

    def stop(self):
        self._isRunning = False
        self.finished.emit()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QDialog()
    ui = IntegratedSleeveUi(window)
    window.show()
    sys.exit(app.exec_())