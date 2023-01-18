import cv2
import time

# load xml files
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Active camera
cap = cv2.VideoCapture(0)
while True:
    success, frame = cap.read()

    # Convert frame to grayscale
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face Detection
    faces = face_classifier.detectMultiScale(gray_img)     # tuning cascade classifiers
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

    if faces is ():    # When no faces detected
        print("No faces found")

    # horizontal flipping
    img = cv2.flip(frame, 1)

    # Get current time
    current_time = str(time.ctime())
    cv2.putText(img, current_time, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Live', img)

    # To exit from live, press Esc key
    if cv2.waitKey(1)& 0xFF == 27: #27 is the Esc Key
        break

# release camera and close windows
cap.release()
cv2.destroyAllWindows()