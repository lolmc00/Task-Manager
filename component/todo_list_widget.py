import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from component import week_paging_widget, tooltip, custom_widget
from datetime import datetime, timedelta
from module import task, colors, data

class TodoItem(tooltip.ToolTipWidget):
    def __init__(self, parent:QtWidgets.QWidget=None, todo:task.Todo=None, grid:QtWidgets.QWidget=None):
        super().__init__(parent)
        self.parent = parent
        self.todo = todo
        self.grid = grid
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setFixedSize(230, 200)
        self.setObjectName("container")
        self.setStyleSheet("QWidget#container{border:1px solid %s}" % todo.getColor())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(1,1,1,1)
        self.layout.setSpacing(0)

        # 상단 제목, 도구 컨테이너
        self.widget_top = QtWidgets.QWidget(self)
        self.widget_top.setFixedHeight(26)
        self.widget_top.setObjectName("widget_top")
        self.widget_top.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.widget_top.setStyleSheet("background-color:%s" % todo.getColor())
        self.layout_top = QtWidgets.QHBoxLayout(self.widget_top)
        self.layout_top.setContentsMargins(5,0,0,7)
        self.layout_top.setSpacing(5)
        self.layout.addWidget(self.widget_top)

        # 제목 라벨
        self.label_title = QtWidgets.QLabel()
        self.label_title.setStyleSheet("font: 600 15px;")
        elided_title = self.label_title.fontMetrics().elidedText(todo.getTitle(), QtCore.Qt.TextElideMode.ElideRight, self.label_title.width())
        self.label_title.setText(elided_title)
        self.layout_top.addWidget(self.label_title)

        self.layout_top.addStretch(1)

        # 컨텐츠 컨테이너
        self.widget_contents = QtWidgets.QWidget(self)
        self.layout_contents = QtWidgets.QVBoxLayout(self.widget_contents)
        self.layout_contents.setContentsMargins(5,2,2,5)
        self.layout_contents.setSpacing(0)
        self.layout.addWidget(self.widget_contents)

        # 시작 시간, 끝 시간 레이블
        if todo.getParentSchedule() != None:
            self.label_time = QtWidgets.QLabel("%s" % todo.getParentSchedule().getTitle())
            self.label_time.setStyleSheet("font: 500 15px; color:%s;" % (todo.getParentSchedule().getColor()))
        else:
            self.label_time = QtWidgets.QLabel("%s:%s ~ %s:%s" % (todo.getTimePeriod().getStartTimeString(), todo.getTimePeriod().getStartTimeMinuteString(), \
            todo.getTimePeriod().getEndTimeString(), todo.getTimePeriod().getEndTimeMinuteString()))
            self.label_time.setStyleSheet("font: 500 15px; color:#dedede;")
        self.layout_contents.addWidget(self.label_time)


        # 설명 박스
        self.edit_todo_description = QtWidgets.QTextEdit(self.todo.getDescription())
        self.edit_todo_description.setStyleSheet("font: 400 13px; border:0px")
        self.edit_todo_description.setFixedHeight(90)
        self.edit_todo_description.setContentsMargins(0, 0, 0, 0)
        self.edit_todo_description.setReadOnly(True)
        self.layout_contents.addWidget(self.edit_todo_description)

        # 완료, 수정 버튼 컨테이너
        self.layout_btn_container = QtWidgets.QHBoxLayout()
        self.layout_contents.addLayout(self.layout_btn_container)
        # 완료, 삭제 버튼
        self.btn_complete = QtWidgets.QPushButton("complete")
        self.btn_complete.setFixedSize(90, 10)
        self.btn_complete.setStyleSheet("font:600 10px; border: 2px solid %s" % colors.COLOR_PURPLE)
        self.layout_btn_container.addWidget(self.btn_complete)
        self.btn_edit = QtWidgets.QPushButton("edit")
        self.btn_edit.setFixedSize(90, 10)
        self.btn_edit.setStyleSheet("font:600 10px; border: 2px solid %s" % colors.COLOR_AQUA)
        self.btn_edit.clicked.connect(self.onClickEditBtn)
        self.layout_btn_container.addWidget(self.btn_edit)

    def onClickCompleteBtn(self):
        self.grid.editTodo(self)

    def onClickEditBtn(self):
        self.grid.editTodo(self)

    def setFocusOn(self, isFocusOn):
        if isFocusOn:
            self.setGraphicsEffect(None)
        else:
            opacity = QtWidgets.QGraphicsOpacityEffect(self)
            opacity.setOpacity(0.1)
            self.setGraphicsEffect(opacity)

