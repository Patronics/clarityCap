import face_recognition
import cv2
import numpy as np
import os



directory = os.fsencode("./knownPeople")

knownFaces = {}


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
for file in os.listdir(directory):
        filename = os.fsdecode(file)
        username = filename.split(".")[0]
        print(username)
        workingFaceFile = face_recognition.load_image_file((directory.decode("UTF-8"))+"/"+filename)
        knownFaces[username] = face_recognition.face_encodings(workingFaceFile)[0]




# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    face_locations = face_recognition.face_locations(frame)

    # unknown_encoding = face_recognition.face_encodings(frame)[0]
    # results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    faces = []
    for floc in face_locations:
        print(floc)
        # faces.append(frame[floc[0]:floc[0]-floc[2], floc[1]:floc[1]-floc[3]])
        frame = cv2.circle(frame, (floc[1], floc[2]), 10, (0, 255, 0))
        frame = cv2.circle(frame, (floc[0], floc[3]), 10, (0, 255, 0))

    unknown_face_encodings = face_recognition.face_encodings(frame)

    for subject in unknown_face_encodings:
       for refName, ref in knownFaces.items():
           if(face_recognition.compare_faces([subject],ref)):
              print("saw"+refName)
    # for face in faces:
    #     print(face.size)
    #     cv2.imshow('Video', face)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
    cv2.imshow('Video', frame)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
