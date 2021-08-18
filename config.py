import os
import sys

if hasattr(sys, "_MEIPASS"):
    abs_home = os.path.abspath(os.path.expanduser("~"))
    abs_dir_app = os.path.join(abs_home, f".TaskManager")
    if not os.path.exists(abs_dir_app):
        os.mkdir(abs_dir_app)
    os.chdir(abs_dir_app)
    cfg_path = os.path.join(abs_dir_app, "login.properties")
else:
    os.chdir(os.getcwd())

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(ROOT_PATH, "image")
SOUND_PATH = os.path.join(ROOT_PATH, "sound")
APP_NAME = "Task Manager"
APP_ID = 'lolmc.TaskManager'
AUTHOR = "LOLMC"
RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"