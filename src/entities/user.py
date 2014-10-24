from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from entities import BaseEntity
from constants import Gender, UserStatus, Device, APIStatus
from errors import DataError


class User(BaseEntity):
    name = ndb.StringProperty(required=True)
    mail = ndb.StringProperty()
    gender = msgprop.EnumProperty(Gender, required=True, default=Gender.UNKNOWN)
    birthday = ndb.DateProperty()
    avatar = ndb.BlobProperty(compressed=True)
    status = msgprop.EnumProperty(UserStatus, required=True, default=UserStatus.ACTIVE)
    device = msgprop.EnumProperty(Device, required=True, default=Device.UNKNOWN)
    update_date = ndb.DateTimeProperty(required=True, auto_now=True)

    @classmethod
    def get(cls, uuid):
        user = cls.get_by_id(uuid)
        if user:
            return user
        else:
            raise DataError(APIStatus.DATA_NOT_FOUND, 'User not found, uuid: %s' % uuid)


class StartupHistory(BaseEntity):
    version = ndb.StringProperty(required=True)
    ip = ndb.StringProperty(required=True)
