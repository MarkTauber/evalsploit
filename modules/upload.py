import modules.send as send
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from base64 import b64encode
import base64
import os

def upload(url,pwd,uagent):
    Tk().withdraw() 
    filename = askopenfilename() 
    if filename == "":
        print("Ошибка выбора файла")
        return 0
    with open(filename, "rb") as fuf:
        base = b64encode(fuf.read())

    name = os.path.basename(filename)

    if 'INetCache' in filename: 
        if '[1][1].' in filename: name = name.replace('[1][1].','[1].')
        else:name = name.replace('[1]','')

    with open('modules\\upload\\upload.php') as f:data = f.read()
    data = data.replace("$cat = $_LOCAL;", f"$cat = \'{pwd+'/'+name}\';").replace("$base = $_BASE;", f"$base = {base};")
    
    if send.send(url,data,uagent) != "X":
        print("Файл загружен")
    else:
        print("Ошибка загрузки")