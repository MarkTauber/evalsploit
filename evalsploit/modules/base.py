"""Base module and snippet loading."""

from __future__ import annotations

import configparser
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


def _snippets_dir() -> Path:
    return Path(__file__).resolve().parent / "snippets"


_SNIPPETS_CONFIG: Optional[configparser.ConfigParser] = None


def _get_snippets_config() -> Optional[configparser.ConfigParser]:
    global _SNIPPETS_CONFIG
    if _SNIPPETS_CONFIG is None:
        path = _snippets_dir() / "snippets.ini"
        if path.exists():
            _SNIPPETS_CONFIG = configparser.ConfigParser()
            _SNIPPETS_CONFIG.read(path, encoding="utf-8")
    return _SNIPPETS_CONFIG


_DEFAULT_STYLES: dict[str, list[str]] = {
    "ls": ["dir", "ls"],
    "cat": ["bcat", "cat"],
    "rm": ["rm"],
    "dl": ["dl"],
    "upload": ["upload"],
    "rename": ["rename"],
    "stat": ["stat"],
    "touch": ["touch"],
    "mf": ["mf"],
    "md": ["md"],
    "copy": ["copy"],
}


def get_styles(category: str) -> List[str]:
    """Return list of style names for a category from snippets.ini, or default list."""
    cfg = _get_snippets_config()
    if cfg and cfg.has_section(category):
        return sorted(cfg.options(category))
    return _DEFAULT_STYLES.get(category, [])


def load_snippet(name: str, category: Optional[str] = None) -> Optional[str]:
    """Load PHP snippet. If category is set, use snippets.ini [category] name=file. Else snippets/<name>.php."""
    root = _snippets_dir()
    if category:
        cfg = _get_snippets_config()
        if cfg and cfg.has_section(category) and cfg.has_option(category, name):
            name = cfg.get(category, name).strip()
        path = root / name if name.endswith(".php") else root / f"{name}.php"
    else:
        path = root / f"{name}.php"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


class Module:
    """Base for all commands. Override run()."""

    name: str = ""

    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        """Execute command. Return optional message; may print instead."""
        raise NotImplementedError


def php_quote(s: str) -> str:
    """Escape and wrap string for PHP single-quoted literal (paths, commands, base64)."""
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def substitute(php: str, replacements: dict[str, str]) -> str:
    """Replace placeholders in PHP. Keys must match exactly (e.g. $_LOCAL, $directory)."""
    for k, v in replacements.items():
        php = php.replace(k, v)
    return php


def confirm_dangerous(ctx: "SessionContext", action: str, detail: str = "") -> bool:
    """If config.confirm is False, return True. Else prompt; return True only for y/yes."""
    if not getattr(ctx.config, "confirm", True):
        return True
    msg = f"Confirm {action}?"
    if detail:
        msg += f" ({detail})"
    msg += " [y/N] "
    try:
        ans = input(msg).strip().lower()
        return ans in ("y", "yes")
    except EOFError:
        return False
