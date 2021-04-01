import os
import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from module import custom_date, colors, data, task

CELL_SIZE = 33
WIDTH = 1300
HEIGHT = CELL_SIZE * 26

class TodoListView(QtWidgets.QWidget):
    def __init__(self, main=None):
        super().__init__(None)