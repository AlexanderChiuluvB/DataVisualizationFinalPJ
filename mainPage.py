# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainPage.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from morphGUI import *
from swapGUI import *
from eigenGUI import *

class Ui_MainPage(object):

    #打开融合脸界面的函数
    def startMorph(self):
        self.morph=Ui_Morph()
        self.morph.show()
    #打开换脸界面的函数
    def startSwap(self):
        self.Swap=Ui_Swap()
        self.Swap.show()
    #打开生成特征脸的函数
    def startEigen(self):
        self.Eigen=Ui_Eigen()
        self.Eigen.show()
    #打开主界面的函数
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(718, 493)
        MainWindow.setStyleSheet("background-color: rgb(2, 136, 209);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 180, 231, 91))
        self.label.setStyleSheet("font: 75 40pt \"Microsoft YaHei UI\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 450, 731, 41))
        self.graphicsView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.graphicsView.setObjectName("graphicsView")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 260, 401, 61))
        self.label_2.setStyleSheet("font: 25 12pt \"Microsoft YaHei UI\";\n"
"text-decoration: underline;\n"
"color: rgb(255, 255, 255);\n"
"color: rgb(225, 225, 225);")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 170, 141, 34))
        self.pushButton.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"

                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton.clicked.connect(self.startMorph)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 250, 141, 34))
        self.pushButton_2.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"
                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton_2.clicked.connect(self.startSwap)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 320, 141, 34))
        self.pushButton_3.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"
                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.startEigen)
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 0, 731, 41))
        self.graphicsView_2.setStyleSheet("background-color: rgb(2, 136, 209);\n"
"border:none")
        self.graphicsView_2.setObjectName("graphicsView_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #对主界面部件加上文字
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Face#"))
        self.label_2.setText(_translate("MainWindow", "Better Codes. Better Faces"))
        self.pushButton.setText(_translate("MainWindow", "Face Morphing"))
        self.pushButton_2.setText(_translate("MainWindow", "Face Swap"))
        self.pushButton_3.setText(_translate("MainWindow", "EigenFace"))


class MyWindow(QtWidgets.QWidget, Ui_MainPage):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
#启动该文件，会启动GUI画面
if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    login = Ui_MainPage()
    login.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())