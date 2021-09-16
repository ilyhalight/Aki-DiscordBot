import discord
import requests
import math
from scripts.parsers.links import links


WINDOWS_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36'}
crypto_emoji = {
    'btc': '<:btc:888036655980773417>',
    'eth': '<:eth:888036682052567060>',
    'ada': '<:ada:888036720967319562>',
    'bnb': '<:bnb:888036734376509471>',
    'usdt': '<:usdt:888036749878628362>',
    'xrp': '<:xrp:888036807885848616>',
    'zec': '<:zec:888036826797985813>',
    'dash': '<:dash:888036840936996874>',
    'ltc': '<:ltc:888036851523420210>'
}

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
        crypto_courses.append({
            'crypto' : crypto,
            'price' : price
        })
        i = i + 1

    for items in crypto_courses:
        if items['crypto'].lower() in crypto_emoji:
            emoji = crypto_emoji[items['crypto'].lower()]
        else:
            emoji = ':coin:'
        emb.add_field(name = f'{emoji}{items["crypto"]}', value = f'{items["price"]} ₽', inline = True)
        # Вы можете добавить до 25 криптовалют. Дальше не проверял.