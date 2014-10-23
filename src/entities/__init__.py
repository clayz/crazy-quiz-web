from google.appengine.ext import ndb


class BaseEntity(ndb.Model):
    create_date = ndb.DateTimeProperty(required=True, auto_now_add=True)