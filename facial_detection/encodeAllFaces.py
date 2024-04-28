import face_recognition
import os



directory = os.fsencode("./knownPeople")

knownFaces = {}

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	username = filename.split(".")[0]
	print(username)
	workingFaceFile = face_recognition.load_image_file((directory.decode("UTF-8"))+"/"+filename)
	knownFaces[username] = face_recognition.face_encodings(workingFaceFile)[0]
