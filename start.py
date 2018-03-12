from transferLadle.base import set_config
from transferLadle import cleanFriendPT as clean
from transferLadle import present
from transferLadle import accomplishment as acmp
import time
import datetime
import os
from configparser import ConfigParser

config = 'config.ini'
config_path = os.path.dirname(os.path.realpath(__file__)) + '\\expedition\\' + config
set_config(config_path)

acmp.get_friendPT()
present.present()
clean.get_card_info()
target_card_list = clean.clean()

try:
	cfg = ConfigParser()
	cfg.read(config_path)
	cfg.set('clean', 'target_card_list', str(target_card_list))
	cfg.write(open(config_path, 'w'))
except:
	pass
