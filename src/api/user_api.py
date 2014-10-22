from flask import Blueprint, request
from google.appengine.ext import ndb
from entities import User, UserStatus
from utilities import json_response

user_api = Blueprint('user', __name__, url_prefix='/api/user')


@ndb.transactional()
@user_api.route('/register/', methods=['POST'])
def register():
    from main import app

    uuid = request.form['uuid']
    device = int(request.form['device'])
    app.logger.debug("User register, device: %d, UUID: %s" % (device, uuid))
    user = User.get_by_id(uuid)

    if user:
        if user.status is UserStatus.ACTIVE:
            app.logger.debug("User already exists: %s" % user)
        elif user.status is UserStatus.UNINSTALL:
            app.logger.debug("User reinstall: %s" % user)
            user.status = UserStatus.REINSTALL
            user.put()
    else:
        user = User(id=uuid, name='Clay Zhong')
        user.put()
        app.logger.info("Created new user: %s" % user)

    return json_response()