from flask import Flask
from flask.ext.bower import Bower
from flask.ext.login import * 
from flask_debugtoolbar import DebugToolbarExtension

import post_management.views as post_blueprint 
import admin.views as admin_blueprint
import auth.views as auth_blueprint
import engagements.views as eng_blueprint
from werkzeug.routing import BaseConverter

from db import init_app

# setting up upload dirrectory for images
UPLOAD_DIRECTORY = '/home/romanstatkevich/development/pets/bd/blog/post_data/'

def configure(app):
	app.config['SECRET_KEY'] = '1488'

	#enabling bleuprints
	app.register_blueprint(post_blueprint.blueprint, url_prefix='/feed')
	app.register_blueprint(admin_blueprint.blueprint, url_prefix='/admin')
	app.register_blueprint(auth_blueprint.blueprint, url_prefix='/auth')
	app.register_blueprint(eng_blueprint.blueprint, url_prefix='/social')

	#enabling debug mode
	app.debug = True
	
	# initialize Mongoengine
	init_app(app)

	# initializing Flask login
	auth_blueprint.login_manager.init_app(app)
	
	# setting up debug toolbar
	#DebugToolbarExtension(app)

	# config bower
	app.config['BOWER_COMPONENTS_ROOT'] = '../bower_components'

	# configuring bower
	Bower(app)

app = Flask(__name__, static_url_path='')
configure(app)
