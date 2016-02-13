from flask import request, jsonify, session
import requests
from constraints import *
import json
from functools import wraps
from models import SocialNetworkUser

def get_user():
	access_token = session['access_token']
	provider = session['auth_provider']
	if provider == 'facebook':
		url_me = 'https://graph.facebook.com/v2.5/me'
		_user = json.loads(requests.get(url_me, params={'access_token':access_token}).text)
		user = SocialNetworkUser.objects(provider='facebook', social_network_id=_user['id'])

		if len(user)>0:
			return user.first()
		else:
			user = SocialNetworkUser(provider='facebook',social_network_id=_user['id'], name=_user['name'], 
				photo='https://graph.facebook.com/v2.5/%s/picture' % (_user['id']))
			user.save()
			return user 

def fb_user(f):
	@wraps(f)
	def _(*args,**argv):
		url_debug = 'https://graph.facebook.com/debug_token'
		url_me = 'https://graph.facebook.com/v2.5/me'
		if 'access_token' in session:
			access_token = session['access_token']
			provider = session['auth_provider']

			if provider == 'facebook':
				params = {
					'input_token': access_token,
					'access_token' : '%s|%s' % (FB_APP_ID, FB_APP_SECRET),
				}
				data = json.loads(requests.get(url_debug, params=params).text)['data']

			if data['is_valid'] == True:
				return f(*args, **argv)
			else:
				return jsonify(**{'status': 'token_expired'}), 403
		else: 
			return jsonify(**{'status': 'unauthorized'}), 401

	return _