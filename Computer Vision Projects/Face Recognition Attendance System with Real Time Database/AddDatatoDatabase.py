import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# Get database link
# Use your api key from firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': ""
})

ref = db.reference('Students')

# users data
data = {
    "321654":
        {
            "name": "Abdullah Wagih",
            "major": "Medical Informatics",
            "starting_year": 2019,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

# send data to database
for key, value in data.items():
    ref.child(key).set(value)