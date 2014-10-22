from datetime import datetime
from flask import Blueprint, request
from google.appengine.ext import ndb
from wtforms import Form, StringField, IntegerField, validators
from constants import APIStatus
from entities import User, LoginHistory
from utilities import json_response

user_api = Blueprint('user', __name__, url_prefix='/api/user')


class StartupForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=500)])
    name = StringField('name', [validators.Optional(), validators.Length(min=1, max=8)])
    version = StringField('version', [validators.Length(min=3, max=5)])
    device = IntegerField('device', [validators.NumberRange(min=0, max=3)])


@ndb.transactional()
@user_api.route('/startup/', methods=['POST'])
def register():
    from main import app

    form = StartupForm(request.form)
    if not form.validate():
        return json_response(APIStatus.PARAMETER_ERROR)

    uuid = form.uuid.data
    name = form.name.data
    version = form.version.data
    device = form.device.data

    app.logger.debug("User startup, name: %s, device: %d, UUID: %s" % (name, device, uuid))
    user = User.get_by_id(uuid)

    if user:
        # handle user startup history
        login_history = LoginHistory.get_today(user.key)
        app.logger.debug("login_history: %s" % login_history)
    else:
        # create new user and all related data
        user = User(id=uuid, name=name, device=device)
        user.put()
        app.logger.info("Created new user: %s" % user)

        login_history = LoginHistory(parent=user.key, version=version, ip=[request.remote_addr], startup_time=[datetime.now()])
        login_history.put()
        app.logger.debug("Created login history: %s" % login_history)

    return json_response()