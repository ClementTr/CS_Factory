from flask import Flask, render_template, session, request, redirect, jsonify
import time

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    success = 1
    return render_template('index.html', success=success)


@app.route('/api', methods=['GET', 'POST'])
def comptor():
    jsonResp = {'jack': 4098, 'sape': 4139}
    return jsonify(jsonResp)


if __name__ == '__main__':
    app.run(debug=True)
