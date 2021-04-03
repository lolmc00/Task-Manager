import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from module import task, colors, data
from component import custom_widget, schedule_time_setting_widget

class ScheduleListBox(QtWidgets.QWidget):
	class ScheduleItem(QtWidgets.QWidget):
		def __init__(self, parent=None):
			super().__init__(parent)

	class ScheduleTimeItem(ScheduleItem):
		def __init__(self, parent=None, schedule_time:task.WeeklyScheduleTime = None):
			super().__init__(parent)
			self.parent = parent
			self.schedule_time = schedule_time
			self.setFixedHeight(44)
			self.setAttribute(QtCore.Qt.WA_StyledBackground)
			self.setObjectName("container")
			self.setStyleSheet("QWidget#container{border:1px solid #448aff}")
			self.layout = QtWidgets.QVBoxLayout(self)
			self.layout.setContentsMargins(1,1,1,1)
			self.layout.setSpacing(0)

			# 상단 요일, 도구 컨테이너
			self.widget_top = QtWidgets.QWidget(self)
			self.widget_top.setFixedHeight(26)
			self.widget_top.setObjectName("widget_top")
			self.widget_top.setAttribute(QtCore.Qt.WA_StyledBackground)
			self.widget_top.setStyleSheet("background-color:#448aff")
			self.layout_top = QtWidgets.QHBoxLayout(self.widget_top)
			self.layout_top.setContentsMargins(5,0,0,7)
			self.layout_top.setSpacing(5)
			self.layout.addWidget(self.widget_top)

			# 요일 라벨
			self.label_day_of_the_week = QtWidgets.QLabel(schedule_time.getDayOfTheWeek())
			self.label_day_of_the_week.setStyleSheet("font: 600 15px;")
			self.layout_top.addWidget(self.label_day_of_the_week)

			self.layout_top.addStretch(1)

			# 수정 버튼
			self.btn_edit = custom_widget.HoverButton("edit", 20)
			self.btn_edit.clicked.connect(lambda: self.edit())
			self.layout_top.addWidget(self.btn_edit)

			# 삭제 버튼
			self.btn_remove = custom_widget.HoverButton("remove", 20)
			self.btn_remove.clicked.connect(lambda: self.delete())
			self.layout_top.addWidget(self.btn_remove)

			# 컨텐츠 컨테이너
			self.widget_contents = QtWidgets.QWidget(self)
			self.layout_contents = QtWidgets.QHBoxLayout(self.widget_contents)
			self.layout_contents.setContentsMargins(5,2,2,5)
			self.layout_contents.setSpacing(0)
			self.layout.addWidget(self.widget_contents)

			# 시작 시간, 끝 시간 레이블
			self.label_time_schedule_time = QtWidgets.QLabel("%s:%s ~ %s:%s" % (schedule_time.getTimePeriod().getStartTimeString(), schedule_time.getTimePeriod().getStartTimeMinuteString(), \
				schedule_time.getTimePeriod().getEndTimeString(), schedule_time.getTimePeriod().getEndTimeMinuteString()))
			self.label_time_schedule_time.setStyleSheet("font: 500 15px; color:#666")
			self.layout_contents.addWidget(self.label_time_schedule_time)

		def delete(self):
			self.parent.removeItem(self)
		
		def cancelEdit(self):
			self.parent.cancelEditItem()

		def edit(self):
			self.parent.cancelEditItem()
			self.setFocusOn(True)
			self.parent.editItem(self)

		def apply(self, schedule_time:task.WeeklyScheduleTime):
			self.schedule_time = schedule_time
			self.setFocusOn(False)
			self.label_day_of_the_week.setText(schedule_time.getDayOfTheWeek())
			self.label_time_schedule_time.setText("%s:%s ~ %s:%s" % (schedule_time.getTimePeriod().getStartTimeString(), schedule_time.getTimePeriod().getStartTimeMinuteString(), \
							schedule_time.getEndTimeString(), schedule_time.getEndTimeMinuteString()))
						
		def setFocusOn(self, isFocusOn):
			self.setStyleSheet("QWidget#container{border:1px solid %s}" % (colors.COLOR_DARK_PINK if isFocusOn else colors.COLOR_DARK_BLUE))
			self.widget_top.setStyleSheet("background-color:%s" %  (colors.COLOR_DARK_PINK if isFocusOn else colors.COLOR_DARK_BLUE))

	def __init__(self, parent=None):
		super().__init__(parent)
		# 전체 레이아웃
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0,0,0,0)

		self.current_editing_item = None

		# 리스트 박스 제목
		self.label_title = QtWidgets.QLabel("Time List")
		self.label_title.setStyleSheet("font: 600 22px")
		self.layout.addWidget(self.label_title)

		# 리스트 박스 컨테이너
		self.layout_schedule_list_container = QtWidgets.QVBoxLayout()
		self.layout_schedule_list_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		self.layout_schedule_list_container.setContentsMargins(0,0,0,0)
		self.layout_schedule_list_container.setSpacing(0)
		self.layout.addLayout(self.layout_schedule_list_container)

		# 리스트 박스
		self.widget_schedule_list = QtWidgets.QWidget()
		self.widget_schedule_list.setFixedWidth(270)
		self.widget_schedule_list.setContentsMargins(2,2,2,2)
		self.widget_schedule_list.setObjectName("list_container")
		self.widget_schedule_list.setStyleSheet("QWidget{background-color:%s;} QWidget#list_container{border: 1px solid #111}" % (colors.COLOR_DARK_BACKGROUND))
		self.layout_schedule_list = QtWidgets.QVBoxLayout(self.widget_schedule_list)
		self.layout_schedule_list.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		self.layout_schedule_list.setContentsMargins(0,0,0,0)
		self.layout_schedule_list.setSpacing(1)

		# 리스트 박스 스크롤 에리어
		self.scroll_schedule_list = QtWidgets.QScrollArea()
		self.scroll_schedule_list.setFixedHeight(230)
		self.scroll_schedule_list.setWidgetResizable(True)
		self.scroll_schedule_list.setWidget(self.widget_schedule_list)
		self.layout_schedule_list_container.addWidget(self.scroll_schedule_list)

	def addItem(self, time:task.WeeklyScheduleTime):
		self.layout_schedule_list.addWidget(ScheduleListBox.ScheduleTimeItem(self, time))

	def removeItem(self, item: ScheduleItem):
		self.layout_schedule_list.removeWidget(item)
		self.parent().openAddTimeSetting()
		item.setParent(None)

	def cancelEditItem(self):
		if self.current_editing_item != None:
			self.current_editing_item.setFocusOn(False)

	def editItem(self, item: ScheduleItem):
		self.current_editing_item = item
		self.parent().openEditTimeSetting(item.schedule_time)
		
	def applyItem(self, schedule_time:task.WeeklyScheduleTime):
		self.current_editing_item.apply(schedule_time)
		self.current_editing_item = None

	def setScheduleItem(self, schedule_time_list:[task.WeeklyScheduleTime]):
		QtWidgets.QWidget().setLayout(self.widget_schedule_list.layout())
		self.layout_schedule_list = QtWidgets.QVBoxLayout(self.widget_schedule_list)
		self.layout_schedule_list.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
		self.layout_schedule_list.setContentsMargins(0,0,0,0)
		self.layout_schedule_list.setSpacing(1)
		for schedule_time in schedule_time_list:
			self.addItem(schedule_time)

	def getScheduleTimeList(self) -> task.WeeklyScheduleTime:
		schedule_time_list = []
		for i in range(self.layout_schedule_list.count()):
			schedule_time_list.append(self.layout_schedule_list.itemAt(i).widget().schedule_time)
		# 끝나는 시간순 정렬
		schedule_time_list = sorted(schedule_time_list, key = lambda schedule_time: schedule_time.getSortKey())
		return schedule_time_list