import cv2
import os
import pickle
import face_recognition

# Importing students' images
folderpath = r'c:\Users\Hp\Desktop\FacialRecognition\images'  # Use a raw string to avoid escaping backslashes
pathlist = os.listdir(folderpath)
print(folderpath)
img_list = []
std_ids = []
for path in pathlist:
    img_list.append(cv2.imread(os.path.join(folderpath, path)))
    std_ids.append(os.path.splitext(path)[0])

# Print the std_ids list once after all images have been processed
print(std_ids)

def findencodings(img_list):
    encodinglist = []
    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodinglist.append(encode)
    
    print('Encoding started .....')
    print('Encoding Completed....')
    
    return encodinglist

encodinglistknown = findencodings(img_list)
encodinglistknownwithids = [encodinglistknown, std_ids]

file = open('encodefile.p', 'wb')
pickle.dump(encodinglistknownwithids, file)
file.close()
print('File Saved....')
