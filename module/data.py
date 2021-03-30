import dill
from typing import List
from . import task

schedule_list:List[task.Schedule] = []

def load():
	with open('load.data', 'rb') as file:
		global schedule_list
		schedule_list = dill.load(file)

def save():
	with open('save.data', 'wb') as file:
		dill.dump(schedule_list, file)