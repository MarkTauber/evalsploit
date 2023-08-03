import modules.send as send
import modules.exist as exist
import os

def obj(url,pwd,com,uagent):
    if com !="":
        what = com.split(" : ")[0]
        try: how = com.split(" : ")[1]
        except: 
            print("Ошибка, не указан конечный файл")
            return 0
        with open('modules\\rename\\rename.php') as f:data = f.read()
        if "/" in what: #Проверка на абсолютный путь копируемого
            if exist.file(url,what,uagent) == "1":
                data = data.replace("$cat = $_LOCAL;", f"$cat = \"{what}\";").replace("$ren = $_LOCAL;", f"$ren = \"{os.path.dirname(what)}/{os.path.basename(how)}\";")
                send.send(url,data,uagent)
                if exist.file(url,what,uagent) != "1":
                    print("Переименовано")
                else:
                    print("Ошибка")
            else:
                print("Файла не существует")
        else:
            if exist.file(url,pwd+'/'+what,uagent) == "1":
                data = data.replace("$cat = $_LOCAL;", f"$cat = \"{pwd+'/'+what}\";").replace("$ren = $_LOCAL;", f"$ren = \"{pwd}/{os.path.basename(how)}\";")
                send.send(url,data,uagent)
                if exist.file(url,what,uagent) != "1":
                    print("Переименовано")
                else:
                    print("Ошибка")
            else:
                print("Файла не существует")