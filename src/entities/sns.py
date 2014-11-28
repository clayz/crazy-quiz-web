from google.appengine.ext import ndb
from entities import BaseEntity


class Facebook(BaseEntity):
    id = ndb.StringProperty()
    access_token = ndb.StringProperty()
    expires = ndb.IntegerProperty()
    code = ndb.StringProperty()
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)

    @classmethod
    def get(cls, user_key):
        data = cls.query(ancestor=user_key).fetch(1)
        return data[0] if data else None


class Twitter(BaseEntity):
    id = ndb.StringProperty()
    token = ndb.StringProperty()
    token_secret = ndb.StringProperty()
    code = ndb.StringProperty()
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)

    @classmethod
    def get(cls, user_key):
        data = cls.query(ancestor=user_key).fetch(1)
        return data[0] if data else None