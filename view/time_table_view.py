import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import time_period_widget, schedule_list_widget, color_picker
from module import custom_date, colors

class ScheduleInputView(QtWidgets.QWidget):
    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.parent = parent
        # 세팅 스케쥴 입력 위젯 & 레이아웃 생성
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10,0,10,0)

        # 스케쥴 제목 레이블 생성
        self.label_schedule_title = QtWidgets.QLabel("New Schedule")
        self.label_schedule_title.setStyleSheet("font: 600 22px")
        self.layout.addWidget(self.label_schedule_title)

        # 스케쥴 제목 인풋 생성
        self.edit_schedult_title = QtWidgets.QLineEdit("")
        self.edit_schedult_title.setPlaceholderText("SCHEDULE TITLE")
        self.edit_schedult_title.setStyleSheet("font: 400 17px")
        self.layout.addWidget(self.edit_schedult_title)

        self.layout.addStretch(1)

        # 스케쥴 색상 설정 위젯 생성
        self.widget_color_box = color_picker.ColorItemBox(self)
        self.layout.addWidget(self.widget_color_box)

        self.layout.addStretch(1)

        # 시간 목록 위젯 & 레이아웃 생성
        self.widget_time_list = schedule_list_widget.ScheduleListBox(self, "Time List")
        self.layout.addWidget(self.widget_time_list)

        # 일정 시간 설정 위젯 & 레이아웃
        self.widget_time_setting = QtWidgets.QWidget(self)
        self.layout_time_setting = QtWidgets.QVBoxLayout(self.widget_time_setting)
        self.layout.addWidget(self.widget_time_setting)

        # 요일 설정 라벨
        self.label_day_of_the_week = QtWidgets.QLabel("Day of the week")
        self.label_day_of_the_week.setStyleSheet("font: 500 15px")
        self.layout_time_setting.addWidget(self.label_day_of_the_week)

        # 요일 설정 콤보 박스
        self.combo_day_of_the_week = QtWidgets.QComboBox()
        self.combo_day_of_the_week.addItem("Monday")
        self.combo_day_of_the_week.addItem("Tuesday")
        self.combo_day_of_the_week.addItem("Wednesday")
        self.combo_day_of_the_week.addItem("Thursday")
        self.combo_day_of_the_week.addItem("Friday")
        self.combo_day_of_the_week.addItem("Saturday")
        self.combo_day_of_the_week.addItem("Sunday")
        self.combo_day_of_the_week.setStyleSheet("font: 400 15px")
        self.layout_time_setting.addWidget(self.combo_day_of_the_week)

        # From To 시간 설정 위젯
        self.widget_time_period = time_period_widget.TimePeriodWidget(self)
        self.layout_time_setting.addWidget(self.widget_time_period)

        # 설정한 시간 추가 버튼
        self.btn_time_setting_add = QtWidgets.QPushButton("Add")
        self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_BLUE, colors.COLOR_DARK_BLUE))
        self.btn_time_setting_add.clicked.connect(lambda: self.addTimeSetting())
        self.layout_time_setting.addWidget(self.btn_time_setting_add)

        self.layout.addStretch(1)

        # 스케쥴 생성 & 테이블 초기화 버튼 레이아웃
        self.layout_create_reset_btn_hbox = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.layout_create_reset_btn_hbox)
        
        # 스케쥴 생성 버튼
        self.btn_create_schedule = QtWidgets.QPushButton("Create Schedule")
        self.btn_create_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px} QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
        self.layout_create_reset_btn_hbox.addWidget(self.btn_create_schedule)

        # 테이블 초기화 버튼
        self.btn_reset_table = QtWidgets.QPushButton("Reset Timetable")
        self.btn_reset_table.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_RED, colors.COLOR_DARK_RED))
        self.layout_create_reset_btn_hbox.addWidget(self.btn_reset_table)

    def addTimeSetting(self):
        period = custom_date.Period(self.combo_day_of_the_week.currentText(), self.widget_time_period.getCurrentStartTime(), \
            self.widget_time_period.getCurrentStartMinute(), self.widget_time_period.getCurrentEndTime(), self.widget_time_period.getCurrentEndMinute())
        self.widget_time_list.addItem(self.widget_time_list.PeriodItem(self, period))

