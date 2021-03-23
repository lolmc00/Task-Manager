import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class TimeTableView(QtWidgets.QWidget):
    """메인 윈도우"""
    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        # 메인 윈도우 설정
        self.parent = parent
        self.parent.setFixedHeight(600)
        self.parent.setFixedWidth(800)
        self.parent.setWindowTitle("Task Manager (Weekly Time Table)")
        # 전체 레이아웃 생성
        window_layout = QtWidgets.QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # 컨테이너 생성
        container = QtWidgets.QP(self)
        window_layout.addWidget(container)