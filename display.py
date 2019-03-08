import os
import pickle
import time

import face_recognition
import numpy as np

import cv2

cap = cv2.VideoCapture('./fifo264')

KNOWN_FACES_DIR = './known_faces'
KNOWN_FACES = os.listdir(KNOWN_FACES_DIR)

KNOWN_FACES_ENCODINGS = './known_face_encodings.dat'
KNOWN_FACES_NAMES = 'known_face_names.dat'

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

if os.path.isfile(KNOWN_FACES_ENCODINGS) and os.path.isfile(KNOWN_FACES_NAMES):
    with open(KNOWN_FACES_ENCODINGS, 'rb') as f:
      known_face_encodings = pickle.load(f)
    with open(KNOWN_FACES_NAMES, 'rb') as f:
      known_face_names = pickle.load(f)
else:
    for name in KNOWN_FACES:
        path = os.path.join(KNOWN_FACES_DIR, name)
        faces = os.listdir(path)
        for f in faces:
            image = face_recognition.load_image_file(os.path.join(path, f))
            face_encodings = face_recognition.face_encodings(image, num_jitters=100)
            for face_encoding in face_encodings:
                known_face_encodings.append(face_encoding)
                known_face_names.append(name)

    with open(KNOWN_FACES_ENCODINGS, 'wb') as f:
        pickle.dump(known_face_encodings, f)
    with open(KNOWN_FACES_NAMES, 'wb') as f:
        pickle.dump(known_face_names, f)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while cap.isOpened():
    ret, frame = cap.read()

    frame = cv2.flip(frame, -1)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.3)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        width = int((right - left)/4)
        height = int((top - bottom)/4)
        line_color = (28, 99, 44)
        alpha = 0.6
        overlay = frame.copy()
        cv2.line(overlay, (left, top), (left + width, top), line_color, 2)
        cv2.line(overlay, (left, top), (left, top - height), line_color, 2)
        cv2.line(overlay, (left, bottom), (left, bottom + height), line_color, 2)
        cv2.line(overlay, (left, bottom), (left + width, bottom), line_color, 2)

        cv2.line(overlay, (right, top), (right - width, top), line_color, 2)
        cv2.line(overlay, (right, top), (right, top - height), line_color, 2)
        cv2.line(overlay, (right, bottom), (right, bottom + height), line_color, 2)
        cv2.line(overlay, (right, bottom), (right - width, bottom), line_color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(overlay, (left - 1, bottom + 38), (right + 1, bottom), line_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(overlay, name, (left + 6, bottom + 26), font, 1.0, (255, 255, 255), 1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.imshow('frame', frame)
    if not ret:
        print(ret)
        break
    # if cv2.waitKey(1) & 0xFF == ord('c'):
    #     cv2.imwrite('./{}.jpg'.format(time.time()), cv2.flip(frame, -1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
