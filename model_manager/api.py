from flask import Blueprint, Response

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def hello_world() -> Response:
    return 'Hello, World!'


@bp.route('/request-upload', methods=['POST'])
def request_upload() -> Response:
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
@bp.route('/file-transport', method=['Post'])
def transport_file():
    """ transport file
    Args:
        process_id(str)
        file(byte)
    Return:
    do process.write_file()
    """


@bp.route('/check-progress')
def check_progress() -> Response:
    """
    Args:
        process_id(str)
    Return:
        progress(int)
    do process.get_progress
    """