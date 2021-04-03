import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from . import custom_widget, tooltip
from module import task, colors, data

CELL_HEIGHT = 33
CELL_WIDTH = 125

class TimeTableScheduleItem(tooltip.ToolTipWidget):
    def __init__(self, parent:QtWidgets.QWidget=None, title:str="New Schedule", color:str=colors.COLOR_AQUA, schedule:task.Schedule=None, schedule_time:task.WeeklyScheduleTime=None, table:QtWidgets.QWidget=None):
        super().__init__(parent)
        self.table = table
        self.parent = parent
        self.schedule = schedule
        self.schedule_time = schedule_time
        self.title = title
        self.color = color
        for schedule_time in schedule.getScheduleTimeList():
            super().addItem(title, schedule_time, schedule_time == self.schedule_time, color)
        self.setObjectName("container")
        self.setStyleSheet("QWidget{background-color:%s; font-family:'나눔스퀘어';} QWidget#container{border-top: 3px solid #DDDDDD;}" % (color))
        self.setContentsMargins(4, 6, 2, 2)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setGeometryByTime()

        # 전체 레이아웃
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # 일정 제목 라벨
        self.label_title = custom_widget.MultipleLineLabel(self, self.title, parent.geometry())
        self.label_title.setMouseTracking(True)
        self.label_title.mouseMoveEvent = lambda event: self.mouseMoveEvent(event)
        self.label_title.mouseReleaseEvent = lambda event : self.table.editSchedule(self.schedule)
        self.layout.addWidget(self.label_title)

    def setGeometryByTime(self):
        parent_height = float(self.parent.height())
        DAY_MINUTE = float(24 * 60)
        start_minute = float(self.schedule_time.getTimePeriod().getStartTimeToMinute())
        end_minute = float(self.schedule_time.getTimePeriod().getEndTimeToMinute())
        x = self.parent.contentsMargins().left()
        y = parent_height * (start_minute/DAY_MINUTE)
        height = (parent_height * (end_minute/DAY_MINUTE)) - y
        width = self.parent.contentsRect().width()
        self.setGeometry(x, y, width, height)

    def mouseReleaseEvent(self, event):
        self.table.editSchedule(self.schedule)

    def setFocusOn(self, isFocusOn):
        if isFocusOn:
            self.setGraphicsEffect(None)
        else:
            opacity = QtWidgets.QGraphicsOpacityEffect(self)
            opacity.setOpacity(0.1)
            self.setGraphicsEffect(opacity)

class TimeTableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.parent = parent
        self.main = main
        # 타임 테이블 위젯 생성
        self.setFixedSize(1000, CELL_HEIGHT * 26)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 스케쥴 아이템 컨테이너 레이아웃 리스트 생성
        self.widget_time_list = []
        for i in range(1, 8):
            widget_time = QtWidgets.QWidget()
            widget_time.setContentsMargins(12, 3, 12, 3)
            widget_time.setFixedSize(CELL_WIDTH, CELL_HEIGHT*24)
            self.widget_time_list.append(widget_time)
            self.layout.addWidget(widget_time, 2, i, 24, 1)
        
        # 요일 레이블 생성
        date_str_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i in range(1, 8):
            label_date = QtWidgets.QLabel(date_str_list[i - 1])
            label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            label_date.setFixedSize(CELL_WIDTH, CELL_HEIGHT)
            label_date.setStyleSheet("font: 200 20px;" + ("border-right: 1px solid #fff" if i != 7 else ""))
            self.layout.addWidget(label_date, 0, i)

        # 시간 레이블 생성
        for i in range(0, 25):
            label_time = QtWidgets.QLabel("%i:00" % i if i >= 10 else "0%i:00" % i)
            label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            label_time.setFixedSize(CELL_WIDTH, CELL_HEIGHT)
            label_time.setStyleSheet("font: 400 14px;" + ("border-top: 1px solid #3e3e3e; border-radius: 0px;" if i == 24 else ""))
            self.layout.addWidget(label_time, i + 2, 0)
        
        # 경계선 레이블 생성
        for i in range(1, 8):
            label_time = QtWidgets.QLabel("")
            label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_time.setFixedSize(CELL_WIDTH, CELL_HEIGHT)
            label_time.setStyleSheet("border-top: 1px solid #3e3e3e; border-radius: 0px")
            self.layout.addWidget(label_time, 26, i)

    def addSchedule(self, schedule:task.Schedule):
        for schedule_time in schedule.schedule_time_list:
            idx = schedule_time.getDayOfTheWeekIndex()
            item = TimeTableScheduleItem(self.widget_time_list[idx], schedule.getTitle(), schedule.getColor(), schedule, schedule_time, self)
            item.show()

    def deleteSchedule(self, schedule:task.Schedule):
        for idx in range(len(self.widget_time_list)):
            for schedule_item in self.widget_time_list[idx].children():
                if schedule_item.schedule == schedule:
                    schedule_item.setParent(None)

    def editSchedule(self, schedule:task.Schedule):
        if self.parent.widget_setting.current_editing_schedule == schedule:
            return
        for idx in range(len(self.widget_time_list)):
            for schedule_item in self.widget_time_list[idx].children():
                schedule_item.setFocusOn(schedule_item.schedule == schedule)
        self.parent.widget_setting.openEditSchedule(schedule)

    def resetFocusItems(self):
        for idx in range(len(self.widget_time_list)):
            for schedule_item in self.widget_time_list[idx].children():
                schedule_item.setFocusOn(True)