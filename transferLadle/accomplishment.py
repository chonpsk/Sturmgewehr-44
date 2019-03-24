# -*- coding: UTF-8 -*-

from .base import *
import requests
import time
import datetime

def getList():
    data = getData()
    data['state'] = '3'
    return auto_post('/1/Accomplishment/getAccomplishmentList', data, 30).json()['action']['not_received']

def receive(acmp_lst_id, acc_ids, tot = 999):
    while tot > 0:
        acmp_lst = getList()[acmp_lst_id]
        acc_ids_ = acc_ids.copy()
        for acc in acc_ids_:
            if acmp_lst[acc]['complete_flg']:
                acc_ids.remove(acc)
        if len(acc_ids) == 0:
            return False
        data = getData()
        data['accomplishment_ids[]'] = acc_ids
        try:
            session.post('http://' + host + '/1/Accomplishment/receiveAccomplishmentRewardBundle', data = data, timeout = 30)
        except:
            pass
        tot -= 1
        time.sleep(0.2)
    return True

def accomplishment():
    print ('accomplishment start')
    init_time = datetime.datetime.now()
    not_received = getList()
    for state in range(1, 4):
        time.sleep(0.2)
        receive(str(state), not_received[str(state)])
        print ('spend ' + str((datetime.datetime.now() - init_time).seconds) + 's now')

def get_friendPT():
    tot = cfg.getint('accomplishment', 'friendPT')
    receive('3', ['40700101'], tot)
