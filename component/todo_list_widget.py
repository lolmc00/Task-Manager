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
    def __init__(self, parent:QtWidgets.QWidget=None, main:QtWidgets.QWidget=None, todo:task.Todo=None, grid:QtWidgets.QWidget=None):
        super().__init__(parent, main)
        self.todo = todo
        self.grid = grid
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setFixedSize(230, 110)
        self.setObjectName("container")
        self.setStyleSheet("QWidget#container{border:1px solid %s}" % todo.getColor())
        self.layout_ = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout_)
        self.layout_.setContentsMargins(1,1,1,1)
        self.layout_.setSpacing(0)
        super().addTodoItem(todo, True)

        # 완료된 할 일일 경우 Opacity처리
        if self.todo.isCompleted():
            effect = QtWidgets.QGraphicsColorizeEffect(self)
            effect.setColor(QtGui.QColor("#000"))
            effect.setStrength(0.5)
            self.setGraphicsEffect(effect)

        # 상단 제목, 도구 컨테이너
        self.widget_top = QtWidgets.QWidget(self)
        self.widget_top.setFixedHeight(26)
        self.widget_top.setObjectName("widget_top")
        self.widget_top.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.widget_top.setStyleSheet("background-color:%s" % todo.getColor())
        self.widget_top.mouseMoveEvent = lambda event: self.mouseMoveEvent(event)
        self.widget_top.setMouseTracking(True)
        self.layout_top = QtWidgets.QHBoxLayout(self.widget_top)
        self.layout_top.setContentsMargins(5,0,0,7)
        self.layout_top.setSpacing(5)
        self.layout_.addWidget(self.widget_top)

        # 제목 라벨
        self.label_title = QtWidgets.QLabel()
        self.label_title.setStyleSheet("font: 600 15px; %s" % ("text-decoration:line-through" if todo.isCompleted() else ""))
        elided_title = self.label_title.fontMetrics().elidedText(todo.getTitle(), QtCore.Qt.TextElideMode.ElideRight, self.label_title.width())
        self.label_title.setText(elided_title)
        self.layout_top.addWidget(self.label_title)

        self.layout_top.addStretch(1)

        # 컨텐츠 컨테이너
        self.widget_contents = QtWidgets.QWidget(self)
        self.layout_contents = QtWidgets.QVBoxLayout(self.widget_contents)
        self.layout_contents.setContentsMargins(5,2,2,5)
        self.layout_contents.setSpacing(0)
        self.layout_.addWidget(self.widget_contents)

        # 시작 시간, 끝 시간 레이블
        if todo.getParentSchedule() != None:
            self.label_time = QtWidgets.QLabel("%s" % todo.getParentSchedule().getTitle())
            self.label_time.setStyleSheet("font: 500 15px; color:%s;" % (todo.getParentSchedule().getColor()))
        else:
            self.label_time = QtWidgets.QLabel("%s:%s ~ %s:%s" % (todo.getTimePeriod().getStartTimeString(), todo.getTimePeriod().getStartTimeMinuteString(), \
            todo.getTimePeriod().getEndTimeString(), todo.getTimePeriod().getEndTimeMinuteString()))
            self.label_time.setStyleSheet("font: 500 15px; color:#dedede;")
        self.label_time.mouseMoveEvent = lambda event: self.mouseMoveEvent(event)
        self.label_time.setMouseTracking(True)
        self.layout_contents.addWidget(self.label_time)

        if self.todo.getDescription() != '':
            # 설명 박스
            self.edit_todo_description = QtWidgets.QTextEdit(self.todo.getDescription())
            self.edit_todo_description.setStyleSheet("font: 400 13px; border:0px")
            self.setFixedHeight(200)
            self.edit_todo_description.setFixedHeight(90)
            self.edit_todo_description.setContentsMargins(0, 0, 0, 0)
            self.edit_todo_description.setReadOnly(True)
            self.layout_contents.addWidget(self.edit_todo_description)
            

        # 완료(재시작), 수정 버튼 컨테이너
        self.widget_btn_container = QtWidgets.QWidget()
        self.widget_btn_container.setMouseTracking(True)
        self.widget_btn_container.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout_btn_container = QtWidgets.QHBoxLayout(self.widget_btn_container)
        self.layout_btn_container.setContentsMargins(0, 0, 0, 0)
        self.layout_contents.addWidget(self.widget_btn_container)
        # 완료(재시작), 삭제 버튼
        self.btn_complete_redo = QtWidgets.QPushButton("redo" if todo.isCompleted() else "complete")
        self.btn_complete_redo.setFixedSize(90, 10)
        self.btn_complete_redo.clicked.connect(self.onClickRedoBtn if todo.isCompleted() else self.onClickCompleteBtn)
        self.btn_complete_redo.setStyleSheet("font:600 10px; border: 2px solid %s" % colors.COLOR_PURPLE)
        self.btn_complete_redo.mouseMoveEvent = lambda event: self.mouseMoveEvent(event)
        self.btn_complete_redo.setMouseTracking(True)
        self.btn_complete_redo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout_btn_container.addWidget(self.btn_complete_redo)
        self.btn_edit = QtWidgets.QPushButton("edit")
        self.btn_edit.setFixedSize(90, 10)
        self.btn_edit.setStyleSheet("font:600 10px; border: 2px solid %s" % colors.COLOR_AQUA)
        self.btn_edit.clicked.connect(self.onClickEditBtn)
        self.btn_edit.mouseMoveEvent = lambda event: self.mouseMoveEvent(event)
        self.btn_edit.setMouseTracking(True)
        self.btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout_btn_container.addWidget(self.btn_edit)
        self.setMouseTracking(True)
        
    def onClickCompleteBtn(self):
        # Todo Completed로 수정하고 저장 & 업데이트
        self.todo.complete()
        data.save()
        self.grid.deleteTodoItem(self.todo)
        self.grid.addTodoItem(self.todo)

    def onClickRedoBtn(self):
        # Todo Not Completed로 수정하고 저장 & 업데이트
        self.todo.redo()
        data.save()
        self.grid.deleteTodoItem(self.todo)
        self.grid.addTodoItem(self.todo)

    def onClickEditBtn(self):
        self.grid.editTodoItem(self.todo)

    def setFocusOn(self, isFocusOn):
        if isFocusOn:
            self.setGraphicsEffect(None)
        else:
            opacity = QtWidgets.QGraphicsOpacityEffect(self)
            opacity.setOpacity(0.1)
            self.setGraphicsEffect(opacity)

