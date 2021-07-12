#---
# IMPORTS
from CameraAnalyzer import CameraAnalyzer
from Interpreter import Interpreter
import time

#---
# CONSTANTS
WEBCAM_INDEX = 1

#---
# LOGIC
	# Initialize analyzer (OpenCV)
analyzer = CameraAnalyzer(WEBCAM_INDEX)

	# Initialize application specific interpreter
time.sleep(5)
interpreter = Interpreter(analyzer)