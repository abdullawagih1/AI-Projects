import os
import cv2
import cvzone
import pickle
import numpy as np
from datetime import datetime
import face_recognition
import firebase_admin
from firebase_admin import db
from firebase_admin import  storage
from firebase_admin import credentials

# Get database links
# Use your api key from firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})

bucket = storage.bucket()

# Active camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# get background
imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load the encoding file
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

# create parameters for system pages
modeType = 0    # detect mode [active - main page - marked - already marked]
counter = 0     # increase counter to change mode
id = -1
imgStudent = []

# Detect camera
while True:
    success, img = cap.read()
    # Horizontal flipping
    img = cv2.flip(img, 1)
    # resize image for simplicity
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # convert image from bgr to rgb
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # get face locations and encode image
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # edit image in background
    imgBackground[162 : 162+480, 55 : 55+640] = img
    imgBackground[44 : 44+633, 808 : 808+414] = imgModeList[modeType]

    # Compare real image with image in database
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # compare faces
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            # get difference between faces
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            # get matching index
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])

                # get bounding box
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                # create bounding box
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                # get user id
                id = studentIds[matchIndex]

                # if the user
                if counter == 0:
                    counter = 1
                    modeType = 1

            if counter != 0:
                if counter == 1:
                    # Get the Data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)

                    # Get the Image from the storage (image can be in .jpg or .png format)
                    try:
                        blob = bucket.get_blob(f'Images/{id}.jpg')
                    except:
                        blob = bucket.get_blob(f'Images/{id}.png')

                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    imgStudent = cv2.resize(imgStudent, (216, 216))

                    # Update data of attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                    # Update after 12 hours
                    if secondsElapsed > 60 * 60 * 12:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:

                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

    # Show results
    cv2.imshow('Live', imgBackground)

    # # To exit from live, press Esc key
    if cv2.waitKey(1) & 0xFF == 27: # 27 is the Esc Key
        break

# release camera and close windows
cap.release()
cv2.destroyAllWindows()
