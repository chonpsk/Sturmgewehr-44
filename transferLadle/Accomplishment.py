# -*- coding: UTF-8 -*-

from .base import *
import requests
import time
import datetime

def getList():
	data = getData()
	data['state'] = '3'
	while True:
		try:
			lst = session.post('http://sb69.geechs-app.com/1/Accomplishment/getAccomplishmentList', data = data, headers = headers).json()['action']['not_received']
		except:
			continue
		return lst

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
		session.post('http://sb69.geechs-app.com/1/Accomplishment/receiveAccomplishmentRewardBundle', data = data, headers = headers, timeout = 30)
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

def get_friendPT(tot = 0):
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
			session.post('http://sb69.geechs-app.com/1/Accomplishment/receiveAccomplishmentRewardBundle', data = data, headers = headers, timeout = 30)
		except:
			continue
		tot -= 1
	print('get finished')

