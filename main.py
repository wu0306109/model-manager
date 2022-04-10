import os
from typing import NoReturn

import google.cloud.logging

from model_manager import create_app

# Retrieves a Cloud Loggin handler and intergrates with Python loggin module
client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', '8080')),
    )
