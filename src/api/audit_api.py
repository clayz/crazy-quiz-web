from flask import Blueprint, request
from wtforms import Form, StringField, IntegerField, validators
from entities.user import User
from entities.audit import Purchase
from constants import APIStatus
from utilities import json_response
from errors import ParameterError, DataError

audit_api = Blueprint('audit', __name__, url_prefix='/api/audit')


class PurchaseForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=500)])
    goods_id = IntegerField('goods_id', [validators.NumberRange(min=1, max=5)])
    product_id = StringField('product_id', [validators.InputRequired(), validators.Length(max=100)])
    gem = IntegerField('gem', [validators.NumberRange(min=10, max=400)])
    cost = IntegerField('cost', [validators.NumberRange(min=100, max=3000)])
    version = StringField('version', [validators.Length(min=3, max=5)])


@audit_api.route('/purchase/', methods=['POST'])
def purchase():
    from main import app

    form = PurchaseForm(request.form)
    if not form.validate():
        raise ParameterError(form.errors.items())

    uuid, goods_id, product_id = form.uuid.data, form.goods_id.data, form.product_id.data
    user = User.get_by_id(uuid)

    if not user:
        raise DataError(APIStatus.DATA_NOT_FOUND, 'User not found, uuid: %s' % uuid)

    app.logger.info('[%s] Purchased goods_id: %d, product_id: %s' % (uuid, goods_id, product_id))
    Purchase(parent=user.key, goods_id=goods_id, product_id=product_id, gem=form.gem.data, cost=form.cost.data, version=form.version.data).put()

    return json_response()