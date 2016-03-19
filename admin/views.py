from flask import *
from flask.ext.login import login_required
from post_management.models import Post
import datetime
import json
import os
import configs  

blueprint = Blueprint('admin', __name__, 
	static_folder='static',
	template_folder='templates',
)

@blueprint.route('/')
@login_required
def render_admin_index():
	return render_template('admin.html')

@blueprint.route('/post')
@login_required
def render_admin_post():
	return render_template('admin-post.html', edit_mode=False)

@blueprint.route('/post/<id>/')
@login_required
def render_edit_admin_post(id):
	return render_template('admin-post.html',id=id, edit_mode=True)

@blueprint.route('/api/post', methods=['GET','POST', 'DELETE'])
@login_required
def post_manage():
	if request.method == 'POST':
		data = request.json
		newPost = Post(**data)
		newPost.background_image = newPost.id+'/banner'
		newPost.save()

		if os.path.exists(os.path.join(configs.settings.UPLOAD_DIRECTORY, str(newPost.id))) == False:
			os.makedirs(os.path.join(configs.settings.UPLOAD_DIRECTORY, str(newPost.id)))

		return jsonify(**{"status": "ok"})
	
	elif request.method == 'GET':
		
		params = request.args
		order_by = '+date'
		filter_by = { 'published': True}

		if 'order_by' in params:
			order_by = params['order_by']
		if 'not_published' in params: 
			filter_by['published'] = False
		q = Post.objects(**filter_by).order_by(order_by)
		
		query = []
		for k in q.as_pymongo():
			if 'comments' in k:
				del k['comments']
			k['_id'] = str(k['_id'])
			query.append(k)
		
		return jsonify(**{'data':query})

	elif request.method == 'DELETE':
		# add file delete

		ids = request.args['ids'].split(',')
		q = Post.objects(id__in=ids)
		return jsonify(**{"status": "ok"})
	# avoid 500 error

@blueprint.route('/api/post/image/<id>', methods=['POST'])
@login_required
def add_banner_image(id):
	if request.method == 'POST':
		_file = request.files['file']
		save_dir = os.path.join(configs.settings.UPLOAD_DIRECTORY, str(id))
		
		if os.path.exists(save_dir) == False:
			os.makedirs(save_dir)

		# check for valid file format
		_file.save(os.path.join(save_dir, 'banner'))
		
		return jsonify(**{'status':'ok'})
	# avoid 500 error

@blueprint.route('/api/post/<id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def single_post_manage(id):
	o = Post.objects(id=id)

	if request.method == 'GET':
		o = o.as_pymongo()[0]
		o = json.loads(configs.JSONEncoder().encode(o))
		if 'comments' in o :
			del o['comments']
		return jsonify(**{'data':o})

	elif request.method == 'PUT':
		o = o[0]
		data = request.json
		data['last_edit_time'] = datetime.datetime.now() 
		data['background_image'] = str(o.id)+'/banner'
		o.update(**data)

		if os.path.exists(os.path.join(configs.settings.UPLOAD_DIRECTORY, str(o.id))) == False:
			os.makedirs(os.path.join(configs.settings.UPLOAD_DIRECTORY, str(o.id)))

		return jsonify(**{'status':'ok'})

	elif request.method == 'DELETE':
		# add file delete
		o.delete()
		return jsonify(**{"status": "ok"})
	# avoid 500 error

@blueprint.route('/api/tags')
@login_required
def get_tags():
	# finish tags
	# CRUD operations
	match = {'$regex':'.*'}
	if 'text' in request.args:
		match['$regex'] = request.args['text']+'.*'

	query = list(Post.objects.aggregate(*[
		{'$unwind':'$tags'},
		{'$match':{'tags': match}},
		{'$group': {
			'_id': None,
			'tags': {'$addToSet': '$tags'},
		}}
	]))

	return jsonify(**{"data": query[0] if len(query)!=0 else {'tags':[]}})
