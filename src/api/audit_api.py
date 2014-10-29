from google.appengine.ext import ndb
from flask import Blueprint, request
from utilities import response, get_form, get_timestamp
from entities.user import User
from entities.audit import Purchase, Exchange, Earn, Consume
from api import *
from datetime import datetime

audit_api = Blueprint('audit', __name__, url_prefix='/api/audit')


@audit_api.route('/last/<string:uuid>/')
def last(uuid):
    from main import app

    user_key = ndb.Key(User, uuid)
    purchase = Purchase.get_last(user_key).fetch(1)
    exchange = Exchange.get_last(user_key).fetch(1)
    earn = Earn.get_last(user_key).fetch(1)
    consume = Consume.get_last(user_key).fetch(1)

    app.logger.info('[%s] Retrieve last purchase: %s' % (uuid, purchase))
    app.logger.info('[%s] Retrieve last exchange: %s' % (uuid, exchange))
    app.logger.info('[%s] Retrieve last earn: %s' % (uuid, earn))
    app.logger.info('[%s] Retrieve last consume: %s' % (uuid, consume))

    return response(purchase=get_timestamp(purchase[0].date) if purchase else None,
                    exchange=get_timestamp(exchange[0].date) if exchange else None,
                    earn=get_timestamp(earn[0].date) if earn else None,
                    consume=get_timestamp(consume[0].date) if consume else None)


@audit_api.route('/sync/', methods=['POST'])
def sync():
    from main import app

    data = request.json
    app.logger.info('data: %s' % data)

    if 'purchase' in data:
        app.logger.info('purchase: %s' % data['purchase'])

    if 'exchange' in data:
        app.logger.info('exchange: %s' % data['exchange'])

    if 'earn' in data:
        app.logger.info('earn: %s' % data['earn'])

    if 'consume' in data:
        app.logger.info('consume: %s' % data['consume'])

    return response()


@audit_api.route('/purchase/', methods=['POST'])
def save_purchase():
    from main import app

    form = get_form(PurchaseForm(request.form))
    uuid, goods_id, product_id = form.uuid.data, form.goods_id.data, form.product_id.data
    user = User.get(uuid)

    app.logger.info('[%s] Purchased goods_id: %d, product_id: %s' % (uuid, goods_id, product_id))
    Purchase(parent=user.key, goods_id=goods_id, product_id=product_id, gem=form.gem.data, cost=form.cost.data, version=form.version.data,
             date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@audit_api.route('/exchange/', methods=['POST'])
def save_exchange():
    form = get_form(ExchangeForm(request.form))
    user = User.get(form.uuid.data)
    Exchange(parent=user.key, goods_id=form.goods_id.data, gem=form.gem.data, coin=form.coin.data, version=form.version.data,
             date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@audit_api.route('/earn/', methods=['POST'])
def save_earn():
    form = get_form(EarnForm(request.form))
    user = User.get(form.uuid.data)
    Earn(parent=user.key, type_id=form.type_id.data, gem=form.gem.data, coin=form.coin.data, version=form.version.data,
         date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@audit_api.route('/consume/', methods=['POST'])
def save_consume():
    form = get_form(ConsumeForm(request.form))
    user = User.get(form.uuid.data)
    Consume(parent=user.key, type_id=form.type_id.data, gem=form.gem.data, coin=form.coin.data, album=form.album.data, level=form.level.data,
            picture=form.picture.data, version=form.version.data, date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


class PurchaseForm(BaseForm):
    goods_id = IntegerField('goods_id', [validators.input_required()])
    product_id = StringField('product_id', [validators.input_required(), validators.length(max=100)])
    gem = IntegerField('gem', [validators.input_required()])
    cost = IntegerField('cost', [validators.input_required()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])


class ExchangeForm(BaseForm):
    goods_id = IntegerField('goods_id', [validators.input_required()])
    gem = IntegerField('gem', [validators.input_required()])
    coin = IntegerField('coin', [validators.input_required()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])


class EarnForm(BaseForm):
    type_id = IntegerField('type_id', [validators.input_required()])
    gem = IntegerField('gem', [validators.optional()])
    coin = IntegerField('coin', [validators.optional()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])


class ConsumeForm(BaseForm):
    type_id = IntegerField('type_id', [validators.input_required()])
    gem = IntegerField('gem', [validators.optional()])
    coin = IntegerField('coin', [validators.optional()])
    album = IntegerField('album', [validators.optional()])
    level = IntegerField('level', [validators.optional()])
    picture = IntegerField('picture', [validators.optional()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])