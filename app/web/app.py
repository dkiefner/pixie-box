from flask import Flask, render_template

app = Flask(__name__)

# css style from: https://moderncss.dev/custom-select-styles-with-pure-css/
@app.route('/')
def index():
    return render_template('index.html', rfids=["one", "two"])


@app.route('/shutdown_system')
def shutdown_system():
    print("shutdown system")
    return "nothing"
