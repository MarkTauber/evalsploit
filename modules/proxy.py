import requests

def test(proxy):

    proxiy = []
    if ":" not in proxy: 
        print("Ты глупый? Мне самому порт угадывать?")
        return 'X'
    proxiy = proxy.split(":")

    proxies = {
    "http": f"http://{proxiy[0]}:{proxiy[1]}/",
    "https": f"http://{proxiy[0]}:{proxiy[1]}/"
    }

    url = 'https://api.ipify.org'

    try:
        response = requests.get(url, proxies=proxies)
        assert response.text==proxiy[0]
        return 'V'
    except:
        print ("Прокси гавно ебаное")
        return 'X'