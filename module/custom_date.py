class DayScheduleTime():
    def __init__(self, day_of_the_week, start_time, start_time_minute, end_time, end_time_minute):
        self.day_of_the_week = day_of_the_week
        self.start_time = int(start_time)
        self.start_time_minute = int(start_time_minute)
        self.end_time = int(end_time)
        self.end_time_minute = int(end_time_minute)
	
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
        return self.getDayOfTheWeekIndex() * 24 * 60 + self.getStartTimeToMinute()

    def checkConflict(self, other):
        if self.day_of_the_week == other.getDayOfTheWeek():
           return (self.getStartTimeToMinute() < other.getEndTimeToMinute()) and (self.getEndTimeToMinute() > other.getStartTimeToMinute())
        return False
                