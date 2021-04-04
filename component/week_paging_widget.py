import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import custom_widget
from datetime import datetime, date, timedelta

class WeekPagingWidget(QtWidgets.QWidget):
	def __init__(self, parent:QtWidgets.QWidget=None, todo_list_widget:QtWidgets.QWidget=None):
		super().__init__(parent)
		self.todo_list_widget = todo_list_widget
		# 현재 주 시작일, 종료일 가져오기
		self.week_start_date:date = datetime.today().date() - timedelta(days=datetime.today().weekday())
		self.week_end_date:date = self.week_start_date + timedelta(days=6)

		# 위젯 설정
		self.setFixedWidth(self.parentWidget().width() / 2)
		self.setStyleSheet("font: 100 25px 'Segoe UI'")

		# 레이아웃
		self.layout = QtWidgets.QHBoxLayout(self)

		# 년, 월, 주 레이아웃
		self.layout_hbox_1 = QtWidgets.QHBoxLayout()
		self.layout_hbox_1.setContentsMargins(0, 0, 0, 0)
		self.layout_hbox_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		# 년, 월, 주 라벨
		self.label_year_month = QtWidgets.QLabel()
		self.layout_hbox_1.addWidget(self.label_year_month)
		self.applyLabelText()

		# 이전 월 버튼
		self.btn_prev_month = custom_widget.HoverButton('left_arrow', 36)
		self.btn_prev_month.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_prev_month.clicked.connect(lambda: self.prevWeek())

		# 다음 월 버튼
		self.btn_next_month = custom_widget.HoverButton('right_arrow', 36)
		self.btn_next_month.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.btn_next_month.clicked.connect(lambda: self.nextWeek())

		# 전체 레이아웃에 추가
		self.layout.addWidget(self.btn_prev_month)
		self.layout.addLayout(self.layout_hbox_1)
		self.layout.addWidget(self.btn_next_month)

	def getStringFormat(self, number):
		return "0" + str(number) if number < 10 else str(number)

	def nextWeek(self):
		self.week_start_date += timedelta(days=7)
		self.week_end_date += timedelta(days=7)
		self.applyLabelText()
		self.todo_list_widget.applyGrid()
		
	def prevWeek(self):
		self.week_start_date -= timedelta(days=7)
		self.week_end_date -= timedelta(days=7)
		self.applyLabelText()
		self.todo_list_widget.applyGrid()

	def applyLabelText(self):
		self.label_year_month.setText("%s.%s.%s ~ %s.%s.%s" % (self.getStringFormat(self.week_start_date.year),\
			self.getStringFormat(self.week_start_date.month), self.getStringFormat(self.week_start_date.day),\
			self.getStringFormat(self.week_end_date.year), self.getStringFormat(self.week_end_date.month),\
			self.getStringFormat(self.week_end_date.day)))

# month_string_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# weekday_string_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]