class TimeTableView(QtWidgets.QWidget):
    CELL_SIZE = 33

    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        # 메인 윈도우 설정
        self.parent = parent
        self.parent.setSize(self.CELL_SIZE * 26, 1300)
        self.parent.setWindowTitle("Task Manager (Weekly Time Table)")

        # TimeTableView 설정
        self.setFixedHeight(self.CELL_SIZE * 26)

        # 전체 레이아웃 생성
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 상단 정렬용 레이아웃
        self.layout_vertical_1 = QtWidgets.QVBoxLayout()
        self.layout_vertical_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # 타임 테이블 위젯 생성
        self.widget_table = QtWidgets.QWidget(self)
        self.widget_table.setFixedHeight(self.CELL_SIZE * 26)
        self.widget_table.setFixedWidth(1000)
        self.layout.addWidget(self.widget_table)
        self.layout_table = QtWidgets.QGridLayout(self.widget_table)
        self.layout_table.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_table.setContentsMargins(0, 0, 0, 0)
        self.layout_table.setSpacing(0)
        self.layout_vertical_1.addWidget(self.widget_table)
        self.layout.addLayout(self.layout_vertical_1)

        # 타임라인 위젯 리스트 & 레이아웃 리스트 생성
        self.widget_time_list = []
        self.layout_time_list = []
        for i in range(1, 8):
            widget_time = QtWidgets.QWidget(self.widget_table)
            layout_time = QtWidgets.QVBoxLayout(widget_time)
            widget_time.setFixedHeight(self.CELL_SIZE)
            self.widget_time_list.append(widget_time)
            self.layout_time_list.append(layout_time)
            self.layout_table.addWidget(self.widget_time_list[i - 1], 1, i, 24, 1)

        # 요일 레이블 생성
        dateStrList = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i in range(1, 8):
            label_date = QtWidgets.QLabel(dateStrList[i - 1])
            label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            label_date.setFixedHeight(self.CELL_SIZE)
            label_date.setStyleSheet("font: 200 20px;" + ("border-right: 1px solid #fff" if i != 7 else ""))
            self.layout_table.addWidget(label_date, 0, i)

        # 시간 레이블 생성
        for i in range(0, 25):
            label_time = QtWidgets.QLabel("%i:00" % i if i >= 10 else "0%i:00" % i)
            label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            label_time.setFixedHeight(self.CELL_SIZE)
            label_time.setStyleSheet("font: 400 14px;" + ("border-top: 1px solid #3e3e3e; border-radius: 0px;" if i == 24 else ""))
            self.layout_table.addWidget(label_time, i + 1, 0)
        
        # 경계선 레이블 생성
        for i in range(1, 8):
            label_time = QtWidgets.QLabel("")
            label_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_time.setFixedHeight(self.CELL_SIZE)
            label_time.setStyleSheet("border-top: 1px solid #3e3e3e; border-radius: 0px")
            self.layout_table.addWidget(label_time, 25, i)

        # 상단 정렬용 레이아웃
        self.layout_vertical_2 = QtWidgets.QVBoxLayout()
        self.layout_vertical_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.layout_vertical_2)
        # 세팅 컨테이너 위젯 & 레이아웃 생성
        self.widget_setting_container = QtWidgets.QWidget(self)
        self.widget_setting_container.setObjectName("setting_container")
        self.widget_setting_container.setFixedHeight(self.CELL_SIZE * 25)
        self.widget_setting_container.setStyleSheet("QWidget#setting_container{border-left: 1px solid #3e3e3e;}")
        self.layout_setting_container = QtWidgets.QVBoxLayout(self.widget_setting_container)
        self.layout_setting_container.setSpacing(0)
        self.layout_setting_container.setContentsMargins(0, 0, 0, 0)
        self.layout_setting_container.addWidget(ScheduleInputView(self.widget_setting_container))
        self.layout_vertical_2.addWidget(self.widget_setting_container)


        # self.layout.removeWidget(self.widget_setting_container)