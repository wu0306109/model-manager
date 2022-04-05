from flask import Blueprint

model_manager = Blueprint('website',
                          __name__,
                          static_folder='static',
                          template_folder='templates')


@model_manager.route('/')
def hello_world():
    return 'Hello World'