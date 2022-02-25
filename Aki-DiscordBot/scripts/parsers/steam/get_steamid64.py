import requests
import xml.etree.ElementTree as ET

from core.logger import logger

WINDOWS_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36'}

def get_steamid64(url):
    try:
        response = requests.get(url + '/?xml=1', headers=WINDOWS_AGENT).text
        myroot = ET.fromstring(response)
        steamid64 = myroot.find('steamID64').text
        return steamid64
    except:
        return None