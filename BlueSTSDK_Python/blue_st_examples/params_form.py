# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'params_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt

import sys

import globals


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
        self.recordBtn = QtWidgets.QPushButton(self.widget)
        self.recordBtn.setGeometry(QtCore.QRect(230, 420, 291, 85))
        self.recordBtn.setStyleSheet("")
        self.recordBtn.setObjectName("recordBtn")
        self.streamCheck = QtWidgets.QCheckBox(self.widget)
        self.streamCheck.setGeometry(QtCore.QRect(160, 180, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.streamCheck.setFont(font)
        self.streamCheck.setObjectName("streamCheck")
        self.settingsLabel = QtWidgets.QLabel(self.widget)
        self.settingsLabel.setGeometry(QtCore.QRect(300, 120, 150, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.settingsLabel.setFont(font)
        self.settingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.settingsLabel.setObjectName("settingsLabel")
        self.warningLabel = QtWidgets.QLabel(self.widget)
        self.warningLabel.setGeometry(QtCore.QRect(390, 180, 301, 70))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.warningLabel.setFont(font)
        self.warningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.warningLabel.setObjectName("warningLabel")
        self.durationLabel = QtWidgets.QLabel(self.widget)
        self.durationLabel.setGeometry(QtCore.QRect(160, 280, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.durationLabel.setFont(font)
        self.durationLabel.setObjectName("durationLabel")
        self.saveCheck = QtWidgets.QCheckBox(self.widget)
        self.saveCheck.setGeometry(QtCore.QRect(160, 220, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.saveCheck.setFont(font)
        self.saveCheck.setObjectName("saveCheck")
        self.gridLayoutWidget = QtWidgets.QWidget(self.widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(100, 320, 561, 71))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.secondsLayout = QtWidgets.QHBoxLayout()
        self.secondsLayout.setObjectName("secondsLayout")
        self.secondBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.secondBox.setFont(font)
        self.secondBox.setMinimum(1)
        self.secondBox.setMaximum(59)
        self.secondBox.setObjectName("secondBox")
        self.secondsLayout.addWidget(self.secondBox)
        self.secondLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.secondLabel.setFont(font)
        self.secondLabel.setObjectName("secondLabel")
        self.secondsLayout.addWidget(self.secondLabel)
        self.gridLayout.addLayout(self.secondsLayout, 0, 2, 1, 1)
        self.hoursLayout = QtWidgets.QHBoxLayout()
        self.hoursLayout.setObjectName("hoursLayout")
        self.hourBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.hourBox.setFont(font)
        self.hourBox.setMaximum(23)
        self.hourBox.setObjectName("hourBox")
        self.hoursLayout.addWidget(self.hourBox)
        self.hourLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.hourLabel.setFont(font)
        self.hourLabel.setObjectName("hourLabel")
        self.hoursLayout.addWidget(self.hourLabel)
        self.gridLayout.addLayout(self.hoursLayout, 0, 0, 1, 1)
        self.minsLayout = QtWidgets.QHBoxLayout()
        self.minsLayout.setObjectName("minsLayout")
        self.minBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.minBox.setFont(font)
        self.minBox.setMaximum(59)
        self.minBox.setObjectName("minBox")
        self.minsLayout.addWidget(self.minBox)
        self.minLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.minLabel.setFont(font)
        self.minLabel.setObjectName("minLabel")
        self.minsLayout.addWidget(self.minLabel)
        self.gridLayout.addLayout(self.minsLayout, 0, 1, 1, 1)
        self.mainLabel.raise_()
        self.micLabel.raise_()
        self.header.raise_()
        self.headerFade.raise_()
        self.headerLabel.raise_()
        self.exitBtn.raise_()
        self.recordBtn.raise_()
        self.streamCheck.raise_()
        self.settingsLabel.raise_()
        self.warningLabel.raise_()
        self.durationLabel.raise_()
        self.saveCheck.raise_()
        self.gridLayoutWidget.raise_()

        self.exitBtn.clicked.connect(self.exit)
        self.recordBtn.clicked.connect(self.recording)
        self.widget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.exitBtn.setText(_translate("Form", "X"))
        self.recordBtn.setText(_translate("Form", "START RECORDING"))
        self.streamCheck.setText(_translate("Form", "Stream audio on my PC"))
        self.settingsLabel.setText(_translate("Form", "SETTINGS"))
        self.warningLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">Make sure the STM32 is at a reasonable</span></p><p><span style=\" font-size:9pt; font-weight:600; font-style:italic;\">distance from your PC (microphonics)!</span></p></body></html>"))
        self.durationLabel.setText(_translate("Form", "Set the session duration:"))
        self.saveCheck.setText(_translate("Form", "Save recording"))
        self.secondLabel.setText(_translate("Form", "seconds"))
        self.hourLabel.setText(_translate("Form", "hours"))
        self.minLabel.setText(_translate("Form", "minutes"))

    def exit(self):
        sys.exit(0)

    def recording(self):
        
        to_secs = self.hourBox.value()*60*60 + self.minBox.value()*60 + self.secondBox.value()
        r = str(int(self.streamCheck.isChecked())) + "," + \
            str(int(self.saveCheck.isChecked())) + "," + \
                str(to_secs) #stream, save, duration

        sys.stdout.write(r)

        sys.exit(globals.RECORDING_CODE)



class Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
                delta = QPoint(event.globalPos() - self.oldPosition)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPosition = event.globalPos()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
