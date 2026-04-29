import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands() # this outputs the landmarks of hands (gives the co-ordinates)
mpDraw = mp.solutions.drawing_utils

### for FPS ####
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    picRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(picRGB)
    #print(results.multi_hand_landmarks) #this checks whether something is detected or not

    if results.multi_hand_landmarks:
       for handLms in results.multi_hand_landmarks:
           for id, handLm in enumerate(handLms.landmark):
               #print(id, handLm)
               h, w, c = img.shape
               cx, cy = int(handLm.x * w), int(handLm.y * h)
               print(id,cx,cy)
           mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    FPS = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(FPS)), (10,70),cv2.FONT_ITALIC,3,(255,0,255), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)