from flask import jsonify
from constants import APIStatus
from errors import ParameterError
import datetime
import time


def response(status=APIStatus.SUCCESS, message='', **kwargs):
    data = {
        'status': status.__int__(),
        'message': message
    }

    if len(kwargs):
        data['data'] = kwargs

    return jsonify(data)


def get_form(form):
    if form.validate():
        return form
    else:
        raise ParameterError(form.errors.items())


def get_timestamp(date):
    return time.mktime(date.timetuple())


def get_date_from_js_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp / 1000))
