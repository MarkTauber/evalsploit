import os
import modules.exist as exist

def chdir(url,dir,pwd,uagent):
    if dir == "..":
        if pwd[-1]=="/":
            pwd = pwd[:-1]
        dir = os.path.dirname(pwd) 
        print(dir)
        return(dir)
        
    else:
        if "/" in dir:
            if exist.file(url,dir,uagent):
                dir = dir.replace('//','/').replace('//','/')
                return(dir)
        else:
            dir = pwd+'/'+dir  
            if exist.file(url,dir,uagent): 
                dir = dir.replace('//','/').replace('//','/')

                return (dir)
            else:
                print("Каталог не существует")
                return pwd

