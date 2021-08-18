import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import schedule_time_setting_widget, schedule_time_list_widget, color_picker
from modules import colors, data, task
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

		# 스케쥴 타임 설정 위젯
		self.widget_time_setting = schedule_time_setting_widget.ScheduleTimeSettingWidget(self)
		self.layout.addWidget(self.widget_time_setting)

		self.layout.addStretch(1)

		# 버튼 컨테이너
		self.widget_btn_container = QtWidgets.QWidget(self)
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.layout.addWidget(self.widget_btn_container)

		# 로드 데이터
		self.loadData()

	def loadData(self):
		# 스케쥴 생성 UI 열기
		self.openCreateNewSchedule()
		

	def openCreateNewSchedule(self):
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.resetInput()
		self.parent.widget_table.resetFocusItems()
		self.label_schedule_title.setText("New Schedule")
		self.current_editing_schedule = None
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		# 스케쥴 생성 버튼
		self.btn_create_schedule = QtWidgets.QPushButton("Create Schedule")
		self.btn_create_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 600 15px; border-radius:0px} QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_create_schedule.clicked.connect(self.createSchedule)
		self.btn_create_schedule.setFixedHeight(35)
		self.btn_create_schedule.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		# 테이블 초기화 버튼
		self.btn_reset_table = QtWidgets.QPushButton("Reset Timetable")
		self.btn_reset_table.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_reset_table.setFixedHeight(35)
		self.btn_reset_table.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 600 15px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_RED, colors.COLOR_DARK_RED))
		self.layout_btn_container.addWidget(self.btn_create_schedule)
		self.layout_btn_container.addWidget(self.btn_reset_table)
		

	def openEditSchedule(self, schedule:task.Schedule):
		self.current_editing_schedule = schedule
		self.setScheduleEditInput(schedule)
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		# 스케쥴 적용 버튼
		self.btn_apply_schedule = QtWidgets.QPushButton("Apply")
		self.btn_apply_schedule.setFixedHeight(35)
		self.btn_apply_schedule.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_apply_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 600 15px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_AQUA, colors.COLOR_DARK_AQUA))
		self.btn_apply_schedule.clicked.connect(lambda:self.applySchedule(schedule))

		# 스케쥴 삭제 버튼
		self.btn_delete_schedule = QtWidgets.QPushButton("Delete")
		self.btn_delete_schedule.setFixedHeight(35)
		self.btn_delete_schedule.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_delete_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 600 15px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_PINK, colors.COLOR_DARK_PINK))
		self.btn_delete_schedule.clicked.connect(lambda:self.deleteSchedule(schedule))

		# 새로운 스케쥴 생성 버튼
		self.btn_new_schedule = QtWidgets.QPushButton("New Schedule")
		self.btn_new_schedule.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_new_schedule.setFixedHeight(35)
		self.btn_new_schedule.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 600 15px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_new_schedule.clicked.connect(lambda:self.openCreateNewSchedule())
		self.layout_btn_container.addWidget(self.btn_apply_schedule)
		self.layout_btn_container.addWidget(self.btn_delete_schedule)
		self.layout_btn_container.addWidget(self.btn_new_schedule)

	def setScheduleEditInput(self, schedule:task.Schedule):
		self.label_schedule_title.setText("Edit Schedule")
		self.edit_schedule_title.setText(schedule.getTitle())
		self.widget_color_box.selectColorItem(schedule.getColor())
		self.widget_time_setting.widget_time_list.setScheduleItem(schedule_time_list=schedule.getScheduleTimeList())
		self.widget_time_setting.widget_time_period.setCurrentTime(task.TimePeriod("0", "0", "1", "0"))

	def getSchedule(self):
		title = self.edit_schedule_title.text()
		schedule_time_list = self.widget_time_setting.widget_time_list.getScheduleTimeList()
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
		test_text = self.testScheduleSetting(self.getSchedule())
		if test_text != None:
			self.showAlertText(test_text)
			return
		self.createSchedule()
		self.deleteSchedule(schedule)

	def resetInput(self):
		self.edit_schedule_title.setText("")
		self.widget_color_box.selectColorItem(colors.COLOR_GREEN)
		self.widget_time_setting.widget_time_list.setScheduleItem([])
		self.widget_time_setting.resetTimeSettingInput()

	def showAlertText(self, text):
		alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.NoIcon, "Todo Manager", "[ ! ] " + text, QtWidgets.QMessageBox.StandardButton.Yes)
		alert.setStyleSheet("QPushButton{width:80px}")
		alert.exec()
	
	def testScheduleSetting(self, schedule:task.Schedule):
		if schedule.getTitle() == "":
			return "Please enter schedule title."
		if len(schedule.getScheduleTimeList()) == 0:
			return "Please add schedule time."
		for other_schedule in data.schedule_list:
			if other_schedule != self.current_editing_schedule and other_schedule.getTitle() == schedule.getTitle():
				return "This schedule title already exist."
		return None