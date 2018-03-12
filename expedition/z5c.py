from ..transferLadle import base
from ..transferLadle import cleanFriendPT as clean
from ..transferLadle import present
from ..transferLadle import Accomplishment as acmp
import time
import datetime

base.headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 6.0; SO-02H Build/32.1.F.1.38)'
base.headers['SBR-PLATFORM'] = 'Android'

base.headers['SBR-AUTHORIZED-TOKEN'] = 'ffeb26eb1c56eb3625c8ff12db74b7ee'

base.setFullTime('2017-08-20 18:44:04')
base.stamina_max = 176

base.user_id = '14551639695147'

#present.friend = True
#present.gold = True
#present.present()
for card in ['1179963374', '1179963329', '1187633681', '1185241842', '1188741577', '1187558171']:
	clean.clean(card)
	print (' ==== ' + card + ' cleaned ====')
