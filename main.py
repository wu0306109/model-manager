import os
from typing import NoReturn

from model_manager import create_app


def main() -> NoReturn:
    app = create_app()
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', '8080')))


if __name__ == '__main__':
    main()
