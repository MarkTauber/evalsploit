import modules.send as send

def file(url,file,uagent):
    with open('modules\\exist\\exist.php') as f:data = f.read()
    data = data.replace("$directory = __DIR__;", f"$directory = \'{file}\';")
    return send.send(url,data,uagent)