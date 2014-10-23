class ParameterError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class DataError(Exception):
    def __init__(self, api_status, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.api_status = api_status
        self.message = message
        self.payload = payload

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv