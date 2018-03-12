from ..transferLadle import base
from ..transferLadle import cleanFriendPT as clean
from ..transferLadle import present
from ..transferLadle import Accomplishment as acmp
import time
import datetime

base.headers['User-Agent'] = 'SB69/4.5.4 CFNetwork/758.5.3 Darwin/15.6.0'
base.headers['SBR-PLATFORM'] = 'iOS'

base.headers['SBR-AUTHORIZED-TOKEN'] = 'eb2eeb1fe1d16cf5c60a933b033640f5'

base.setFullTime('2017-06-16 21:08:23')
base.stamina_max = 183

base.user_id = '14437337035616'

acmp.accomplishment()
present.friend = True
present.present()
clean.sellN = True
for card in ['1109977840', '1110746009']:
	clean.clean(card, 9)
	print (' ==== ' + card + ' cleaned ====')
