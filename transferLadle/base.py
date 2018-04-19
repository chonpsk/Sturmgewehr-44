# -*- coding: UTF-8 -*-

import requests
import time
import random
import datetime
from configparser import ConfigParser
import os

host = 'api.sb69gbmm.com'

session = requests.Session()

cfg = ConfigParser()
cfg.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

for pair in cfg.items('headers'):
	session.headers[pair[0].upper()] = pair[1]

yon = ['10415', '10416', '10447', '10448', '10638', '10639', '10781']

def setFullTime(full_time_):
	if not full_time_:
		full_time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	global full_time
	full_time = datetime.datetime.strptime(full_time_, '%Y-%m-%d %H:%M:%S')
	full_time -= datetime.timedelta(hours = 1)

def uniqueDate():
	return time.strftime('%Y%m%d%M%S', time.localtime(time.time()))

def getData():
	data = {'user_id': user_id, 'owner_user_id': user_id}
	data['unique_date'] = uniqueDate()
	if full_time <= datetime.datetime.now():
		data['front_user_stamina'] = str(stamina_max)
	else:
		data['front_user_stamina'] = str(stamina_max - ((full_time - datetime.datetime.now()).seconds - 1) // 180 - 1)
	return data

def auto_post(url, data, timeout = 30):
	while (True):
		try:
			return session.post('http://' + host + url, data = data, timeout = timeout)
		except:
			continue

def normalPost(url, timeout = 9):
	data = getData()
	return auto_post(url, data, timeout)

def set_config(dir_):
	cfg.read(dir_)
	for pair in cfg.items('headers'):
		session.headers[pair[0].upper()] = pair[1]
	setFullTime(cfg.get('data', 'stamina_full_time'))
	global stamina_max
	stamina_max = cfg.getint('data', 'stamina_max')
	global user_id
	user_id = cfg.get('data', 'user_id')
	if cfg.has_section('proxies'):
		session.proxies = {prx: cfg['proxies'][prx] for prx in cfg['proxies']}
		print ('proxies == ' + str(session.proxies))

def login(cfg_):
	data = {'uuid': cfg.get('data', 'uuid'), 'owner_user_id': '0', 'front_user_stamina': '0'}
	data['unique_date'] = uniqueDate()
	del session.headers['SBR-AUTHORIZED-TOKEN']
	r = auto_post('/1/startup/login', data, 90)
	token = r.headers['SBR_AUTHORIZED_TOKEN']

	user = r.json()['common']['user']
	global stamina_max
	stamina_max = max(int(user['stamina']), int(user['stamina_max']))
	setFullTime(user['stamina_full_time'])
	global user_id
	user_id = user['user_id']
	data = getData()
	del data['user_id']
	auto_post('/1/index/getBanner', data)

	session.headers['SBR-AUTHORIZED-TOKEN'] = token
	data = getData()
	del data['user_id']
	data['uuid'] = cfg.get('data', 'uuid')
	token = auto_post('/1/startup/login', data, 90).headers['SBR_AUTHORIZED_TOKEN']
	session.headers['SBR-AUTHORIZED-TOKEN'] = token

	cfg_.set('data', 'stamina_max', str(max(int(user['stamina']), int(user['stamina_max']))))
	cfg_.set('data', 'stamina_full_time', user['stamina_full_time'])
	cfg_.set('data', 'user_id', user['user_id'])
	cfg_.set('headers', 'SBR-AUTHORIZED-TOKEN', token)
	cfg_.set('login', 'if_logined', 'True')
