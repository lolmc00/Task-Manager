import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from module import task

class TimeSettingWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, label=None):
		super().__init__(parent)
		# 시작 시간 위젯 & 레이아웃
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		
		# 레이블
		self.label = QtWidgets.QLabel(label)
		self.label.setStyleSheet("font: 500 15px; color:#dcdcdc;")
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
		self.combo_time.currentIndexChanged.connect(self.setDisabledComboMinute)
		for i in range(0, 25):
			self.combo_time.addItem(("0" if i < 10 else "") + str(i))
		self.layout_time_combo_container.addWidget(self.combo_time)

		# seperate (:) 레이블
		self.label_seperate = QtWidgets.QLabel(":")
		self.label_seperate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.label_seperate.setStyleSheet("font: 500 20px;")
		self.layout_time_combo_container.addWidget(self.label_seperate)

		# 분(Minute) 콤보 박스
		self.combo_minute = QtWidgets.QComboBox(self.widget_time_combo_container)
		self.combo_minute.setStyleSheet("font: 400 15px")
		self.combo_minute.setFixedWidth(123)
		for i in range(0, 61):
			self.combo_minute.addItem(("0" if i < 10 else "") + str(i))
		self.layout_time_combo_container.addWidget(self.combo_minute)

	def setDisabledComboMinute(self, value):
		if hasattr(self, 'combo_minute'):
			if value == 24:
				self.combo_minute.setCurrentIndex(0)
				self.combo_minute.setDisabled(True)
			else:
				self.combo_minute.setDisabled(False)

class TimePeirodWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, time_period:task.TimePeriod=task.TimePeriod(0, 0, 1, 0)):
		super().__init__(parent)
		self.layout = QtWidgets.QVBoxLayout(self)
		# Start, End 시간 설정 위젯
		self.widget_start_time = TimeSettingWidget(self, "Start Time")
		self.layout.addWidget(self.widget_start_time)
		self.widget_end_time = TimeSettingWidget(self, "End Time")
		self.layout.addWidget(self.widget_end_time)

	def setCurrentTime(self, time_period:task.TimePeriod):
		self.widget_start_time.combo_time.setCurrentIndex(time_period.getStartTime())
		self.widget_start_time.combo_minute.setCurrentIndex(time_period.getStartTimeMinute())
		self.widget_end_time.combo_time.setCurrentIndex(time_period.getEndTime())
		self.widget_end_time.combo_minute.setCurrentIndex(time_period.getEndTimeMinute())

	def getCurrentStartTime(self):
		return self.widget_start_time.combo_time.currentText()

	def getCurrentStartMinute(self):
		return self.widget_start_time.combo_minute.currentText()

	def getCurrentEndTime(self):
		return self.widget_end_time.combo_time.currentText()

	def getCurrentEndMinute(self):
		return self.widget_end_time.combo_minute.currentText()

	def getCurrentTimePeriod(self):
		return task.TimePeriod(self.getCurrentStartTime(), self.getCurrentStartMinute(), \
			self.getCurrentEndTime(), self.getCurrentEndMinute())