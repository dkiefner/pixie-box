from flask import Flask, render_template, send_file, request

from lib.file_system import FileSystem
from lib.shutdown import Shutdown
from lib.zip import Zip

app = Flask(__name__)
app.config["UPLOAD_DIR"] = FileSystem.UPLOAD_DIR


# css style from: https://moderncss.dev/custom-select-styles-with-pure-css/
@app.route('/')
def index():
    return render_template('index.html', rfids=["one", "two"])


@app.route('/backup', methods=["GET", "POST"])
def backup():
    if request.method == 'POST':
        file = request.files['backup']
        file_path = FileSystem.save(file, app.config['UPLOAD_DIR'])
        Zip.unzip(file_path, FileSystem.DATA_DIR)
        FileSystem.delete_content(FileSystem.UPLOAD_DIR)

        return render_template("backup.html", msg="Backup successfully restored.")
    return render_template("backup.html", msg="")


# https://code-maven.com/flask-upload-multiple-files

# CTA endpoints

@app.route('/shutdown_system')
def shutdown_system():
    Shutdown.halt()


@app.route('/export_backup')
def export_backup():
    backup_file_path = Zip.create_from_directory(FileSystem.DATA_DIR, f"{FileSystem.TEMP_DIR}/pixiebox-backup")
    return send_file(backup_file_path, as_attachment=True)
