"""윈도우 타이틀 꾸미기
https://soma0sd.tistory.com/
"""
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from . import custom_widget
from view import view_type

class TopBar(QtWidgets.QWidget):
    """제목 표시줄 위젯"""
    qss = """
        QWidget {
            color: #FFFFFF;
            background: #1e1e1e;
            height: 32px;
            font: "Segoe UI";
        }
        QLabel {
            color: #FFFFFF;
            background: #1e1e1e;
            font-size: 16px;
            padding: 5px 5px;
        }
        QToolButton {
            background: #1e1e1e;
            border: none;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bar_height = 36
        self.parent = parent
        self.has_clicked = False
        self.is_maximized = False
        self.setStyleSheet(self.qss)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(self.bar_height)
        self.left_layout = QtWidgets.QHBoxLayout()
        self.left_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.left_layout.setContentsMargins(7, 7, 7, 0)
        self.btn_home = custom_widget.HoverButton("")
        self.btn_home.setImage("home_icon")
        self.btn_home.clicked.connect(lambda: self.parent.setView(view_type.HOME_VIEW))
        self.btn_home.setFixedSize(self.bar_height, self.bar_height)
        self.right_layout = QtWidgets.QHBoxLayout()
        self.right_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        btn_minimize = self.create_tool_btn('minimize.png', "#141414")
        btn_minimize.clicked.connect(self.show_minimized)
        btn_close = self.create_tool_btn('close.png', "#FF0000")
        btn_close.clicked.connect(self.close)

        self.right_layout.addWidget(btn_minimize)
        self.right_layout.addWidget(btn_close)
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

    def create_home_btn(self):
        self.left_layout.addWidget(self.btn_home)
    
    def remove_home_btn(self):
        self.left_layout.removeWidget(self.btn_home)

    def create_tool_btn(self, icon_path, color):
        """제목표시줄 아이콘 생성"""
        icon = os.path.join(config.IMAGE_PATH, icon_path)
        btn = QtWidgets.QToolButton(self)
        btn.setStyleSheet("QToolButton:hover {background: %s;border: none;}" % color)
        btn.setIcon(QtGui.QIcon(icon))
        btn.setIconSize(QtCore.QSize(self.bar_height, self.bar_height))
        btn.setFixedSize(self.bar_height, self.bar_height)
        return btn

    def show_minimized(self):
        """버튼 명령: 최소화"""
        self.parent.showMinimized()

    def close(self):
        """버튼 명령: 닫기"""
        self.parent.close()

    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.parent.is_moving = True
            self.parent.offset = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.parent.is_moving:
            delta = QtCore.QPoint (event.globalPos() - self.parent.offset)
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.offset = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        """오버로딩: 더블클릭 이벤트
        - 제목 표시줄 더블클릭시 최대화
        """
        if self.is_maximized:
            self.parent.showNormal()
            self.is_maximized = False
        else:
            self.parent.showMaximized()
            self.is_maximized = True