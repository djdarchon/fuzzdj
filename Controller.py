import random
from threading import Thread
from time import sleep
from PositionalState import PositionalState

#---
# FrameState
#	These state objects each represent a set of frames that form a category. A FrameState's job
#	is to be Tick()ed. When it is Tick()ed, it may internally decide how to be rendered.
#
class FrameState:
	def __init__(self, frames):
		self.alive_time = 0.0
		self.request_time = 0.0
		self.request = False
		self.frames = frames
		self.current_frame = frames[0]
		self.offset_x = 0
		self.offset_y = 0
		self.scale_x = 1
		self.scale_y = 1

	def Begin(self):
		self.current_frame = random.choose(frames)

	def End(self):
		pass

	def GetAliveTime(self):
		return self.alive_time

	def Request(self, next_frame_state, next_left):
		self.request = True
		self.request_time = 0.0
		return True, next_frame_state, next_left

	def Tick(self, delta_time)
		self.alive_time += delta_time
		if self.request:
			self.request_time += delta_time

	def Render(self, delta_time)
		pass

class FrameStateDance(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_DANCE_0", "FRAME_DANCE_1", "FRAME_DANCE_2", "FRAME_DANCE_3", "FRAME_DANCE_4", "FRAME_DANCE_5", "FRAME_DANCE_6"])

class FrameStateEQ(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_EQ_0", "FRAME_EQ_1", "FRAME_EQ_2"])

class FrameStateEQDual(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_EQ_DUAL_0"])

class FrameStateLine(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_FX_0"])

class FrameStateLineDual(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_LINE_DUAL_0"])

class FrameStateFun(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_FUN_0", "FRAME_FUN_1"])

class FrameStateFX(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_FX_0"])

class FrameStateIdle(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_IDLE_0", "FRAME_IDLE_1", "FRAME_IDLE_2", "FRAME_IDLE_3"])

class FrameStatePitch(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_PITCH_0", "FRAME_PITCH_1", "FRAME_PITCH_2", "FRAME_PITCH_3"])

class FrameStateScratch(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_SCRATCH_0", "FRAME_SCRATCH_1", "FRAME_SCRATCH_2"])

class FrameStateTune(FrameState):
	def __init__(self, frames):
		super().__init__(["FRAME_TUNE_0"])

#---
# State
#	State is how we represent the avatar. It consists of a physical position and a set of frame states to transition
#	between.
#
class State:
	def __init__(self):
		self.update = False
		self.x = 0
		self.y = 0
		self.left = 0
		self.frame_state = StateIdle()
		self.frame_state.Begin()

	def StateTransition(self, new_state, new_left=True)
		self.frame_state.End()
		self.frame_state = new_state
		self.frame_state.Begin()

	def ReceiveUpdate(self, new_left, new_right):
		self.update = True
		self.input = [new_left, new_right]

	def Tick(self, delta_time):
		#---
		# State Machine
			# idling
		if self.input is [PositionalState.NONE, PositionalState.NONE]
			next_frame_state = FrameStateIdle()

			# EQ Dual
		if PositionalState.LEFT_EQ in self.input and PositionalState.RIGHT_EQ in self.input:
			next_frame_state = FrameStateEQDual()
			# EQ Left
		elif PositionalState.LEFT_EQ in self.input:
			next_frame_state = FrameStateEQ()
			next_left = True
			# EQ Right
		elif PositionalState.LEFT_EQ in self.input:
			next_frame_state = FrameStateEQ()
			next_left = False
		
			# Scratching
		if PositionalState.LEFT_SCRATCH in self.input:
			next_frame_state = FrameStateScratch()
			next_left = True
		elif PositionalState.RIGHT_SCRATCH in self.input:
			next_frame_state = FrameStateScratch()
			next_left = False

			# Line faders
		if PositionalState.LEFT_LINE in self.input:
			next_frame_state = FrameStateLine()
			next_left = True
		elif PositionalState.RIGHT_LINE in self.input:
			next_frame_state = FrameStateLine()
			next_left = False

			# FX (currently unsupported)
		#if PositionalState.LEFT_LINE in self.input:
		#	next_frame_state = FrameStateLine()
		#	next_left = True
		#elif PositionalState.RIGHT_LINE in self.input:
		#	next_frame_state = FrameStateLine()
		#	next_left = False

			# Tune
		if PositionalState.LEFT_TUNE in self.input:
			next_frame_state = FrameStateTune()
			next_left = True
		elif PositionalState.RIGHT_TUNE in self.input:
			next_frame_state = FrameStateTune()
			next_left = False

			# Pitch
		if PositionalState.LEFT_PITCH in self.input:
			next_frame_state = FrameStatePitch()
			next_left = True
		elif PositionalState.RIGHT_PITCH in self.input:
			next_frame_state = FrameStatePitch()
			next_left = False

			# ask current state to allow the transition
			# some transitions may not be allowed as they are nonsensical. other transitions can be achieved,
			# but only by going through an intermediate state
		if next_frame_state is not self.frame_state:
			allow, modified_next_frame_state, modified_next_left = self.frame_state.Request(next_frame_state, next_left)
			if allow:
				StateTransition(modified_next_frame_state, modified_next_left)

		if self.update:
			self.update = False

	def Render(self, delta_time):
		self.frame_state.Render(delta_time)

#---
# Controller
#	Manages input from the interpreter and feeds it to the state object for state transition.
#
class Controller:
	def __init__(self, new_interpreter):
		self.interpreter = new_interpreter

			# interpretation
		self.current_left = [0.0, None, 0]
		self.last_left = [0.0, None, 0]
		self.current_right = [0.0, None, 0]
		self.last_right = [0.0, None, 0]
		self.HYSTERESIS_THRESHOLD = 5

			# render state
		self.state = State()

	def LockLeft(self, new_left):
		self.current_left = new_left

	def LockRight(self, new_right):
		self.current_right = new_right

	def ProcessInterpretation(self, delta_time):
		update = False

		# ask the Interpreter what it thinks is going on
		# a combination of the interpreter's confidence and our current state
		# will direct us to our next state (or the same state)
		left, right = self.interpreter.Poll()

		# hysteresis: only change our current interpretation if we've seen this 
		# new interpretation several times in a row
		if self.last_left[2] == 0:
			# we're currently clueless. latch on to whatever this is and mark
			# a confidence of 1
			self.last_left = left + [1]
		else:
			# we're currently guessing. is our guess the same as what we're seeing
			# now? if it is, increase our confidence by 1. otherwise, decrease it
			# by 1.
			if self.last_left[1] == left[1]:
				if self.last_left[2] < self.HYSTERESIS_THRESHOLD:
					self.last_left[2] += 1

					# we just hit the threshold. change if it's a new
					# thing. it's also possible that we're re-entering
					# the same current frame -- for example, if we lost
					# confidence and then regained it.
					if self.last_left[2] == self.HYSTERESIS_THRESHOLD:
						if self.current_left[1] != self.last_left[1]:
							# this guess has high enough confidence that we should
							# lock to it. only call this function if we're transitioning
							# to a new lock (avoid extraneous callbacks)
							self.LockLeft(self.last_left)
							update = True
			else:
				# losing confidence in our prior guess. we always subtract one
				# here because if we hit zero the next iteration will replace us
				# anyway. in effect, we never go negative.
				self.last_left[2] -= 1
			
		# identical processing for right
		if self.last_right[2] == 0:
			self.last_right = right + [1]
		else:
			if self.last_right[1] == right[1]:
				if self.last_right[2] < self.HYSTERESIS_THRESHOLD:
					self.last_right[2] += 1

					if self.last_right[2] == self.HYSTERESIS_THRESHOLD:
						if self.current_right[1] != self.last_right[1]:
							self.LockRight(self.last_right)
							update = True
			else:
				self.last_right[2] -= 1

		return update

	def Tick(self, delta_time):
		# collect latest results; returns true if we have a new update
		# forward results to our actor
		if self.ProcessInterpretation():
			self.state.ReceiveUpdate(self.current_left, self.current_right)

		self.state.Tick(delta_time)

	def Render(self, delta_time):
		self.state.Render(delta_time)