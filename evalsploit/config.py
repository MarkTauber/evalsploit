"""Single config layer: global settings and session (url + keys)."""

from __future__ import annotations

import configparser
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

from evalsploit.modules.base import get_styles


def _project_root() -> Path:
    """Project root (where data/, pyproject.toml live)."""
    # __file__ is evalsploit/evalsploit/config.py or evalsploit/evalsploit/transport/...
    p = Path(__file__).resolve().parent
    while p.name != "evalsploit":
        p = p.parent
    # p is .../evalsploit (package dir); project root is parent
    root = p.parent
    if (root / "pyproject.toml").exists():
        return root
    return p  # fallback: package dir as root


def project_root() -> Path:
    """Public project root."""
    return _project_root()


@dataclass
class EvalsploitConfig:
    """Global settings (from settings.ini) and current connection (url, Z, V)."""

    # Connection (can be overridden by session)
    url: str = ""
    Z: str = "Z"
    V: str = "V"
    send_mode: str = "bypass"  # bypass | classic | simple

    # Global preferences
    proxy: str = ""
    proxy_list: list[str] = field(default_factory=list)
    proxy_validated: list[int] = field(default_factory=list)  # 0-based indices
    proxy_enabled: bool = False
    proxy_use_index: int | None = None  # None = random, else index into proxy_list
    _proxy_session: str | None = field(default=None, repr=False)  # cache for random mode
    ls_style: str = "ls"  # ls | dir
    cat_style: str = "bcat"  # from snippets.ini [cat]; legacy: base64->bcat, html->cat
    run_shell: str = "exec"
    silent: bool = False
    reverse_type: str = "monkey"  # monkey | ivan
    confirm: bool = True  # prompt for dangerous ops (rm, mutate, upl, edit)

    # Snippet choice per command (from snippets.ini; set via set rm, set dl, ...)
    snippet_rm: str = "rm"
    snippet_dl: str = "dl"
    snippet_upload: str = "upload"
    snippet_rename: str = "rename"
    snippet_stat: str = "stat"
    snippet_touch: str = "touch"
    snippet_mf: str = "mf"
    snippet_md: str = "md"
    snippet_copy: str = "copy"

    # Paths
    _root: Path = field(default_factory=_project_root, repr=False)

    @property
    def data_dir(self) -> Path:
        return self._root / "data"

    @property
    def sessions_dir(self) -> Path:
        d = self.data_dir / "sessions"
        d.mkdir(parents=True, exist_ok=True)
        return d

    @property
    def settings_path(self) -> Path:
        return self.data_dir / "settings.ini"

    @property
    def proxies_file(self) -> Path:
        return self.data_dir / "proxies.txt"

    def get_current_proxy(self) -> str:
        """Return proxy string for current request; one per session when random."""
        if not self.proxy_enabled or not self.proxy_list:
            self._proxy_session = None
            return ""
        if self.proxy_use_index is None:
            if self._proxy_session is not None:
                return self._proxy_session
            pool = (
                [self.proxy_list[i] for i in self.proxy_validated]
                if self.proxy_validated
                else self.proxy_list
            )
            if not pool:
                return ""
            chosen = random.choice(pool)
            self._proxy_session = chosen
            return chosen
        idx = self.proxy_use_index
        if idx < 0 or idx >= len(self.proxy_list):
            return ""
        return self.proxy_list[idx]

    def clear_proxy_session_cache(self) -> None:
        """Reset session proxy cache (e.g. for proxy_switch)."""
        self._proxy_session = None

    def load_global(self) -> None:
        """Load from data/settings.ini."""
        path = self.settings_path
        if not path.exists():
            self._ensure_data_dir()
            return
        cfg = configparser.ConfigParser()
        cfg.read(path, encoding="utf-8")
        s = cfg.get("SETTINGS", "url", fallback=self.url)
        if s:
            self.url = s
        self.Z = cfg.get("SETTINGS", "Z", fallback=self.Z)
        self.V = cfg.get("SETTINGS", "V", fallback=self.V)
        self.send_mode = cfg.get("SETTINGS", "send", fallback=self.send_mode).lower()
        self.proxy = cfg.get("SETTINGS", "proxy", fallback=self.proxy)
        if cfg.has_option("SETTINGS", "proxy_enabled"):
            self.proxy_enabled = cfg.get("SETTINGS", "proxy_enabled", fallback="0") == "1"
        if cfg.has_option("SETTINGS", "proxy_use_index"):
            val = cfg.get("SETTINGS", "proxy_use_index", fallback="random").strip().lower()
            if val == "random" or val == "":
                self.proxy_use_index = None
            else:
                try:
                    self.proxy_use_index = int(val)
                except ValueError:
                    self.proxy_use_index = None
        px_path = self.proxies_file
        if px_path.exists():
            lines = []
            for line in px_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and ":" in line:
                    lines.append(line)
            self.proxy_list = lines
        if not self.proxy_list and self.proxy and ":" in self.proxy:
            self.proxy_list = [self.proxy]
        self.ls_style = cfg.get("SETTINGS", "ls", fallback=self.ls_style)
        read_val = cfg.get("SETTINGS", "read", fallback=self.cat_style)
        if read_val == "base64":
            self.cat_style = "bcat"
        elif read_val == "html":
            self.cat_style = "cat"
        else:
            self.cat_style = read_val
        self.run_shell = cfg.get("SETTINGS", "shell", fallback=self.run_shell)
        self.silent = cfg.get("SETTINGS", "silent", fallback="0") == "1"
        self.reverse_type = cfg.get("SETTINGS", "reverse", fallback=self.reverse_type)
        self.confirm = cfg.get("SETTINGS", "confirm", fallback="1") == "1"
        if cfg.has_section("SNIPPETS"):
            self.snippet_rm = cfg.get("SNIPPETS", "rm", fallback=self.snippet_rm)
            self.snippet_dl = cfg.get("SNIPPETS", "dl", fallback=self.snippet_dl)
            self.snippet_upload = cfg.get("SNIPPETS", "upload", fallback=self.snippet_upload)
            self.snippet_rename = cfg.get("SNIPPETS", "rename", fallback=self.snippet_rename)
            self.snippet_stat = cfg.get("SNIPPETS", "stat", fallback=self.snippet_stat)
            self.snippet_touch = cfg.get("SNIPPETS", "touch", fallback=self.snippet_touch)
            self.snippet_mf = cfg.get("SNIPPETS", "mf", fallback=self.snippet_mf)
            self.snippet_md = cfg.get("SNIPPETS", "md", fallback=self.snippet_md)
            self.snippet_copy = cfg.get("SNIPPETS", "copy", fallback=self.snippet_copy)
        self._validate_snippet_keys()

    def save_global(self) -> None:
        """Save to data/settings.ini."""
        self._ensure_data_dir()
        cfg = configparser.ConfigParser()
        proxy_use_val = "random" if self.proxy_use_index is None else str(self.proxy_use_index)
        cfg["SETTINGS"] = {
            "url": self.url,
            "Z": self.Z,
            "V": self.V,
            "send": self.send_mode,
            "proxy": self.proxy_list[0] if self.proxy_list else self.proxy,
            "proxy_enabled": "1" if self.proxy_enabled else "0",
            "proxy_use_index": proxy_use_val,
            "ls": self.ls_style,
            "read": self.cat_style,
            "shell": self.run_shell,
            "silent": "1" if self.silent else "0",
            "reverse": self.reverse_type,
            "confirm": "1" if self.confirm else "0",
        }
        cfg["SNIPPETS"] = {
            "rm": self.snippet_rm,
            "dl": self.snippet_dl,
            "upload": self.snippet_upload,
            "rename": self.snippet_rename,
            "stat": self.snippet_stat,
            "touch": self.snippet_touch,
            "mf": self.snippet_mf,
            "md": self.snippet_md,
            "copy": self.snippet_copy,
        }
        with open(self.settings_path, "w", encoding="utf-8") as f:
            cfg.write(f)
        self.proxies_file.write_text("\n".join(self.proxy_list), encoding="utf-8")

    def _ensure_data_dir(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _validate_snippet_keys(self) -> None:
        """Ensure each snippet_* value is a valid key for its category; reset and warn if not."""
        defaults = {
            "rm": "rm", "dl": "dl", "upload": "upload", "rename": "rename",
            "stat": "stat", "touch": "touch", "mf": "mf", "md": "md", "copy": "copy",
        }
        for category, default in defaults.items():
            attr = f"snippet_{category}"
            val = getattr(self, attr)
            styles = get_styles(category)
            if styles and val not in styles:
                setattr(self, attr, default if default in styles else styles[0])
                print(f"[evalsploit] Unknown snippet key {val!r} for {category}, using {getattr(self, attr)!r}", file=sys.stderr)

    def load_session(self, session_name: str) -> bool:
        """Load url, Z, V from data/sessions/<name>.ini. Returns True if loaded."""
        path = self.sessions_dir / f"{session_name}.ini"
        if not path.exists():
            return False
        cfg = configparser.ConfigParser()
        cfg.read(path, encoding="utf-8")
        self.url = cfg.get("SESSION", "url", fallback=self.url)
        self.Z = cfg.get("SESSION", "Z", fallback=self.Z)
        self.V = cfg.get("SESSION", "V", fallback=self.V)
        if cfg.has_option("SESSION", "send_mode"):
            self.send_mode = cfg.get("SESSION", "send_mode")
        if cfg.has_option("SESSION", "silent"):
            self.silent = cfg.get("SESSION", "silent", fallback="0") == "1"
        return True

    def save_session(self, session_name: str) -> None:
        """Save current url, Z, V to data/sessions/<name>.ini."""
        cfg = configparser.ConfigParser()
        cfg["SESSION"] = {
            "url": self.url,
            "Z": self.Z,
            "V": self.V,
            "send_mode": self.send_mode,
            "silent": "1" if self.silent else "0",
        }
        path = self.sessions_dir / f"{session_name}.ini"
        with open(path, "w", encoding="utf-8") as f:
            cfg.write(f)

    def list_sessions(self) -> list[str]:
        """Return session names (filename without .ini)."""
        names: list[str] = []
        for p in self.sessions_dir.glob("*.ini"):
            names.append(p.stem)
        return sorted(names)
