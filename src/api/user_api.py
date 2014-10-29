from google.appengine.ext import ndb
from flask import Blueprint, request
from constants import DEFAULT_GEM, DEFAULT_COIN, Device, UserStatus, APIStatus
from utilities import response, get_form
from entities.user import User, StartupHistory
from entities.currency import Currency
from api import *
from errors import DataError

user_api = Blueprint('user', __name__, url_prefix='/api/user')


@user_api.route('/startup/', methods=['POST'])
def startup():
    from main import app

    form = get_form(StartupForm(request.form))
    uuid, name, device, version = form.uuid.data, form.name.data, form.device.data, form.version.data

    app.logger.info("App startup, uuid: %s" % uuid)
    user = User.get_by_id(uuid) or create_user(uuid, name, Device.lookup_by_number(device))

    if user.status == UserStatus.INACTIVE and name != '':
        user.name = name
        user.status = UserStatus.ACTIVE
        user.put()
        app.logger.info("Active user: %s" % user)

    startup_history = StartupHistory(parent=user.key, version=version, ip=request.remote_addr)
    startup_history.put()

    return response()


@user_api.route('/register/', methods=['POST'])
def register():
    from main import app

    form = get_form(RegisterForm(request.form))
    user = User.get(form.uuid.data)

    if user.status == UserStatus.ACTIVE:
        raise DataError(APIStatus.DATA_SAVE_FAILED, 'User already registered: %s' % user)

    app.logger.info("User register, uuid: %s" % user.key)
    user.name = form.name.data
    user.status = UserStatus.ACTIVE
    user.put()

    return response()


@user_api.route('/notification/', methods=['POST'])
def register_notification():
    from main import app

    form = get_form(PushNotificationForm(request.form))
    user, push_token = User.get(form.uuid.data), form.push_token.data

    if user.push_token != push_token:
        app.logger.info('Update push token, uuid: %s, push_token: %s' % user.key, push_token)
        user.push_token = push_token
        user.put()

    return response()


@ndb.transactional()
def create_user(uuid, name, device):
    from main import app

    user = User(id=uuid, name=name, device=device)
    user.put()
    app.logger.info("Created new user: %s" % user)

    currency = Currency(parent=user.key, gem=DEFAULT_GEM, coin=DEFAULT_COIN)
    currency.put()
    app.logger.debug("Created currency: %s" % currency)

    return user


class StartupForm(BaseForm):
    name = StringField('name', [validators.optional(), validators.length(min=1, max=8)])
    version = StringField('version', [validators.length(min=3, max=5)])
    device = IntegerField('device', [validators.number_range(min=0, max=3)])


class RegisterForm(BaseForm):
    name = StringField('name', [validators.optional(), validators.length(min=1, max=8)])


class PushNotificationForm(BaseForm):
    push_token = StringField('push_token', [validators.required(), validators.length(max=500)])