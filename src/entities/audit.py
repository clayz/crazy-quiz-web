from google.appengine.ext import ndb
from entities import BaseEntity


class Purchase(BaseEntity):
    goods_id = ndb.IntegerProperty(required=True)
    product_id = ndb.StringProperty()
    gem = ndb.IntegerProperty(required=True)
    cost = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)


class Exchange(BaseEntity):
    goods_id = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty(required=True)
    gem = ndb.IntegerProperty(required=True)


class Earn(BaseEntity):
    type = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty()
    gem = ndb.IntegerProperty()


class Consume(BaseEntity):
    type = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty()
    gem = ndb.IntegerProperty()
    album = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    picture = ndb.IntegerProperty()