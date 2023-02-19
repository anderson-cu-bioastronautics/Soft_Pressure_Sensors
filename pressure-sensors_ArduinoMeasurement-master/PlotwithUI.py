import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import PlotAnalog

 
qtCreatorFile = "Ui.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog) 
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)

    def start(self):
        self.ser = PlotAnalog.serialSetup()
        if self.radioButton.isChecked() is True:
            PlotAnalog.click(64,413)
        g = PlotAnalog.serialGraph(self.ser, )
        g.update()
    def stop(self):
        name = self.sensorName.text()
        PlotAnalog.exit_handler(self.ser,self.radioButton.isChecked(),name)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MyApp(window)
    window.show()
    sys.exit(app.exec_())