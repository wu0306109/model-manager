import os

import google.cloud.logging
from flask import Flask
from model_manager.model_manager import model_manager

app = Flask(__name__)
app.register_blueprint(model_manager, url_prefix='/manager')

# Retrieves a Cloud Loggin handler and intergrates with Python loggin module
client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()


@app.route('/')
def hellow_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', '8080')))
