from configs.db import db 
from flask.ext.login import UserMixin

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
