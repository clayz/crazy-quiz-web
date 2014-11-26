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


class Date(object):
    YYYY_MM_DD = '%Y-%m-%d'
    YYYY_MM_DD_HH_MM_SS = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def now():
        return datetime.datetime.utcnow()

    @staticmethod
    def str_to_date(date, fm=YYYY_MM_DD_HH_MM_SS):
        return datetime.datetime.strptime(date, fm)

    @staticmethod
    def date_to_str(date, fm=YYYY_MM_DD_HH_MM_SS):
        return date.strftime(fm)

    @staticmethod
    def get_date_jp(date=None):
        if date:
            return date + datetime.timedelta(hours=+9)
        else:
            return datetime.datetime.utcnow() + datetime.timedelta(hours=+9)

    @staticmethod
    def get_timestamp(date):
        return time.mktime(date.timetuple())

    @staticmethod
    def get_date_from_js_timestamp(timestamp):
        return datetime.datetime.fromtimestamp(int(timestamp / 1000))