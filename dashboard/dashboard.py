from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        with open('logs.json', 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
