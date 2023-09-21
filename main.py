import cv2
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

try:
    # Initialize Firebase Admin SDK with your service account credentials
    cred = credentials.Certificate(r'credentials.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://icat22-778f4-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
except Exception as e:
    print("Firebase initialization failed:", e)

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
background_path = r'C:\Users\Hp\Desktop\FacialRecognition\resourses\background.png'
background_img = cv2.imread(background_path)

# Resize the background image to match the screen resolution (1280x720)
background_img = cv2.resize(background_img, (1280, 720))

# Specify the dimensions of the region where you want to display the webcam video
region_height = 670
region_width = 1280

# Load the encoding file
file = open('encodefile.p', 'rb')
encodinglistknownwithid = pickle.load(file)
file.close()
encodinglistknown, std_ids = encodinglistknownwithid
print(std_ids)

# Define a list to keep track of recognized student IDs
recognized_student_ids = []

# Load a pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    success, webcam_img = cap.read()

    # Resize the webcam image to match the region dimensions
    webcam_img = cv2.resize(webcam_img, (region_width, region_height))

    # Create a copy of the background image to overlay the webcam video on
    display_img = background_img.copy()

    # Replace the region below the navigation bar with the resized webcam video
    display_img[50:50 + region_height, 0:region_width] = webcam_img

    cv2.imshow("Face Attendance", display_img)

    # Face detection using OpenCV's face_cascade
    gray = cv2.cvtColor(webcam_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw a red rectangle around each detected face

    # Face recognition logic using face_recognition library (your existing code)
    imgs = cv2.resize(webcam_img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    faceCurframe = face_recognition.face_locations(imgs)
    encodeCurframe = face_recognition.face_encodings(imgs, faceCurframe)

    for i, (encodeFace, faceLoc) in enumerate(zip(encodeCurframe, faceCurframe)):
        matches = face_recognition.compare_faces(encodinglistknown, encodeFace)
        face_distance = face_recognition.face_distance(encodinglistknown, encodeFace)

        matchIndex = np.argmin(face_distance)

        if matches[matchIndex]:
            std_id = std_ids[matchIndex]

            # Check if this student ID has already been recognized in this session
            if std_id not in recognized_student_ids:
                # Mark attendance only if it's the first recognition in this session
                recognized_student_ids.append(std_id)

                # Check if attendance has already been marked for this student
                try:
                    ref = db.reference('students/' + std_id + '/Attendance')
                    current_attendance = ref.get()
                    if current_attendance is None or current_attendance == False:
                        # If there's no attendance data for this student or it's False, mark them as "Present"
                        ref.set(True)
                        print(f"Marked attendance as 'Present' for student with ID {std_id}")
                except Exception as e:
                    print(f"Error marking attendance for student {std_id}: {e}")

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                # Draw a rectangle around the recognized face using OpenCV
                cv2.rectangle(display_img, (x1 + 55, y1 + 162), (x2 + 55, y2 + 162), (0, 255, 0), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
