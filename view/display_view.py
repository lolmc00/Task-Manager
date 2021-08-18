import os
import sys
import webbrowser
import threading
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from typing import List
from modules import data, task, colors
from datetime import datetime
from component import todo_list_widget, todo_input_widget

WIDTH = 400
HEIGHT = 200

class TodoItem(QtWidgets.QWidget):
	def __init__(self, parent=None, todo:task.Todo=None):
		super().__init__(parent)
		self.todo = todo
		self.setFixedHeight(57)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)


		# 제목 라벨
		self.label_title = QtWidgets.QLabel()
		self.label_title.setAttribute(QtCore.Qt.WA_InputMethodTransparent)
		self.label_title.setStyleSheet("font: 600 15px '나눔스퀘어';")
		elided_title = self.label_title.fontMetrics().elidedText(todo.getTitle(), QtCore.Qt.TextElideMode.ElideRight, self.label_title.width())
		self.label_title.setText(elided_title)
		self.label_title.adjustSize()
		self.layout.addWidget(self.label_title)

		# 하단 레이아웃
		self.layout_hbox = QtWidgets.QHBoxLayout()
		self.layout_hbox.setContentsMargins(0, 0, 0, 0)
		self.layout.addLayout(self.layout_hbox)

		# 시작 시간, 끝 시간 레이블
		if todo.getParentSchedule() != None:
			self.label_time = QtWidgets.QLabel("%s" % todo.getParentSchedule().getTitle())
			self.label_time.setStyleSheet("font: 500 15px '나눔스퀘어'; color:%s" % (todo.getParentSchedule().getColor()))
		else:
			self.label_time = QtWidgets.QLabel("%s:%s ~ %s:%s" % (todo.getTimePeriod().getStartTimeString(), todo.getTimePeriod().getStartTimeMinuteString(), \
			todo.getTimePeriod().getEndTimeString(), todo.getTimePeriod().getEndTimeMinuteString()))
			self.label_time.setStyleSheet("font: 500 15px;")
		self.label_time.adjustSize()
		self.layout_hbox.addWidget(self.label_time)
		
		# 완료 버튼  
		self.btn_complete = QtWidgets.QPushButton("complete")
		self.btn_complete.setStyleSheet("padding: 0px; border:2px solid %s" % colors.COLOR_PURPLE)
		self.btn_complete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_complete.setContentsMargins(0, 0, 0, 0)
		self.btn_complete.setFixedSize(85, 28)
		self.btn_complete.clicked.connect(self.onClickedCompleteBtn)
		self.layout_hbox.addWidget(self.btn_complete)

	def onClickedCompleteBtn(self):
		self.todo.complete()
		data.save()
		self.setParent(None)
		self.deleteLater()
		QtMultimedia.QSound.play(os.path.join(config.SOUND_PATH, "complete.wav"))

weekday_string_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

class MySignal(QtCore.QObject):
	''' Why a whole new class? See here: 
	https://stackoverflow.com/a/25930966/2441026 '''
	sig_todo = QtCore.pyqtSignal(datetime)
	sig_schedule = QtCore.pyqtSignal(datetime)

