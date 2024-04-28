from flask import Flask, render_template, request
app = Flask(__name__)

newPerson = False
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
		currentPerson = request.args["name"]
		with open("static/knownPeople/"+currentPerson+".json") as personData
			currentPerson = personData
		newPerson = True
		return "True"
	except Exception as e:
		print(e)
		#error
		return "False"

@app.route("/")

def main():
	return render_template('index.html')

app.run(host="0.0.0.0")
