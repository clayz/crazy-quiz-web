from flask import Blueprint
from flask import jsonify
from entity.account import Account


account_api = Blueprint('account', __name__, url_prefix='/api/account')


@account_api.route('/')
def index():
    from main import app

    account = Account(name='Clay Zhong', email='zjclay@gmail.com')
    key = account.put()
    app.logger.debug(key)

    return 'User API'


@account_api.route('/get/')
def get():
    return jsonify(username='Clay Zhong',
                   email='zjclay@gmail.com',
                   role=['Admin', 'Engineer'])
