# -*- coding: UTF-8 -*-

from .base import *
import requests
import time
import random
import datetime

rare = ['N', 'R', 'SR', 'SSR', 'UR', 'UR+', 'LR']
pt= [0, 1, 10, 25]


tot = 0

class GachaError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def gacha():
	data = getData()
	data['detail_flg'] = '1'
	auto_post('/1/gacha/getGachaMstAll', data, 45)

	normalPost('/1/gacha/getGachaData')

	normalPost('/1/cache/setGachaToken')

	data = getData()
	data['gacha_id'] = '1'
	data['repeat_num'] = '10'
	data['rare_sell_list'] = ''
	if (sellN):
		data['rare_sell_list'] = '1,,'
	data['rare_point_list'] = ''
	if (allDecompose):
		data['rare_point_list'] = '2,3'
	data['is_sell_card'] = '1'
	data['is_over_soundoll'] = '1'
	try:
		r = session.post('http://' + host + '/1/gacha/execGacha', data = data, timeout = 30)
	except:
		return 
	
	global gacha_turns
	gacha_turns -= 1
	print ('error == "' + str(r.json()['common']['api_status']['error_message_flg']) + '"')
	if (str(r.json()['common']['api_status']['error_message_flg']) == '1'):
		raise GachaError("can't gacha")
	
	if r.json()['action'].get('card_point_data'):
		cpd = r.json()['action']['card_point_data']
		global tot
		tot += int(cpd['add_recycle_point'])
		for card in cpd['list']:
			print (str(rare[int(card['card_rare']) - 1] + " " + card['card_name'].encode('gbk', 'ignore').decode('gbk')))

	cards = []
	for card in r.json()['action']['gacha_drop_list']:
		if ((not sellN and card['drop_item_master']['card_rare'] == '1') or (card['drop_item_master']['card_max_soul_red'] == '1' and int(card['drop_item_master']['card_id']) < 40000)):
			cards.append(card['create_flg']['inserted_id'])

	normalPost('/1/user/getUser')

	data = getData()
	data['detail_flg'] = '1'
	auto_post('/1/gacha/getGachaMstAll', data, 45)

	normalPost('/1/gacha/getGachaData')

	return cards

def recycle():
	data = getData()
	data['detail_flg'] = '1'
	r = auto_post('/1/RecycleGacha/getCardDataAll', data, 45)
	
	material_card_ids = []

	for card in r.json()['action']['card_data']:
		if (card['rock_flg'] == '0' and card['card_band_id'] != '19' and int(card['card_rare']) <= 3 and card['card_soul_yellow'] != '1'):
			material_card_ids.append(card['user_card_id'])
			global tot
			tot += pt[int(card['card_rare']) - 1]
			print (str(card['user_card_id']) + " " + rare[int(card['card_rare']) - 1] + " " + card['card_name'].encode('gbk', 'ignore').decode('gbk'))
		if (len(material_card_ids) == 30):
			break
	
	if (len(material_card_ids) > 0):
		card_ids = ''
		for i in range(0, len(material_card_ids)):
			if (i > 0):
				card_ids += ','
			card_ids += material_card_ids[i]
		normalPost('/1/cache/setRecycleToken')
		data = getData()
		data['material_card_ids'] = card_ids
		#print (card_ids)
		try:
			session.post('http://' + host + '/1/RecycleGacha/execRecycleCard', data = data, timeout = 30)
		except:
			return False

	data = getData()
	data['detail_flg'] = '1'
	auto_post('/1/RecycleGacha/getCardDataAll', data)
	return True

def recycle_card():
	while (not recycle()):
		time.sleep(0.1)

