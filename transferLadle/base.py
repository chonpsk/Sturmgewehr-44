# -*- coding: UTF-8 -*-

import requests
import time
import random
import datetime
from configparser import ConfigParser
import os

session = requests.Session()

cfg = ConfigParser()
cfg.read(os.path.dirname(os.path.realpath(__file__)) + '\\config.ini')

headers = {}
for pair in cfg.items('headers'):
	headers[pair[0]] = pair[1]

yon = ['10415', '10416', '10447', '10448', '10638', '10639', '10781']

def setFullTime(full_time_s):
	global full_time
	full_time = time.strptime(full_time_s, '%Y-%m-%d %H:%M:%S')
	full_time = datetime.datetime(full_time[0], full_time[1], full_time[2], full_time[3], full_time[4], full_time[5])

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

def auto_post(url, data, headers, timeout):
	while (True):
		try:
			return session.post(url, data = data, headers = headers, timeout = timeout)
		except:
			continue

def normalPost(url, timeout = 9):
	data = getData()
	return auto_post(url, data, headers, timeout)

def set_config(dir_):
	cfg.read(dir_)
	for pair in cfg.items('headers'):
		headers[pair[0]] = pair[1]
	setFullTime(cfg.get('data', 'stamina_full_time'))
	global stamina_max
	stamina_max = cfg.getint('data', 'stamina_max')
	global user_id
	user_id = cfg.get('data', 'user_id')
