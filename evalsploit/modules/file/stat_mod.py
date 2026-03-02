from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("stat", description="File or directory info (size, permissions, dates)", usage="stat [path]")
class StatModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        path = ctx.resolve_path(args.strip()) if args.strip() else ctx.pwd
        snip = load_snippet(ctx.config.snippet_stat or "stat", "stat")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"__DIR_PLACEHOLDER__": php_quote(path)})
        print(ctx.send(php))
        return None
