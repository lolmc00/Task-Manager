import os
import sys
import ctypes
from PyQt5 import QtWidgets, QtGui, QtCore
import home_view, time_table_view, view_type
from component import topbar
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class MainWindow(QtWidgets.QWidget):
    """메인 윈도우"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_widget = None

        # 전체 레이아웃 생성
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        self.window_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # 컨테이너 생성
        self.container = QtWidgets.QWidget(self)
        # 컨테이너 레이아웃 생성
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.container.setStyleSheet('color: #ffffff; background: #1e1e1e; font-family: "Segoe UI";')
        self.setFixedHeight(650)
        self.setFixedWidth(500)
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        self.window_layout.setContentsMargins(50, 50, 50, 50)
        effect.setOffset(0, 0)
        effect.setBlurRadius(50)
        effect.setColor(QtGui.QColor(0, 0, 0, 212))
        self.container.setGraphicsEffect(effect)
        self.layout.addWidget(topbar.TopBar(self))
        # 현재 View 설정
        self.setView(view_type.HOME_VIEW)
        self.window_layout.addWidget(self.container)

    def setView(self, type):
        new_widget = None
        if type == view_type.HOME_VIEW:
            new_widget = home_view.HomeView(self)
        elif type == view_type.TIME_TABLE_VIEW:
            new_widget = time_table_view.TimeTableView(self)
        # elif type == view_type.TODO_LIST_VIEW:
        #     new_widget = time_table_view.TimeTableView(widget)
        # elif type == view_type.TIME_TABLE_VIEW:
        #     new_widget = time_table_view.TimeTableView(widget)
        if self.current_widget != None:
            self.layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
        self.current_widget = new_widget
        self.layout.addWidget(self.current_widget)
if __name__ == "__main__":
    # App ID 설정
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)

    # App 생성
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon(os.path.join(config.ROOT_PATH, "image", "icon.png"))
    app.setWindowIcon(app_icon)

    # Window 생성
    window = MainWindow()
    window.show()

    # TrayIcon 생성
    trayIcon = QtWidgets.QSystemTrayIcon(app_icon, parent=app)
    trayIcon.setToolTip(config.APP_NAME + '가 실행 중입니다.')

    # TrayIcon Context 설정
    menu = QtWidgets.QMenu()
    exitAction = menu.addAction('종료')
    exitAction.triggered.connect(app.quit)
    trayIcon.setContextMenu(menu)
    trayIcon.show()

    app.exec()