import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from module import custom_date


class TimeSettingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, label=None):
        super().__init__(parent)
        # 시작 시간 위젯 & 레이아웃
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # 레이블
        self.label = QtWidgets.QLabel(label)
        self.label.setStyleSheet("font: 500 15px")
        self.layout.addWidget(self.label)

        # 시작 시간 콤보 박스 컨테이너 위젯 & 레이아웃
        self.widget_time_combo_container = QtWidgets.QWidget(self)
        self.layout_time_combo_container = QtWidgets.QHBoxLayout(self.widget_time_combo_container)
        self.layout_time_combo_container.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.widget_time_combo_container)

        # 시간 콤보 박스
        self.combo_time = QtWidgets.QComboBox(self.widget_time_combo_container)
        self.combo_time.setStyleSheet("font: 400 15px")
        self.combo_time.setFixedWidth(123)
        for i in range(0, 25):
            self.combo_time.addItem(("0" if i < 10 else "") + str(i))
        self.layout_time_combo_container.addWidget(self.combo_time)

        # seperate (:) 레이블
        self.label_seperate = QtWidgets.QLabel(":")
        self.label_seperate.setStyleSheet("font: 500 20px;")
        self.layout_time_combo_container.addWidget(self.label_seperate)

        # 분(Minute) 콤보 박스
        self.combo_minute = QtWidgets.QComboBox(self.widget_time_combo_container)
        self.combo_minute.setStyleSheet("font: 400 15px")
        self.combo_minute.setFixedWidth(123)
        for i in range(0, 61):
            self.combo_minute.addItem(("0" if i < 10 else "") + str(i))
        self.layout_time_combo_container.addWidget(self.combo_minute)

class ScheduleTimeSettingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
		# 전체 레이아웃
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.widget_start_time = TimeSettingWidget(self, "Start")
        self.layout.addWidget(self.widget_start_time)
        self.widget_end_time = TimeSettingWidget(self, "End")
        self.layout.addWidget(self.widget_end_time)

    def setCurrentTime(self, schedule_time:custom_date.DayScheduleTime):
        self.widget_start_time.combo_time.setCurrentIndex(schedule_time.getStartTime())
        self.widget_start_time.combo_minute.setCurrentIndex(schedule_time.getStartTimeMinute())
        self.widget_end_time.combo_time.setCurrentIndex(schedule_time.getEndTime())
        self.widget_end_time.combo_minute.setCurrentIndex(schedule_time.getEndTimeMinute())

    def getCurrentStartTime(self):
        return self.widget_start_time.combo_time.currentText()

    def getCurrentStartMinute(self):
        return self.widget_start_time.combo_minute.currentText()

    def getCurrentEndTime(self):
        return self.widget_end_time.combo_time.currentText()

    def getCurrentEndMinute(self):
        return self.widget_end_time.combo_minute.currentText()
        