from flask import Blueprint

model_manager = Blueprint('website',
                          __name__,
                          static_folder='static',
                          template_folder='templates')


@model_manager.route('/')
def hello_world():
    return 'Hello World'


@model_manager.route('/request-upload')
def request_upload():
    """Request a upload process.

    Args:
        name (str)
        decription (str)

    Return:
        process_id (str)
    """
    pass


@model_manager.route('/upload')
def upload():
    """Upload a file.

    Args:
        process_id (str)
        file (File)
    
    Return:
        success (bool)
    """
    import requests
    requests.post('', params={}, files='')
    pass


@model_manager.route('/check-progress')
def check_progress():
    pass
