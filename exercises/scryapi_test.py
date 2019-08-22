#!/usr/bin/env python3


import requests
import json


#card_name = 'Jaya, Venerated Firemage'
card_name = 'chuchu'
url = 'https://api.scryfall.com/cards/named?'
parameters = {'fuzzy': card_name, 'format': 'json'}

r = requests.get(url=url, params=parameters)
if r.status_code == 404:
    print('Could not find')
else:    
    content = r.json()
    price = content['prices']['eur']
    card_image = content['image_uris']['normal']
    set_code = content['set']
    print(price)
    print(card_image)
    print(set_code)

# except Exception as e:
#     print(e)

# try:
# card = scrython.cards.Named(fuzzy=card_name)
# time.sleep(1)
# print(card.mana_cost())
# print(card.colors())
# print(card.oracle_text())
#card.image_uris()['normal'] # image
# r = requests.get(card.uri())
# content = r.json()

# price = content['prices']['eur']
# card_image = content['image_uris']['normal']
# set_code = content['set']

# print(price)
# print(card_image)
# print(set_code)
# except Exception as e:
#   print(e)