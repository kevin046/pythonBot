import requests
import json

import globals

from api.exception import raise_exception
from utilities.log import log

def pre_login(email: str, password: str) -> str:
	# copy headers to append content type
	local_headers = globals.headers.copy()
	local_headers['Content-Type'] = 'application/json'

	# pre 2FA POST
	response = requests.post(globals.endpoint_authenticate, headers = local_headers, data = json.dumps({
		'password': password,
		'strategy': 'local',
		'totpType': 'sms',
		'username': email
	}))

	# make sure we have 2xx status
	if (not response.ok):
		log('Something went wrong when login (pre 2FA): {}'.format(response.text))
		
		raise_exception(response.status_code)

	response = response.json()
	return response['accessToken']

def mfa_login(code: str, pre_token: str) -> str:
	# copy headers to append content type
	local_headers = globals.headers.copy()
	local_headers['Content-Type'] = 'application/json'
	local_headers['Authorization'] = pre_token

	# 2FA POST
	response = requests.post(globals.endpoint_authenticate, headers = local_headers, data = json.dumps({
		'mfaToken': code,
		'strategy': 'mfa'
	}))

	# make sure we have 2xx status
	if (not response.ok):
		log('Something went wrong when login (2FA): {}'.format(response.text))
		
		raise_exception(response.status_code)

	response = response.json()

	return response['accessToken']
