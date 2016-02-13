import datetime

from configs.db import db 
from engagements.models import Comment, Like

class Post(db.Document):
	title 				= db.StringField(max_length=200, required=True)
	text 				= db.StringField(max_length=20000, required=True)
	background_image 	= db.StringField()
	short_description 	= db.StringField(required=True)
	create_date  	 	= db.DateTimeField(default=datetime.datetime.now)
	last_edit_time   	= db.DateTimeField()
	tags 			 	= db.ListField()
	published		 	= db.BooleanField(default=False)
	likes 				= db.ListField(db.ReferenceField(Like))
	comments 			= db.ListField(db.ReferenceField(Comment))
