#---
# IMPORTS
from threading import Thread
import mediapipe as mp
import cv2
import time

class CameraAnalyzer:
	#---
	# Init
	#	Begin holistic model. Begin camera video capture. Begin Run.
	def __init__(self, new_camera_index, new_fps):
		self.mp_drawing = mp.solutions.drawing_utils
		self.mp_holistic = mp.solutions.holistic
		self.fps = new_fps
	
		# Open webcam
		self.cap = cv2.VideoCapture(new_camera_index)

		thread = Thread(target = self.Run)
		thread.start()
	
	#---
	# Run
	#	Begin a never-ending loop of analysis on the Camera.
	def Run(self):
		# Initiate holistic model
		with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
			while self.cap.isOpened():
				# Make Detections
				ret, frame = self.cap.read()
				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				self.SetResults(holistic.process(image))
				
				time.sleep(1.0/self.fps)

		self.cap.release()
		cv2.destroyAllWindows()

	#---
	# SetResults
	#	Assign the latest set of fetched results from the Analyzer.
	def SetResults(self, new_results):
		self.results = new_results

	#---
	# GetResults
	#	Return the latest set of fetched results from the Analyzer.
	def GetResults(self):
		return self.results