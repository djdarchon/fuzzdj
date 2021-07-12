from threading import Thread
import time
from Geo import Point, AABB
import mediapipe as mp

class Interpreter:
	CONST_CALIBRATION_DELAY = 5
	CONST_POLLING_PERIOD = 0.2

	def __init__(self, new_analyzer):
		self.analyzer = new_analyzer

			# set up models
		self.mp_hands = mp.solutions.hands

			# set up bounding boxes for detection
		self.aabbs = [	AABB("RIGHT_PITCH",   Point(0.0, 1.0),     Point(0.22, 0.75)    ),
						AABB("RIGHT_TUNE",    Point(0.06, 0.64),   Point(0.18, 0.140)   ),
						AABB("RIGHT_SCRATCH", Point(0.25, 0.544),  Point(0.374, 0.044)  ),
						AABB("RIGHT_EQ",      Point(0.38, 1.0),    Point(0.462, 0.358)  ),
						AABB("RIGHT_LINE",    Point(0.400, 0.283), Point(0.483, 0.0)    ),

                        AABB("LEFT_PITCH",    Point(0.626, 1.0),   Point(0.847, 0.75)   ),
						AABB("LEFT_TUNE",     Point(0.868, 0.620), Point(0.926, 0.115)  ),
						AABB("LEFT_SCRATCH",  Point(0.771, 0.535), Point(0.854, 0.025)  ),
						AABB("LEFT_EQ",       Point(0.518, 1.0),   Point(0.577, 0.358)  ),
                        AABB("LEFT_LINE",     Point(0.505, 0.283), Point(0.590, 0.0)    )
		]

		thread = Thread(target = self.InterpretationLoop)
		thread.start()

	def TipsAverage(self, hand):
		x = 0
		y = 0
		total = 0
		
		tips = [ 	hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
					hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
					hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
					hand.landmark[self.mp_hands.HandLandmark.PINKY_TIP]	]
					
		for tip in tips:
			if tip is not None:
				total += 1
				x += tip.x
				y += tip.y

		if total > 0:
			x /= total
			y /= total

		print (str(total)+ " TIPS -> "+str(Point(x,y)))

		return Point(x, y)

	def TipsAABB(self, hand):
		tips = [ 	hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
					hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
					hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
					hand.landmark[self.mp_hands.HandLandmark.PINKY_TIP]	]
		return AABB.FromPoints(tips)

	def InterpretationLoop(self):
			# Calibrate
		print("CALIBRATING...")

		print("--------------------------------------------")
		print("POINT DOWN AT AT NEAR-SIDE CORNERS OF TURNTABLES")
		print("--------------------------------------------")
		results = None
		while results is None:
			time.sleep(self.CONST_CALIBRATION_DELAY)
			
			results = self.analyzer.GetResults()
			if results is None:
				continue
	
			left = results.left_hand_landmarks
			if left is None:
				results = None
				continue
			right = results.right_hand_landmarks
			if right is None:
				results = None
				continue
	
			back_left = self.TipsAverage(right)
			back_right = self.TipsAverage(left)
			print(str(back_left))
			print(str(back_right))
		print("-= NEXT =-")
		
		print("--------------------------------------------")
		print("POINT DOWN AT FAR-SIDE CORNERS OF TURNTABLES")		
		print("--------------------------------------------")
		results = None
		while results is None:
			time.sleep(self.CONST_CALIBRATION_DELAY)
			
			results = self.analyzer.GetResults()
			if results is None:
				continue

			left = results.left_hand_landmarks
			if left is None:
				results = None
				continue

			right = results.right_hand_landmarks
			if right is None:
				results = None
				continue
	
			front_left = self.TipsAverage(right)
			front_right = self.TipsAverage(left)
			# Jaden's glorious hack to align the tables with the camera
			front_left.y = 1.0
			front_right.y = 1.0
			print(str(front_left))
			print(str(front_right))
		
		print("-= NEXT =-")

			# Construct main area aabb
		main_area = AABB("MAIN_AREA", front_left, Point(front_right.x, back_right.y))

		# Realtime process and interpret.
		print("INTERPRETATION ACTIVE")

		while True:
			time.sleep(self.CONST_POLLING_PERIOD)

				# get hands
			results = self.analyzer.GetResults()
			if results is None:
				continue

				# it's ok if one hand is missing, just make it none
			hands = []
			for hand in [ results.left_hand_landmarks , results.right_hand_landmarks ]:
				hand_normal = None

				if hand is not None:
					hand_aabb = self.TipsAABB(hand)
					intersection = main_area.QueryAABB(hand_aabb)
					if intersection is not None:
						inter_bl = intersection.point_bl
						inter_tr = intersection.point_tr

							# Normalize
						# intersection. clamp to main area and average.
						inter_bl.x = (inter_bl.x - main_area.point_bl.x) / (main_area.point_tr.x - main_area.point_bl.x)
						inter_bl.y = (inter_bl.y - main_area.point_tr.y) / (main_area.point_bl.y - main_area.point_tr.y)

						inter_tr.x = (inter_tr.x - main_area.point_bl.x) / (main_area.point_tr.x - main_area.point_bl.x)
						inter_tr.y = (inter_tr.y - main_area.point_tr.y) / (main_area.point_bl.y - main_area.point_tr.y)

						hand_normal = AABB("NORMALIZED_INTERSECTION", inter_bl, inter_tr)
				
				hands += [ hand_normal ]

				# now see where the fuck the points land
			hands_result = []
			for hand in hands:
				result = None
				confidence = -999
				if hand is not None:
					for aabb in self.aabbs:
						next_confidence = 0
						intersection = aabb.QueryAABB(hand)
						if intersection is not None:
							aabb_area = aabb.Area()
							intersection_area = intersection.Area()
							next_confidence = (intersection_area / aabb_area)
						if next_confidence > confidence:
							confidence = next_confidence
							result = aabb
				hands_result += [(confidence, result)]
					
				# results ready now interpret
				# each result is: <confidence, resultant aabb>
			left_hand = hands_result[0]
			right_hand = hands_result[1]

			if left_hand[0] > 0.0:
				print("HIT: "+str(left_hand[1]))
			if right_hand[0] > 0.0:
				print("HIT: "+str(right_hand[1]))