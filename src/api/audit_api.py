from google.appengine.ext import ndb
from flask import Blueprint, request
from utilities import response, get_form, get_timestamp, get_date_from_js_timestamp
from entities.user import User
from entities.audit import Purchase, Exchange, Earn, Consume
from api import *
from datetime import datetime

audit_api = Blueprint('audit', __name__, url_prefix='/api/audit')


@audit_api.route('/sync/', methods=['POST'])
def sync():
    from main import app

    data = request.json
    app.logger.debug('Received sync data: %s' % data)

    user = User.get(data['uuid'])
    sync_history(user.key, data['version'], data)
    last_purchase, last_exchange, last_earn, last_consume = get_last_sync_timestamp(user.key)

    return response(purchase=last_purchase, exchange=last_exchange, earn=last_earn, consume=last_consume)


@audit_api.route('/purchase/', methods=['POST'])
def save_purchase():
    from main import app

    form = get_form(PurchaseForm(request.form))
    uuid, goods_id = form.uuid.data, form.goods_id.data
    user = User.get(uuid)
    app.logger.info('[%s] Purchased goods_id: %d' % (uuid, goods_id))
    Purchase(parent=user.key, goods_id=goods_id, version=form.version.data, date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@audit_api.route('/exchange/', methods=['POST'])
def save_exchange():
    form = get_form(ExchangeForm(request.form))
    user = User.get(form.uuid.data)
    Exchange(parent=user.key, goods_id=form.goods_id.data, version=form.version.data, date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@audit_api.route('/earn/', methods=['POST'])
def save_earn():
    form = get_form(EarnForm(request.form))
    user = User.get(form.uuid.data)
    Earn(parent=user.key, type_id=form.type_id.data, version=form.version.data, date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@audit_api.route('/consume/', methods=['POST'])
def save_consume():
    form = get_form(ConsumeForm(request.form))
    user = User.get(form.uuid.data)
    Consume(parent=user.key, type_id=form.type_id.data, album=form.album.data, level=form.level.data, picture=form.picture.data,
            version=form.version.data, date=datetime.fromtimestamp(int(form.date.data))).put()

    return response()


@ndb.transactional()
def sync_history(user_key, version, data):
    from main import app

    last_purchase, last_exchange, last_earn, last_consume = get_last_sync_timestamp(user_key)
    purchases, exchanges, earns, consumes = data['purchase'], data['exchange'], data['earn'], data['consume']

    for purchase in purchases:
        if int(purchase['date'] / 1000) > last_purchase:
            app.logger.debug('Save new purchase: %s' % purchase)
            Purchase(parent=user_key, goods_id=purchase['goods'], version=version, date=get_date_from_js_timestamp(purchase['date'])).put()

    for exchange in exchanges:
        if int(exchange['date'] / 1000 > last_exchange):
            app.logger.debug('Save new exchange: %s' % exchange)
            Exchange(parent=user_key, goods_id=exchange['goods'], version=version, date=get_date_from_js_timestamp(exchange['date'])).put()

    for earn in earns:
        if int(earn['date'] / 1000 > last_earn):
            app.logger.debug('Save new earn: %s' % earn)
            Earn(parent=user_key, type_id=earn['type'], version=version, date=get_date_from_js_timestamp(earn['date'])).put()

    for consume in consumes:
        if int(consume['date'] / 1000 > last_consume):
            app.logger.debug('Save new consume: %s' % consume)
            Consume(parent=user_key, type_id=consume['type'], album=consume['album'], level=consume['level'], picture=consume['picture'],
                    version=version, date=get_date_from_js_timestamp(consume['date'])).put()


def get_last_sync_timestamp(user_key):
    purchase = Purchase.get_last(user_key).fetch(1)
    exchange = Exchange.get_last(user_key).fetch(1)
    earn = Earn.get_last(user_key).fetch(1)
    consume = Consume.get_last(user_key).fetch(1)

    return (get_timestamp(purchase[0].date) if purchase else None,
            get_timestamp(exchange[0].date) if exchange else None,
            get_timestamp(earn[0].date) if earn else None,
            get_timestamp(consume[0].date) if consume else None)


class PurchaseForm(BaseForm):
    goods_id = IntegerField('goods_id', [validators.input_required()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])


class ExchangeForm(BaseForm):
    goods_id = IntegerField('goods_id', [validators.input_required()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])


class EarnForm(BaseForm):
    type_id = IntegerField('type_id', [validators.input_required()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])


class ConsumeForm(BaseForm):
    type_id = IntegerField('type_id', [validators.input_required()])
    album = IntegerField('album', [validators.optional()])
    level = IntegerField('level', [validators.optional()])
    picture = IntegerField('picture', [validators.optional()])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = IntegerField('date', [validators.input_required()])