import cv2
import dlib
import time

# landmarks from shape_predictor_68_face_landmarks.dat
path = 'shape_predictor_68_face_landmarks.dat'

# face detection
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(path)

# Active camera
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    # Get current time
    current_time = str(time.ctime())
    cv2.putText(frame, current_time, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray_frame)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        # show landmarks
        landmarks = predictor(gray_frame, face)
        for lm in range(68):
            x = landmarks.part(lm).x
            y = landmarks.part(lm).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # horizontal flipping
    img = cv2.flip(frame, 1)

    cv2.imshow('Live', img)
    if cv2.waitKey(1) == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()