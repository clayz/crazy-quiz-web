from google.appengine.ext import ndb
from entities import BaseEntity


class Purchase(BaseEntity):
    goods_id = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)

    @classmethod
    def get_last(cls, user_key):
        return cls.query(ancestor=user_key).order(-cls.date)


class Exchange(BaseEntity):
    goods_id = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)

    @classmethod
    def get_last(cls, user_key):
        return cls.query(ancestor=user_key).order(-cls.date)


class Earn(BaseEntity):
    type_id = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)

    @classmethod
    def get_last(cls, user_key):
        return cls.query(ancestor=user_key).order(-cls.date)


class Consume(BaseEntity):
    type_id = ndb.IntegerProperty(required=True)
    album = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    picture = ndb.IntegerProperty()
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)

    @classmethod
    def get_last(cls, user_key):
        return cls.query(ancestor=user_key).order(-cls.date)