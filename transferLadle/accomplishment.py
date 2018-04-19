# -*- coding: UTF-8 -*-

from .base import *
import requests
import time
import datetime

def getList():
	data = getData()
	data['state'] = '3'
	return auto_post('/1/Accomplishment/getAccomplishmentList', data, 30).json()['action']['not_received']

def receive(lst):
	acc_ids = []
	for acc in lst:
		if lst[acc]['complete_flg']:
			acc_ids.append(acc)
	if len(acc_ids) == 0:
		return False
	data = getData()
	data['accomplishment_ids[]'] = acc_ids
	try:
		session.post('http://' + host + '/1/Accomplishment/receiveAccomplishmentRewardBundle', data = data, timeout = 30)
	except:
		pass
	return True

def accomplishment():
	print ('accomplishment start')
	init_time = datetime.datetime.now()
	not_received = getList()
	for state in range(1, 4):
		time.sleep(0.2)
		while receive(not_received[str(state)]):
			not_received = getList()
			time.sleep(0.2)
			print ('spend ' + str((datetime.datetime.now() - init_time).seconds) + 's now')

def get_friendPT():
	tot = cfg.getint('accomplishment', 'friendPT')
	friendPT = ['40700101']
	print ('get friendPT start')
	while tot > 0:
		time.sleep(0.2)
		lst = getList()['3']
		if not lst[friendPT[0]]['complete_flg']:
			break
		data = getData()
		data['accomplishment_ids[]'] = friendPT
		time.sleep(0.2)
		try:
			session.post('http://' + host + '/1/Accomplishment/receiveAccomplishmentRewardBundle', data = data, timeout = 30)
		except:
			continue
		tot -= 1
	print('get finished')

