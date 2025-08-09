# Palm Gesture Photo Capture App

A Python application that uses hand gesture recognition to capture photos with a webcam. The app detects an open palm (five fingers) using Mediapipe and OpenCV, then starts a visible 3-second countdown timer before automatically clicking and saving a photo. The countdown continues even if the hand is removed from the frame.

## Features

- Detects both left and right hands accurately.
- Real-time video feed with hand landmark visualization.
- 3-second countdown timer displayed on the video feed when a palm is detected.
- Automatic photo capture after countdown.
- Simple Tkinter GUI with buttons to open and close the webcam.
- Photos saved locally with incremental filenames.

## Technologies Used

- Python 3
- OpenCV
- Mediapipe
- Tkinter

## Installation

Make sure you have Python installed. Then install the required packages:

```bash
pip install opencv-python mediapipe
