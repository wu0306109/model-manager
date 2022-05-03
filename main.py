import os
from typing import NoReturn

import firebase_admin
from firebase_admin import credentials

from model_manager import create_app

cred = credentials.Certificate(
    'secrets/model-manager-349101-firebase-adminsdk-pzrld-ca1a04e3a6.json')
firebase_admin.initialize_app(cred)

app = create_app()


def main() -> NoReturn:
    app.run(debug=True, host='0.0.0.0', port='8080')


if __name__ == '__main__':
    main()
