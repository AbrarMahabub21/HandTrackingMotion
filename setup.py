from setuptools import setup

setup(
    name='my_htm',
    version='0.1',
    py_modules=['HandTrackingModule'], # This must match your filename
    install_requires=[
        'mediapipe',
        'opencv-python',
    ],
)
