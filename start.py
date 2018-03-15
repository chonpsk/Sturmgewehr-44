from transferLadle.base import set_config
from transferLadle.base import login
from transferLadle import cleanFriendPT as clean
from transferLadle import present
from transferLadle import accomplishment as acmp
import time
import datetime
import os
from configparser import ConfigParser

config = 'config.ini'
config_path = os.path.dirname(os.path.realpath(__file__)) + '\\expedition\\' + config
cfg = ConfigParser()
cfg.read(config_path)
set_config(config_path)
if not cfg.getboolean('login', 'if_logined'):
	login(cfg)

acmp.get_friendPT()
present.present()
card_info = clean.get_card_info()
fl = open(os.path.dirname(os.path.realpath(__file__)) + '\\card_info', 'w')
for card in card_info:
	print (card, file = fl)
target_card_list = clean.clean()

cfg.set('clean', 'target_card_list', str(target_card_list))

cfg.write(open(config_path, 'w'))
