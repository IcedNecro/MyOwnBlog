from flask import * 
import models
from forms import *
from flask.ext.login import LoginManager, login_user

login_manager = LoginManager()

blueprint = Blueprint('auth', __name__, 
	static_folder='static',
	template_folder='templates',
)

@login_manager.user_loader
def load_user(user_id):
	return models.User.objects.get(id=user_id)

@blueprint.route('/register')
def register():
	models.User(email='admin', password='admin').save()
	return jsonify(**{'code':'ok'})

@blueprint.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if request.method == 'GET':
		return render_template('login.html', form=form)
	else:
		try:
			user = models.User.objects.get(email=request.form['email'], password=request.form['password'])
			login_user(user)
			return redirect('/admin')
		except:
			return render_template('login.html', form=form)
		
