from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from constants import Gender, UserStatus, Device, AccountType


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    mail = ndb.StringProperty()
    gender = msgprop.EnumProperty(Gender, required=True, default=Gender.UNKNOWN)
    birthday = ndb.DateProperty()
    avatar = ndb.BlobProperty(compressed=True)
    status = msgprop.EnumProperty(UserStatus, required=True, default=UserStatus.ACTIVE)
    device = msgprop.EnumProperty(Device, required=True, default=Device.UNKNOWN)
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)
    update_date = ndb.DateTimeProperty()


class Currency(ndb.Model):
    coin = ndb.IntegerProperty(required=True, default=0)
    gem = ndb.IntegerProperty(required=True, default=0)
    total_spend = ndb.IntegerProperty(required=True, default=0)
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)
    update_date = ndb.DateTimeProperty()


class Purchase(ndb.Model):
    goods_id = ndb.IntegerProperty(required=True)
    product_id = ndb.StringProperty()
    gem = ndb.IntegerProperty(required=True)
    cost = ndb.IntegerProperty(required=True)
    version = ndb.StringProperty(required=True)
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)


class Exchange(ndb.Model):
    goods_id = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty(required=True)
    gem = ndb.IntegerProperty(required=True)
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)


class Earn(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty()
    gem = ndb.IntegerProperty()
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)


class Consume(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    coin = ndb.IntegerProperty()
    gem = ndb.IntegerProperty()
    album = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    picture = ndb.IntegerProperty()
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)


class LoginHistory(ndb.Model):
    version = ndb.StringProperty(required=True)
    ip = ndb.StringProperty()
    continue_login_days = ndb.IntegerProperty(required=True, default=1)
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)


class Account(ndb.Model):
    type = msgprop.EnumProperty(AccountType, required=True)
    id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(required=True, auto_now=True)
    update_date = ndb.DateTimeProperty()
    expire_date = ndb.DateTimeProperty()