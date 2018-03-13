# Sturmgewehr-44

## Usage

Need to capture packets first. Use tools such as Fiddler4.

`/expedition/config.ini` is a config file template. You can use other config files also but config files must be put in `/expedition/` folder.

Get your `User-Agent`, `PLATFORM`, `AUTHORIZED-TOKEN`, `FullTime` and `max stamina` from packets and fill them into the config file.

Set what functions you need.

Save.

Run 
```
python3 start.py
```

## Function
### [present]
`friend` If receive the friendPTs from the gift box.

`gold` If receive the gold coins from the gift box.

`exp` The number of exp for each attribute. **not the number of experience materials**

The order of attributes is darkness, fire, water, plant, light.

### [accomplishment]
`friendPT` How many times you need to receive the friendPTs from accomplishment *"obtain 5000 pts per 200 rounds normal gacha"*.

### [clean]
`sellN` If sell card with rarity N. Or they will be fed to cards.

`allDecompose` If decompose all cards that can be decomposed. Or it won't decompose cards of 04.

`gacha_turns` The times you need to do normal gacha.

`target_card_list` Use all cards in the card box which is experience material or whose rarity is N to feed the assigned card.

Need to get `card_id` from `card_info`. The first column of `card_info` is the `card_id`.

`drop_only` If only use cards from last normal gacha.
