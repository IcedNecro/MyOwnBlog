from configs.db import db

class Comment(db.Document):
	comment_text = db.StringField(max_length=1000, required=True)
	author = db.ReferenceField('SocialNetworkUser')
	post = db.ReferenceField('Post')

class Like(db.Document):
	author = db.ReferenceField('SocialNetworkUser')
	post = db.ReferenceField('Post')	

class SocialNetworkUser(db.Document):
	social_network_id = db.StringField(required=True)
	name = db.StringField(required=True)
	photo = db.StringField(max_length=1000)		
	provider = db.StringField(required=True)
