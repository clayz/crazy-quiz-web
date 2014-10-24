from flask import Blueprint, request
from wtforms import Form, StringField, IntegerField, validators
from entities.user import User
from entities.audit import Purchase, Exchange
from utilities import json_response, get_form

audit_api = Blueprint('audit', __name__, url_prefix='/api/audit')


class PurchaseForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=500)])
    goods_id = IntegerField('goods_id', [validators.InputRequired()])
    product_id = StringField('product_id', [validators.InputRequired(), validators.Length(max=100)])
    gem = IntegerField('gem', [validators.InputRequired()])
    cost = IntegerField('cost', [validators.InputRequired()])
    version = StringField('version', [validators.Length(min=3, max=5)])


@audit_api.route('/purchase/', methods=['POST'])
def purchase():
    from main import app

    form = get_form(PurchaseForm(request.form))
    uuid, goods_id, product_id = form.uuid.data, form.goods_id.data, form.product_id.data
    user = User.get(uuid)

    app.logger.info('[%s] Purchased goods_id: %d, product_id: %s' % (uuid, goods_id, product_id))
    Purchase(parent=user.key, goods_id=goods_id, product_id=product_id, gem=form.gem.data, cost=form.cost.data, version=form.version.data).put()

    return json_response()


class ExchangeForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=500)])
    goods_id = IntegerField('goods_id', [validators.InputRequired()])
    gem = IntegerField('gem', [validators.InputRequired()])
    coin = IntegerField('coin', [validators.InputRequired()])
    version = StringField('version', [validators.Length(min=3, max=5)])


@audit_api.route('/exchange/', methods=['POST'])
def exchange():
    from main import app

    form = get_form(ExchangeForm(request.form))
    uuid, goods_id = form.uuid.data, form.goods_id.data
    user = User.get(uuid)

    app.logger.debug('[%s] Exchange goods_id: %d' % goods_id)
    Exchange(parent=user.key, goods_id=goods_id, gem=form.gem.data, coin=form.coin.data, version=form.version.data).put()

    return json_response()