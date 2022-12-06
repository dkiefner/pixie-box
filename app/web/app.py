from flask import Flask, render_template, send_file, request, redirect, url_for

from lib.command import SystemCommand
from lib.di import ServiceLocatorFactory, ServiceName
from lib.file_system import FileSystem
from lib.store import ServiceStateStore
from lib.system_info import SystemInfo
from lib.zip import Zip

app = Flask(__name__)

service_locator = ServiceLocatorFactory.create()

player = service_locator.get(ServiceName.Player)
service_state_store = service_locator.get(ServiceName.ServiceStateStore)
shutdown = service_locator.get(ServiceName.Shutdown)
system_tag_store = service_locator.get(ServiceName.SystemTagStore)
volume = service_locator.get(ServiceName.Volume)
sleep_timer = service_locator.get(ServiceName.SleepTimer)


# css style from: https://moderncss.dev/custom-select-styles-with-pure-css/
@app.route('/', methods=["GET", "POST"])
def index():
    message = ""
    if request.method == 'POST':
        is_sleep_timer_enabled = request.form.get("enable-sleep-timer") == "on"
        if is_sleep_timer_enabled:
            timeout_value = request.form.get("sleep-timer-timeout-in-minutes")
            sleep_timer_timeout_in_seconds = int(timeout_value) * 60
            sleep_timer.enable(sleep_timer_timeout_in_seconds)

            message = f"Sleep timer enabled with {timeout_value} minutes"
        else:
            if sleep_timer.is_enabled():
                message = f"Sleep timer disabled"
            sleep_timer.disable()

    sleep_timer_timeout_in_minutes = None
    if sleep_timer.get_timeout() is not None:
        sleep_timer_timeout_in_minutes = int(sleep_timer.get_timeout() / 60)

    return render_template('index.html', volume=volume.get(), msg=message,
                           sleep_timer_timeout=sleep_timer_timeout_in_minutes)


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

            # clear all old files for the given tag if requested
            rfid_path = FileSystem.path(FileSystem.RFID_BASE_DIR, tag)
            if request.form.get("overwrite"):
                FileSystem.delete_content(rfid_path)

            # create the tag directory if necessary
            FileSystem.create_path(rfid_path)

            # move all files from UPLOAD_DIR to new tag directory and clear everything in UPLOAD_DIR
            FileSystem.move(FileSystem.UPLOAD_DIR, str(rfid_path))
            FileSystem.delete_content(FileSystem.UPLOAD_DIR)

            # delete system tag if assigned previously
            system_tag_store.delete(tag)

            result_message = f"Adding audio content to RFID tag {tag} successful."

        tag = request.form.get("systemTag")
        if tag is not None:
            command = request.form.get("command")
            system_tag_store.save(tag, command)
            # delete audio tag if it was assigned previously
            FileSystem.delete_content(FileSystem.path(FileSystem.RFID_BASE_DIR, tag))

            result_message = f"Adding system command {command} to RFID tag {tag} successful."

    return render_template("assign_tag.html", msg=result_message,
                           system_commands=[SystemCommand.STOP, SystemCommand.VOLUME_UP, SystemCommand.VOLUME_DOWN,
                                            SystemCommand.SHUTDOWN, SystemCommand.NEXT, SystemCommand.PREVIOUS])


@app.route('/system_info')
def system_info():
    return render_template('system_info.html', gpu_temp=SystemInfo.gpu_temp(), cpu_temp=SystemInfo.cpu_temp(),
                           pixiebox_logs=SystemInfo.pixiebox_logs(), web_app_logs=SystemInfo.web_app_logs(),
                           sleep_timer_logs=SystemInfo.sleep_timer_logs())


# CTA endpoints

@app.route('/run_system_command')
def run_system_command():
    command = request.args['command']

    if command == SystemCommand.STOP.name:
        player.stop()
    elif command == SystemCommand.VOLUME_UP.name:
        volume.up()
        return redirect(url_for('index'))
    elif command == SystemCommand.VOLUME_DOWN.name:
        volume.down()
        return redirect(url_for('index'))
    elif command == SystemCommand.SHUTDOWN.name:
        shutdown.halt()
    elif command == SystemCommand.NEXT.name:
        player.next()
    elif command == SystemCommand.PREVIOUS.name:
        player.prev()
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

    last_scanned_rfid = service_state_store.get_string(ServiceStateStore.KEY_LAST_SCANNED_RFID)
    return last_scanned_rfid if last_scanned_rfid is not None else ""
