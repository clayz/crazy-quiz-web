from flask import Flask
from flask import render_template
from api.user import user_api

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
app.register_blueprint(user_api)


@app.route('/')
def index():
    # app.logger.debug(app.config['USERNAME'])
    return render_template('index.html')


@app.route('/api/version/')
def version():
    return app.config['VERSION']


@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, nothing at this URL.', 404
