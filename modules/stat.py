import modules.send as send
import modules.exist as exist

def data(url,pwd,com,uagent):
    with open('modules\\stat\\stat.php') as f:data = f.read()
    if "/" in com: #Проверка на абсолютный путь удяляемого
        if exist.file(url,com,uagent) == "1":
            data = data.replace("$directory = __DIR__;", f"$directory = \'{com}\';")
            print(send.send(url,data,uagent))
        else:
            print("Файла не существует")
    else:
        if exist.file(url,pwd+'/'+com,uagent) == "1":
            data = data.replace("$directory = __DIR__;", f"$directory = \'{pwd+'/'+com}\';")
            print(send.send(url,data,uagent))
        else:
            print("Файла не существует")