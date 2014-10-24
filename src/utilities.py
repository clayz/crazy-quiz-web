from flask import jsonify
from constants import APIStatus
from errors import ParameterError


def json_response(status=APIStatus.SUCCESS, message='', *args, **kwargs):
    return jsonify(status=status.__int__(), message=message, *args, **kwargs)


def get_form(form):
    if form.validate():
        return form
    else:
        raise ParameterError(form.errors.items())
