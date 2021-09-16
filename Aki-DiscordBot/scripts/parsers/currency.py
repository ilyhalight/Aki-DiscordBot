import requests
from bs4 import BeautifulSoup
from scripts.parsers.links import links


WINDOWS_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36'}


def parse_cbr():
    """Парсинг USD, EUR, Au, Ag, Pt, Pd с ЦБР (www.cbr.ru)

    Args:
        None

    Returns:
        rates_array: [USD, EUR, Au, Ag, Pt, Pd]
    """
    cbr = links['cbr']
    response = requests.get(cbr['url'], headers = WINDOWS_AGENT)
    soup = BeautifulSoup(response.content, 'html.parser')
    rates = soup.findAll('td', {'class': cbr['find']})

    rates_array = []
    for rate in rates:
        rate = rate.text.replace(',', '.').replace(' ', '')
        rate = float(rate)
        rates_array.append(rate)
    return rates_array