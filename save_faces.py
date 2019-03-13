import os
import pickle
import sys
import time

import face_recognition
import numpy as np

import cv2

cap = cv2.VideoCapture('./fifo264')

COLLECT_DIR = './collect'

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations)>0:
        cv2.imwrite(f'./{COLLECT_DIR}/{time.time()}.jpg', frame)

    if not ret:
        break

cap.release()
cv2.destroyAllWindows()
