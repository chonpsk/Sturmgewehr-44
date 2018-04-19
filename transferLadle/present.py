# -*- coding: UTF-8 -*-

from .base import *
import requests
import time
import random
import datetime

def present():
	friend = cfg.getboolean('present', 'friend')
	gold = cfg.getboolean('present', 'gold')
	foods = eval(cfg.get('present', 'exp'))
	fv = [750, 1500, 3750]
	tot = 0
	init_time = datetime.datetime.now()
	while True:
		print ('present start')
		print ('spend ' + str((datetime.datetime.now() - init_time).seconds) + 's now')
	
		data = getData()
		data['offset'] = '0'
		data['tab_id'] = '1'
		rs = auto_post('/1/presentBox/getNotReceivedPresent', data,  45)
		js = rs.json()
		pages = (int(js['action']['max_page']) - 1) // 5 + 1

		normalPost('/1/home/top')

		cnt = 0
		seq_ids = []
		for page in range(0, pages):
			data = getData()
			data['offset'] = str(page * 100)
			data['tab_id'] = 1
			rs = auto_post('/1/presentBox/getNotReceivedPresent', data,  45)
			for prst in rs.json()['action']['present']:
				if (prst['item_type'] == '17' or prst['item_type'] == '21' or prst['item_type'] == '3'):
					seq_ids.append(prst['seq_id'])
				if (prst['item_type'] == '13' and friend):
					seq_ids.append(prst['seq_id'])
				if (prst['item_type'] == '4' and gold):
					seq_ids.append(prst['seq_id'])
				if (prst['item_type'] == '10' and int(prst['item_id']) > 30000 and int(prst['item_id']) < 30016):
					if (foods[int(prst['item_id']) % 5] >= int(prst['item_count']) * fv[(int(prst['item_id']) - 30001) // 5]):
						seq_ids.append(prst['seq_id'])
						foods[int(prst['item_id']) % 5] -= int(prst['item_count']) * fv[(int(prst['item_id']) - 30001) // 5]
				if (len(seq_ids) == 20):
					break
			if (len(seq_ids) == 20):
				break
	
		if (len(seq_ids) == 0):
			return
	
		normalPost('/1/cache/setPresentToken')

		data = getData()
		data['seq_ids[]'] = seq_ids
		try:
			session.post('http://' + host + '/1/presentBox/receivePresentBundle', data = data)
		except:
			time.sleep(4)
			continue

		tot += len(seq_ids)
		print ('get ' + str(tot))

		if (len(seq_ids) < 20):
			return

		time.sleep(4)
