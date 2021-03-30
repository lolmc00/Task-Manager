import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import main, time_table_view, view_type, config
from component import custom_widget

WIDTH = 400
HEIGHT = 515

class HomeView(QtWidgets.QWidget):
    """메인 윈도우"""
    def __init__(self, main=None):
        super().__init__(None)
        self.main = main
        self.setFixedSize(WIDTH, HEIGHT)
        # 전체 레이아웃 생성
        window_layout = QtWidgets.QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # 컨테이너 생성
        container = QtWidgets.QWidget(self)
        # 컨테이너 레이아웃 생성
        layout = QtWidgets.QVBoxLayout(container)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # logo 레이블 생성
        logo_label = QtWidgets.QLabel(config.APP_NAME, self)
        logo_label.setStyleSheet('font: 900 40px "Segoe UI";')
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Author 버튼 + Github 버튼 컨테이너 Hbox 생성
        author_hbox = QtWidgets.QHBoxLayout()
        author_hbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        author_hbox.setSpacing(7)

        # author 레이블 생성
        author_label = QtWidgets.QLabel("By " + config.AUTHOR)
        author_label.setStyleSheet('font: 700 16px; color: #59EAB3')
        author_label.setAlignment(QtCore.Qt.AlignCenter)

        # Github 버튼 생성
        github_button = custom_widget.HoverButton("github_icon", 32)
        github_button.clicked.connect(lambda: webbrowser.open('https://github.com/lolmc00'))
        author_hbox.addWidget(author_label)
        author_hbox.addWidget(github_button)
        layout.addLayout(author_hbox)

        # 위젯 수직 위치 조절
        layout.addStretch(2)
        # 버튼 컨테이너 생성
        button_vbox = QtWidgets.QVBoxLayout()
        button_vbox.setContentsMargins(20, 0, 20, 20)
        button_vbox.setSpacing(20)
        # Weekly Time Table 메뉴 버튼 생성
        timetable_widget = MenuButton(self, self.main)
        timetable_widget.setImage("timetable_icon")
        timetable_widget.setTitle("Weekly planner")
        timetable_widget.setDescription("Set weekly planner")
        timetable_widget.setViewType(view_type.TIME_TABLE_VIEW)
        # To do List 메뉴 버튼 생성
        todolist_widget = MenuButton(self, self.main)
        todolist_widget.setImage("todolist_icon")
        todolist_widget.setTitle("To-do List")
        todolist_widget.setDescription("Make a to-do list on calendar")
        todolist_widget.setViewType(view_type.TODO_LIST_VIEW)
        # Display Current Tasks 메뉴 버튼 생성
        display_widget = MenuButton(self, self.main)
        display_widget.setImage("display_icon")
        display_widget.setTitle("Display Current Tasks")
        display_widget.setDescription("Display current tasks as a PIP window")
        display_widget.setViewType(view_type.DISPLAY_VIEW)
        button_vbox.addWidget(timetable_widget)
        button_vbox.addWidget(todolist_widget)
        button_vbox.addWidget(display_widget)
        layout.addLayout(button_vbox)
        layout.addStretch(2)
        window_layout.addWidget(container)

class MenuButton(QtWidgets.QWidget):
    qss = """
        QWidget{
            background-color:rgba(0,0,0,0)
        }
        QWidget#container:hover{
            background-color:rgba(16,16,16,255)
        }
    """
    def __init__(self, parent:QtWidgets.QWidget=None, main:QtWidgets.QWidget=None):
        super().__init__(parent)
        self.parent = parent
        self.main = main
        layout = QtWidgets.QVBoxLayout(self)
        container = QtWidgets.QWidget(self)
        container.setObjectName("container")
        container.setStyleSheet(self.qss)
        hlayout = QtWidgets.QHBoxLayout(container)
        hlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        hlayout.setSpacing(10)

        self.icon_label = QtWidgets.QLabel()
        self.type = None
        hlayout.addWidget(self.icon_label)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        self.title_label = QtWidgets.QLabel("Title")
        self.title_label.setStyleSheet("font: 600 25px Segoe UI")
        self.description_label = QtWidgets.QLabel("description")
        self.description_label.setStyleSheet("font: 400 14px Segoe UI")
        vlayout.addWidget(self.title_label)
        vlayout.addWidget(self.description_label)
        hlayout.addLayout(vlayout)
        layout.addWidget(container)
    
    def setImage(self, image_name):
        self.icon_pixmap = QtGui.QPixmap(os.path.join(config.IMAGE_PATH, image_name + '.png'))
        self.icon_pixmap = self.icon_pixmap.scaled(48, 48, QtCore.Qt.KeepAspectRatio)
        self.icon_label.setPixmap(self.icon_pixmap)

    def setTitle(self, title):
        self.title_label.setText(title)
    
    def setDescription(self, description):
        self.description_label.setText(description)
    
    def setViewType(self, type):
        self.type = type
    
    def mousePressEvent(self, event):
        self.main.setView(self.type)
