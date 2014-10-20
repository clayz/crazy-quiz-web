from protorpc import messages
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop


class Gender(messages.Enum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class Account(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    age = ndb.IntegerProperty()
    gender = msgprop.EnumProperty(Gender, required=True, default=Gender.UNKNOWN)
    create_date = ndb.DateTimeProperty(auto_now=True)
    update_date = ndb.DateTimeProperty()


    @classmethod
    def query_user(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)