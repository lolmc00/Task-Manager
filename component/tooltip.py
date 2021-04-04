import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
from module import task, colors

class ToolTipWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.main = main
        self.text_list = ["<span style=\"font: 400 14px 'Segoe UI';\">", "</span>"]
        self.show_text = ""
        self.setMouseTracking(True)

    def addScheduleItem(self, title, time:task.WeeklyScheduleTime, isFocusOn, color):
        weight = "bold" if isFocusOn else "400"
        title = "<span style=\"font-weight:%s; color:%s\">%s</span>" % (weight, color, title)
        time = "<span style=\"font-weight:%s;\">%s %s</span>" % (weight, time.getDayOfTheWeek()[:3].upper() + ".", time.getTimePeriod().getTimeString())
        text = "<div>%s<br>%s</div>" % (title, time)
        self.text_list.insert(len(self.text_list) - 1, text)

    def addTodoItem(self, todo:task.Todo, isFocusOn):
        completed = "<div style=\"color:%s; font-weight: 700\">[ Completed Task ]</div><br>" % colors.COLOR_AQUA
        title = "<span style=\"font-weight: 700\">TITLE: </span><span style=\"color:%s;font-weight:400'\">%s</span>" % (todo.getColor(), todo.getTitle())
        date = "<div>%s</div>" % (todo.getDate().strftime("%Y-%m-%d %a"))
        scheduled_on = "<br><div style=\"font-weight: 700\">SCHEDULED ON:</div>%s<div>%s</div>" % (date, todo.getTimePeriod().getTimeString() if todo.getParentSchedule() == None else todo.getParentSchedule().getTitle())
        description = "<br><div style=\"font-weight: 700\">DESCRIPTION:</div>%s" % todo.getDescriptionHtml()
        if todo.getDescription() == '':
            description = ""
        if not todo.isCompleted():
            completed = ""
        text = "<div>%s%s%s%s</div>" % (completed, title, scheduled_on, description)
        self.text_list.insert(len(self.text_list) - 1, text)
        self.show_text = ''.join(self.text_list)

    # def enterEvent(self, event):
    #     self.main.tooltip.showToolTip(self.show_text)
    # def leaveEvent(self, event):
    #     self.main.tooltip.hideToolTip()
    # def mouseMoveEvent(self, event):
    #     self.main.tooltip.moveToolTip(event.x(), event.y())
    # def mouseMoveEvent(self, event):
    #     pos = QtCore.QPoint(event.globalX(), event.globalY())
    #     size = QtCore.QSize(100, 100)
    #     QtWidgets.QToolTip.showText(pos, self.show_text, self, QtCore.QRect(pos, size))
    #     super().mouseMoveEvent(event)