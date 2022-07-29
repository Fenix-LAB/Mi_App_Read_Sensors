from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QPoint
from gui_design import *
import pyqtgraph as pg
import numpy as np

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Usamos la funcion QPoint() para guardar la posicion del mouse
        self.click_position = QPoint()
        # Se configura la ventana
        self.btn_normal.hide()
        self.btn_minimizar.clicked.connect(lambda: self.showMinimized())
        self.btn_cerrar.clicked.connect(lambda: self.close())
        self.btn_normal.clicked.connect(self.control_btn_normal)
        self.btn_maximizar.clicked.connect(self.control_btn_maximizar)

        # Se elimina la barra de titulo por default
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Size grip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Movimiento de la ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        # Control connect
        self.serial = QSerialPort()
        self.btn_actualizar.clicked.connect(self.read_ports)
        self.btn_conectar.clicked.connect(self.serial_conect)
        self.btn_desconectar.clicked.connect(lambda: self.serial.close())

        # Asociacion de metodos
        self.serial.readyRead.connect(self.read_data)

        # Listas para la grficas
        self.x = list(np.linspace(0, 100, 100))
        self.y = list(np.linspace(0, 0, 100))

        self.xi = list(np.linspace(0, 100, 100))
        self.yi = list(np.linspace(0, 0, 100))

        # Creacion de la grafica 1
        pg.setConfigOption('background', '#2c2c2c')
        pg.setConfigOption('foreground', '#ffffff')
        self.plt = pg.PlotWidget(title='Grafica Sensor 1')
        self.graph_grafica1.addWidget(self.plt)

        # Creacion de la grafica 2
        pg.setConfigOption('background', '#2c2c2c')
        pg.setConfigOption('foreground', '#ffffff')
        self.plt2 = pg.PlotWidget(title='Grafica Sensor 2')
        self.graph_grafica2.addWidget(self.plt2)

        self.read_ports()

    def read_ports(self):
        self.baudrates = ['1200', '2400', '4800', '9600', '19200', '34800', '115200']
        portList = []
        ports = QSerialPortInfo().availablePorts()
        for i in ports:
            portList.append(i.portName())

        self.comboBox_puerto.clear()
        self.comboBox_velocidad.clear()
        self.comboBox_puerto.addItems(portList)
        self.comboBox_velocidad.addItems(self.baudrates)
        self.comboBox_velocidad.setCurrentText("9600")


    def serial_conect(self):
        self.serial.waitForReadyRead(100)
        self.port = self.comboBox_puerto.currentText()
        self.baud = self.comboBox_velocidad.currentText()
        self.serial.setBaudRate(int(self.baud))
        self.serial.setPortName(self.port)
        self.serial.open(QIODevice.ReadWrite)


    def read_data(self):
        if not self.serial.canReadLine(): return
        rx = self.serial.readLine()

        datos = str(rx, 'utf-8').strip()
        listaDatos = datos.split(",")
        self.dato1 = listaDatos[0]
        self.dato2 = listaDatos[1]

        self.showInfo()

        x1 = float(self.dato1)
        x2 = float(self.dato2)
        print(listaDatos)

        self.y = self.y[1:]
        self.y.append(x1)
        self.yi = self.yi[1:]
        self.yi.append(x2)

        self.plt.clear()
        self.plt.plot(self.x, self.y, pen=pg.mkPen('#da0037', width=2))
        self.plt2.clear()
        self.plt2.plot(self.xi, self.yi, pen=pg.mkPen('#da0037', width=2))

    def showInfo(self):
        self.val_actual1.setText(str(self.dato1))
        self.val_actual2.setText(str(self.dato2))

        max1 = int(max(self.y))
        max2 = int(max(self.yi))
        min1 = int(min(self.y))
        min2 = int(min(self.yi))
        prom1 = np.mean(self.y)
        prom2 = np.mean(self.yi)

        self.val_max1.setText(str(max1))
        self.val_max2.setText(str(max2))
        self.val_min1.setText(str(min1))
        self.val_min2.setText(str(min2))
        self.val_prom1.setText(str(prom1))
        self.val_prom2.setText(str(prom2))

    def control_btn_normal(self):
        self.showNormal()
        self.btn_normal.hide()
        self.btn_maximizar.show()

    def control_btn_maximizar(self):
        self.showMaximized()
        self.btn_maximizar.hide()
        self.btn_normal.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.btn_maximizar.hide()
            self.btn_normal.show()
        else:
            self.showNormal()
            self.btn_normal.hide()
            self.btn_maximizar.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()