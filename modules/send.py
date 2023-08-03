import requests
import base64
from os import urandom

def send(url, data, uagent):


    r = requests.post(url, data={'Z': data},headers={"User-Agent" : uagent})
    return(r.text)