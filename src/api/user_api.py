from batch.notification import GCMSender
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
    uuid, device, version = form.uuid.data, form.device.data, form.version.data,
    app.logger.info("App startup, UUID: %s" % uuid)

    user = User.get_by_id(uuid)
    if not user:
        user = User(id=uuid, device=Device.lookup_by_number(device))
        user.put()
        app.logger.info("Created new user: %s" % user)

    startup_history = StartupHistory(parent=user.key, version=version, ip=request.remote_addr)
    startup_history.put()

    GCMSender('a').push()

    return response()


@user_api.route('/register/', methods=['POST'])
def register():
    from main import app

    form = get_form(RegisterForm(request.form))
    user = User.get(form.uuid.data)
    if user.status == UserStatus.ACTIVE:
        raise DataError(APIStatus.DATA_SAVE_FAILED, 'User already registered: %s' % user)

    app.logger.info("User register, UUID: %s" % user.key)
    user.name = form.name.data
    user.status = UserStatus.ACTIVE
    user.put()

    currency = Currency(parent=user.key, gem=DEFAULT_GEM, coin=DEFAULT_COIN)
    currency.put()

    return response()


@user_api.route('/notification/', methods=['POST'])
def register_notification():
    form = get_form(PushNotificationForm(request.form))
    user = User.get(form.uuid.data)
    user.push_token = form.push_token.data
    user.put()

    return response()


class StartupForm(BaseForm):
    version = StringField('version', [validators.length(min=3, max=5)])
    device = IntegerField('device', [validators.number_range(min=0, max=3)])


class RegisterForm(BaseForm):
    name = StringField('name', [validators.optional(), validators.length(min=1, max=8)])


class PushNotificationForm(BaseForm):
    push_token = StringField('push_token', [validators.required(), validators.length(max=500)])