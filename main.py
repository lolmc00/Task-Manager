import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import math
import ctypes
from PyQt5 import QtWidgets, QtGui, QtCore
from view import home_view, todo_list_view, time_table_view, display_view, view_type
from component import topbar
from modules import colors, data
import config

class ToolTip(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumSize(400, 700)
        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("background-color:#111;")

    def showToolTip(self, text):
        self.setText(text)
        self.adjustSize()
        self.show()
        
    def hideToolTip(self):
        self.hide()

    def moveToolTip(self, x, y):
        self.move(x, y)

class MainWindow(QtWidgets.QWidget):
    """메인 윈도우"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Manager")
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 전체 레이아웃 생성
        self.window_layout = QtWidgets.QVBoxLayout(self)

        # 컨테이너 생성
        self.container = QtWidgets.QWidget(self)
        self.container.setStyleSheet('color: #ffffff; background: %s; border-radius: 0px;' % colors.COLOR_BACKGROUND)
        # 컨테이너 레이아웃 생성
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

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
        self.display_view = display_view.DisplayView(main=self)
        self.container_view.addWidget(self.home_view)
        self.container_view.addWidget(self.time_table_view)
        self.container_view.addWidget(self.todo_list_view)
        self.container_view.addWidget(self.display_view)
        
        # 현재 View 설정
        self.setShadowEffect()
        self.setView(view_type.DISPLAY_VIEW)
        self.window_layout.addWidget(self.container)
        # ToolTip 생성
        self.tooltip = ToolTip(self)
        self.tooltip.hide()


    def setView(self, type):
        if type == view_type.HOME_VIEW:
            if self.container_view.currentWidget() == self.display_view:
                self.setShadowEffect()
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            self.show()
            self.container_view.setCurrentWidget(self.home_view)
            self.setSize(home_view.WIDTH, home_view.HEIGHT, True)
            self.setWindowTitle("Task Manager")
        elif type == view_type.TIME_TABLE_VIEW:
            if self.container_view.currentWidget() == self.display_view:
                self.setShadowEffect()
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            self.show()
            self.time_table_view.loadData()
            self.container_view.setCurrentWidget(self.time_table_view)
            self.setSize(time_table_view.WIDTH, time_table_view.HEIGHT, True)
            self.setWindowTitle("Task Manager - Time Table")
        elif type == view_type.TODO_LIST_VIEW:
            if self.container_view.currentWidget() == self.display_view:
                self.setShadowEffect()
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            self.show()
            self.todo_list_view.loadData()
            self.container_view.setCurrentWidget(self.todo_list_view)
            self.setSize(todo_list_view.WIDTH, todo_list_view.HEIGHT, True)
            self.setWindowTitle("Task Manager - Todo List")
        elif type == view_type.DISPLAY_VIEW:
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.show()
            if self.container_view.currentWidget() != self.display_view:
                self.setOpacityEffect()
            self.display_view.loadData()
            self.container_view.setCurrentWidget(self.display_view)
            self.setSize(display_view.WIDTH, display_view.HEIGHT, False)
            self.setWindowTitle("Task Manager - Display")

    def setShadowEffect(self):
        self.window_layout.setContentsMargins(50, 50, 50, 50)
        # 컨테이너 외곽 그림자 효과
        self.container.setStyleSheet('color: #ffffff; background: %s; border-radius: 0px;' % colors.COLOR_BACKGROUND)

    def setOpacityEffect(self):
        # self.window_layout.setContentsMargins(0, 0, 0, 0)
        # 윈도우 투명화
        self.container.setStyleSheet('color: #ffffff; background: rgba(0, 0, 0, 0); border-radius: 0px;')
        # effect = QtWidgets.QGraphicsOpacityEffect()
        # effect.setOpacity(0.7)
        # self.container.setGraphicsEffect(effect)

    def setSize(self, width: int, height:int, isCenter:bool):
        temp = QtWidgets.QWidget()
        # Margin값으로 빼진만큼 더해줌, Height는 상단 도구바 높이 추가로 더해줌
        margin = self.window_layout.contentsMargins()
        width += margin.left() + margin.right()
        height += margin.top() + margin.bottom() + + self.topbar.bar_height
        temp.setFixedSize(width, height)
        # 화면 가운데로 옮기기
        frameGm = temp.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        if isCenter:
            frameGm.moveCenter(QtWidgets.QApplication.desktop().screenGeometry(screen).center())
        else:
            frameGm.moveTopRight(QtWidgets.QApplication.desktop().screenGeometry(screen).topRight())
        temp.move(frameGm.topLeft())
        self.move(frameGm.topLeft())
        self.setFixedSize(temp.size())

def setTheme(app, color):
    arrow_path = os.path.join(config.IMAGE_PATH, 'down_arrow.png').replace('\\', '/')
    arrow_disabled_path = os.path.join(config.IMAGE_PATH, 'down_arrow_disabled.png').replace('\\', '/')
    qss = f"""
        QWidget
        {{
            font: 600 15px 'Segoe UI';
        }}
        QPushButton
        {{
            padding:5px;
        }}
        QTextEdit
        {{
            border: 1px solid {color};
            font: 600 15px '나눔스퀘어';
            padding: 0px;
        }}
        QComboBox
        {{
            padding: 2px;
            border-bottom: 2px solid {color}
        }}
        QComboBox::drop-down
        {{
            border: 0px;
        }}
        QComboBox:down-arrow
        {{
            image: url({arrow_path});
            width: 14px;
            height: 14px;
        }}
        QComboBox:disabled {{
            padding: 2px;
            border-bottom: 2px solid #B8B8B8;
        }}
        QComboBox:down-arrow:disabled
        {{
            image: url({arrow_disabled_path});
            width: 14px;
            height: 14px;
        }}
        QLineEdit
        {{
            padding: 2px;
            font: 400 15px '나눔스퀘어';
            border-bottom: 2px solid {color}
        }}
        QScrollBar:vertical
        {{          
            background:none;
            width: 7px;
        }}
        QScrollBar::handle:vertical
        {{
            border-radius: 3px;
            background: {color};
            min-height: 0px;
        }}
        QScrollBar::add-page:vertical
        {{
            background:none;
        }}
        QScrollBar::sub-page:vertical
        {{
            background:none;
        }}
        QScrollBar::add-line:vertical
        {{
            height: 0px;
        }}
        QScrollBar::sub-line:vertical
        {{
            height: 0px;
        }}
        QProgressBar::chunk
        {{
            background-color: {colors.COLOR_BLUE}
        }}
    """
    app.setStyleSheet(qss)
if __name__ == "__main__":
    # 시작 프로그램 등록
    setting = QtCore.QSettings(config.RUN_PATH, QtCore.QSettings.NativeFormat)
    if not setting.contains(config.APP_NAME):
        setting.setValue(config.APP_NAME, sys.argv[0])

    # 데이터 로드
    data.load()

    # App ID 설정
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)

    # App 생성
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, "icon.png"))
    app.setWindowIcon(app_icon)
    setTheme(app, colors.COLOR_BLUE)

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