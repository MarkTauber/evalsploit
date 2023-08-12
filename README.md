# evalsploit
Бэкдор, основанный на `eval` функции 


### Особенности

-   **Тихая работа**: The framework is made by paranoids, for paranoids
    -   Работа на POST-запросах, практическая невидимая для логов
    -   Встроенная надстройка для байпаса WAF
    -   Новый юзерагент каждую новую сессию
    -   Тихий режим работы 

-   **Универсальный**
    -   Встроенная надстройка для байпаса WAF
    -   Новый юзерагент каждую новую сессию
    -   Тихий режим работы 

--

# Руководство

#### Работа с файловой системой

-   `ls`: список файлов в директории 
    -   Надстройка `ls`: основано на функции DirectoryIterator (стоит по умолчанию)
	-   Надстройка `dir`: основано на функции ScanDir

-   `cp`: копирование файлов
    -   Использовать разделитель ` : ` (/что.txt : /куда/что.txt)

-   `cd`: перемещение по файловой системе

-	`mkd`: создать новую директорию

-	`upl`: загрузить файл на сервер

-	`home`: вернуться в __DIR__

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

-	`set`: настройка модулей. Чтобы посмотреть список параметров использовать `set модуль help` (так же вместо help допустимы -h, h, ?, /?)
	-	**run**: exec, shell_exec, system, passthru, popen, proc_open, expect_popen, pcntl_exec, do
	-	**ls**: ls, dir
	-	**cat**: html, base64
	-	**silent**: 1, 0 (тихий режим)
	-	**reverse**: ivan, monkey 
	-	**send**: bypass, classic, simple (модуль отправки)
	
