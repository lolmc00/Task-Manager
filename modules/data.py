import dill
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from typing import List
from modules import task

schedule_list:List[task.Schedule] = []
todo_list:List[task.Todo] = []

def load():
	try:
		with open('save.data', 'rb') as file:
			global schedule_list, todo_list
			schedule_list, todo_list = dill.load(file)
	except FileNotFoundError:
		return

def save():
	with open('save.data', 'wb') as file:
		dill.dump((schedule_list, todo_list), file)