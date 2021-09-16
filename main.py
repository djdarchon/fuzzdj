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
FPS = 60

#---
# LOGIC

	# Initialize analyzer
print("Spawn: CameraAnalyzer")
analyzer = CameraAnalyzer(new_camera_index=WEBCAM_INDEX, new_fps=FPS)

	# Initialize application specific interpreter
time.sleep(5)
print("Spawn: Interpreter")
interpreter = Interpreter(new_analyzer=analyzer)

	# Initialize controller
print("Spawn: Controller")
controller = Controller(new_interpreter=interpreter)

	# Initialize renderer
print("Spawn: Renderer")
renderer = Renderer(new_controller=controller)

	# Main Loop
while True:
	controller.Tick(1.0/FPS)
	renderer.Tick(1.0/FPS)
	time.sleep (1.0/FPS)