# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eigen.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from  eigenface_origin import *

class Ui_Eigen(QMainWindow):

    def __init__(self):
        super(Ui_Eigen, self).__init__()
        self.setupUi(self)

    def loaddir(self):
        self.dirname=QFileDialog.getExistingDirectory()
        print(self.dirname)
    def eigen(self):
        eigenFace(self.dirname)

    def setupUi(self, Eigen):
        Eigen.setObjectName("Eigen")
        Eigen.resize(715, 398)
        Eigen.setStyleSheet("background-color: rgb(2, 136, 209);")
        self.centralwidget = QtWidgets.QWidget(Eigen)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 30, 250, 120))
        self.label.setStyleSheet("font: 75 25pt \"Microsoft YaHei UI\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 360, 731, 41))
        self.graphicsView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_dir.setGeometry(QtCore.QRect(290, 170, 141, 34))
        self.pushButton_dir.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"

                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton_dir.setObjectName("pushButton_dir")
        self.pushButton_dir.clicked.connect(self.loaddir)
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 0, 731, 41))
        self.graphicsView_2.setStyleSheet("background-color: rgb(2, 136, 209);\n"
"border:none")
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.pushButton_Eigen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Eigen.setGeometry(QtCore.QRect(290, 250, 141, 34))
        self.pushButton_Eigen.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"

                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton_Eigen.setObjectName("pushButton_Eigen")
        self.pushButton_Eigen.clicked.connect(self.eigen)
        Eigen.setCentralWidget(self.centralwidget)
        self.retranslateUi(Eigen)
        QtCore.QMetaObject.connectSlotsByName(Eigen)

    def retranslateUi(self, Eigen):
        _translate = QtCore.QCoreApplication.translate
        Eigen.setWindowTitle(_translate("Eigen", "MainWindow"))
        self.label.setText(_translate("Eigen", "EigenFace"))
        self.pushButton_dir.setText(_translate("Eigen", "选择文件夹"))
        self.pushButton_Eigen.setText(_translate("Eigen", "EigenFace"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileload =Ui_Eigen()
    fileload.show()
    sys.exit(app.exec_())