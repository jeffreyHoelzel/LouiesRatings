from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# For testing only


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/', methods=['GET', 'POST'])
def send_message():
    message = ''
    # check if form is for post request
    if request.method == 'POST':
        # get message from user with name = demo in home.html
        message = request.form.get('demo')
        # modify message
        message = f'We got your message: "{message}".'
    # render new home.HTML page with modified message
    return render_template('home.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
