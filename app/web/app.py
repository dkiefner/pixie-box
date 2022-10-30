from flask import Flask, render_template, send_file

from lib.file_system import FileSystem
from lib.shutdown import Shutdown
from lib.zip import Zip

app = Flask(__name__)


# css style from: https://moderncss.dev/custom-select-styles-with-pure-css/
@app.route('/')
def index():
    return render_template('index.html', rfids=["one", "two"])


@app.route('/backup')
def backup():
    return render_template('backup.html')


# https://code-maven.com/flask-upload-multiple-files

# CTA endpoints

@app.route('/shutdown_system')
def shutdown_system():
    Shutdown.halt()


@app.route('/export_backup')
def export_backup():
    backup_file_path = Zip.create_from_directory(FileSystem.DATA_DIR, f"{FileSystem.TEMP_DIR}/pixiebox-backup")
    return send_file(backup_file_path, as_attachment=True)
