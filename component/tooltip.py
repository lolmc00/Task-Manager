import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
from module import custom_date

class ToolTipWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.text_list = ["<span style=\"font: 100 14px '나눔스퀘어';\">", "</span>"]
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips)

    def addItem(self, title, time:custom_date.DayScheduleTime, color):
        title = "<span style=\"font-weight:500; color:%s\">%s</span>" % (color, title)
        day_of_the_week = time.getDayOfTheWeek()[:3].upper() + "."
        text = "<div>%s<br>%s %s</div>" % (title, day_of_the_week, time.getTimeString())
        self.text_list.insert(len(self.text_list) - 1, text)

    def mouseMoveEvent(self, event):
        pos = QtCore.QPoint(event.globalX(), event.globalY())
        size = QtCore.QSize(100, 100)
        QtWidgets.QToolTip.showText(pos, ''.join(self.text_list), self, QtCore.QRect(pos, size))
        super().mouseMoveEvent(event)