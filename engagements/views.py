from flask import *
import requests
from utils import *

from constraints import *
import json
from post_management.models import Post
from models import *

blueprint = Blueprint('social', __name__, 
	static_folder='static',
	template_folder='templates',
)

# TODO: Issues when invoking token first time

@blueprint.route('/auth/fb')
def fb_auth():
	code = request.args['code']
	url = 'https://graph.facebook.com/v2.5/oauth/access_token'
	url_me = 'https://graph.facebook.com/v2.5/me'

	params = {
    	'client_id':FB_APP_ID,
   		'redirect_uri':'http://localhost:5000/social/auth/fb',
   		'client_secret':FB_APP_SECRET,
   		'code':code
	}

	response = json.loads(requests.post(url, params=params).text)
	access_code = response['access_token']
	
	session['access_token'] = access_code
	session['auth_provider'] = 'facebook'

	response = requests.get(url_me, params = {'access_token':access_code})
	return '<script>window.opener.resolve('+response.text+'); window.close()</script>'

@blueprint.route('/auth/fb/validate')
@fb_user
def validate_fb_auth():
	return jsonify(**get_user())

@blueprint.route('/comment/<post_id>', methods=["POST", 'GET', 'DELETE', 'PUT'])
@fb_user
def comment_endpoint(post_id):

	if request.method == 'POST':
		data = request.json
		user = get_user()

		comment = Comment(comment_text=data['comment_text'], author=user)
		comment.save()

		Post.objects(id=post_id).update_one(push__comments=comment)
		return jsonify(**{'status':'ok'})

	if request.method == 'DELETE':
		comment = Comment.objects(id=post_id).delete()
		return jsonify(**{'status':'ok'})

	if request.method == 'PUT':
		comment = Comment.objects(id=post_id).first()
		comment['comment_text'] = request.json['comment_text']
		comment.save()
		return jsonify(**{'status':'ok'})

@blueprint.route('/like/<post_id>', methods=["POST", 'GET', 'DELETE'])
@fb_user
def like_endpoint(post_id):
	if request.method == 'POST':
		data = request.json
		user = get_user()

		obj = Like.objects(author=user, post=post_id)
		if len(obj)==0:
			like.save()

			Post.objects(id=post_id).update_one(push__likes=like)
			return jsonify(**{'status':'ok'})
		else: 
			obj.delete()