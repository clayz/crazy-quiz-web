from flask import Blueprint
from flask import jsonify
# from main
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()

    @classmethod
    def query_user(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)


user_api = Blueprint('user', __name__, url_prefix='/api/user')


@user_api.route('/')
def index():
    user = User(name='Clay Zhong', email='zjclay@gmail.com')
    user_key = user.put()
    # app.logger.debug(user_key)

    return 'User API'


@user_api.route('/get/')
def get():
    return jsonify(username='Clay Zhong',
                   email='zjclay@gmail.com',
                   role=['Admin', 'Engineer'])
