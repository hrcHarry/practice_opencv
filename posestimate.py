import cv2
import mediapipe as mp
import time
import os

"""
You must install opencv-python(cv2) and mediapipe before excuting this module.

By the way, the python devolopment is ver3.9


==============================================================================
Usage:

1. Put this module in any dirctory.

2. Put any media file (.mp4, .gif, etc.) in the same directory

3. Excute this module in cmd: python poseesti.py

4. Follow the instruction in the program

Enjoy!

"""

class poseDetector():
	def __init__(self, mode= False, upBody= False, smooth= True, detectionCon= 0.5, trackCon= 0.5):
		self.mode = mode
		self.upBody = upBody
		self.smooth = smooth
		self.detectionCon = detectionCon
		self.trackCon = trackCon

		self.mpDraw = mp.solutions.drawing_utils
		self.mpPose = mp.solutions.pose 
		self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

	def findPose(self, img, draw= True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.pose.process(imgRGB)
		if self.results.pose_landmarks:
			if draw:
				self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

		return img


def main():
	inputVid = str(input("\n Enter ONE file name in the same directory (eg. movie.mp4, or animation.gif): "))
	inputKey = int(input("\n Enter the integer number controlling the display rate (the larger number the slower display): "))
	dirPath = "./"
	if inputVid in os.listdir(dirPath):
		cap = cv2.VideoCapture(inputVid)
		pTime = 0	# previous time
		detector = poseDetector()

		while True:
			success, img = cap.read()
			img = detector.findPose(img)

			cTime = time.time()    # current time
			fps = 1/(cTime - pTime)
			pTime = cTime

			cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

			cv2.imshow("Video", img)
			cv2.waitKey(inputKey)
	else:
		print("\n Go checking the file name and excute again")


if __name__ == "__main__":
	main()