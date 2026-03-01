from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("mkdir")
class MkdModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        path = ctx.resolve_path(args.strip())
        snip = load_snippet(ctx.config.snippet_md or "md", "md")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(path)})
        out = ctx.send(php)
        if "X" in out:
            print(f"Error: {out}")
        else:
            print("Directory created")
        return None


register("md")(MkdModule)
register("mkd")(MkdModule)
