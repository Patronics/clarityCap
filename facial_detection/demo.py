import face_recognition
import cv2
import numpy as np

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
known_face_encodings = []
known_face_names = []

known_image = face_recognition.load_image_file("facial_detection/knownPeople/kyle.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
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
            if face_encodings == []:
                print("No face encodings enter name for face")
                name = input("name: ")
                print(name)
                face_encodings.append(face_encoding)
                face_names.append(name)
            else:
                best_guess = np.argmax(result)
                print(best_guess)

            print("found face")
            print(result)
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