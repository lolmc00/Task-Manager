import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class TimeTableView(QtWidgets.QWidget):
    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        # 메인 윈도우 설정
        self.parent = parent
        self.parent.setFixedHeight(1000)
        self.parent.setFixedWidth(1400)
        self.parent.setWindowTitle("Task Manager (Weekly Time Table)")

        # 전체 레이아웃 생성
        layout = QtWidgets.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 타임 테이블 위젯 생성
        widget_table = QtWidgets.QWidget(self)
        widget_table.setFixedHeight(858)
        widget_table.setFixedWidth(1000)
        layout_table = QtWidgets.QGridLayout(widget_table)
        layout_table.setContentsMargins(0, 0, 0, 0)
        layout_table.setSpacing(0)

        # 타임라인 위젯 리스트 & 레이아웃 리스트 생성
        self.widget_timeline_list = []
        self.layout_timeline_list = []
        for i in range(1, 8):
            widget_timeline = QtWidgets.QWidget(widget_table)
            # widget_timeline.setStyleSheet('background:#000')
            layout_timeline = QtWidgets.QVBoxLayout(widget_timeline)
            self.widget_timeline_list.append(widget_timeline)
            self.layout_timeline_list.append(layout_timeline)
            layout_table.addWidget(self.widget_timeline_list[i - 1], 1, i, 24, 1)

        # 요일 레이블 생성
        dateStrList = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i in range(1, 8):
            label_date = QtWidgets.QLabel(dateStrList[i - 1])
            label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            label_date.setStyleSheet("font: 200 20px;" + ("border-right: 1px solid #fff" if i != 7 else ""))
            layout_table.addWidget(label_date, 0, i)

        # 시간 레이블 생성
        for i in range(0, 25):
            label_time = QtWidgets.QLabel("%i:00" % i if i >= 10 else "0%i:00" % i)
            label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            label_time.setStyleSheet("font: 400 14px;" + ("border-top: 1px solid #3e3e3e" if i == 24 else ""))
            layout_table.addWidget(label_time, i + 1, 0)
        # 경계선 레이블 생성
        for i in range(1, 8):
            label_time = QtWidgets.QLabel("")
            label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_time.setStyleSheet("border-top: 1px solid #3e3e3e")
            layout_table.addWidget(label_time, 25, i)

        layout.addWidget(widget_table)

        # 세팅 위젯 & 레이아웃 생성
        self.widget_setting = QtWidgets.QWidget(self)
        self.widget_setting.setFixedHeight(792)
        self.widget_setting.setStyleSheet("border-left: 1px solid #3e3e3e")
        self.layout_setting = QtWidgets.QVBoxLayout(self.widget_setting)
        self.layout_setting.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout_setting.setContentsMargins(0, 0, 0, 0)
        self.layout_setting.setSpacing(0)

        # 스케쥴 생성 버튼 생성
        self.btn_create_schedule = QtWidgets.QPushButton("Create New Schedule")
        self.btn_create_schedule.setStyleSheet("QPushButton{border:0px; background-color: #50C878; font: 500 16px} QPushButton:hover{background-color:#50A688}")
        self.btn_create_schedule.setFixedHeight(35)
        self.btn_create_schedule.setFixedWidth(210)
        self.layout_setting.addWidget(self.btn_create_schedule)

        self.layout_setting.addStretch()

        # 타임테이블 리셋 버튼 생성
        btn_reset_table = QtWidgets.QPushButton("Reset Timetable")
        btn_reset_table.setStyleSheet("QPushButton{border:0px; background-color: #D24141; font: 500 16px}  QPushButton:hover{background-color:#CC0000}")
        btn_reset_table.setFixedHeight(35)
        btn_reset_table.setFixedWidth(210)
        self.layout_setting.addWidget(btn_reset_table)

        layout.addWidget(self.widget_setting)
