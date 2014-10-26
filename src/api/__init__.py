from wtforms import Form, StringField, IntegerField, DateTimeField, validators


class BaseForm(Form):
    uuid = StringField('uuid', [validators.InputRequired(), validators.Length(max=100)])