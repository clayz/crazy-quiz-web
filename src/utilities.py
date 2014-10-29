from flask import jsonify
from constants import APIStatus
from errors import ParameterError


def response(status=APIStatus.SUCCESS, message='', **kwargs):
    data = {
        'status': status.__int__(),
        'message': message,
        'data': kwargs
    }

    return jsonify(data)


def get_form(form):
    if form.validate():
        return form
    else:
        raise ParameterError(form.errors.items())
