#---
# IMPORTS
from CameraAnalyzer import CameraAnalyzer
from Interpreter import Interpreter
from Renderer import Renderer
from Controller import Controller
import time

#---
# CONSTANTS
WEBCAM_INDEX = 1

#---
# LOGIC
	# Initialize renderer
print("Spawn: Renderer")
renderer = Renderer()

	# Initialize analyzer
print("Spawn: CameraAnalyzer")
analyzer = CameraAnalyzer(new_camera_index=WEBCAM_INDEX)

	# Initialize application specific interpreter
time.sleep(5)
print("Spawn: Interpreter")
interpreter = Interpreter(new_analyzer=analyzer)

	# Initialize controller
print("Spawn: Controller")
controller = Controller(new_renderer=renderer, new_interpreter=interpreter)