import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import schedule_time_setting_widget, schedule_time_list_widget, color_picker
from module import custom_date, colors, data, task
import threading

class ScheduleInputWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, schedule:task.Schedule=None):
		super().__init__(parent)
		self.parent = parent
		# 세팅 스케쥴 입력 위젯 & 레이아웃 생성
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(10,0,10,0)

		# 현재 수정중인 스케쥴 아이템 (None == New Schedule)
		self.current_editing_schedule = None

		# 스케쥴 제목 레이블 생성
		self.label_schedule_title = QtWidgets.QLabel("New Schedule")
		self.label_schedule_title.setStyleSheet("font: 600 22px")
		self.layout.addWidget(self.label_schedule_title)

		# 스케쥴 제목 인풋 생성
		self.edit_schedule_title = QtWidgets.QLineEdit("")
		self.edit_schedule_title.setPlaceholderText("SCHEDULE TITLE")
		self.edit_schedule_title.setStyleSheet("font: 400 17px")
		self.layout.addWidget(self.edit_schedule_title)

		self.layout.addStretch(1)

		# 스케쥴 색상 설정 위젯 생성
		self.widget_color_box = color_picker.ColorItemBox(self)
		self.layout.addWidget(self.widget_color_box)

		self.layout.addStretch(1)

		# 시간 목록 위젯 & 레이아웃 생성
		self.widget_time_list = schedule_time_list_widget.ScheduleListBox(self, "Time List")
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
		self.widget_time_schedule = schedule_time_setting_widget.ScheduleTimeSettingWidget(self)
		self.layout_time_setting.addWidget(self.widget_time_schedule)

		# 설정한 시간 추가 버튼
		self.btn_time_setting_add = QtWidgets.QPushButton("Add")
		self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_BLUE, colors.COLOR_DARK_BLUE))
		self.btn_time_setting_add.mouseReleaseEvent = lambda event:self.addTimeSetting()
		self.layout_time_setting.addWidget(self.btn_time_setting_add)

		self.layout.addStretch(1)

		# 버튼 컨테이너
		self.widget_btn_container = QtWidgets.QWidget(self)
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.layout.addWidget(self.widget_btn_container)

		# 스케쥴 생성 UI로 열기
		self.openCreateNewSchedule()

		# 아이템 로드
		self.loadScheduleItem()

	def loadScheduleItem(self):
		for schedule in data.schedule_list:
			self.parent.widget_table.addSchedule(schedule)

	def openCreateNewSchedule(self):
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.resetInput()
		self.parent.widget_table.resetFocusItems()
		self.label_schedule_title.setText("New Schedule")
		self.current_editing_schedule = None
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		# 스케쥴 생성 버튼
		self.btn_create_schedule = QtWidgets.QPushButton("Create Schedule")
		self.btn_create_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px} QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_create_schedule.clicked.connect(self.createSchedule)
		# 테이블 초기화 버튼
		self.btn_reset_table = QtWidgets.QPushButton("Reset Timetable")
		self.btn_reset_table.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_RED, colors.COLOR_DARK_RED))
		self.layout_btn_container.addWidget(self.btn_create_schedule)
		self.layout_btn_container.addWidget(self.btn_reset_table)

	def openEditSchedule(self, schedule:task.Schedule):
		if self.current_editing_schedule == schedule:
			return
		self.current_editing_schedule = schedule
		self.setScheduleEditInput(schedule)
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		# 스케쥴 적용 버튼
		self.btn_apply_schedule = QtWidgets.QPushButton("Apply")
		self.btn_apply_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_AQUA, colors.COLOR_DARK_AQUA))
		self.btn_apply_schedule.clicked.connect(lambda:self.applySchedule(schedule))

		# 스케쥴 삭제 버튼
		self.btn_delete_schedule = QtWidgets.QPushButton("Delete")
		self.btn_delete_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_RED, colors.COLOR_DARK_RED))
		self.btn_delete_schedule.clicked.connect(lambda:self.deleteSchedule(schedule))

		# 새로운 스케쥴 생성 버튼
		self.btn_new_schedule = QtWidgets.QPushButton("New Schedule")
		self.btn_new_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_new_schedule.clicked.connect(lambda:self.openCreateNewSchedule())
		self.layout_btn_container.addWidget(self.btn_apply_schedule)
		self.layout_btn_container.addWidget(self.btn_delete_schedule)
		self.layout_btn_container.addWidget(self.btn_new_schedule)

	def setScheduleTimeInput(self, schedule_time:custom_date.DayScheduleTime):
		self.combo_day_of_the_week.setCurrentIndex(schedule_time.getDayOfTheWeekIndex())
		self.widget_time_schedule.setCurrentTime(schedule_time)

	def setScheduleEditInput(self, schedule:task.Schedule):
		self.label_schedule_title.setText("Edit Schedule")
		self.edit_schedule_title.setText(schedule.getTitle())
		self.widget_color_box.selectColorItem(schedule.getColor())
		self.widget_time_list.setScheduleItem(schedule_time_list=schedule.getScheduleTimeList())
		self.widget_time_schedule.setCurrentTime(custom_date.DayScheduleTime("Monday", "0", "0", "0", "0"))

	def getSchedule(self):
		title = self.edit_schedule_title.text()
		schedule_time_list = self.widget_time_list.getScheduleTimeList()
		color = self.widget_color_box.getCurrentColorItem().color
		schedule = task.Schedule(title, color, schedule_time_list)
		return schedule

	def createSchedule(self):
		schedule = self.getSchedule()
		test_text = self.testScheduleSetting(schedule)
		if test_text != None:
			self.showAlertText(test_text)
			return
		data.schedule_list.append(schedule)
		data.save()
		self.parent.widget_table.addSchedule(schedule)
		self.resetInput()

	def deleteSchedule(self, schedule:task.Schedule):
		data.schedule_list.remove(schedule)
		data.save()
		self.parent.widget_table.deleteSchedule(schedule)
		self.openCreateNewSchedule()

	def applySchedule(self, schedule:task.Schedule):
		self.createSchedule()
		self.deleteSchedule(schedule)

	def resetInput(self):
		self.edit_schedule_title.setText("")
		self.widget_color_box.selectColorItem(colors.COLOR_GREEN)
		self.widget_time_list.setScheduleItem([])
		self.resetTimeSettingInput()

	def resetTimeSettingInput(self):
		self.combo_day_of_the_week.setCurrentIndex(0)
		self.widget_time_schedule.setCurrentTime(custom_date.DayScheduleTime("Monday", "0", "0", "0", "0"))
		self.btn_time_setting_add.setText("Add")
		self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_BLUE, colors.COLOR_DARK_BLUE))
		self.btn_time_setting_add.mouseReleaseEvent = lambda event:self.addTimeSetting()

	def getScheduleTimeInCombo(self):
		schedule_time = custom_date.DayScheduleTime(self.combo_day_of_the_week.currentText(), self.widget_time_schedule.getCurrentStartTime(), \
					self.widget_time_schedule.getCurrentStartMinute(), self.widget_time_schedule.getCurrentEndTime(), self.widget_time_schedule.getCurrentEndMinute())
		return schedule_time

	def addTimeSetting(self):
		test_text = self.testScheduleTime(self.getSchedule())
		if test_text != None:
			self.showAlertText(test_text)
			return
		self.widget_time_list.addItem(self.getScheduleTimeInCombo())
		self.resetTimeSettingInput()
	
	def editTimeSetting(self, schedule_time:custom_date.DayScheduleTime):
		self.setScheduleTimeInput(schedule_time)
		self.btn_time_setting_add.setText("Edit")
		self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_PINK, colors.COLOR_PINK))
		self.btn_time_setting_add.mouseReleaseEvent = lambda event:self.applyTimeSetting()
		
	def applyTimeSetting(self):
		test_text = self.testScheduleTime(self.getSchedule())
		if test_text != None:
			self.showAlertText(test_text)
			return
		self.btn_time_setting_add.setText("Add")
		self.widget_time_list.applyItem(self.getScheduleTimeInCombo())
		self.btn_time_setting_add.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 16px} QPushButton:hover{background-color:%s}" % (colors.COLOR_BLUE, colors.COLOR_DARK_BLUE))
		self.btn_time_setting_add.mouseReleaseEvent = lambda event:self.addTimeSetting()
		self.resetTimeSettingInput()

	def showAlertText(self, text):
		alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.NoIcon, "Task Manager", "[ ! ] " + text, QtWidgets.QMessageBox.StandardButton.Yes)
		alert.setStyleSheet("font: bold 13px 'Segoe UI';")
		alert.exec()
	
	def testScheduleSetting(self, schedule:task.Schedule):
		if schedule.getTitle() == "":
			return "Please enter schedule title."
		if len(schedule.getScheduleTimeList()) == 0:
			return "Please add schedule time."
		return None

	def testScheduleTime(self, schedule:task.Schedule):
		schedule_time = self.getScheduleTimeInCombo()
		if schedule_time.getStartTimeToMinute() >= schedule_time.getEndTimeToMinute():
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
					print(other_schedule_time.getStartTime())
					return "The time you set overlaps with another schedule."
		return None