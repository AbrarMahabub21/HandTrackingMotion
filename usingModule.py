import cv2
import mediapipe as mp
import time

import HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector   = htm.handDetector()
while True:
        success, img = cap.read()
        img = detector.findHands(img)
        positionList = detector.findPosition(img)
        if len(positionList) != 0:
            print(positionList)
        cTime = time.time()
        FPS = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(FPS)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 3)
        cv2.imshow("image", img)
        cv2.waitKey(1)