from threading import Thread
from time import sleep
from PositionalState import PositionalState
from Renderer import Renderer

class Controller:
	def __init__(self, new_renderer, new_interpreter):
		self.interpreter = new_interpreter
		self.renderer = new_renderer

			# Begin execution
		thread = Thread(target = self.Run, args = ())
		thread.start()

	def Run(self):
		while True:
			sleep(0.2)
			print("test")