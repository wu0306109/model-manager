from flask import Blueprint, request,  Response
from model_manager.process import Process
from model_manager.process_manager import ProcessManager
bp = Blueprint('api', __name__, url_prefix='/api')
process_manager = ProcessManager('./temp')

@bp.route('/')
def hello_world() -> Response:
    return 'Hello, World!'


@bp.route('/upload-file-request', methods=['POST'])
def upload_file_request () -> Response:
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

    do put process into process queue
    """