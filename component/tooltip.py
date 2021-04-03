import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
from module import task

class ToolTipWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.text_list = ["<span style=\"font: 100 14px '나눔스퀘어';\">", "</span>"]
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AlwaysShowToolTips)

    def addItem(self, title, time:task.WeeklyScheduleTime, isFocusOn, color):
        weight = "bold" if isFocusOn else "400"
        title = "<span style=\"font-weight:%s; color:%s\">%s</span>" % (weight, color, title)
        time = "<span style=\"font-weight:%s;\">%s %s</span>" % (weight, time.getDayOfTheWeek()[:3].upper() + ".", time.getTimePeriod().getTimeString())
        text = "<div>%s<br>%s</div>" % (title, time)
        self.text_list.insert(len(self.text_list) - 1, text)

    def mouseMoveEvent(self, event):
        pos = QtCore.QPoint(event.globalX(), event.globalY())
        size = QtCore.QSize(100, 100)
        QtWidgets.QToolTip.showText(pos, ''.join(self.text_list), self, QtCore.QRect(pos, size))
        super().mouseMoveEvent(event)