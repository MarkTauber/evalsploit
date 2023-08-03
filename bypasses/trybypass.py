import modules.send as send
def cmd(url,uagent):
    with open('bypasses\\try\\try.php') as f:data = f.read()
    return send.send(url,data,uagent)
