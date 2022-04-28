from flask import Blueprint, Response

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def hello_world() -> Response:
    return 'Hello, World!'


@bp.route('/upload-file-request', methods=['POST'])
def upload_file_request (request) -> Response:
    request_body = request.data
    """Request a upload process.
    Args:
        name (str)
        decription (str)
      
    Return:
        process_id (str)
    
    do create process
    """
    pass
@bp.route('/file-transport', method=['Post'])
def transport_file():
    """ transport file
    Args:
        process_id(str)
        file(byte)
    Return:
    do process.write_file()
    """

@bp.route('/check-progress', methods=['POST'])
def check_progress(request) -> Response:
    """ comfirm request
    Args:
        process_id(str)
        activate(boolean)
    Return:

    do put process into process queue
    """