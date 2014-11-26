from google.appengine.ext import ndb
from flask import Blueprint, request
from api import *
from utilities import response, get_form
from entities.sns import Facebook, Twitter, Instagram
from entities.user import User

sns_api = Blueprint('sns', __name__, url_prefix='/api/sns')


@sns_api.route('/auth/facebook/', methods=['POST'])
def auth_facebook():
    form = get_form(FacebookForm(request.form))
    uuid, access_token, expires, code = form.uuid.data, form.access_token.data, form.expires.data, form.code.data
    user_key = User.get(uuid).key
    facebook = Facebook.get(user_key)

    if not facebook:
        Facebook(parent=user_key, access_token=access_token, expires=expires, code=code).put()
    elif facebook.access_token != access_token:
        facebook.access_token = access_token
        facebook.expires = expires
        facebook.code = code
        facebook.put()

    return response()


@sns_api.route('/auth/twitter/', methods=['POST'])
def auth_twitter():
    form = get_form(TwitterForm(request.form))
    uuid, token, token_secret, code = form.uuid.data, form.token.data, form.token_secret.data, form.code.data
    user_key = User.get(uuid).key
    twitter = Twitter.get(user_key)

    if not twitter:
        Twitter(parent=user_key, token=token, token_secret=token_secret, code=code).put()
    elif twitter.token != token:
        twitter.token = token
        twitter.token_secret = token_secret
        twitter.code = code
        twitter.put()

    return response()


@sns_api.route('/auth/instagram/', methods=['POST'])
def auth_instagram():
    form = get_form(InstagramForm(request.form))
    uuid, access_token, code = form.uuid.data, form.access_token.data, form.code.data
    user_key = User.get(uuid).key
    instagram = Instagram.get(user_key)

    if not instagram:
        Instagram(parent=user_key, access_token=access_token, code=code).put()
    elif instagram.access_token != access_token:
        instagram.access_token = access_token
        instagram.code = code
        instagram.put()

    return response()


class FacebookForm(BaseForm):
    access_token = StringField('access_token', [validators.input_required()])
    expires = IntegerField('expires', [validators.input_required()])
    code = StringField('code', [validators.input_required()])


class TwitterForm(BaseForm):
    token = StringField('token', [validators.input_required()])
    token_secret = StringField('token_secret', [validators.input_required()])
    code = StringField('code', [validators.input_required()])


class InstagramForm(BaseForm):
    access_token = StringField('access_token', [validators.input_required()])
    code = StringField('code', [validators.input_required()])