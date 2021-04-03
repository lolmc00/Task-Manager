import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import schedule_time_list_widget
from module import task, colors, data

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

class ScheduleTimeSettingWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, time_period:task.TimePeriod=task.TimePeriod(0, 0, 1, 0)):
		super().__init__(parent)
		# 전체 레이아웃
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)

		# 일정 시간 리스트 박스
		self.widget_time_list = schedule_time_list_widget.ScheduleListBox(self)
		self.layout.addWidget(self.widget_time_list)

		# 요일 설정 라벨
		self.label_day_of_the_week = QtWidgets.QLabel("Day of the week")
		self.label_day_of_the_week.setStyleSheet("font: 500 15px; color:#dcdcdc")
		self.layout.addWidget(self.label_day_of_the_week)

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
		self.layout.addWidget(self.combo_day_of_the_week)

		# Start, End 시간 설정 위젯
		self.widget_start_time = TimeSettingWidget(self, "Start Time")
		self.layout.addWidget(self.widget_start_time)
		self.widget_end_time = TimeSettingWidget(self, "End Time")
		self.layout.addWidget(self.widget_end_time)

		# 버튼 컨테이너
		self.widget_btn_container = QtWidgets.QWidget()
		self.layout_btn_contaienr = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.layout.addWidget(self.widget_btn_container)
		self.openAddTimeSetting()

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

	def resetTimeSettingInput(self):
		self.combo_day_of_the_week.setCurrentIndex(0)
		self.setCurrentTime(task.TimePeriod("0", "0", "1", "0"))
		self.openAddTimeSetting()

	def getScheduleTimeInCombo(self):
		schedule_time = task.WeeklyScheduleTime(self.combo_day_of_the_week.currentText(), self.getCurrentTimePeriod())
		return schedule_time

	def addTimeSetting(self):
		test_text = self.testScheduleTime(self.parent().getSchedule())
		if test_text != None:
			self.parent().showAlertText(test_text)
			return
		self.widget_time_list.addItem(self.getScheduleTimeInCombo())
		self.resetTimeSettingInput()
	
	def openEditTimeSetting(self, schedule_time:task.WeeklyScheduleTime):
		self.setScheduleTimeInput(schedule_time)
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.btn_time_setting_edit = QtWidgets.QPushButton("Edit")
		self.btn_time_setting_edit.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_PINK, colors.COLOR_DARK_PINK))
		self.btn_time_setting_edit.mouseReleaseEvent = lambda event:self.applyTimeSetting()
		self.btn_time_setting_edit_cancel = QtWidgets.QPushButton("Cancel")
		self.btn_time_setting_edit_cancel.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_PURPLE, colors.COLOR_DARK_PURPLE))
		self.btn_time_setting_edit_cancel.mouseReleaseEvent = lambda event:self.openAddTimeSetting()
		self.layout_btn_container.addWidget(self.btn_time_setting_edit)
		self.layout_btn_container.addWidget(self.btn_time_setting_edit_cancel)

	def openAddTimeSetting(self):
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.btn_time_setting_add = QtWidgets.QPushButton("Add")
		self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_BLUE, colors.COLOR_DARK_BLUE))
		self.btn_time_setting_add.mouseReleaseEvent = lambda event:self.addTimeSetting()
		self.layout_btn_container.addWidget(self.btn_time_setting_add)
		
	def applyTimeSetting(self):
		test_text = self.testScheduleTime(self.parent().getSchedule())
		if test_text != None:
			self.showAlertText(test_text)
			return
		self.applyItem(self.getScheduleTimeInCombo())
		self.resetTimeSettingInput()

	def testScheduleTime(self, schedule:task.Schedule):
		schedule_time = self.getScheduleTimeInCombo()
		if schedule_time.getTimePeriod().getStartTimeToMinute() >= schedule_time.getTimePeriod().getEndTimeToMinute():
			return "The start time cannot be equal to or later than the end time."
		schedule_time_list = schedule.getScheduleTimeList()
		# 일정 시간이 겹치는 경우 알림
		for i in range(len(schedule_time_list) - 1):
			if schedule_time_list[i].checkConflict(schedule_time_list[i + 1]):
				return "The time you set overlaps with the other time."
		
		# 다른 스케쥴과 겹치는 시간이 있으면 알림
		for schedule in data.schedule_list:
			for other_schedule_time in schedule.getScheduleTimeList():
				if schedule_time.checkConflict(other_schedule_time):
					print(other_schedule_time.getTimePeriod().getStartTime())
					return "The time you set overlaps with another schedule."
		return None

	def setScheduleTimeInput(self, schedule_time:task.WeeklyScheduleTime):
		self.combo_day_of_the_week.setCurrentIndex(schedule_time.getDayOfTheWeekIndex())
		self.setCurrentTime(schedule_time.getTimePeriod())