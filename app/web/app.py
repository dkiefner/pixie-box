from flask import Flask, render_template, send_file, request

from lib.command import SystemCommand
from lib.file_system import FileSystem
from lib.player import LocalFilePlayer
from lib.shutdown import Shutdown
from lib.store import ServiceStateStore, SystemTagStore
from lib.zip import Zip

app = Flask(__name__)

serviceStateStore = ServiceStateStore()
systemTagStore = SystemTagStore()
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
    result_message = ''

    if request.method == 'POST':
        tag = request.form.get("audioTag")
        if tag is not None:
            # move all files into the UPLOAD_DIR
            for file in request.files.getlist('files'):
                FileSystem.save(file, FileSystem.UPLOAD_DIR)

            # clear all old files for the given tag or create the tag directory if necessary
            rfid_path = FileSystem.path(FileSystem.RFID_BASE_DIR, tag)
            FileSystem.delete_content(rfid_path)
            FileSystem.create_path(rfid_path)

            # move all files from UPLOAD_DIR to new tag directory and clear everything in UPLOAD_DIR
            FileSystem.move(FileSystem.UPLOAD_DIR, str(rfid_path))
            FileSystem.delete_content(FileSystem.UPLOAD_DIR)

            result_message = f"Adding audio content to RFID tag {tag} successful."

        tag = request.form.get("systemTag")
        if tag is not None:
            command = request.form.get("command")
            systemTagStore.save(tag, command)

            result_message = f"Adding system command {command} to RFID tag {tag} successful."

    return render_template("assign_tag.html", msg=result_message,
                           system_commands=[SystemCommand.STOP, SystemCommand.VOLUME_UP, SystemCommand.VOLUME_DOWN])


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


@app.route('/last_scanned_tag')
def last_scanned_tag():
    if player.is_playing():
        player.stop()

    last_scanned_rfid = serviceStateStore.get(ServiceStateStore.KEY_LAST_SCANNED_RFID)
    return last_scanned_rfid if last_scanned_rfid is not None else ""
