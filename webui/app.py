from flask import Flask, render_template, request
import json
app = Flask(__name__)

newPerson = False
global currentPerson 
currentPerson = {}
#currentPerson = ""
#currentImage = ""
#currentRelation = ""
#currentLastSeen = ""
#currentFirstSeen = ""


@app.route("/api/queryForUpdate")


def queryForUpdate():
	return str(newPerson)


@app.route("/api/showPersonInfo")

def showPersonInfo():
	try:
		with open("static/knownPeople/"+request.args["name"]+".json") as personData:
			global currentPerson
			currentPerson = json.load(personData)
		global newPerson
		newPerson = True
		return "True", 200
	except Exception as e:
		print(e)
		#error
		return "False", 400

@app.route("/")

def main():
	print("showing", end="")
	print(currentPerson)
	global newPerson
	newPerson = False
	return render_template('index.html', person = currentPerson)

app.run(host="0.0.0.0")
