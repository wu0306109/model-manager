from flask import Blueprint, request, Response
from model_manager.process import Process

from flask import (Blueprint, Response, current_app, redirect, request,
                   send_from_directory, url_for)

from model_manager.process_manager import ProcessManager

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def hello_world() -> Response:
    return 'Hello, World!'


@bp.route('/upload-file-request', methods=['POST'])
def upload_file_request() -> Response:
    file_name = request.form.get("name")
    description = request.form.get("description")
    manager = ProcessManager()
    process_id = manager.upload_file_request(file_name, description)
    return process_id

@bp.route('/file-transport', methods=['Post'])
def transport_file():
    manager = ProcessManager()
    process_id = request.form.get("process_id")
    stream = request.stream
    result = manager.transport_file(process_id, stream)
    return result


@bp.route('/check-progress', methods=['POST'])
def check_progress() -> Response:
    manager = ProcessManager()
    process_id = request.form.get("process_id")
    progress = manager.check_progress(process_id)
    return progress


@bp.route('list-files')
def list_files() -> Response:
    pass


@bp.route('/files/<string:filename>')
def view_file(filename: str) -> Response:
    return redirect(url_for('.download_file', filename=filename))


@bp.route('/files/<string:filename>/detail')
def view_file_detail(filename: str) -> Response:
    pass


@bp.route('/files/<string:filename>/download')
def download_file(filename: str) -> Response:
    return send_from_directory(current_app.instance_path, filename)
