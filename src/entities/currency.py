from google.appengine.ext import ndb
from entities import BaseEntity


class Currency(BaseEntity):
    coin = ndb.IntegerProperty(required=True, default=0)
    gem = ndb.IntegerProperty(required=True, default=0)
    total_spend = ndb.IntegerProperty(required=True, default=0)
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)