class TodoListWidget(QtWidgets.QWidget):
    def __init__(self, parent:QtWidgets.QWidget=None):
        super().__init__(parent)
        # 현재 날짜
        self.date = datetime.today()

        # 위젯 크기 설정
        self.setFixedSize(1000, 858)
        self.setContentsMargins(0, 0, 0, 0)

        # 전체 레이아웃
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(24, 0, 24, 18)

        # Week Paging 위젯 컨테이너
        self.widget_paging_container = QtWidgets.QWidget()
        self.widget_paging_container.setFixedSize(952, 50)
        self.layout_paging_container = QtWidgets.QHBoxLayout(self.widget_paging_container)
        self.layout_paging_container.setContentsMargins(0, 0, 0, 0)
        self.layout_paging_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        # Week Paging 위젯
        self.widget_week_paiging = week_paging_widget.WeekPagingWidget(self.widget_paging_container, self)
        self.layout_paging_container.addWidget(self.widget_week_paiging)

        # TodoList Grid 레이아웃
        self.layout_gird = QtWidgets.QGridLayout()
        self.layout_gird.setSpacing(5)
        self.layout_gird.setContentsMargins(0, 0, 0, 0)
        # Grid 레이아웃 채우기
        self.label_date_list = []
        self.widget_todo_list = []
        for i in range(7):
            y = 1 + (i >= 4) * 2
            x = (i * 2)
            if x > 7:
                x -= 7
            # 요일 레이블 생성
            label_date = QtWidgets.QLabel("")
            label_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_date.setFixedHeight(40)
            label_date.setStyleSheet("font: 200 20px; border-bottom: 1px solid #fff")
            self.label_date_list.append(label_date)
            self.layout_gird.addWidget(label_date, y - 1, x, 1, 2)
            # Todo Item Container 생성
            widget_todo_container = QtWidgets.QWidget()
            widget_todo_container.setContentsMargins(0, 0, 3, 0)
            layout_todo_container = QtWidgets.QVBoxLayout(widget_todo_container)
            layout_todo_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            layout_todo_container.setContentsMargins(0, 0, 0, 0)
            layout_todo_container.setSpacing(0)
            widget_todo_container.setStyleSheet("background-color:%s" % (colors.COLOR_DARK_BACKGROUND))
            scroll_todo_container = QtWidgets.QScrollArea()
            scroll_todo_container.setWidgetResizable(True)
            scroll_todo_container.setFixedHeight(350)
            scroll_todo_container.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            scroll_todo_container.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_todo_container.setWidget(widget_todo_container)
            self.layout_gird.addWidget(scroll_todo_container, y, x, 1, 2)
            print(self.layout_gird.cellRect(y, x).size().width(), self.layout_gird.cellRect(y, x).size().height())
            self.widget_todo_list.append(widget_todo_container)

        # 전체 레이아웃에 아이템 포함시키기
        self.layout.addWidget(self.widget_paging_container)
        self.layout.addLayout(self.layout_gird)

    def applyGrid(self):
        # 요일 레이블 설정
        for i in range(len(self.label_date_list)):
            weekday_string_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
            month = self.widget_week_paiging.getStringFormat((self.widget_week_paiging.week_start_date + timedelta(days=i)).month)
            day = self.widget_week_paiging.getStringFormat((self.widget_week_paiging.week_start_date + timedelta(days=i)).day)
            weekday = weekday_string_list[i]
            self.label_date_list[i].setText("%s.%s %s" % (month, day, weekday))

        # Todo 컨테이너 설정
        for widget in self.widget_todo_list:
            layout = widget.layout()
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().deleteLater()
        todo_list = list(filter(lambda todo: self.widget_week_paiging.week_start_date <= todo.getDate() <= self.widget_week_paiging.week_end_date, data.todo_list))
        for todo in todo_list:
            self.addTodo(todo)

    def addTodo(self, todo:task.Todo):
        if todo.getDate() > self.widget_week_paiging.week_end_date:
            return
        idx = todo.getDate().weekday()
        self.widget_todo_list[idx].layout().addWidget(TodoItem(self.widget_todo_list[idx], todo, self))

    def editTodo(self, item:TodoItem):
        if self.parent().widget_setting.current_editing_todo_item == item:
            return
        for idx in range(len(self.widget_todo_list)):
            for i in range(self.widget_todo_list[idx].layout().count()):
                todo_item = self.widget_todo_list[idx].layout().itemAt(i).widget()
                todo_item.setFocusOn(todo_item == item)
        self.parent().widget_setting.openEditTodo(item)

    def deleteTodo(self, item:TodoItem):
        item.setParent(None)

    def resetFocusItems(self):
        for idx in range(len(self.widget_todo_list)):
            for i in range(self.widget_todo_list[idx].layout().count()):
                todo_item = self.widget_todo_list[idx].layout().itemAt(i).widget()
                todo_item.setFocusOn(True)

    