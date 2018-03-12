from ..transferLadle import base
from ..transferLadle import cleanFriendPT as clean
from ..transferLadle import present
from ..transferLadle import Accomplishment as acmp
import time
import datetime

base.headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 5 Build/LMY48B)'
base.headers['SBR-PLATFORM'] = 'Android'

base.headers['SBR-AUTHORIZED-TOKEN'] = 'e2fa4822fd6dad8ceb77795618f80c39'

base.setFullTime('2017-12-24 15:52:48')
base.stamina_max = 152

base.user_id = '14677228627537'

present.friend = True
present.gold = True
#present.present([0, 0, 0, 0, 0])
#exit()
clean.gacha_turns = 700
#clean.sellN = True
for card in ['1255587686', '1247258743', '1255507783', '1224617086', '1080846054', '1255253842', '1261434782', '1251423454', '1254001845']:
	clean.clean_drop_only(card)
	print (' ==== ' + card + ' cleaned ====')
