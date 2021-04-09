from routes.home import main as mainHome
from routes.about import main as mainAbout
from routes.sentiment import main as mainSentiment
from flask import Flask, jsonify, request
import os


app = Flask(
    __name__,
    static_folder = 'templates/assets'
)


@app.route('/', methods=['GET'])
def home():
    return mainHome()

@app.route('/about', methods=['GET'])
def about():
    return mainAbout()

@app.route('/sentiment', methods=['POST'])
def sentiment():
    formData = request.form.to_dict()
    return mainSentiment(formData)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
