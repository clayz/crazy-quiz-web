from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from entities import BaseEntity
from constants import Gender, UserStatus, Device, APIStatus
from errors import DataError


class User(BaseEntity):
    name = ndb.StringProperty()
    mail = ndb.StringProperty()
    gender = msgprop.EnumProperty(Gender)
    birthday = ndb.DateProperty()
    avatar = ndb.BlobProperty(compressed=True)
    status = msgprop.EnumProperty(UserStatus, required=True, default=UserStatus.INACTIVE)
    device = msgprop.EnumProperty(Device, required=True)
    push_token = ndb.StringProperty()
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)

    @classmethod
    def get(cls, uuid):
        user = cls.get_by_id(uuid)
        if user:
            return user
        else:
            raise DataError(APIStatus.DATA_NOT_FOUND, 'User not found, uuid: %s' % uuid)


class Currency(BaseEntity):
    gem = ndb.IntegerProperty(required=True, default=0)
    coin = ndb.IntegerProperty(required=True, default=0)
    total_spend = ndb.IntegerProperty(required=True, default=0)
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)


class StartupHistory(BaseEntity):
    version = ndb.StringProperty(required=True)
    ip = ndb.StringProperty(required=True)
