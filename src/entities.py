from datetime import datetime, date, time
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from constants import Gender, UserStatus, Device, AccountType


class BaseEntity(ndb.Model):
    create_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)
    delete = ndb.BooleanProperty(required=True, default=False)


class User(BaseEntity):
    name = ndb.StringProperty(required=True)
    mail = ndb.StringProperty()
    gender = msgprop.EnumProperty(Gender, required=True, default=Gender.UNKNOWN)
    birthday = ndb.DateProperty()
    avatar = ndb.BlobProperty(compressed=True)
    status = msgprop.EnumProperty(UserStatus, required=True, default=UserStatus.ACTIVE)
    device = msgprop.EnumProperty(Device, required=True, default=Device.UNKNOWN)


class Currency(BaseEntity):
    coin = ndb.IntegerProperty(required=True, default=0)
    gem = ndb.IntegerProperty(required=True, default=0)
    total_spend = ndb.IntegerProperty(required=True, default=0)


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


class LoginHistory(BaseEntity):
    version = ndb.StringProperty(required=True)
    ip = ndb.StringProperty(required=True, repeated=True)
    startup_time = ndb.TimeProperty(required=True, repeated=True)

    @classmethod
    def get_today(cls, ancestor_key):
        return cls.query(ndb.AND(cls.create_date >= datetime.combine(date.today(), time()),
                                 cls.create_date < datetime.combine(date.today() + datetime.timedelta(days=1), time())),
                         ancestor=ancestor_key).fetch()


class Account(BaseEntity):
    type = msgprop.EnumProperty(AccountType, required=True)
    id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty()
    expire_date = ndb.DateTimeProperty()