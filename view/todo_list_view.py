import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import todo_list_widget, todo_input_widget

CELL_SIZE = 33
WIDTH = 1300
HEIGHT = CELL_SIZE * 26

class TodoListView(QtWidgets.QWidget):
    def __init__(self, main=None):
        super().__init__(None)
        self.main = main
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        # 상단 정렬용 레이아웃
        self.layout_vertical_1 = QtWidgets.QVBoxLayout()
        self.layout_vertical_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.layout_vertical_1)

        # Todo List 위젯
        self.widget_todo_list = todo_list_widget.TodoListWidget(self, self.main)
        self.layout_vertical_1.addWidget(self.widget_todo_list)

        # 상단 정렬용 레이아웃
        self.layout_vertical_2 = QtWidgets.QVBoxLayout()
        self.layout_vertical_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addLayout(self.layout_vertical_2)

        # 세팅 컨테이너 위젯 & 레이아웃 생성
        self.widget_setting_container = QtWidgets.QWidget(self)
        self.widget_setting_container.setObjectName("setting_container")
        self.widget_setting_container.setStyleSheet("QWidget#setting_container{border-left: 1px solid #3e3e3e;}")
        self.layout_setting_container = QtWidgets.QVBoxLayout(self.widget_setting_container)
        self.layout_setting_container.setSpacing(0)
        self.layout_setting_container.setContentsMargins(0, 0, 0, 0)
        self.widget_setting = todo_input_widget.TodoInputWidget(self)
        self.layout_setting_container.addWidget(self.widget_setting)
        self.layout_vertical_2.addWidget(self.widget_setting_container)

    def loadData(self):
        self.widget_todo_list.loadData()
        self.widget_setting.loadData()