import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import schedule_time_list_widget, time_period_widget
from module import task, colors, data

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

		# 시간 선택 위젯
		self.widget_time_period = time_period_widget.TimePeirodWidget(self)
		self.layout.addWidget(self.widget_time_period)

		# 버튼 컨테이너
		self.widget_btn_container = QtWidgets.QWidget()
		self.layout_btn_contaienr = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.layout.addWidget(self.widget_btn_container)
		self.openAddTimeSetting()

	def resetTimeSettingInput(self):
		self.combo_day_of_the_week.setCurrentIndex(0)
		self.widget_time_period.setCurrentTime(task.TimePeriod("0", "0", "1", "0"))
		self.openAddTimeSetting()

	def getScheduleTimeInCombo(self):
		schedule_time = task.WeeklyScheduleTime(self.combo_day_of_the_week.currentText(), self.widget_time_period.getCurrentTimePeriod())
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
		self.btn_time_setting_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
		self.btn_time_setting_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_BLUE, colors.COLOR_DARK_BLUE))
		self.btn_time_setting_add.mouseReleaseEvent = lambda event:self.addTimeSetting()
		self.layout_btn_container.addWidget(self.btn_time_setting_add)
		
	def applyTimeSetting(self):
		test_text = self.testScheduleTime(self.parent().getSchedule())
		if test_text != None:
			self.showAlertText(test_text)
			return
		self.widget_time_list.applyItem(self.getScheduleTimeInCombo())
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
					return "The time you set overlaps with another schedule."
		return None

	def setScheduleTimeInput(self, schedule_time:task.WeeklyScheduleTime):
		self.combo_day_of_the_week.setCurrentIndex(schedule_time.getDayOfTheWeekIndex())
		self.setCurrentTime(schedule_time.getTimePeriod())