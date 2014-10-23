from google.appengine.ext import ndb
from entities import BaseEntity


class Facebook(BaseEntity):
    id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty()
    expire_date = ndb.DateTimeProperty()
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)


class Twitter(BaseEntity):
    id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty()
    expire_date = ndb.DateTimeProperty()
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)