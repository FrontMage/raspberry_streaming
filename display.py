import cv2

cap = cv2.VideoCapture('./fifo264')

COLLECT_DIR = './collect'

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    cv2.imshow('frame', frame)

    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
