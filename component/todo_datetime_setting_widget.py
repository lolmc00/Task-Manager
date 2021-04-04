import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from datetime import date, timedelta
from component import time_period_widget
from module import task, data

weekday_string_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

class TodoDatetimeSettingWidget(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)

		# 스케쥴 날짜 레이블 생성
		self.label_schedule_datetime = QtWidgets.QLabel("Todo DateTime")
		self.label_schedule_datetime.setStyleSheet("font: 600 22px")
		self.layout.addWidget(self.label_schedule_datetime)

		# 날짜 형식 레이블 생성
		self.label_date_format = QtWidgets.QLabel("Year / Month / Date")
		self.label_date_format.setStyleSheet("font: 500 15px; color:#dcdcdc;")
		self.layout.addWidget(self.label_date_format)

		# 날짜 설정 Container
		self.layout_date_select_container = QtWidgets.QHBoxLayout()
		# 연 설정 콤보 박스
		self.combo_year = QtWidgets.QComboBox()
		self.combo_year.setStyleSheet("font: 400 15px")
		self.layout_date_select_container.addWidget(self.combo_year)
		# 월 설정 콤보 박스
		self.combo_month = QtWidgets.QComboBox()
		self.combo_month.setStyleSheet("font: 400 15px")
		self.layout_date_select_container.addWidget(self.combo_month)
		# 일 설정 콤보 박스
		self.combo_day = QtWidgets.QComboBox()
		self.combo_day.setStyleSheet("font: 400 15px")
		self.layout_date_select_container.addWidget(self.combo_day)
		self.layout.addLayout(self.layout_date_select_container)

		# 부모 스케쥴 레이블 생성
		self.label_parent_schedule = QtWidgets.QLabel("Parent Schedule")
		self.label_parent_schedule.setStyleSheet("font: 500 15px; color:#dcdcdc;")
		self.layout.addWidget(self.label_parent_schedule)

		# 부모 스케쥴 설정 콤보 박스
		self.combo_parent_schedule = QtWidgets.QComboBox()
		self.combo_parent_schedule.setStyleSheet("font: 400 15px")
		self.layout.addWidget(self.combo_parent_schedule)

		# From To 시간 설정 위젯
		self.widget_time_schedule = time_period_widget.TimePeirodWidget(self)
		self.layout.addWidget(self.widget_time_schedule)

		# Items 초기화
		self.resetItems()

		# Combobox Change 핸들링
		self.combo_year.currentTextChanged.connect(self.onChangeYear)
		self.combo_month.currentTextChanged.connect(self.onChangeMonth)
		self.combo_day.currentTextChanged.connect(self.onChangeDay)
		self.combo_parent_schedule.currentIndexChanged.connect(self.onChangeParentScheduleIndex)

	def resetItems(self):
		year = date.today().year
		month = date.today().month
		day = date.today().day
		new_date = date(year, month, day)
		self.combo_year.addItems([str(year + i) for i in range(3)])
		self.combo_month.addItems([(str(i) if i >= 10 else "0" + str(i)) for i in range(1, 13)])
		self.combo_month.setCurrentIndex(month - 1)
		self.applyDayComboBox(new_date)
		self.onChangeDate(new_date)
		self.widget_time_schedule.setCurrentTime(task.TimePeriod(0, 0, 24, 0))

	def applyDayComboBox(self, new_date:date):
		last_day = last_day_of_month(new_date).day
		self.combo_day.clear()
		for i in range(1, last_day + 1):
			self.combo_day.addItem(self.getDayStrFormat(new_date.replace(day=i)))
		self.combo_day.setCurrentIndex(new_date.day - 1)

	def onChangeYear(self, value):
		year = int(value)
		month = int(self.combo_month.currentText())
		day = int(self.combo_day.currentText()[:2])
		self.applyDayComboBox(date(year, month, day))

	def onChangeMonth(self, value):
		year = int(self.combo_year.currentText())
		month = int(value)
		day = int(self.combo_day.currentText()[:2])
		self.applyDayComboBox(date(year, month, day))

	def onChangeDay(self, value):
		if value == "":
			return
		year = int(self.combo_year.currentText())
		month = int(self.combo_month.currentText())
		day = int(value[:2])
		self.onChangeDate(date(year, month, day))

	def onChangeDate(self, new_date:date):
		day_of_week = self.getDate().weekday()
		schedule_list = []
		for schedule in data.schedule_list:
			for schedule_time in schedule.getScheduleTimeList():
				if day_of_week == schedule_time.getDayOfTheWeekIndex():
					schedule_list.append(schedule)
					break
		self.combo_parent_schedule.clear()
		self.combo_parent_schedule.addItem("(None)")
		self.combo_parent_schedule.addItems([schedule.getTitle() for schedule in schedule_list])

	def onChangeParentScheduleIndex(self, value:int):
		self.widget_time_schedule.setDisabled(value != 0)

	def getDate(self):
		year = int(self.combo_year.currentText())
		month = int(self.combo_month.currentText())
		day = int(self.combo_day.currentText()[:2])
		return date(year, month, day)

	def getParentSchedule(self):
		if self.combo_parent_schedule.currentIndex() <= 0:
			return None
		day_of_week = self.getDate().weekday()
		for schedule in data.schedule_list:
			if schedule.getTitle() == self.combo_parent_schedule.currentText():
				for schedule_time in schedule.getScheduleTimeList():
					if day_of_week == schedule_time.getDayOfTheWeekIndex():
						return schedule
		return None

	def getTimePeriod(self):
		if self.combo_parent_schedule.currentIndex() > 0:
			return None
		return self.widget_time_schedule.getCurrentTimePeriod()

	def setCurrentDateTime(self, todo:task.Todo):
		date = todo.getDate()
		year = str(date.year)
		month = ("0" + str(date.month) if date.month < 10 else str(date.month))
		day = self.getDayStrFormat(date)
		self.combo_year.setCurrentText(year)
		self.combo_month.setCurrentText(month)
		self.combo_day.setCurrentText(day)
		if todo.getParentSchedule() != None:
			self.combo_parent_schedule.setCurrentText(todo.getParentSchedule().getTitle())
		else:
			self.combo_parent_schedule.setCurrentIndex(0)
			self.widget_time_schedule.setCurrentTime(todo.getTimePeriod())

	def getDayStrFormat(self, date:date):
		day = date.day
		day_of_week = (date.replace(day=day)).weekday()
		day_of_week_str = weekday_string_list[day_of_week]
		day = ("0" + str(day) if day < 10 else str(day)) + " " + day_of_week_str
		return day


def last_day_of_month(day) -> date:
	# this will never fail
	# get close to the end of the month for any day, and add 4 days 'over'
	next_month = day.replace(day=28) + timedelta(days=4)
	# subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
	return next_month - timedelta(days=next_month.day)