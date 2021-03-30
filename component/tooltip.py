import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore

class ToolTipWidget(QtWidgets.QWidget):
    title_list = []
    time_list = []
    text_list = ["<span style=\"font-size:12px;\">"]
    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips)

    def addItem(self, title, time):
        self.title_list.append(title)
        self.time_list.append(time)
        text = "%s<br>%s" % (title, time)
        self.text_list.append(text)

    def mouseMoveEvent(self, event):
        pos = QtCore.QPoint(event.globalX(), event.globalY())
        size = QtCore.QSize(100, 100)
        QtWidgets.QToolTip.showText(pos, ''.join(self.text_list), self, QtCore.QRect(pos, size))
        super().mouseMoveEvent(event)