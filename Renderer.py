from threading import Thread
from time import sleep
import os

import numpy
import glfw
from OpenGL.GL import *
from PIL import Image

from PositionalState import PositionalState

class Texture:
	def __init__(self, new_image):
		self.image = new_image

	def Draw(self):
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.image)
		glBegin(GL_QUADS)
		glTexCoord2f(0,0)
		glVertex2f(0,0)
		glTexCoord2f(0,1)
		glVertex2f(0,Renderer.WINDOW_HEIGHT)
		glTexCoord2f(1,1)
		glVertex2f(Renderer.WINDOW_WIDTH,Renderer.WINDOW_HEIGHT)
		glTexCoord2f(1,0)
		glVertex2f(Renderer.WINDOW_WIDTH,0)
		glEnd()
		glDisable(GL_TEXTURE_2D)

class TextureSet:
	def __init__(self, textures):
		self.textures = textures

	def Draw(self, index):
		self.textures[index].Draw()

class Renderer:
	# Class variables
		#---
		# PUBLIC ACCESS (constants)
	WINDOW_TITLE = "FuzzDJ 1.0"
	WINDOW_HEIGHT = 512
	WINDOW_WIDTH = 512
	
	FRAME_DIR = "./res/frame"

		#---
		# INTERNAL ACCESS
		# all available texture sets. each set corresponds to a positional state.
	images = {}

	def __init__(self):
		if not glfw.init():
			sys.exit
		glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
		glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
		self.window = glfw.create_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.WINDOW_TITLE, None, None)
		if not self.window:
			sys.exit()
		glfw.make_context_current(self.window)
		glEnable(GL_BLEND)
		glClearColor(1.0/255.0*68.0, 1.0/255.0*68.0, 1.0/255.0*68.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT)
		glViewport(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 0.0, 0.0, 1.0)

			# Load all images we're going to use
		for filename in os.listdir(self.FRAME_DIR):
			if filename.endswith(".PNG"):
				print("LOAD IMAGE: "+filename)
				shortname = os.path.splitext(filename)[0]
				self.images[shortname] = self.LoadImage(os.path.join(self.FRAME_DIR, filename))
			break

	def LoadImage(self, new_image):
		try:
			image = Image.open(new_image)
		except IOError as ex:
			print('IOError: failed to open texture file')
			message = template.format(type(ex).__name__, ex.args)
			print(message)
			return -1
		image_data = numpy.array(list(image.getdata()), numpy.uint8)

		texture_id = glGenTextures(1)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
		glBindTexture(GL_TEXTURE_2D, texture_id)
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

		image.close()
		return texture_id

	#---
	# Tick
	#	Perform a single tick of gamestate.
	def Tick(self, delta_time):
		glfw.poll_events()            
		glClear(GL_COLOR_BUFFER_BIT)
		glfw.swap_buffers(self.window)