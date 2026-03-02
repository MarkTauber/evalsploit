from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("touch", description="Touch file (update timestamp or create empty)", usage="touch <path> [settime YYYY-MM-DD HH:MM:SS]")
class TouchModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        parts = args.split("settime", 1)
        path = ctx.resolve_path(parts[0].strip())
        date_sec = None
        if len(parts) > 1:
            # "Year-Month-Day Hour:Minute:Second"
            from datetime import datetime
            try:
                date_sec = int(datetime.strptime(parts[1].strip(), "%Y-%m-%d %H:%M:%S").timestamp())
            except ValueError:
                pass
        if date_sec is None:
            date_str = "time()"
        else:
            date_str = str(date_sec)
        snip = load_snippet(ctx.config.snippet_touch or "touch", "touch")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(path), "$_DATE": date_str})
        out = ctx.send(php)
        if "X" in out:
            print("Touch failed")
        else:
            print("Done")
        return None
