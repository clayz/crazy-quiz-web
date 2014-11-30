# coding=utf-8

from google.appengine.ext import ndb
from flask import Blueprint, request
import tweepy
import facebook as fb
import os
from constants import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, APIStatus
from errors import DataError
from api import *
from utilities import response, get_form
from entities.sns import Facebook, Twitter
from entities.user import User

sns_api = Blueprint('sns', __name__, url_prefix='/api/sns')


@sns_api.route('/auth/facebook/', methods=['POST'])
def auth_facebook():
    from main import app

    form = get_form(FacebookForm(request.form))
    uuid, access_token, expires, code = form.uuid.data, form.access_token.data, form.expires.data, form.code.data
    user_key = User.get(uuid).key
    facebook = Facebook.get(user_key)

    if not facebook:
        app.logger.debug('Create Facebook, uuid: %s, access_token: %s' % (uuid, access_token))
        Facebook(parent=user_key, access_token=access_token, expires=expires, code=code).put()
    elif facebook.access_token != access_token:
        app.logger.debug('Update Facebook, uuid: %s, access_token: %s' % (uuid, access_token))
        facebook.access_token = access_token
        facebook.expires = expires
        facebook.code = code
        facebook.put()

    return response()


@sns_api.route('/share/facebook/', methods=['POST'])
def share_facebook():
    from main import app

    form = get_form(ShareForm(request.form))
    uuid, message, album, picture = form.uuid.data, form.message.data, form.album.data, form.picture.data

    user = User.get(uuid)
    facebook = Facebook.get(user.key)
    graph = fb.GraphAPI(facebook.access_token)
    message_template = '【熱狂クイズ】%s facebook.com/nekyou.quiz'

    try:
        if album and picture:
            app.logger.debug('Share picture, uuid: %s, message: %s, picture: %d' % (uuid, message, picture))
            graph.put_photo(open(get_picture_path(album, picture)), message_template % message)
        else:
            app.logger.debug('Share message, uuid: %s, message: %s' % (uuid, message))
            graph.put_object('me', 'feed', link='http://www.facebook.com/nekyou.quiz', message=message_template % message)
    except Exception as e:
        app.logger.error('Twitter share failed: %s' % str(e))

    return response()


@sns_api.route('/auth/twitter/', methods=['POST'])
def auth_twitter():
    from main import app

    form = get_form(TwitterForm(request.form))
    uuid, token, token_secret, code = form.uuid.data, form.token.data, form.token_secret.data, form.code.data
    user_key = User.get(uuid).key
    twitter = Twitter.get(user_key)

    if not twitter:
        app.logger.debug('Create Twitter, uuid: %s, token: %s' % (uuid, token))
        Twitter(parent=user_key, token=token, token_secret=token_secret, code=code).put()
    elif twitter.token != token:
        app.logger.debug('Update Twitter, uuid: %s, token: %s' % (uuid, token))
        twitter.token = token
        twitter.token_secret = token_secret
        twitter.code = code
        twitter.put()

    return response()


@sns_api.route('/share/twitter/', methods=['POST'])
def share_twitter():
    from main import app

    form = get_form(ShareForm(request.form))
    uuid, message, album, picture = form.uuid.data, form.message.data, form.album.data, form.picture.data

    user = User.get(uuid)
    twitter = Twitter.get(user.key)

    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(twitter.token, twitter.token_secret)
    api = tweepy.API(auth)
    message_template = '【熱狂クイズ】%s facebook.com/nekyou.quiz'

    try:
        if album and picture:
            app.logger.debug('Share picture, uuid: %s, message: %s, picture: %d' % (uuid, message, picture))
            api.update_with_media(get_picture_path(album, picture), message_template % message)
        else:
            app.logger.debug('Share message, uuid: %s, message: %s' % (uuid, message))
            api.update_status(message_template % message)
    except Exception as e:
        app.logger.error('Twitter share failed: %s' % str(e))

    return response()


def get_picture_path(album, picture):
    if album == 1:
        path = os.path.join(os.path.dirname(__file__), '../../static/img/album/default/%d.png' % picture)
    elif album == 2:
        path = os.path.join(os.path.dirname(__file__), '../../static/img/album/default/%d.png' % picture)
    else:
        raise DataError(APIStatus.DATA_INCORRECT, 'Unsupported album: %d' % album)

    return path


class FacebookForm(BaseForm):
    access_token = StringField('access_token', [validators.input_required()])
    expires = IntegerField('expires', [validators.input_required()])
    code = StringField('code', [validators.input_required()])


class TwitterForm(BaseForm):
    token = StringField('token', [validators.input_required()])
    token_secret = StringField('token_secret', [validators.input_required()])
    code = StringField('code', [validators.input_required()])


class ShareForm(BaseForm):
    message = StringField('message', [validators.input_required()])
    album = IntegerField('album', [validators.optional()])
    picture = IntegerField('picture', [validators.optional()])