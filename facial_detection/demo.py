import face_recognition
import cv2
import numpy as np
import os, json, datetime

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

dir = "facial_detection/knownPeople/"

def load_faces(dir):
    encodings = []
    names = []
    for file in os.listdir(dir):
        if file.split(".")[-1] == "json":
            f = open(dir + file)
            data = f.read()
            f.close()
            obj = json.loads(data)
            for enc in obj["encodings"]:
                encodings.append(np.array(enc))
                names.append(obj["name"])
    return encodings, names

face_encodings, face_names = load_faces(dir)


# Create arrays of known face encodings and their names
# known_face_encodings = []
# known_face_names = []

# Initialize some variables
face_locations = []
process_this_frame = True

def is_whole_list_false(lst):
    for item in lst:
        if item != False: 
            return False
    return True

def build_new_face(face_encoding, face_image):
    print("No face encodings enter name for face")
    name = input("name: ")
    if name == "q": return
    if not (name + ".json" in os.listdir(dir)):
        relation = input("relation: ")
        face_encodings.append(face_encoding)
        face_names.append(name)
        print(name)
        cv2.imwrite(dir + name + ".jpg", face_image)
        f = open(dir + name + ".json", "w")
        f.write(json.dumps({
            "name": name,
            "image": name + ".jpg",
            "relation": relation,
            "firstSeen": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "lastSeen": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "encodings": [face_encoding.tolist()],
        }))
        f.close()

while True:

    # Grab a single frame of video
    ret, frame = video_capture.read()

    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    # frame = frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(frame)
    image_face_encodings = face_recognition.face_encodings(frame, face_locations)

    # results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    faces = []
    for floc in face_locations:
        x2 = floc[1]
        x1 = floc[3]
        y2 = floc[2]
        y1 = floc[0]
        # print(floc)
        padding = 0
        faces.append(frame[y1 - padding:y2 + padding, x1 - padding:x2 + padding])
        # frame = cv2.circle(frame, (x1, y1), 10, (0, 255, 0))
        # frame = cv2.circle(frame, (x2, y2), 10, (255, 0, 0))

    indx = -1
    for face in faces:
        indx +=1
        face_encoding_success = False
        try:
            face_encoding = image_face_encodings[indx]
            face_encoding_success = True
        except:
            pass
        if face_encoding_success:
            result = face_recognition.compare_faces(face_encodings, face_encoding)
            is_false = False
            best_guess = -1
            if face_encodings == []:
                build_new_face(face_encoding, face)
            else:
                best_guess = np.argmax(result)
                is_false = is_whole_list_false(result)

            if is_false:
                build_new_face(face_encoding, face)
            else:
                if best_guess >= 0:
                    print(face_names[best_guess])            

        else:
            print("ERROR")
        # print(face.size)
        cv2.imshow(str(indx), face)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
    cv2.imshow('Video', frame)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()