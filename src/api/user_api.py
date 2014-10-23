from google.appengine.ext import ndb
from flask import Blueprint, request
from wtforms import Form, StringField, IntegerField, validators
from entities.user import User, StartupHistory
from entities.currency import Currency
from constants import Device, DEFAULT_GEM, DEFAULT_COIN
from utilities import json_response
from errors import ParameterError

user_api = Blueprint('user', __name__, url_prefix='/api/user')


class StartupForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=500)])
    name = StringField('name', [validators.Optional(), validators.Length(min=1, max=8)])
    version = StringField('version', [validators.Length(min=3, max=5)])
    device = IntegerField('device', [validators.NumberRange(min=0, max=3)])


@user_api.route('/startup/', methods=['POST'])
def startup():
    from main import app

    form = StartupForm(request.form)
    if not form.validate():
        raise ParameterError(form.errors.items())

    uuid, name, version, device = form.uuid.data, form.name.data or None, form.version.data, form.device.data
    app.logger.info("User startup, name: %s, device: %d, UUID: %s" % (name, device, uuid))

    user = User.get_by_id(uuid) or create_user(uuid, name, Device.lookup_by_number(device))
    startup_history = StartupHistory(parent=user.key, version=version, ip=request.remote_addr)
    startup_history.put()

    return json_response()


@ndb.transactional()
def create_user(uuid, name, device):
    from main import app

    user = User(id=uuid, name=name, device=device)
    user.put()
    app.logger.info("Created new user: %s" % user)

    currency = Currency(parent=user.key, coin=DEFAULT_COIN, gem=DEFAULT_GEM)
    currency.put()
    app.logger.debug("Created currency: %s" % currency)

    return user