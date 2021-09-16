#---
# IMPORTS
from threading import Thread
import mediapipe as mp
import cv2

class CameraAnalyzer:
	#---
	# Init
	#	Begin holistic model. Begin camera video capture. Begin Run.
	def __init__(self, new_camera_index):
		self.mp_drawing = mp.solutions.drawing_utils
		self.mp_holistic = mp.solutions.holistic
	
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
				ret, frame = self.cap.read()
				
				# Recolor Feed
				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		
				# Make Detections
				self.SetResults(holistic.process(image))
				
				# Recolor image back to BGR for rendering
				image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				
				# Draw face landmarks
				#self.mp_drawing.draw_landmarks(image, self.GetResults().face_landmarks, self.mp_holistic.FACE_CONNECTIONS)
				
				# Right hand
				self.mp_drawing.draw_landmarks(image, self.GetResults().right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
		
				# Left Hand
				self.mp_drawing.draw_landmarks(image, self.GetResults().left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
		
				# Pose Detections
				#self.mp_drawing.draw_landmarks(image, self.GetResults().pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)
								
				cv2.imshow('Raw Webcam Feed', image)
		
				if cv2.waitKey(10) & 0xFF == ord('q'):
					break

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