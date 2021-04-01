import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import ctypes
from PyQt5 import QtWidgets, QtGui, QtCore
from view import home_view, todo_list_view, time_table_view, view_type
from component import topbar
from module import colors, data
import config
from qt_material import apply_stylesheet

class MainWindow(QtWidgets.QWidget):
    """메인 윈도우"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 전체 레이아웃 생성
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(50, 50, 50, 50)

        # 컨테이너 생성
        self.container = QtWidgets.QWidget(self)
        # 컨테이너 레이아웃 생성
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.container.setStyleSheet('color: #ffffff; background: %s; border-radius: 0px;' % colors.COLOR_BACKGROUND)
        # 컨테이너 외곽 그림자 효과
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setOffset(0, 0)
        effect.setBlurRadius(50)
        effect.setColor(QtGui.QColor(0, 0, 0, 212))
        self.container.setGraphicsEffect(effect)

        # Top bar 생성
        self.topbar = topbar.TopBar(self)
        self.layout.addWidget(self.topbar)

        # View Container 생성
        self.container_view = QtWidgets.QStackedWidget(self.container)
        self.layout.addWidget(self.container_view)

        # View 인스턴스 생성
        self.home_view = home_view.HomeView(main=self)
        self.todo_list_view = todo_list_view.TodoListView(main=self)
        self.time_table_view = time_table_view.TimeTableView(main=self)
        
        self.container_view.addWidget(self.home_view)
        self.container_view.addWidget(self.time_table_view)
        self.container_view.addWidget(self.todo_list_view)
        
        # ToolTip 생성
        self.toolTip = QtWidgets.QWidget(self)
        self.toolTip.setFixedWidth(220)
        self.toolTip.setObjectName("toolTip")
        self.toolTip.setStyleSheet("QWidget#toolTip{background-color: rgba(0, 0, 0, 170)}")
        self.toolTip.hide()

        # 현재 View 설정
        self.setView(view_type.HOME_VIEW)
        self.window_layout.addWidget(self.container)

    def showToolTip(self, layout:[QtWidgets.QVBoxLayout]):
        n = len(layout)
        # self.toolTip.move(pos)
        self.toolTip.setFixedHeight(70 * n)
        # ToolTip layout 비우고 교체하기
        if self.toolTip.layout() != None:
            QtWidgets.QWidget().setLayout(self.toolTip.layout())
        layout_toolTip = QtWidgets.QGridLayout(self.toolTip)
        layout_toolTip.setContentsMargins(5, 5, 5, 5)
        # for i in range(n):
        layout_toolTip.addLayout(layout[0], 0, 0)
        self.toolTip.show()

    def hideToolTip(self):
        self.toolTip.hide()

    def moveToolTip(self, x, y):
        self.toolTip.move(x, y)

    def setView(self, type):
        if type == view_type.HOME_VIEW:
            self.container_view.setCurrentWidget(self.home_view)
            self.setSize(home_view.WIDTH, home_view.HEIGHT)
            self.setWindowTitle("Task Manager")
            self.topbar.hide_home_btn()
        elif type == view_type.TIME_TABLE_VIEW:
            self.container_view.setCurrentWidget(self.time_table_view)
            self.setSize(time_table_view.WIDTH, time_table_view.HEIGHT)
            self.setWindowTitle("Task Manager - Time Table")
            self.topbar.show_home_btn()
        elif type == view_type.TODO_LIST_VIEW:
            self.container_view.setCurrentWidget(self.todo_list_view)
            self.setSize(todo_list_view.WIDTH, todo_list_view.HEIGHT)
            self.setWindowTitle("Task Manager - Todo List")
            self.topbar.show_home_btn()
        elif type == view_type.TIME_TABLE_VIEW:
            self.container_view.setCurrentWidget(self.time_table_view)
            self.topbar.show_home_btn()

    def setSize(self, width: int, height:int):
        temp = QtWidgets.QWidget()
        # Margin값으로 빼진만큼 더해줌, Height는 상단 도구바 높이 추가로 더해줌
        temp.setFixedSize(width + 100, height + 100 + self.topbar.bar_height)
        # 화면 가운데로 옮기기
        frameGm = temp.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        temp.move(frameGm.topLeft())
        self.move(frameGm.topLeft())
        self.setFixedSize(temp.size())

if __name__ == "__main__":
    # 데이터 로드
    data.load()

    # App ID 설정
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)

    # App 생성
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon(os.path.join(config.ROOT_PATH, "image", "icon.png"))
    app.setWindowIcon(app_icon)
    apply_stylesheet(app, theme='dark_blue.xml')
    app.setStyleSheet(app.styleSheet() + "QWidget{font-family:'Segoe UI'}")

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