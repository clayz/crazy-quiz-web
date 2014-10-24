from wtforms import Form, IntegerField, StringField, DateTimeField, validators


class BaseForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=100)])


class StartupForm(BaseForm):
    name = StringField('name', [validators.input_required, validators.length(min=1, max=8)])
    version = StringField('version', [validators.length(min=3, max=5)])
    device = IntegerField('device', [validators.number_range(min=0, max=3)])


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


class EarnForm(Form):
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