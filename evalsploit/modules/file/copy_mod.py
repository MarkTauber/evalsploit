from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("cp")
class CopyModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        parts = [p.strip() for p in args.split(":", 1)]
        if len(parts) != 2:
            print("Use: cp from : to")
            return None
        what = ctx.resolve_path(parts[0])
        where = ctx.resolve_path(parts[1])
        if not ctx.file_exists(what):
            print("Source does not exist")
            return None
        snip = load_snippet(ctx.config.snippet_copy or "copy", "copy")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"__WHAT__": php_quote(what), "__WHERE__": php_quote(where)})
        out = ctx.send(php)
        if "+" in out:
            print("Copied")
        else:
            print(out)
        return None
