import cv2
import mediapipe as mp
import time

class handDetector:
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackingCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        #self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackingCon)  # this outputs the landmarks of hands (gives the co-ordinates)
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackingCon
        )

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        # print(results.multi_hand_landmarks) #this checks whether something is detected or not
        picRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(picRGB)

        if self.results.multi_hand_landmarks:
             for handLms in self.results.multi_hand_landmarks:
                 if draw:
                   self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo = 0, draw = True):

        positionList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, handLm in enumerate(myHand.landmark):
                # print(id, handLm)
                h, w, c = img.shape
                cx, cy = int(handLm.x * w), int(handLm.y * h)
                positionList.append([id,cx,cy])

        return positionList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
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

if __name__ == "__main__":
    main()
