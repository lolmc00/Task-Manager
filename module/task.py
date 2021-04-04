from . import colors
from typing import List
from datetime import date, datetime

class TimePeriod():
	def __init__(self, start_time, start_time_minute, end_time, end_time_minute):
		self.start_time = int(start_time)
		self.start_time_minute = int(start_time_minute)
		self.end_time = int(end_time)
		self.end_time_minute = int(end_time_minute)

	def getStartTime(self):
		return self.start_time
	def getStartTimeMinute(self):
		return self.start_time_minute
	def getEndTime(self):
		return self.end_time
	def getEndTimeMinute(self):
		return self.end_time_minute

	def getStartTimeString(self):
		return "0" + str(self.start_time) if self.start_time < 10 else str(self.start_time)
	def getStartTimeMinuteString(self):
		return "0" + str(self.start_time_minute) if self.start_time_minute < 10 else str(self.start_time_minute)
	def getEndTimeString(self):
		return "0" + str(self.end_time) if self.end_time < 10 else str(self.end_time)
	def getEndTimeMinuteString(self):
		return "0" + str(self.end_time_minute) if self.end_time_minute < 10 else str(self.end_time_minute)

	def getTimeString(self):
		return "%s:%s ~ %s:%s" % (self.getStartTimeString(), self.getStartTimeMinuteString(), self.getEndTimeString(), self.getEndTimeMinuteString())

	def getStartTimeToMinute(self):
		return self.start_time * 60 + self.start_time_minute

	def getEndTimeToMinute(self):
		return self.end_time * 60 + self.end_time_minute

	def getSortKey(self):
		return self.getStartTimeToMinute()

	def isInTime(self, datetime:datetime):
		if self.getStartTimeToMinute() <= (datetime.hour * 60 + datetime.minute) <= self.getEndTimeToMinute():
			return True

	def getDuringMinute(self):
		return self.getEndTimeToMinute() - self.getStartTimeToMinute()

class WeeklyScheduleTime():
	def __init__(self, day_of_the_week, time_period:TimePeriod):
		self.day_of_the_week = day_of_the_week
		self.time_period = time_period
	
	def getDayOfTheWeek(self):
		return self.day_of_the_week
	
	def getDayOfTheWeekIndex(self):
		if self.day_of_the_week.lower() == "monday":
			return 0
		elif self.day_of_the_week.lower() == "tuesday":
			return 1
		elif self.day_of_the_week.lower() == "wednesday":
			return 2
		elif self.day_of_the_week.lower() == "thursday":
			return 3
		elif self.day_of_the_week.lower() == "friday":
			return 4
		elif self.day_of_the_week.lower() == "saturday":
			return 5
		elif self.day_of_the_week.lower() == "sunday":
			return 6
		return -1

	def getTimePeriod(self):
		return self.time_period

	def getSortKey(self):
		return self.getDayOfTheWeekIndex() * 24 * 60 + self.time_period.getSortKey()

	def checkConflict(self, other):
		if self.day_of_the_week == other.getDayOfTheWeek():
			return (self.time_period.getStartTimeToMinute() < other.time_period.getEndTimeToMinute()) and (self.time_period.getEndTimeToMinute() > other.time_period.getStartTimeToMinute())
		return False

	def isInTime(self, datetime:datetime):
		if self.getDayOfTheWeekIndex() == datetime.weekday():
			if self.getTimePeriod().isInTime(datetime):
				return True
		return False

class Schedule():
	def __init__(self, title:str="New Schedule", color:str=colors.COLOR_AQUA, schedule_time_list:List[WeeklyScheduleTime] = []):
		self.title = title
		self.color = color
		self.schedule_time_list = schedule_time_list

	def getTitle(self):
		return self.title
	
	def getColor(self):
		return self.color
	
	def getScheduleTimeList(self):
		return self.schedule_time_list

	def checkConflict(self, other):
		for schedule_time in self.schedule_time_list:
			for other_schedule_time in other.getScheduleTimeList():
				if schedule_time.checkConflict(other_schedule_time):
					return True
		return False

class Todo():
	def __init__(self, title:str, descriptionHtml:str, description:str, date:date, parent_schedule: Schedule, color:str, time_period:TimePeriod=TimePeriod(0, 0, 24, 0), completed:bool=False):
		self.title = title
		self.descriptionHtml = descriptionHtml
		self.description = description
		self.date = date
		self.time_period = time_period
		self.parent_schedule = parent_schedule
		self.color = color
		self.completed = completed
		
	def getTitle(self):
		return self.title

	def getDescriptionHtml(self):
		return self.descriptionHtml

	def getDescription(self):
		return self.description

	def getDate(self):
		return self.date

	def getTimePeriod(self):
		return self.time_period

	def getParentSchedule(self):
		return self.parent_schedule

	def getColor(self):
		return self.color

	def getSortKey(self):
		return self.isCompleted() * 10000 + self.time_period.getSortKey()

	def isInTime(self, datetime:datetime):
		if self.getParentSchedule() != None:
			for schedule_time in self.getParentSchedule().getScheduleTimeList():
				if schedule_time.isInTime(datetime):
					return True
		else:
			if self.getDate().strftime("%Y %m %d") == datetime.strftime("%Y %m %d"):
				if self.getTimePeriod().isInTime(datetime):
					return True
		return False

	def isCompleted(self):
		return self.completed

	def complete(self):
		self.completed = True

	def redo(self):
		self.completed = False