import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

class MultipleLineLabel(QtWidgets.QTextEdit):
	def __init__(self, parent:QtWidgets.QWidget=None, text:str="text", max_size:int = 22):
		super().__init__(parent)
		self.parent = parent
		self.origin_text = text
		self.max_size = max_size
		self.setFixedSize(self.parentWidget().contentsRect().size())
		self.setReadOnly(True)
		self.setAlignment(QtCore.Qt.AlignTop)
		self.setText(text)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		font = QtGui.QFont("나눔스퀘어")
		font.setPixelSize(self.max_size)
		font.setWeight(QtGui.QFont.Weight.Bold)
		self.setStyleSheet("border:0px; font: bold %ipx '나눔스퀘어'" % self.max_size)
		self.setFont(font)
		self.updateLabelText()

	def updateLabelText(self):
		try:
			font = self.font()
			metrics = QtGui.QFontMetrics(font)
			# 텍스트 font-size AutoScaling
			parent_size = self.parent.contentsRect().width() * (self.parent.contentsRect().height() * 0.7)
			text_size = metrics.boundingRect(self.toPlainText()).width() * metrics.boundingRect(self.toPlainText()).height()
			scale_mult = (float(parent_size)/float(text_size * 1.5)) ** 0.5
			auto_scaled_font_size = min(self.max_size, int(font.pixelSize() * scale_mult))
			font.setPixelSize(auto_scaled_font_size)
			self.setStyleSheet("border:0px; font: bold %ipx '나눔스퀘어'" % auto_scaled_font_size)
		except:
			self.setText('')

			# # 텍스트 자동 개행
			# text_list = []
			# text = self.text()
			# curr_width = 0
			# prev_pos = 0
			# for pos in range(len(text)):
			# 	width = metrics.boundingRect(text[pos]).width() + metrics.leftBearing(text[pos]) + metrics.rightBearing(text[pos])
			# 	if curr_width + width > self.parent.contentsRect().width():
			# 		text_list.append(text[prev_pos : pos])
			# 		text_list.append('<br>')
			# 		curr_width = width
			# 		prev_pos = pos
			# 	else:
			# 		curr_width += width
			# text_list.append(text[prev_pos:len(text)])
			# self.setText(''.join(text_list))

class HoverButton(QtWidgets.QToolButton):
	def __init__(self, image_name=None, image_size=24):
		QtWidgets.QToolButton.__init__(self)
		self.setContentsMargins(0, 0, 0, 0)
		self.image_name = image_name
		self.image_size = image_size
		self.setFixedHeight(image_size)
		self.setFixedWidth(image_size)
		icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, self.image_name + ".png"))
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(self.image_size, self.image_size))
		self.setStyleSheet('border: 0px;')

	def enterEvent(self, event):
		icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, self.image_name + "_hover.png"))
		self.setIcon(icon)

	def leaveEvent(self, event):
		icon = QtGui.QIcon(os.path.join(config.IMAGE_PATH, self.image_name + ".png"))
		self.setIcon(icon)