class DisplayView(QtWidgets.QWidget):
	def __init__(self, parent=None, main=None):
		super().__init__(parent)
		self.main = main
		# 레이아웃
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		self.layout.setContentsMargins(0, 0, 0, 0)

		# 현재 시간
		self.current_time = datetime.now()
		self.signal = MySignal()
		self.signal.sig_todo.connect(self.updateTodo)
		self.signal.sig_schedule.connect(self.updateSchedule)
		# 현재 스케쥴
		self.current_weekly_schedule_time = None

		# Todo 리스트
		self.widget_todo_list = QtWidgets.QWidget()
		self.layout_todo_list = QtWidgets.QVBoxLayout(self.widget_todo_list)
		self.layout_todo_list.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		self.layout_todo_list.setSpacing(1)
		self.todo_list = []
		# Todo 리스트 scroll area
		scroll_todo_list = QtWidgets.QScrollArea()
		scroll_todo_list.setWidgetResizable(True)
		scroll_todo_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
		scroll_todo_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		scroll_todo_list.setWidget(self.widget_todo_list)
		self.layout.addWidget(scroll_todo_list)

		# Time Schedule Status 컨테이너
		self.widget_time_schedule = QtWidgets.QWidget()
		self.widget_time_schedule.setStyleSheet("font: bold 15px;")
		self.layout_time_schedule = QtWidgets.QVBoxLayout(self.widget_time_schedule)
		self.pb_time_schedule = QtWidgets.QProgressBar()
		self.pb_time_schedule.setMaximum(10000)
		self.pb_time_schedule.setAlignment(QtCore.Qt.AlignCenter)
		self.pb_time_schedule.setStyleSheet('border:2px solid #fff')
		self.layout_time_schedule.addWidget(self.pb_time_schedule)
		# 시간 정보 컨테이너
		self.layout_time_schedule_info = QtWidgets.QHBoxLayout()
		self.layout_time_schedule.addLayout(self.layout_time_schedule_info)
		self.label_start_time = QtWidgets.QLabel()
		self.label_start_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
		self.label_end_time = QtWidgets.QLabel()
		self.label_end_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
		self.label_time_schedule_title = QtWidgets.QLabel()
		self.label_time_schedule_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.label_time_schedule_title.setFixedWidth(200)
		self.layout_time_schedule_info.addWidget(self.label_start_time)
		self.layout_time_schedule_info.addWidget(self.label_time_schedule_title)
		self.layout_time_schedule_info.addWidget(self.label_end_time)
		self.layout.addWidget(self.widget_time_schedule)
		self.updateTodo(self.current_time)
		self.updateSchedule(self.current_time)
		self.updateStatus()
	
	def updateStatus(self):
		now_time = datetime.now()
		if now_time.second != self.current_time.second:
			self.signal.sig_schedule.emit(now_time)
		if now_time.minute != self.current_time.minute:
			self.signal.sig_todo.emit(now_time)
		self.current_time = now_time
		timer = threading.Timer(1, self.updateStatus)
		timer.daemon = True
		timer.start()

	def updateTodo(self, now_time:datetime):
		self.main.topbar.current_datetime_label.setText(now_time.strftime("%Y.%m.%d %a %H:%M"))
		new_todo_list = list(filter(lambda todo: todo.isInTime(now_time) and not todo.isCompleted(), data.todo_list))
		if new_todo_list != self.todo_list:
			self.todo_list = new_todo_list
			self.setTodoList(self.todo_list)

	def updateSchedule(self, now_time:datetime):
		weekly_schedule = None
		weekly_schedule_time = None
		for schedule in data.schedule_list:
			for schedule_time in schedule.getScheduleTimeList():
				if schedule_time.isInTime(now_time):
					weekly_schedule = schedule
					weekly_schedule_time = schedule_time
					break
			else:
				continue
			break
		if weekly_schedule_time != None:
			total_val = weekly_schedule_time.getTimePeriod().getDuringMinute() * 60
			current_val = (now_time.hour * 60 + now_time.minute) * 60 + now_time.second
			current_val -= weekly_schedule_time.getTimePeriod().getStartTimeToMinute() * 60
			percent = float(current_val) / float(total_val)
			self.pb_time_schedule.setValue(int(percent * self.pb_time_schedule.maximum()))
			self.pb_time_schedule.update()
		else:
			self.current_weekly_schedule_time = None
			self.widget_time_schedule.hide()
		if weekly_schedule_time != self.current_weekly_schedule_time:
			self.current_weekly_schedule_time = weekly_schedule_time
			self.label_start_time.setText(weekly_schedule_time.getTimePeriod().getStartTimeString() + ":" + weekly_schedule_time.getTimePeriod().getStartTimeMinuteString())
			self.label_end_time.setText(weekly_schedule_time.getTimePeriod().getEndTimeString() + ":" + weekly_schedule_time.getTimePeriod().getEndTimeMinuteString())
			self.label_time_schedule_title.setStyleSheet("color:%s; font: 800 15px '나눔스퀘어';" % weekly_schedule.getColor())
			elided_title = self.label_time_schedule_title.fontMetrics().elidedText(weekly_schedule.getTitle(), QtCore.Qt.TextElideMode.ElideRight, self.label_time_schedule_title.width())
			self.label_time_schedule_title.setText(elided_title)
			self.widget_time_schedule.show()

	def setTodoList(self, todo_list:List[task.Todo]):
		# 레이아웃 비우기
		for i in reversed(range(self.layout_todo_list.count())): 
			self.layout_todo_list.itemAt(i).widget().deleteLater()
		# 레이아웃 채우기
		for todo in todo_list:
			widget_item = TodoItem(None, todo)
			self.layout_todo_list.addWidget(widget_item)

	def loadData(self):
		self.updateTodo(self.current_time)
		self.current_weekly_schedule_time = None
		self.updateSchedule(self.current_time)