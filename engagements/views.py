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

@blueprint.route('/comment/<post_id>', methods=["POST", 'GET', 'DELETE'])
@fb_user
def comment_endpoint(post_id):
	if request.method == 'POST':
		data = request.json
		user = get_user()

		comment = Comment(comment_text=data['comment_text'], author=user)
		comment.save()

		Post.objects(id=post_id).update_one(push__comments=comment)
		return jsonify(**{'status':'ok'})