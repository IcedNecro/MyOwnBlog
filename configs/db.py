from flask.ext.mongoengine import MongoEngine

MONGO_DB_CONFIG = {
	'MONGODB_DB' : 'blog',
	'MONGODB_HOST' : 'localhost',
	'MONGODB_PORT' : 27017
}

db = MongoEngine()

def init_app(app):

	for k, v in MONGO_DB_CONFIG.iteritems():
		app.config[k] = v
	#app.config['DEBUG_TB_PANELS'] = ['flask.ext.mongoengine.panels.MongoDebugPanel']
	
	db.init_app(app)
	
