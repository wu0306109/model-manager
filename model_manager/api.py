from flask import (Blueprint, Response, current_app, redirect, request,
                   send_from_directory, url_for)

from . import file_manager

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def hello_world() -> Response:
    return 'Hello, World!'


@bp.route('/upload-file-request', methods=['POST'])
def upload_file_request() -> Response:
    file_name = request.form.get("name")
    description = request.form("description")
    """Request a upload process.
    Args:
        name (str)
        decription (str)
      
    Return:
        process_id (str)
    
    do create process
    """
    pass


@bp.route('/comfirm-request', methods=['POST'])
def comfirm_request() -> Response:
    """ comfirm request
    Args:
        process_id(str)
        activate(boolean)
    Return:

    do put process into process queue
    """


@bp.route('/file-transport', methods=['Post'])
def transport_file():
    """ transport file
    Args:
        process_id(str)
        file(byte)
    Return:
    do process.write_file()
    """


@bp.route('/check-progress', methods=['POST'])
def check_progress() -> Response:
    """ comfirm request
    Args:
        process_id(str)
        activate(boolean)
    Return:
        progress(int)
    do process.get_progress
    """


@bp.route('list-files')
def list_files() -> Response:
    return {
        file.name: {
            'type': file.type,
            'description': file.description,
            'path': file.path,
            'uploader': file.uploader,
            'upload_time': file.upload_time.timestamp(),
            'last_used_time': file.last_used_time.timestamp(),
        }
        for file in file_manager.files
    }


@bp.route('/files/<string:filename>')
def view_file(filename: str) -> Response:
    return redirect(url_for('.download_file', filename=filename))


@bp.route('/files/<string:filename>/detail')
def view_file_detail(filename: str) -> Response:
    pass


@bp.route('/files/<string:filename>/download')
def download_file(filename: str) -> Response:
    return send_from_directory(current_app.instance_path, filename)
