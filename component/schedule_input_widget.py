import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import schedule_time_setting_widget, schedule_time_list_widget, color_picker
from module import custom_date, colors, data, task

class ScheduleInputWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, schedule:task.Schedule=None):
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
		self.btn_time_setting_add.clicked.connect(lambda: self.addTimeSetting())
		self.layout_time_setting.addWidget(self.btn_time_setting_add)

		self.layout.addStretch(1)

		# 스케쥴 생성 & 테이블 초기화 버튼 레이아웃
		self.layout_create_reset_btn_hbox = QtWidgets.QHBoxLayout()
		self.layout.addLayout(self.layout_create_reset_btn_hbox)
		
		# 스케쥴 생성 버튼
		self.btn_create_schedule = QtWidgets.QPushButton("Create Schedule")
		self.btn_create_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px} QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_create_schedule.clicked.connect(self.createSchedule)
		self.layout_create_reset_btn_hbox.addWidget(self.btn_create_schedule)

		# 테이블 초기화 버튼
		self.btn_reset_table = QtWidgets.QPushButton("Reset Timetable")
		self.btn_reset_table.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_RED, colors.COLOR_DARK_RED))
		self.layout_create_reset_btn_hbox.addWidget(self.btn_reset_table)

		# 만약 Schedule 값이 들어왔을 경우 Edit 모드로 인식하여 Input 채움
		if schedule != None:
			self.loadScheduleData(schedule)
	def setScheduleTimeInput(self, schedule_time:custom_date.DayScheduleTime):
		self.combo_day_of_the_week.setCurrentIndex(schedule_time.getDayOfTheWeekIndex())
		self.widget_time_schedule.setCurrentTime(schedule_time)

	def setScheduleInput(self, schedule:task.Schedule):
		self.label_schedule_title.setText("Edit Schedule")
		self.edit_schedult_title.setText(schedule.getTitle())
		self.widget_color_box.selectColorItem(schedule.getColor())
		self.widget_time_list.setScheduleItem(schedule_time_list=schedule.getScheduleTimeList())

	def addTimeSetting(self):
		scheduleTime = custom_date.DayScheduleTime(self.combo_day_of_the_week.currentText(), self.widget_time_schedule.getCurrentStartTime(), \
			self.widget_time_schedule.getCurrentStartMinute(), self.widget_time_schedule.getCurrentEndTime(), self.widget_time_schedule.getCurrentEndMinute())
		self.widget_time_list.addItem(self.widget_time_list.ScheduleTimeItem(self, scheduleTime))

	def createSchedule(self, event):
		title = self.edit_schedult_title.text()
		color = self.widget_color_box.getCurrentColorItem().color
		schedule_time_list = self.widget_time_list.getScheduleTimeList()
		schedule = task.Schedule(title, color, schedule_time_list)
		data.schedule_list.append(schedule)
		data.save()
		self.parent.widget_table.addSchedule(schedule)