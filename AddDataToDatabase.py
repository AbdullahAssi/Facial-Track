import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

try:
    cred = credentials.Certificate(r'credentials.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://icat22-778f4-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
    print("Firebase initialization successful")
    
    ref = db.reference('students')

    data = {
        'F22607010': {
            "std_id" :'F22607010',
            "Name": "Muhammad Abdullah",
            "Major": "DSA",
            "batch": 2022,
            "Total Attendence": 6,
            "Attendance": False  
        },
        'F22607013': {
            "std_id" :'F22607013',
            "Name": "Sultan Mehmood",
            "Major": "DSA",
            "batch": 2022,
            "Total Attendence": 4,
            "Attendance": False
        },
        'F22607017': {
            "std_id" :'F22607017',
            "Name": "Zeeshan Abid",
            "Major": "DSA",
            "batch": 2022,
            "Total Attendence": 7,
            "Attendance": False
        },
            'F22607020': {
            "std_id" :'F22607020',
            "Name": "Moez Ahmad",
            "Major": "DSA",
            "batch": 2022,
            "Total Attendence": 7,
            "Attendance": False
        },
            'F22607038': {
            "std_id" :'F22607038',
            "Name": "Awais Liaqat",
            "Major": "DSA",
            "batch": 2022,
            "Total Attendence": 7,
            "Attendance": False
        },
                    'F22607050': {
            "std_id" :'F22607050',
            "Name": "Wahab Zai",
            "Major": "DSA",
            "batch": 2022,
            "Total Attendence": 7,
            "Attendance": False
        }
    }

    for key, value in data.items():
        ref.child(key).set(value)
        print(f"Added data for key {key}")
except Exception as e:
    print(f"Error: {e}")