from flask import Blueprint, request
from utilities import json_response, get_form
from entities.user import User
from entities.audit import Purchase, Exchange, Earn, Consume
from api import *

audit_api = Blueprint('audit', __name__, url_prefix='/api/audit')


@audit_api.route('/purchase/', methods=['POST'])
def purchase():
    from main import app

    form = get_form(PurchaseForm(request.form))
    uuid, goods_id, product_id = form.uuid.data, form.goods_id.data, form.product_id.data
    user = User.get(uuid)

    app.logger.info('[%s] Purchased goods_id: %d, product_id: %s' % (uuid, goods_id, product_id))
    Purchase(parent=user.key, goods_id=goods_id, product_id=product_id, gem=form.gem.data, cost=form.cost.data, version=form.version.data,
             date=form.date.data).put()

    return json_response()


@audit_api.route('/exchange/', methods=['POST'])
def exchange():
    form = get_form(ExchangeForm(request.form))
    user = User.get(form.uuid.data)
    Exchange(parent=user.key, goods_id=form.goods_id.data, gem=form.gem.data, coin=form.coin.data, version=form.version.data,
             date=form.date.data).put()

    return json_response()


@audit_api.route('/earn/', methods=['POST'])
def earn():
    form = get_form(EarnForm(request.form))
    user = User.get(form.uuid.data)
    Earn(parent=user.key, type_id=form.type_id.data, gem=form.gem.data, coin=form.coin.data, version=form.version.data, date=form.date.data).put()

    return json_response()


@audit_api.route('/consume/', methods=['POST'])
def consume():
    form = get_form(ConsumeForm(request.form))
    user = User.get(form.uuid.data)
    Consume(parent=user.key, type_id=form.type_id.data, gem=form.gem.data, coin=form.coin.data, album=form.album.data, level=form.level.data,
            picture=form.picture.data, version=form.version.data, date=form.date.data).put()

    return json_response()


class PurchaseForm(BaseForm):
    goods_id = IntegerField('goods_id', [validators.input_required])
    product_id = StringField('product_id', [validators.input_required, validators.length(max=100)])
    gem = IntegerField('gem', [validators.input_required])
    cost = IntegerField('cost', [validators.input_required])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = DateTimeField('date', [validators.input_required])


class ExchangeForm(BaseForm):
    goods_id = IntegerField('goods_id', [validators.input_required])
    gem = IntegerField('gem', [validators.input_required])
    coin = IntegerField('coin', [validators.input_required])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = DateTimeField('date', [validators.input_required])


class EarnForm(BaseForm):
    type_id = IntegerField('type_id', [validators.input_required])
    gem = IntegerField('gem', [validators.optional])
    coin = IntegerField('coin', [validators.optional])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = DateTimeField('date', [validators.input_required])


class ConsumeForm(BaseForm):
    type_id = IntegerField('type_id', [validators.input_required])
    gem = IntegerField('gem', [validators.optional])
    coin = IntegerField('coin', [validators.optional])
    album = IntegerField('album', [validators.optional])
    level = IntegerField('level', [validators.optional])
    picture = IntegerField('picture', [validators.optional])
    version = StringField('version', [validators.length(min=3, max=5)])
    date = DateTimeField('date', [validators.input_required])