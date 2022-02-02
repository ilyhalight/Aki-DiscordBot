import discord
import requests
import math

from scripts.parsers.links import links
from scripts.parsers.emojis import emojis


WINDOWS_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36'}

crypto_emoji = emojis['crypto_currency']

def parse_cryptonator(emb: discord.Embed):
    """Парсинг курса крипты с cryptonator (https://www.cryptonator.com/api)

    Args:
        None

    Returns:
        rates_array: [USD, EUR, Au, Ag, Pt, Pd]
    """
    cryptonator = links['cryptonator']
    coins = cryptonator['coins']

    crypto_courses = []
    i = 0
    while i != len(coins):
        response = requests.get(f'{cryptonator["url"]}{coins[i]}-{cryptonator["currency"]}', headers = WINDOWS_AGENT)
        response_json = response.json()['ticker']
        crypto = response_json['base']
        price_str = response_json['price']
        price = float(price_str)
        price = math.floor(price)
        price_beautiful = f'{price:,}'
        price_end = price_beautiful.replace(',', '.')
        crypto_courses.append({
            'crypto' : crypto,
            'price' : price_end
        })
        i = i + 1

    for items in crypto_courses:
        if items['crypto'].lower() in crypto_emoji:
            emoji = crypto_emoji[items['crypto'].lower()]
        else:
            emoji = ':coin:'
        emb.add_field(name = f'{emoji} {items["crypto"]}', value = f'{items["price"]} ₽', inline = True)