import cv2
import mediapipe as mp
import time
import threading
import tkinter as tk
from tkinter import messagebox

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

running = False
photo_count = 0
countdown_started = False
captured = False
countdown_start_time = None
frame_to_save = None

def open_camera():
    global running, photo_count, countdown_started, captured, countdown_start_time, frame_to_save
    running = True

    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        finger_open = 0

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                finger_tips = [8, 12, 16, 20]
                thumb_tip = 4

                hand_label = handedness.classification[0].label

                if hand_label == 'Right':
                    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
                        finger_open += 1
                else:  
                    if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_tip - 1].x:
                        finger_open += 1

                for tip in finger_tips:
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        finger_open += 1

        if finger_open == 5 and not countdown_started:
            countdown_started = True
            captured = False
            countdown_start_time = time.time()
            frame_to_save = frame.copy()
            print("Countdown started!")

        if countdown_started:
            elapsed = time.time() - countdown_start_time
            countdown_sec = 3 - int(elapsed)
            if countdown_sec > 0:
                cv2.putText(frame, f"Capturing in {countdown_sec}s", (30, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA)
                frame_to_save = frame.copy()
            else:
                if not captured:
                    photo_count += 1
                    filename = f"palm_photo_{photo_count}.jpg"
                    cv2.imwrite(filename, frame_to_save)
                    print(f"✅ Photo saved as {filename}")
                    messagebox.showinfo("Success", f"Photo saved as {filename}")
                    captured = True
                    countdown_started = False

        cv2.imshow("Palm Gesture Camera", frame)

        if cv2.waitKey(1) & 0xFF == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()

def start_camera():
    threading.Thread(target=open_camera, daemon=True).start()

def stop_camera():
    global running
    running = False
    messagebox.showinfo("Info", "Camera closed")

root = tk.Tk()
root.title("Palm Gesture Photo App")
root.geometry("300x150")

tk.Label(root, text="Palm Gesture Photo Capture", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Open Camera", command=start_camera).pack(pady=5)
tk.Button(root, text="Close Camera", command=stop_camera).pack(pady=5)

root.mainloop()
