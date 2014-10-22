from flask import jsonify
from constants import APIStatus


def json_response(status=APIStatus.SUCCESS.__int__(), message='', *args, **kwargs):
    return jsonify(status=status, message=message, *args, **kwargs)

