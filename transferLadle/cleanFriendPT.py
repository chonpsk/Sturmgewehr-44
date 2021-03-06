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
    if (reserveSR):
        data['rare_sell_list'] = '2,'
    data['is_sell_card'] = '1'
    data['is_over_soundoll'] = '1'

    r = auto_post('/1/gacha/execGacha', data, 45)
    
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

def merge(base_card, drop_list, efficient = False):
    material_card_ids = []

    card_list = drop_list.copy()
    for card in card_list:
        if (not efficient or card['card_attribute_id'] == base_card['card_attribute_id']) and (card['card_rare'] == '1' or (int(card['card_rare']) <= 4 and card['card_soul_yellow'] == '1' and card['rock_flg'] == '0')):
            material_card_ids.append(card['user_card_id'])
            drop_list.remove(card)
        if (len(material_card_ids) == 10):
            break

    if (len(material_card_ids) == 0):
        return False

    normalPost('/1/cache/setCardMergeToken')

    data = getData()
    data['base_card_id'] = base_card['user_card_id']
    data['material_card_ids[]'] = material_card_ids
    try:
        after = session.post('http://' + host + '/1/Bromide/execMergeCard', data = data, timeout = 30).json()['action']['after']
    except:
        return True
    
    normalPost('/1/user/getUser')

    if int(after['card_level']) >= int(after['card_max_level']):
        print ("Level MAX!!!! " + base_card['card_name'].encode('gbk', 'ignore').decode('gbk'))
        target_card_list.remove((base_card['user_card_id'], int(base_card['card_attribute_id']) - 1))
        return False

    print ('Lv. ' + str(after['card_level']) + ' ' + base_card['card_name'].encode('gbk', 'ignore').decode('gbk'))
    
    return len(drop_list) > 0

def get_card_list():
    while True:
        try:
            return normalPost('/1/Bromide/getCardDataAll', 45).json()['action']
        except:
            pass

def merge_card(base_card_id, drop_cards = None, efficient = False):
    normalPost('/1/CardDeck/getDeckList', 30)
    data = getData()
    del data['user_id']
    data['support_id'] = '1'
    auto_post('/1/CardDeck/getSupportDeck', data, 30)

    card_list = get_card_list()
    drop_list = []
    base_card = None
    for card in card_list:
        if card['user_card_id'] == base_card_id: base_card = card
        if drop_cards is not None and card['user_card_id'] in drop_cards: drop_list.append(card)
    if drop_cards is None: drop_list = card_list
    
    while (merge(base_card, drop_list, efficient)):
        time.sleep(0.4)

    normalPost('/1/CardDeck/getDeckList', 30)

    if drop_cards is not None:
        drop_cards.clear()
        for card in drop_list:
            drop_cards.append(card['user_card_id'])

def get_card_info():
    normalPost('/1/CardDeck/getDeckList', 30)
    data = getData()
    del data['user_id']
    data['support_id'] = '1'
    auto_post('/1/CardDeck/getSupportDeck', data, 30)
    card_list = get_card_list()
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
    global reserveSR
    reserveSR = cfg.getboolean('clean', 'reserveSR')
    global allDecompose
    allDecompose = cfg.getboolean('clean', 'allDecompose')
    global gacha_turns
    gacha_turns = cfg.getint('clean', 'gacha_turns')
    global target_card_list
    target_card_list = eval(cfg.get('clean', 'target_card_list'))
    drop_only = cfg.getboolean('clean', 'drop_only')
    merge_only = cfg.getboolean('clean', 'merge_only')

    card_list = get_card_list()
    for card in card_list:
        if card['user_card_id'] in target_card_list:
            pos = target_card_list.index(card['user_card_id'])
            target_card_list[pos] = (target_card_list[pos], int(card['card_attribute_id']) - 1)

    init_time = datetime.datetime.now()
    for round_ in range(0, gacha_turns):
        if len(target_card_list) > 0:
            print ('round ' + str(round_))
            print ('spend ' + str((datetime.datetime.now() - init_time).seconds) + 's now')

            drop_list = None
            if not merge_only:
                try:
                    drop_list = gacha()
                except GachaError as gg:
                    print (gg.value)
                    return [_[0] for _ in target_card_list]
            target_card_list_ = list(target_card_list)
            attribute = [False] * 5
            for card in target_card_list_:
                if not attribute[card[1]]:
                    merge_card(card[0], drop_list, True)
                    if len(drop_list) == 0: break
                    attribute[card[1]] = True

            if len(target_card_list) > 0: merge_card(target_card_list[0][0], drop_list)
        else: break
        print ("                    get " + str(tot) + " pt now")
    return [_[0] for _ in target_card_list]
