from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("ren")
class RenModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        parts = [p.strip() for p in args.split(":", 1)]
        if len(parts) != 2:
            print("Use: ren old_path : new_path")
            return None
        old_path = ctx.resolve_path(parts[0])
        new_path = ctx.resolve_path(parts[1])
        if not ctx.file_exists(old_path):
            print("Source does not exist")
            return None
        snip = load_snippet(ctx.config.snippet_rename or "rename", "rename")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(old_path), "$_REMOTE": php_quote(new_path)})
        ctx.send(php)
        print("Renamed")
        return None


register("mv")(RenModule)
