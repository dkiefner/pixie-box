from flask import Flask, render_template, send_file, request

from lib.command import SystemCommand
from lib.file_system import FileSystem
from lib.player import LocalFilePlayer
from lib.shutdown import Shutdown
from lib.store import ServiceStateStore
from lib.zip import Zip

app = Flask(__name__)
app.config["UPLOAD_DIR"] = FileSystem.UPLOAD_DIR

serviceStateStore = ServiceStateStore()
player = LocalFilePlayer(serviceStateStore)


# css style from: https://moderncss.dev/custom-select-styles-with-pure-css/
@app.route('/')
def index():
    return render_template('index.html', volume=player.get_volume())


@app.route('/backup', methods=["GET", "POST"])
def backup():
    if request.method == 'POST':
        file = request.files['backup']
        file_path = FileSystem.save(file, app.config['UPLOAD_DIR'])
        Zip.unzip(file_path, FileSystem.DATA_DIR)
        FileSystem.delete_content(FileSystem.UPLOAD_DIR)

        return render_template("backup.html", msg="Backup successfully restored.")
    return render_template("backup.html", msg="")


@app.route('/assign_tag', methods=["GET", "POST"])
def assign_tag():
    if request.method == 'POST':
        for file in request.files.getlist('files'):
            FileSystem.save(file, app.config['UPLOAD_DIR'])

        FileSystem.delete_content(FileSystem.UPLOAD_DIR)

        return render_template("assign_tag.html", msg="Adding content to RFID tag successful.")
    return render_template("assign_tag.html", msg="",
                           system_commands=[SystemCommand.STOP, SystemCommand.VOLUME_UP, SystemCommand.VOLUME_DOWN])


# https://code-maven.com/flask-upload-multiple-files

# CTA endpoints

@app.route('/run_system_command')
def run_system_command():
    command = request.args['command']

    if command == SystemCommand.STOP.name:
        player.stop()
    elif command == SystemCommand.VOLUME_UP.name:
        player.volume_up()
    elif command == SystemCommand.VOLUME_DOWN.name:
        player.volume_down()
    elif command == SystemCommand.SHUTDOWN.name:
        Shutdown.halt()
    else:
        return '', 404

    return '', 204


@app.route('/export_backup')
def export_backup():
    backup_file_path = Zip.create_from_directory(FileSystem.DATA_DIR, f"{FileSystem.TEMP_DIR}/pixiebox-backup")
    return send_file(backup_file_path, as_attachment=True)
