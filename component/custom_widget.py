import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class HoverButton(QtWidgets.QPushButton):
	def __init__(self, *args, **kwargs):
		QtWidgets.QPushButton.__init__(self, *args, **kwargs)

	def setImage(self, image_name, image_size=24):
		self.image_name = image_name
		self.image_size = image_size
		icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, self.image_name + ".png"))
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(self.image_size, self.image_size))
		self.setStyleSheet('border: 0px; color: #dddddd')

	def enterEvent(self, event):
		icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, self.image_name + "_hover.png"))
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(self.image_size, self.image_size))

	def leaveEvent(self, event):
		icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, self.image_name + ".png"))
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(self.image_size, self.image_size))