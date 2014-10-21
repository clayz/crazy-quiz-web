from flask import Blueprint, request, jsonify
from entities import User

user_api = Blueprint('user', __name__, url_prefix='/api/user')

# @user_api.route('/')
# def index():
# from main import app
#
# account = Account(name='Clay Zhong', email='zjclay@gmail.com')
# key = account.put()
# app.logger.debug(key)
#
# key = ndb.Key(urlsafe='ahJkZXZ-Y3JhenktcXVpei1kZXZyEQsSBFVzZXIYgICAgICAgAkM')
# app.logger.debug(key.id())
#
# return 'OK'


# @user_api.route('/get/')
# def get():
# return jsonify(username='Clay Zhong',
# email='zjclay@gmail.com',
# role=['Admin', 'Engineer'])


@user_api.route('/register/', methods=['POST'])
def register():
    from main import app

    uuid = request.form['uuid']
    device = int(request.form['device'])
    app.logger.debug("User register, device: %d, UUID: %s" % (device, uuid))

    # exist_user = User.get(uuid)
    # app.logger.debug(exist_user)

    return 'OK'