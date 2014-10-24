from google.appengine.ext import ndb
from entities import BaseEntity


class Purchase(BaseEntity):
    goods_id = ndb.IntegerProperty(required=True)
    product_id = ndb.StringProperty()
    gem = ndb.IntegerProperty(required=True)
    cost = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)


class Exchange(BaseEntity):
    goods_id = ndb.IntegerProperty(required=True)
    gem = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)


class Earn(BaseEntity):
    type_id = ndb.IntegerProperty(required=True)
    gem = ndb.IntegerProperty()
    coin = ndb.IntegerProperty()
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)


class Consume(BaseEntity):
    type_id = ndb.IntegerProperty(required=True)
    gem = ndb.IntegerProperty()
    coin = ndb.IntegerProperty()
    album = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    picture = ndb.IntegerProperty()
    version = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)