class TodoListWidget(QtWidgets.QWidget):
    def __init__(self, parent:QtWidgets.QWidget=None, main=None):
        super().__init__(parent)
        # 현재 날짜
        self.date = datetime.today()
        self.main = main
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
            widget_todo_container.setContentsMargins(0, 0, 5, 0)
            layout_todo_container = QtWidgets.QVBoxLayout(widget_todo_container)
            layout_todo_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            layout_todo_container.setContentsMargins(0, 0, 0, 0)
            layout_todo_container.setSpacing(5)
            widget_todo_container.setStyleSheet("background-color:%s" % (colors.COLOR_DARK_BACKGROUND))
            scroll_todo_container = QtWidgets.QScrollArea()
            scroll_todo_container.setWidgetResizable(True)
            scroll_todo_container.setFixedHeight(350)
            scroll_todo_container.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            scroll_todo_container.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll_todo_container.setWidget(widget_todo_container)
            self.layout_gird.addWidget(scroll_todo_container, y, x, 1, 2)
            self.widget_todo_list.append(widget_todo_container)

        # 전체 레이아웃에 아이템 포함시키기
        self.layout.addWidget(self.widget_paging_container)
        self.layout.addLayout(self.layout_gird)

        # 데이터 로드
        self.loadData()

    def loadData(self):
        self.applyGrid()

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
            self.addTodoItem(todo)

    def addTodoItem(self, todo:task.Todo):
        if todo.getDate() > self.widget_week_paiging.week_end_date:
            return
        idx = todo.getDate().weekday()
        # SortKey값으로 정렬된 위치에 삽입
        for pos in range(self.widget_todo_list[idx].layout().count()):
            if self.widget_todo_list[idx].layout().itemAt(pos).widget().todo.getSortKey() >= todo.getSortKey():
                self.widget_todo_list[idx].layout().insertWidget(pos, TodoItem(parent=None, todo=todo, grid=self, main=self.main))
                return
        self.widget_todo_list[idx].layout().addWidget(TodoItem(parent=None, todo=todo, grid=self, main=self.main))

    def editTodoItem(self, todo:task.Todo):
        if self.parent().widget_setting.current_editing_todo == todo:
            return
        for idx in range(len(self.widget_todo_list)):
            for i in range(self.widget_todo_list[idx].layout().count()):
                todo_item = self.widget_todo_list[idx].layout().itemAt(i).widget()
                todo_item.setFocusOn(todo_item.todo == todo)
        self.parent().widget_setting.openEditTodo(todo)

    def deleteTodoItem(self, todo:task.Todo):
        for idx in range(len(self.widget_todo_list)):
            for i in reversed(range(self.widget_todo_list[idx].layout().count())): 
                todo_item = self.widget_todo_list[idx].layout().itemAt(i).widget()
                if todo_item.todo == todo:
                    todo_item.setParent(None)
                    todo_item.deleteLater()

    def resetFocusItems(self):
        for idx in range(len(self.widget_todo_list)):
            for i in range(self.widget_todo_list[idx].layout().count()):
                todo_item = self.widget_todo_list[idx].layout().itemAt(i).widget()
                todo_item.setFocusOn(True)

    