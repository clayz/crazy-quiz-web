from flask import Blueprint, request
from google.appengine.ext import ndb
from wtforms import Form, StringField, IntegerField, validators
from constants import APIStatus
from entities import User, UserStatus
from utilities import json_response

user_api = Blueprint('user', __name__, url_prefix='/api/user')


class StartupForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=500)])
    name = StringField('name', [validators.Optional(), validators.Length(min=1, max=8)])
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
    device = form.device.data

    app.logger.debug("User register, device: %d, UUID: %s" % (device, uuid))
    user = User.get_by_id(uuid)

    if user and UserStatus.ACTIVE:
        app.logger.debug("User already exists: %s" % user)
    else:
        user = User(id=uuid, name=name, device=device)
        user.put()
        app.logger.info("Created new user: %s" % user)

    return json_response()