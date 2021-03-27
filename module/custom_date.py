class Period():
	def __init__(self, day_of_the_week: str, start_time: str, start_time_minute: str, end_time: str, end_time_minute: str):
		self.day_of_the_week = day_of_the_week
		self.start_time = start_time
		self.start_time_minute = start_time_minute
		self.end_time = end_time
		self.end_time_minute = end_time_minute
	
	def getDayOfTheWeek(self):
		return self.day_of_the_week
	def getStartTime(self):
		return self.start_time
	def getStartTimeMinute(self):
		return self.start_time_minute
	def getEndTime(self):
		return self.end_time
	def getEndTimeMinute(self):
		return self.end_time_minute
	def getStartFullTime(self):
		return self.start_time + ":" + self.start_time_minute
	def getEndFullTime(self):
		return self.end_time + ":" + self.end_time_minute