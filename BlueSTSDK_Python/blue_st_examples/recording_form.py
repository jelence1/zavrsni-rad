# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recording_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt, QTimer

import time
import zmq

import globals

TIME_LEFT = 5

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 20, 750, 550))
        self.widget.setStyleSheet("QPushButton {\n"
"    font: 14pt \"Arial Rounded MT Bold\";\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton#recordBtn {\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.553, y2:0.533409, stop:0.00497512 rgba(78, 75, 108, 255), stop:0.935323 rgba(151, 180, 209, 255))\n"
"}\n"
"\n"
"QPushButton#editBtn {\n"
"color: white;\n"
"background-color:qlineargradient(spread:reflect, x1:0, y1:0, x2:0.513, y2:0.499318, stop:0 rgba(160, 193, 221, 255), stop:0.955224 rgba(74, 99, 119, 255))\n"
"}\n"
"\n"
"QPushButton#editBtn:hover, #recordBtn:hover, #exitBtn:hover {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.731905, y2:0.755, stop:0 rgba(255, 221, 221, 255), stop:0.955224 rgba(238, 103, 100, 255))\n"
"}\n"
"\n"
"QPushButton#exitBtn {\n"
"background-color: rgba(195, 195, 195, 0.3);\n"
"border-radius: 10px; \n"
"}")
        self.widget.setObjectName("widget")
        self.mainLabel = QtWidgets.QLabel(self.widget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 750, 550))
        self.mainLabel.setStyleSheet("border-radius: 50px;\n"
"background-color: rgb(191, 204, 228);")
        self.mainLabel.setText("")
        self.mainLabel.setObjectName("mainLabel")
        self.micLabel = QtWidgets.QLabel(self.widget)
        self.micLabel.setGeometry(QtCore.QRect(30, 130, 80, 80))
        self.micLabel.setText("")
        self.micLabel.setPixmap(QtGui.QPixmap("imgs/microphone.png"))
        self.micLabel.setScaledContents(True)
        self.micLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.micLabel.setObjectName("micLabel")
        self.header = QtWidgets.QLabel(self.widget)
        self.header.setGeometry(QtCore.QRect(0, 0, 750, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(28)
        self.header.setFont(font)
        self.header.setStyleSheet("border-top-left-radius: 50px;\n"
"border-top-right-radius: 50px;\n"
"background-color: rgb(64, 69, 79);\n"
"")
        self.header.setText("")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        self.headerLabel = QtWidgets.QLabel(self.widget)
        self.headerLabel.setGeometry(QtCore.QRect(200, 10, 352, 71))
        self.headerLabel.setText("")
        self.headerLabel.setPixmap(QtGui.QPixmap("imgs/header.png"))
        self.headerLabel.setScaledContents(True)
        self.headerLabel.setObjectName("headerLabel")
        self.headerFade = QtWidgets.QLabel(self.widget)
        self.headerFade.setGeometry(QtCore.QRect(0, 70, 750, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(28)
        self.headerFade.setFont(font)
        self.headerFade.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.511975, y1:0.443, x2:0.522, y2:1, stop:0 rgba(64, 69, 79, 255), stop:1 rgba(64, 69, 79, 0))")
        self.headerFade.setText("")
        self.headerFade.setAlignment(QtCore.Qt.AlignCenter)
        self.headerFade.setObjectName("headerFade")
        self.exitBtn = QtWidgets.QPushButton(self.widget)
        self.exitBtn.setGeometry(QtCore.QRect(690, 30, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.exitBtn.setFont(font)
        self.exitBtn.setObjectName("exitBtn")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(80, 250, 331, 61))
        self.label.setObjectName("label")
        self.mainLabel.raise_()
        self.micLabel.raise_()
        self.header.raise_()
        self.headerFade.raise_()
        self.headerLabel.raise_()
        self.exitBtn.raise_()
        self.label.raise_()

        self.exitBtn.clicked.connect(self.exit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        global TIME_LEFT
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.exitBtn.setText(_translate("Form", "X"))
        self.label.setText(_translate("Form", "Time left: {}".format(TIME_LEFT)))

    def exit(self):
        sys.exit(0)


class Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
                delta = QPoint(event.globalPos() - self.oldPosition)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPosition = event.globalPos()

    def update_gui(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "time is up!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    w.show()

    w.timer.start(5000)

    sys.exit(app.exec_())
