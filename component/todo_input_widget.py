import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import todo_datetime_setting_widget, color_picker, todo_list_widget
from module import colors, data, task

class TodoInputWidget(QtWidgets.QWidget):
	def __init__(self, parent=None, todo:task.Schedule=None):
		super().__init__(parent)
		self.parent = parent
		# 세팅 Todo 입력 위젯 & 레이아웃 생성
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(10,0,10,0)

		# 현재 수정중인 Todo 아이템 (None == New Schedule)
		self.current_editing_todo_item = None

		# Todo 제목 레이블 생성
		self.label_todo_title = QtWidgets.QLabel("New Schedule")
		self.label_todo_title.setStyleSheet("font: 600 22px")
		self.layout.addWidget(self.label_todo_title)

		# Todo 제목 인풋 생성
		self.edit_todo_title = QtWidgets.QLineEdit("")
		self.edit_todo_title.setPlaceholderText("SCHEDULE TITLE")
		self.edit_todo_title.setStyleSheet("font: 400 17px")
		self.layout.addWidget(self.edit_todo_title)

		# Todo 설명 인풋 생성
		self.edit_todo_description = QtWidgets.QTextEdit("")
		self.edit_todo_description.setPlaceholderText("SCHEDULE DESCRIPTION (Optional)")
		self.edit_todo_description.setStyleSheet("font: 400 17px; background-color:%s" % colors.COLOR_DARK_BACKGROUND)
		self.layout.addWidget(self.edit_todo_description)

		self.layout.addStretch(1)

		# Todo 색상 설정 위젯 생성
		self.widget_color_box = color_picker.ColorItemBox(self)
		self.layout.addWidget(self.widget_color_box)

		self.layout.addStretch(1)

		# Todo 날짜 선택 위젯 생성
		self.widget_datetime_setting = todo_datetime_setting_widget.TodoDatetimeSettingWidget(self)
		self.layout.addWidget(self.widget_datetime_setting)

		self.layout.addStretch(1)

		# 버튼 컨테이너
		self.widget_btn_container = QtWidgets.QWidget(self)
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		self.layout.addWidget(self.widget_btn_container)

		# 업무 생성 UI 열기
		self.openCreateNewTodo()

		# 아이템 로드
		self.loadScheduleItem()

	def loadScheduleItem(self):
		self.parent.widget_todo_list.applyGrid()

	def openCreateNewTodo(self):
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.current_editing_todo_item = None
		self.resetInput()
		self.parent.widget_todo_list.resetFocusItems()
		self.label_todo_title.setText("New Todo")
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		# Todo 생성 버튼
		self.btn_create_todo = QtWidgets.QPushButton("Create To Do")
		self.btn_create_todo.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px} QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_create_todo.clicked.connect(self.createTodo)
		self.layout_btn_container.addWidget(self.btn_create_todo)

	def openEditTodo(self, todo_item:todo_list_widget.TodoItem):
		self.current_editing_todo_item = todo_item
		self.setTodoEditInput(todo_item)
		QtWidgets.QWidget().setLayout(self.widget_btn_container.layout())
		self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
		# Todo 적용 버튼
		self.btn_apply_todo = QtWidgets.QPushButton("Apply")
		self.btn_apply_todo.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_AQUA, colors.COLOR_DARK_AQUA))
		self.btn_apply_todo.clicked.connect(lambda:self.applyTodo(todo_item))

		# 새로운 Todo 생성 버튼
		self.btn_new_todo = QtWidgets.QPushButton("Cancel")
		self.btn_new_todo.setStyleSheet("QPushButton{border:0px; background-color: %s; font: 500 11px; border-radius:0px}  QPushButton:hover{background-color:%s}" % (colors.COLOR_GREEN, colors.COLOR_DARK_GREEN))
		self.btn_new_todo.clicked.connect(lambda:self.openCreateNewTodo())
		self.layout_btn_container.addWidget(self.btn_apply_todo)
		self.layout_btn_container.addWidget(self.btn_new_todo)

	def setTodoEditInput(self, todo_item:todo_list_widget.TodoItem):
		todo = todo_item.todo
		self.label_todo_title.setText("Edit Todo")
		self.edit_todo_title.setText(todo.getTitle())
		self.widget_color_box.selectColorItem(todo.getColor())
		self.widget_datetime_setting.setCurrentDateTime(todo)

	def getTodo(self):
		title = self.edit_todo_title.text()
		description = self.edit_todo_description.toHtml()
		color = self.widget_color_box.getCurrentColorItem().color
		date = self.widget_datetime_setting.getDate()
		parent_schedule = self.widget_datetime_setting.getParentSchedule()
		time_period = self.widget_datetime_setting.getTimePeriod()
		todo = task.Todo(title, description, date, time_period, parent_schedule, color)
		return todo

	def createTodo(self):
		todo = self.getTodo()
		test_text = self.testTodoSetting(todo)
		if test_text != None:
			self.showAlertText(test_text)
			return
		data.todo_list.append(todo)
		data.save()
		self.parent.widget_todo_list.addTodo(todo)
		self.resetInput()

	def deleteTodo(self, todo_item:todo_list_widget.TodoItem):
		data.todo_list.remove(todo_item.todo)
		data.save()
		self.parent.widget_todo_list.deleteTodo(todo_item)
		self.openCreateNewTodo()

	def applyTodo(self, todo_item:todo_list_widget.TodoItem):
		self.createTodo()
		self.deleteTodo(todo_item)

	def resetInput(self):
		self.edit_todo_title.setText("")
		self.widget_color_box.selectColorItem(colors.COLOR_GREEN)
		self.resetDateTimeSettingInput()

	def resetDateTimeSettingInput(self):
		self.widget_datetime_setting.resetItems()

	def getScheduleTimeInCombo(self):
		todo_time = task.WeeklyScheduleTime(self.combo_day_of_the_week.currentText(), self.widget_time_schedule.getCurrentTimePeriod())
		return todo_time
	
	def showAlertText(self, text):
		alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.NoIcon, "Task Manager", "[ ! ] " + text, QtWidgets.QMessageBox.StandardButton.Yes)
		alert.setStyleSheet("font: bold 13px 'Segoe UI';")
		alert.exec()
	
	def testTodoSetting(self, todo:task.Todo):
		if todo.getTitle() == "":
			return "Please enter Todo title."
		if self.widget_datetime_setting.getTimePeriod() != None:
			if self.widget_datetime_setting.getTimePeriod().getStartTimeToMinute() >= self.widget_datetime_setting.getTimePeriod().getEndTimeToMinute():
				return "The start time cannot be equal to or later than the end time."
		return None