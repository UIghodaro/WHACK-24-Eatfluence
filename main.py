# python3 -m venv venv
# venv\Script\Activate
# python3 -m pip install -r requirements.txt
# python3 main.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)