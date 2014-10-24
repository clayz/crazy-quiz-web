from flask import Blueprint, request
from google.appengine.ext import ndb
from utilities import json_response, get_form
from entities.user import User, StartupHistory
from entities.currency import Currency
from constants import Device, DEFAULT_GEM, DEFAULT_COIN
from api.forms import StartupForm

user_api = Blueprint('user', __name__, url_prefix='/api/user')


@user_api.route('/startup/', methods=['POST'])
def startup():
    from main import app

    form = get_form(StartupForm(request.form))
    uuid, name, version, device = form.uuid.data, form.name.data, form.version.data, form.device.data
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

    return user