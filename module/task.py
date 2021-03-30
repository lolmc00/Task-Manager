from . import colors, custom_date
from typing import List

class Schedule():
	def __init__(self, title:str="New Schedule", color:str=colors.COLOR_AQUA, schedule_time_list:List[custom_date.DayScheduleTime] = []):
		self.title = title
		self.color = color
		self.schedule_time_list = schedule_time_list

	def getTitle(self):
		return self.title
	
	def getColor(self):
		return self.color
	
	def getScheduleTimeList(self):
		return self.schedule_time_list