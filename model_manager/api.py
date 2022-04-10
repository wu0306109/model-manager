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
    """
    pass


@bp.route('/upload', methods=['POST'])
def upload() -> Response:
    """Upload a file.

    Args:
        process_id (str)
        file (File)
    
    Return:
        success (bool)
    """
    pass


@bp.route('/check-progress')
def check_progress() -> Response:
    pass