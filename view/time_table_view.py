import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
import main
from component import time_table_widget, schedule_input_widget, color_picker
from modules import task, colors, data

CELL_SIZE = 33
WIDTH = 1300
HEIGHT = CELL_SIZE * 26

class TimeTableView(QtWidgets.QWidget):
    def __init__(self, main:main.MainWindow=None):
        super().__init__(None)
        # 메인 윈도우 설정
        self.main = main
        # 전체 레이아웃 생성
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 상단 정렬용 레이아웃
        self.layout_vertical_1 = QtWidgets.QVBoxLayout()
        self.layout_vertical_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.layout_vertical_1)

        # Table 생성
        self.widget_table = time_table_widget.TimeTableWidget(self, self.main)
        self.layout_vertical_1.addWidget(self.widget_table)

        # 상단 정렬용 레이아웃
        self.layout_vertical_2 = QtWidgets.QVBoxLayout()
        self.layout_vertical_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.layout_vertical_2)

        # 세팅 컨테이너 위젯 & 레이아웃 생성
        self.widget_setting_container = QtWidgets.QWidget(self)
        self.widget_setting_container.setObjectName("setting_container")
        self.widget_setting_container.setFixedHeight(CELL_SIZE * 25)
        self.widget_setting_container.setStyleSheet("QWidget#setting_container{border-left: 1px solid #3e3e3e;}")
        self.layout_setting_container = QtWidgets.QVBoxLayout(self.widget_setting_container)
        self.layout_setting_container.setSpacing(0)
        self.layout_setting_container.setContentsMargins(0, 0, 0, 0)
        self.widget_setting = schedule_input_widget.ScheduleInputWidget(self)
        self.layout_setting_container.addWidget(self.widget_setting)
        self.layout_vertical_2.addWidget(self.widget_setting_container)

    def loadData(self):
        self.widget_table.loadData()
        self.widget_setting.loadData()