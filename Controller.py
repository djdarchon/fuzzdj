from threading import Thread
from time import sleep
from PositionalState import PositionalState
from Renderer import Renderer

class FrameState:
	def __init__(self, new_positional_state, new_frames):
		positional_state = new_positional_state
		frames = new_frames

class Actor:
	def __init__(self):
		self.x = 0
		self.y = 0

class Controller:
	def __init__(self, new_renderer, new_interpreter):
		self.interpreter = new_interpreter
		self.renderer = new_renderer
		self.actor = Actor()
		self.current_left = [0.0, None]
		self.last_left = [0.0, None, 0]

	def LockLeft(self, new_left):
		self.current_left = new_left
		print("CHANGE LEFT: "+str(self.current_left))

	def Tick(self, delta_time):
		# ask the Interpreter what it thinks is going on
		# a combination of the interpreter's confidence and our current state
		# will direct us to our next state (or the same state)
		left, right = self.interpreter.Poll()

		# hysteresis: only change our current interpretation if we've seen this 
		# new interpretation several times in a row
		HYSTERESIS_THRESHOLD = 3
		if self.last_left[2] == 0:
			# we're currently clueless. latch on to whatever this is and mark
			# a confidence of 1
			self.last_left = left + [1]
		else:
			# we're currently guessing. is our guess the same as what we're seeing
			# now? if it is, increase our confidence by 1. otherwise, decrease it
			# by 1.
			if self.last_left[1] == left[1]:
				if self.last_left[2] < HYSTERESIS_THRESHOLD:
					self.last_left[2] += 1

					# we just hit the threshold. change if it's a new
					# thing. it's also possible that we're re-entering
					# the same current frame -- for example, if we lost
					# confidence and then regained it.
					if self.last_left[2] == HYSTERESIS_THRESHOLD:
						if self.current_left[1] != self.last_left[1]:
							# this guess has high enough confidence that we should
							# lock to it. only call this function if we're transitioning
							# to a new lock (avoid extraneous callbacks)
							self.LockLeft(self.last_left)
			else:
				# losing confidence in our prior guess. we always subtract one
				# here because if we hit zero the next iteration will replace us
				# anyway. in effect, we never go negative.
				self.last_left[2] -= 1
				
					