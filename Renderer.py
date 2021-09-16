from threading import Thread
from time import sleep

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

		#---
		# INTERNAL ACCESS
		# all available texture sets. each set corresponds to a positional state.
	texture_sets = {}

		# currently selected texture set and index (if applicable)
	texture_set_active = None
	texture_set_index = 0

	def __init__(self):
			# Begin execution
		thread = Thread(target = self.Run, args = ())
		thread.start()

	def ChooseTextureSet(self, positional_state, index):
		self.texture_set_active = self.texture_sets[positional_state]
		self.texture_set_index = index

	#---
	# Rendering:
	#	The following methods must only be called from the glfw context thread.
	#	Attempts otherwise will fail!
	#
	def CreateTextureSet(self, new_images):
		images_loaded = []
		for new_image in new_images:
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
			images_loaded += [Texture(texture_id)]

		return TextureSet(images_loaded)

	#---
	# Run
	#	Begin rendering. Controller directs graphical state.
	def Run(self):
		if not glfw.init():
			sys.exit
		glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
		glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
		window = glfw.create_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.WINDOW_TITLE, None, None)
		if not window:
			sys.exit()
		glfw.make_context_current(window)
		glEnable(GL_BLEND)
		glClearColor(1.0/255.0*68.0, 1.0/255.0*68.0, 1.0/255.0*68.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT)
		glViewport(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 0.0, 0.0, 1.0)

			# Load all images we're going to use
		self.texture_sets[PositionalState.RIGHT_PITCH] = self.CreateTextureSet(["res/frame/IMG_1044.PNG"])

			# Default to right pitch (arbitrary)
		self.texture_set_active = PositionalState.RIGHT_PITCH
		self.texture_set_index = 0

		while True:
			glfw.poll_events()            
			glClear(GL_COLOR_BUFFER_BIT)
			if self.texture_set_active is not None:
				self.texture_sets[self.texture_set_active].Draw(self.texture_set_index)
			glfw.swap_buffers(window)