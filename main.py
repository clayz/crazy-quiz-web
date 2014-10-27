from flask import Flask
from flask import render_template
from api.user_api import user_api
from api.audit_api import audit_api
from errors import ParameterError, DataError
from utilities import response
from constants import APIStatus

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
app.register_blueprint(user_api)
app.register_blueprint(audit_api)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/version/')
def version():
    return app.config['VERSION']


@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, nothing at this URL.', 404


@app.errorhandler(ParameterError)
def handle_parameter_error(error):
    app.logger.warn('Parameter error: %s' % error.to_dict())
    return response(APIStatus.PARAMETER_ERROR)


@app.errorhandler(DataError)
def handle_data_error(error):
    app.logger.error(error.to_dict())
    return response(error.api_status)