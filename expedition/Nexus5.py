from ..transferLadle import base
from ..transferLadle import cleanFriendPT as clean
from ..transferLadle import present
from ..transferLadle import Accomplishment as acmp
import time
import datetime

base.headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 5 Build/LMY48B)'
base.headers['SBR-PLATFORM'] = 'Android'

base.headers['SBR-AUTHORIZED-TOKEN'] = '58c81af3ad61704034389296842d3d39'

base.setFullTime('2018-03-04 00:26:19')
base.stamina_max = 188

base.user_id = '14551639695147'

present.friend = True
present.gold = True
acmp.get_friendPT(30)
#present.present([20000, 10000, 0, 0, 0])
present.present([0, 0, 0, 0, 0])
#exit()
for card in ['1279834773', '1279837009', '1279834434']:
	clean.clean_drop_only(card)
	print (' ==== ' + card + ' cleaned ====')
