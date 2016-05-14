import os

from flask import *
from models import *
import configs

blueprint = Blueprint('post', __name__, 
	static_folder='static',
	template_folder='templates',
	static_url_path='post_management/static'
)

@blueprint.route('/')
def render_index():
	return render_template('main-template.html')

@blueprint.route('/topic/<id>')
def render_post_page(id):
	return render_template('main-template.html', id=id)

@blueprint.route('/api/static')
def get_statics_folder():
	return url_for('post.static')

@blueprint.route('/images/<path:filename>')
def uploaded_file(filename):
	return send_from_directory(configs.settings.UPLOAD_DIRECTORY,filename)

@blueprint.route('/api/post')
def get_posts():

	params = request.args
	order_by = '+date'
	filter_by = { 'published': True}

	if 'order_by' in params:
		order_by = params['order_by']
	if 'not_published' in params: 
		filter_by['published'] = False

	q = Post.objects(**filter_by).order_by(order_by)
	query = map(lambda o: json.loads(o.to_json()),q)
	for o in query:
		o['create_date'] = o['create_date']['$date']
		o['last_edit_time'] = o['last_edit_time']['$date'] if 'last_edit_time' in o else None

		o['_id'] = o['_id']['$oid']	
 
	return jsonify(**{'data':query})

@blueprint.route('/api/post/<id>')
def get_post(id):
	o = Post.objects.get(id=id)

	o = json.loads(o.to_json(populate='comments.author'))
	o['create_date'] = o['create_date']['$date']
	o['_id'] = o['_id']['$oid']	
	return jsonify(**{'data':o})