# coding=utf-8

from google.appengine.ext import ndb
import os
import urllib2
# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream
# import tweepy
from flask import Blueprint, request
import facebook as fb
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


@sns_api.route('/share/facebook/', methods=['POST'])
def share_facebook():
    form = get_form(ShareForm(request.form))
    uuid, message, picture = form.uuid.data, form.message.data, form.picture.data

    user = User.get(uuid)
    facebook = Facebook.get(user.key)
    graph = fb.GraphAPI(facebook.access_token)

    if picture:
        # image = urllib2.urlopen('http://crazy-quiz-dev.appspot.com/static/img/album/default/100.png')
        # fn = os.path.join(os.path.dirname(__file__), '100.png')
        fn = os.path.join(os.path.dirname(__file__), '../../static/img/album/default/100.png')
        graph.put_photo(open(fn), 'Look at this cool photo!')
    else:
        graph.put_object('me', 'feed', link='http://www.facebook.com/nekyou.quiz', message=message)

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


@sns_api.route('/share/twitter/', methods=['POST'])
def share_twitter():
    form = get_form(ShareForm(request.form))
    uuid, message, picture = form.uuid.data, form.message.data, form.picture.data

    user = User.get(uuid)
    twitter = Twitter.get(user.key)

    # auth = tweepy.OAuthHandler('56cakvFora8FZvHdGspXB0sLA', 'ynAmVkei7IUkB2cshm4m6JyFbLWDTu6PCv4WLylFEvJfIUXXLJ')
    # auth.set_access_token('2713692740-FVwZkAZRu4sWVf3noHHfkkOef0vhO0tHZeGfPWs', 'VHsTdpUjymIqakZ7qcHL8d2DxS1kpwgh6S1QcnK7aekU2')
    # api = tweepy.API(auth)
    #
    # from main import app
    #
    # app.logger.info('twitter me: %s' % str(api.me()))
    #
    # if picture:
    #     api.update_status('Updating using OAuth authentication via Tweepy!')
    # else:
    #     api.update_status('Updating using OAuth authentication via Tweepy!')

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


class ShareForm(BaseForm):
    message = StringField('message', [validators.input_required()])
    picture = IntegerField('picture', [validators.optional()])