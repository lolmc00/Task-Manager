import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import ctypes
from PyQt5 import QtWidgets, QtGui, QtCore
import home_view, time_table_view, view_type
from component import topbar
from module import colors
import config
from qt_material import apply_stylesheet

class MainWindow(QtWidgets.QWidget):
    """메인 윈도우"""
    def __init__(self, parent=None):
        super().__init__(parent)

        # 전체 레이아웃 생성
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(50, 50, 50, 50)

        # 컨테이너 생성
        self.container = QtWidgets.QWidget(self)
        # 컨테이너 레이아웃 생성
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.container.setStyleSheet('color: #ffffff; background: %s; font-family: "Segoe UI";  border-radius: 0px;' % colors.COLOR_BACKGROUND)
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setOffset(0, 0)
        effect.setBlurRadius(50)
        effect.setColor(QtGui.QColor(0, 0, 0, 212))
        self.container.setGraphicsEffect(effect)
        self.topbar = topbar.TopBar(self)
        self.layout.addWidget(self.topbar)
        # 현재 View 설정
        self.setView(view_type.HOME_VIEW)
        self.window_layout.addWidget(self.container)

    def setView(self, type):
        current_widget = self.findChild(QtWidgets.QWidget, "current_view")
        if type == view_type.HOME_VIEW:
            new_widget = home_view.HomeView(self)
            self.topbar.remove_home_btn()
        elif type == view_type.TIME_TABLE_VIEW:
            new_widget = time_table_view.TimeTableView(self)
            self.topbar.create_home_btn()
        elif type == view_type.TODO_LIST_VIEW:
            new_widget = time_table_view.TimeTableView(self)
            self.topbar.create_home_btn()
        elif type == view_type.TIME_TABLE_VIEW:
            new_widget = time_table_view.TimeTableView(self)
            self.topbar.create_home_btn()
        new_widget.setObjectName("current_view")
        if current_widget != None:
            self.layout.replaceWidget(current_widget, new_widget)
            current_widget.deleteLater()
        else:
            self.layout.addWidget(new_widget)

    def setSize(self, height:int, width: int):
        # Margin값으로 빼진만큼 더해줌, Height는 상단 도구바 높이 추가로 더해줌
        self.setFixedHeight(height + 100 + self.topbar.bar_height)
        self.setFixedWidth(width + 100)

if __name__ == "__main__":
    # App ID 설정
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)

    # App 생성
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon(os.path.join(config.ROOT_PATH, "image", "icon.png"))
    app.setWindowIcon(app_icon)
    apply_stylesheet(app, theme='dark_blue.xml')
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