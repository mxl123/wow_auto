import os, time
import ctypes
import clr
import random

mouse_dell_path = os.getcwd() + "/KeyMouseFD.dll"

clr.FindAssembly("FinedarKeyMouse")
clr.AddReference("FinedarKeyMouse")
from FinedarKeyMouse import *

class Keymouse:
	def __init__(self):
		self.key_mouse = KeyMouseFDClass()
		self.key_mouse.FindKeyMouse('2017', '2704')
		self.key_mouse.SetScreenSize(3840, 2160)
		print("init keymouse")

	def sleep(self):
		time_space = random.random()
		time.sleep(time_space)
		return time_space
	
	def click(self, key):
		self.sleep()
		print(key)
		self.key_mouse.KeyClick(key)
	
	def mouse_to(self, x, y):
		self.sleep()
		self.key_mouse.Mouse_MoveTo(x, y)
	
	def mouse_left_click(self):
		self.sleep()
		self.sleep()
		self.key_mouse.Mouse_L_BtnClick()

# my_keymouse = Keymouse()
# time.sleep(5)
# my_keymouse.click('esc')