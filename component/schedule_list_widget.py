import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from module import custom_date, colors

class ScheduleListBox(QtWidgets.QWidget):
    class ScheduleItem(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

    class PeriodItem(ScheduleItem):
        def __init__(self, parent=None, period:custom_date.Period = None):
            super().__init__(parent)
            self.setFixedHeight(44)
            self.setAttribute(QtCore.Qt.WA_StyledBackground)
            self.setObjectName("container")
            self.setStyleSheet("QWidget#container{border:1px solid #448aff}")
            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.setContentsMargins(1,1,1,1)
            self.layout.setSpacing(0)

            # 상단 요일, 도구 컨테이너
            self.widget_top = QtWidgets.QWidget(self)
            self.widget_top.setObjectName("widget_top")
            self.widget_top.setAttribute(QtCore.Qt.WA_StyledBackground)
            self.widget_top.setStyleSheet("background-color:#448aff")
            self.layout_top = QtWidgets.QHBoxLayout(self.widget_top)
            self.layout_top.setContentsMargins(5,0,0,5)
            self.layout_top.setSpacing(0)
            self.layout.addWidget(self.widget_top)

            # 요일 라벨
            self.label_day_of_the_week = QtWidgets.QLabel(period.getDayOfTheWeek())
            self.label_day_of_the_week.setStyleSheet("font: 600 15px;")
            self.layout_top.addWidget(self.label_day_of_the_week)

            # 컨텐츠 컨테이너
            self.widget_contents = QtWidgets.QWidget(self)
            self.layout_contents = QtWidgets.QHBoxLayout(self.widget_contents)
            self.layout_contents.setContentsMargins(5,2,2,5)
            self.layout_contents.setSpacing(0)
            self.layout.addWidget(self.widget_contents)

            # 시작 시간, 끝 시간 레이블
            self.label_time_period = QtWidgets.QLabel(period.getStartFullTime() + " ~ " + period.getEndFullTime())
            self.label_time_period.setStyleSheet("font: 500 15px; color:#666")
            self.layout_contents.addWidget(self.label_time_period)


    class TaskItem(ScheduleItem):
        def __init__(self):
            super().__init__()

    def __init__(self, parent=None, title:str = None):
        super().__init__(parent)
		# 전체 레이아웃
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        # 리스트 박스 제목
        self.label_title = QtWidgets.QLabel(title)
        self.label_title.setStyleSheet("font: 600 22px")
        self.layout.addWidget(self.label_title)

        # 리스트 박스 컨테이너
        self.layout_schedule_list_container = QtWidgets.QVBoxLayout()
        self.layout_schedule_list_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_schedule_list_container.setContentsMargins(0,0,0,0)
        self.layout_schedule_list_container.setSpacing(0)
        self.layout.addLayout(self.layout_schedule_list_container)

        # 리스트 박스
        self.widget_schedule_list = QtWidgets.QWidget()
        self.widget_schedule_list.setFixedWidth(270)
        self.widget_schedule_list.setContentsMargins(2,2,2,2)
        self.widget_schedule_list.setObjectName("list_container")
        self.widget_schedule_list.setStyleSheet("QWidget{background-color:%s;} QWidget#list_container{border: 1px solid #111}" % (colors.COLOR_DARK_BACKGROUND))
        self.layout_schedule_list = QtWidgets.QVBoxLayout(self.widget_schedule_list)
        self.layout_schedule_list.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_schedule_list.setContentsMargins(0,0,0,0)
        self.layout_schedule_list.setSpacing(1)

        # 리스트 박스 스크롤 에리어
        self.scroll_schedule_list = QtWidgets.QScrollArea()
        self.scroll_schedule_list.setFixedHeight(230)
        self.scroll_schedule_list.setWidgetResizable(True)
        self.scroll_schedule_list.setWidget(self.widget_schedule_list)
        self.layout_schedule_list_container.addWidget(self.scroll_schedule_list)

    def addItem(self, item: ScheduleItem):
        self.layout_schedule_list.addWidget(item)
        
    def removeItem(self, item: ScheduleItem):
        self.layout_schedule_list.removeWidget(item)
        