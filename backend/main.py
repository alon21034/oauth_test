import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
	return "<h1>Hello Flask!</h1>"

@app.route('/registration', methods=['GET'])
def registration():
    return "registration"

@app.route('/validation', methods=['GET'])
def validation():
    return "token"

app.run()
