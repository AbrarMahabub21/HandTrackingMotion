# HandTrackingMotion

Real time hand tracking from a webcam using MediaPipe and OpenCV. MediaPipe finds 21 landmarks on each hand (finger joints and tips, plus the wrist), and I wrapped that into a small reusable module. I then used the module to control the system volume by pinching my thumb and index finger.

## Files

- `HandTrackingMin.py`: the bare minimum version. Reads webcam frames, runs MediaPipe Hands, draws the landmarks, prints each landmark's pixel position and shows the FPS.
- `HandTrackingModule.py`: the same idea as a reusable `handDetector` class.
  - `findHands(img, draw=True)` detects hands and optionally draws the landmarks and connections.
  - `findPosition(img, handNo=0)` returns a list of `[id, x, y]` pixel positions for the 21 landmarks of one hand.
  - Options for max hands and detection/tracking confidence.
- `usingModule.py`: a short example of importing and using the module.
- `volumeController.py`: gesture volume control. It measures the distance between the thumb tip (landmark 4) and index finger tip (landmark 8), maps it to a volume level from 0 to 1, smooths it so the volume doesn't jump around, and sets the system volume with pycaw. The midpoint circle turns green when the fingers are close together.
- `setup.py`: packages the module as `my_htm` so it can be installed with pip.

## Tech

Python, OpenCV, MediaPipe, NumPy, pycaw

## Running it

```bash
pip install mediapipe opencv-python numpy
python HandTrackingMin.py
# or
python HandTrackingModule.py
```

To install the module as a package:

```bash
pip install .
```

For the volume controller (Windows only, because pycaw uses the Windows audio API):

```bash
pip install pycaw
python volumeController.py
```

## Limitations

- The scripts run in an endless loop, so stop them with Ctrl+C.
- `volumeController.py` has its preview window (`cv2.imshow`) commented out, so it runs without showing the camera feed.
- The volume mapping uses a fixed finger distance range in pixels, so it depends on how far your hand is from the camera.
- It uses MediaPipe's older `mp.solutions.hands` API.