def merge(base_card_id, drop_cards = 0):
	r = normalPost('/1/Bromide/getCardDataAll', 45)
	material_card_ids = []

	try:
		r.json()
	except:
		return True

	for card in r.json()['action']:
		if ((card['card_rare'] == '1' or (int(card['card_rare']) <= 4 and card['card_soul_yellow'] == '1')) and card['rock_flg'] == '0'):
			material_card_ids.append(card['user_card_id'])
		if (len(material_card_ids) == 10):
			break

	if drop_cards != 0:
		material_card_ids = drop_cards

	if (len(material_card_ids) == 0):
		return False

	normalPost('/1/cache/setCardMergeToken')

	data = getData()
	data['base_card_id'] = base_card_id
	data['material_card_ids[]'] = material_card_ids
	try:
		after = session.post('http://' + host + '/1/Bromide/execMergeCard', data = data, timeout = 30).json()['action']['after']
	except:
		return True
	
	normalPost('/1/user/getUser')

	if int(after['card_level']) >= int(after['card_max_level']):
		print ("Level MAX!!!!")
		target_card_list.remove(base_card_id)
		raise GachaError('card level max')

	print ('Lv. ' + str(after['card_level']))
	
	return drop_cards == 0

def merge_card(base_card_id, drop_cards = 0):
	normalPost('/1/CardDeck/getDeckList', 30)
	data = getData()
	del data['user_id']
	data['support_id'] = '1'
	auto_post('/1/CardDeck/getSupportDeck', data, 30)

	while (merge(base_card_id, drop_cards)):
		time.sleep(0.4)

	normalPost('/1/CardDeck/getDeckList', 30)

def clean_all(base_card, merge_turns = 9):
	init_time = datetime.datetime.now()
	try:
		merge(base_card)
		time.sleep(2)
	except GachaError as gg:
		print (gg.value)
		return False
	up_bound = gacha_turns
	for i in range(0, up_bound):
		print ('round ' + str(up_bound - gacha_turns))
		print ('spend ' + str((datetime.datetime.now() - init_time).seconds) + 's now')
		try:
			gacha()
			time.sleep(0.3)
			if not allDecompose:
				recycle_card()
				time.sleep(0.4)
			if sellN:
				if i % merge_turns == 0:
					merge_card(base_card)
			else:
				merge_card(base_card)
		except GachaError as gg:
			print (gg.value)
			return False
		print ("                    get " + str(tot) + " pt now")
	return True

def clean_drop_only(base_card):
	init_time = datetime.datetime.now()
	up_bound = gacha_turns
	for i in range(0, up_bound):
		print ('round ' + str(gacha_turns))
		print ('spend ' + str((datetime.datetime.now() - init_time).seconds) + 's now')
		try:
			drop_cards = gacha()
			time.sleep(0.3)
			merge_card(base_card, drop_cards)
		except GachaError as gg:
			print (gg.value)
			return False
		print ("                    get " + str(tot) + " pt now")
	return True

def get_card_info():
	normalPost('/1/CardDeck/getDeckList', 30)
	data = getData()
	del data['user_id']
	data['support_id'] = '1'
	auto_post('/1/CardDeck/getSupportDeck', data, 30)
	card_list = normalPost('/1/Bromide/getCardDataAll', 45).json()['action']
	card_info = []
	for card in card_list:
		if int(card['card_level']) < int(card['card_max_level']):
			info = card['user_card_id'] + ' ' + rare[int(card['card_rare']) - 1] + ' ' + card['card_name'].encode('gbk', 'ignore').decode('gbk') + ' ' + 'Lv.' + card['card_level']
			if card['rock_flg'] == '1':
				info += ' locked'
			else:
				info += ' unlocked'
			card_info.append(info)
			print (info)
	return card_info

def clean():
	global sellN
	sellN = cfg.getboolean('clean', 'sellN')
	global allDecompose
	allDecompose = cfg.getboolean('clean', 'allDecompose')
	global gacha_turns
	gacha_turns = cfg.getint('clean', 'gacha_turns')
	global target_card_list
	target_card_list = eval(cfg.get('clean', 'target_card_list'))
	target_card_list_ = list(target_card_list)
	drop_only = cfg.getboolean('clean', 'drop_only')
	merge_only = cfg.getboolean('clean', 'merge_only')
	for card in target_card_list_:
		if merge_only:
			try:
				merge_card(card)
			except:
				pass
		elif drop_only:
			clean_drop_only(card)
		else:
			clean_all(card)
		print (' ==== ' + card + ' cleaned ====')
	return target_card_list
