import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from module import colors

class ColorItemBox(QtWidgets.QWidget):
	CELL_SIZE = 17

	class ColorItem(QtWidgets.QWidget):
		def __init__(self, parent=None, color=None, idx=0):
			super().__init__(parent)
			self.parent = parent
			self.idx = idx
			self.color = color
			self.setFixedHeight(ColorItemBox.CELL_SIZE)
			self.setFixedWidth(ColorItemBox.CELL_SIZE)
			self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
			self.setStyleSheet("background-color:%s" % color)
			self.setContentsMargins(0, 0, 0, 0)

		def mouseReleaseEvent(self, event):
			self.parent.selectColorItem(self.color)

		def toggleOn(self):
			self.setStyleSheet("background-color:%s; border: 2px solid #fff" % self.color)
	
		def toggleOff(self):
			self.setStyleSheet("background-color:%s; border: 0px" % self.color)

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

		# Grid 채우고 리스트에 아이템 저장
		self.color_item_list = []
		for y in range(2):
			for x in range(7):
				color_item = self.ColorItem(self, color=colors.COLORS[y*7+x], idx=y*7+x)
				self.color_item_list.append(color_item)
				self.layout_color_box.addWidget(color_item, y, x)
			
		# 선택된 컬러 아이템 인덱스 (기본값: 0)
		self.selected_color_item_idx = 0
		self.color_item_list[self.selected_color_item_idx].toggleOn()

	def selectColorItem(self, color:str):
		idx = colors.COLORS.index(color)
		if self.selected_color_item_idx != None:
			origin_selected_item = self.color_item_list[self.selected_color_item_idx]
			origin_selected_item.toggleOff()
		self.selected_color_item_idx = idx
		selectedColorItem = self.color_item_list[self.selected_color_item_idx]
		selectedColorItem.toggleOn()
	
	def getCurrentColorItem(self):
		return self.color_item_list[self.selected_color_item_idx]