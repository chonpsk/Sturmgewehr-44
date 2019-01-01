from .base import *
from .present import present
import requests
import time
import random
import datetime

def maxMaterialNum(material_list):
    n = 0
    for m in material_list.values():
        if int(m['user_material_count']) // int(m['material_item_quantity']) > n :
            n = int(m['user_material_count']) // int(m['material_item_quantity'])
    return n

def factoryExec(factory_id, item_id, separate):
    data = getData()
    del data['user_id']
    data['event_view_type'] = '2'
    auto_post('/1/EventManager/getEventList', data, 30)

    data = getData()
    del data['user_id']
    data['factory_id'] = factory_id
    material_list = auto_post('/1/Factory/getFactoryItemList', data, 30).json()['action']['factory_item_list'][item_id]['material_list']
    while maxMaterialNum(material_list) > 0:
        data = getData()
        del data['user_id']
        data['factory_item_id'] = item_id
        data['num'] = 1
        if not separate: data['num'] = maxMaterialNum(material_list)
        material_list = auto_post('/1/Factory/execCreateItem', data, 30).json()['action']['factory_item_list'][item_id]['material_list']

def ticketGacha(gacha_id):
    data = getData()
    data['detail_flg'] = '1'
    r = auto_post('/1/gacha/getGachaMstAll', data, 45)
    item_num = 0
    for gc in r.json()['action']:
        if gc['gacha_id'] == gacha_id: item_num = int(gc['user_item_num'])

    normalPost('/1/gacha/getGachaData')

    normalPost('/1/cache/setGachaToken')

    for i in range(0, item_num):
        normalPost('/1/cache/setGachaToken')
        data = getData()
        data['gacha_id'] = gacha_id
        auto_post('/1/gacha/execGacha', data, 30)
        time.sleep(0.4)

    normalPost('/1/user/getUser')

    data = getData()
    data['detail_flg'] = '1'
    auto_post('/1/gacha/getGachaMstAll', data, 45)

    normalPost('/1/gacha/getGachaData')


def otoshitama():
    factoryExec('710', '71001', False)
    present()
    ticketGacha('31')
    present()
    factoryExec('710', '71005', False)

