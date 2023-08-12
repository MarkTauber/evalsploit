import configparser

def sets(com):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    shell =config['SETTINGS']['shell']
    read = config['SETTINGS']['read']
    listdir = config['SETTINGS']['ls']
    silent = config['SETTINGS']['silent']
    reverse = config['SETTINGS']['reverse']
    ts = config['SETTINGS']['send']

    if com !="":
                command = com.split(" ")[0].lower()
                try: setting = com.split(" ")[1].lower()
                except: 
                    print("Ошибка, не указан параметр")

                if command == "run":
                    if setting in ("h","-h","help","?","/?","-h"):
                        print("Список поддерживаемых параметров:")
                        print("exec, expect_popen, passthru, system, shell_exec, popen, proc_open, pcntl_exec")
                        print()
                        print("Сейчас установлен модуль "+shell)
                    else:
                        if setting in ("exec", "expect_popen", "passthru", "system", "shell_exec", "popen", "proc_open", "pcntl_exec"):
                            config['SETTINGS']['shell']=setting
                            with open('settings.ini', 'w') as configfile:
                                config.write(configfile)
                            print("Установлен модуль выполнения "+setting)
                            shell =config['SETTINGS']['shell']
                        else: 
                            print("Этот параметр не поддерживается")
                            print("чтобы узнать список поддерживаемых параметров CMD используйте h")
                
                if command == "ls":
                    if setting in ("h","-h","help","?","/?","-h"):
                        print("Список поддерживаемых параметров:")
                        print("ls, dir")
                        print()
                        print("Сейчас установлен модуль "+listdir)
                    else:
                        if setting in ("ls","dir"):
                            config['SETTINGS']['ls']=setting
                            with open('settings.ini', 'w') as configfile:
                                config.write(configfile)
                            print("Установлен модуль директорий "+setting)
                            listdir = config['SETTINGS']['ls']
                        else: 
                            print("Этот параметр не поддерживается")
                            print("чтобы узнать список поддерживаемых параметров ls используйте h")
                
                if command == "cat":
                    if setting in ("h","-h","help","?","/?","-h"):
                        print("Список поддерживаемых параметров:")
                        print("html, base64")
                        print()
                        print("Сейчас установлен модуль "+read)
                    else:
                        if setting in ("base64","html"):
                            config['SETTINGS']['read']=setting
                            with open('settings.ini', 'w') as configfile:
                                config.write(configfile)
                            print("Установлен модуль директорий "+setting)
                            read = config['SETTINGS']['read']
                        else: 
                            print("Этот параметр не поддерживается")
                            print("чтобы узнать список поддерживаемых параметров cat используйте h")
                 
                if command == "silent":
                    if setting in ("h","-h","help","?","/?","-h"):
                        print("Список поддерживаемых параметров:")
                        print("1, 0")
                        if silent == "1":
                            print("Тихий режим ВКЛЮЧЕН")
                        else:
                            print("Тихий режим ВЫКЛЮЧЕН")
                    else:  
                        if setting in ("1","0"):
                            config['SETTINGS']['silent'] = setting
                            with open('settings.ini', 'w') as configfile:
                                config.write(configfile)
                            silent = config['SETTINGS']['silent']
                            if silent == "1":
                                print("Тихий режим ВКЛЮЧЕН")
                            else:
                                print("Тихий режим ВЫКЛЮЧЕН")

                if command == "reverse":
                    if setting in ("h","-h","help","?","/?","-h"):
                        print("Список поддерживаемых параметров:")
                        print("ivan, monkey")
                        print()
                        print("Сейчас установлен модуль "+reverse)
                    else:
                        if setting in ("ivan","monkey"):
                            config['SETTINGS']['reverse']=setting
                            with open('settings.ini', 'w') as configfile:
                                config.write(configfile)
                            print("Установлен reverse-shell "+setting)
                            reverse = config['SETTINGS']['reverse']
                        else: 
                            print("Этот параметр не поддерживается")
                            print("чтобы узнать список поддерживаемых параметров reverse-shell используйте h")

                if command == "send":
                    if setting in ("h","-h","help","?","/?","-h"):
                        print("Список поддерживаемых параметров:")
                        print("bypass, classic, simple")
                        print()
                        print("Сейчас установлен модуль "+ ts)
                    else:
                        if setting in ("bypass","classic","simple"):
                            config['SETTINGS']['send']=setting
                            with open('settings.ini', 'w') as configfile:
                                config.write(configfile)
                            print("Установлен send "+setting)
                            ts = config['SETTINGS']['send']
                        else: 
                            print("Этот параметр не поддерживается")
                            print("чтобы узнать список поддерживаемых параметров send используйте h")
                    
                
    return shell,read,listdir,silent,reverse,ts