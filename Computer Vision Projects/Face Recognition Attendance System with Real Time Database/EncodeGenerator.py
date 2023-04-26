import os
import cv2
import pickle
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

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)

imgList = []
studentIds = []

# store users images and ids in database
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(path.split('.')[0])

    # store files in database
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

# Define function for image encoding
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

# Image Encoding
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encoded images in a file
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("File Saved")


