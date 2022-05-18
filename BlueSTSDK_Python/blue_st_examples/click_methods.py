#click methods
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt

Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)

self.exitBtn.clicked.connect(self.exit))

self.widget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))

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
