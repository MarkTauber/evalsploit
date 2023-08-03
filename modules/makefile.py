import modules.send as send

def mkfile(url,pwd,com,uagent):
    with open('modules\\mf\\mf.php') as f:data = f.read()

    if "/" in com: #Проверка на абсолютный путь удяляемого
        data = data.replace("$cat = $_LOCAL;", f"$cat = \"{com}\";")
        X = send.send(url,data,uagent)
        if X == "X":
            print("Невозможно создать файл")
    else:
        data = data.replace("$cat = $_LOCAL;", f"$cat = \"{pwd+'/'+com}\";")
        X = send.send(url,data,uagent)
        if X == "X":
            print("Невозможно создать файл")