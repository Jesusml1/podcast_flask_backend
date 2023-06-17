from flask import Flask, jsonify

app = Flask(__name__)

if __name__ == 'main':
    app.run(debug=True, port=5000)

@app.route("/")
def ping():
    return jsonify({"message": "pong"})

@app.route("/login", methods=['POST'])
def login():
    return jsonify({"message": "login"})

@app.route("/upload/<varname>", methods=['POST'])
def uploadPodcast():
    return jsonify({"message": "login"})
# @app.route("/")
# def hello_world():
#     return "Hello, World!"