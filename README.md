# Sturmgewehr-44

## Usage

Need to capture packets first. Use tools such as Fiddler4.

`/expedition/service.py` is a config file template.

Get your `User-Agent`, `PLATFORM`, `AUTHORIZED-TOKEN`, `FullTime` and `max stamina` from packets and fill them into the config file.

Set what functions you need.

Save.

Run 
```
python3 -m Sturmgewehr-44.expediton.service
```

## Function
### present.friend
If receive the friendPTs from the gift box.

### present.gold
If receive the gold coins from the gift box.

### acmp.get_friendPT
Receive the friendPTs from accomplishment *"obtain 5000 pts per 200 rounds normal gacha"*.

You can set how many times it receive.

### present.present([ , , , , ])
Receive scores, evolution materials, friendPTs(if you set), gold coins(if you set), experience materials from the gift box.

You can set the number of exp for each attribute. **not the number of experience materials**

The order of attributes is darkness, fire, water, plant, light.

### clean.sellN
if sell card with rarity N. Or they will be fed to cards.

### clean.allDecompose
if decompose all cards that can be decomposed. Or it won't decompose cards of 04.

### clean.gacha_turns
the times you want to do normal gacha.

### clean.clean
Use all cards in the card box which is experience material or whose rarity is N to feed the assigned card.

Need get `card_id` from packets.

### clean.clean_drop_only
Only use cards from last normal gacha.
