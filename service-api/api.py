from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Service B is running!", 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5555)