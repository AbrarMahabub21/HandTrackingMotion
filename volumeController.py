import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities

cap = cv2.VideoCapture(0)
wCap, hCap = 640, 480
cap.set(3, wCap)
cap.set(4, hCap)
pTime = 0
detector = htm.handDetector()


device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
print(f"Audio output: {device.FriendlyName}")
# print(f"- Muted: {bool(volume.GetMute())}")
# print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
# print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
volumeRange = volume.GetVolumeRange()
minRange = volumeRange[0] # -74 dB
maxRange = volumeRange[1] # 0 dB
smooth_vol = 0


while True:
    success, img = cap.read()
    img  = detector.findHands(img)
    positionList = detector.findPosition(img)
    if len(positionList) != 0:
        # print(positionList[4], positionList[8])

        x1,y1 = positionList[4][1], positionList[4][2]
        x2, y2 = positionList[8][1], positionList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 10,(255,0,0), cv2.FILLED)
        cv2.circle(img, (x2,y2),10,(255,0,0), cv2.FILLED)
        cv2.circle(img, (cx,cy), 10, (255,0,255),cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2), (255,0,255),3)

        length = math.hypot(x1-x2, y1-y2)
        # print(length)
        # hand range 35 - 300
        #volume range -74 - 0
        vol_scalar = np.interp(length, [30,290], [0.0, 1.0])
        # vol = np.interp(volPer,[0,100],[minRange, maxRange])
        # print(vol)
        smooth_vol = 0.3 * vol_scalar + (1 - 0.3) * smooth_vol
        volume.SetMasterVolumeLevelScalar(smooth_vol, None)

        if length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'fps: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3 )
    # cv2.imshow("img", img)
    cv2.waitKey(1)