from flask import jsonify
from constants import APIStatus


def json_response(status=APIStatus.SUCCESS, message='', *args, **kwargs):
    return jsonify(status=status.__int__(), message=message, *args, **kwargs)

