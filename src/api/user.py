from flask import Blueprint

user_api = Blueprint('user', __name__, url_prefix='/api/user')


@user_api.route('/')
def index():
    return 'User API'