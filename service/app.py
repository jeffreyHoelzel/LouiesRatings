from flask import Flask, jsonify
from flask_cors import CORS

# For testing only


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def hello():
    return jsonify(message="Hello from the backend!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
