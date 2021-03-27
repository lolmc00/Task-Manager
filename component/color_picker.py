import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from module import colors

class ColorItemBox(QtWidgets.QWidget):
	CELL_SIZE = 17

	class ColorItem(QtWidgets.QWidget):
		def __init__(self, parent=None, color=None):
			super().__init__(parent)
			self.setFixedHeight(ColorItemBox.CELL_SIZE)
			self.setFixedWidth(ColorItemBox.CELL_SIZE)
			self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
			self.setStyleSheet("background-color:%s" % color)
			self.setContentsMargins(0, 0, 0, 0)

	def __init__(self, parent=None):
		super().__init__(parent)
		# 전체 레이아웃
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.label_title = QtWidgets.QLabel("Schedule Color")
		self.label_title.setStyleSheet("font: 600 22px")
		self.layout.addWidget(self.label_title)

		# 컬러 박스 컨테이너
		self.widget_color_box = QtWidgets.QWidget(self)
		self.widget_color_box.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
		self.widget_color_box.setStyleSheet("background-color:%s" % colors.COLOR_DARK_BACKGROUND)
		self.widget_color_box.setFixedHeight(ColorItemBox.CELL_SIZE * 4)
		self.widget_color_box.setContentsMargins(4, 4, 4, 4)
		self.layout.addWidget(self.widget_color_box)
		self.layout_color_box = QtWidgets.QGridLayout(self.widget_color_box)
		self.layout_color_box.setContentsMargins(0, 0, 0, 0)
		self.colorItemList = []
		# 선택된 컬러 아이템 인덱스 (기본값: 0)
		self.selectedColorIdx = 0
		for y in range(2):
			for x in range(8):
				colorItem = self.ColorItem(self, color=colors.COLORS[y*8+x])
				self.colorItemList.append(colorItem)
				self.layout_color_box.addWidget(colorItem, y, x)