from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("ls")
class LsModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        style = ctx.config.ls_style
        snip = load_snippet(style, "ls")
        if not snip:
            return "Snippet not found"
        directory = ctx.pwd if not args.strip() else ctx.resolve_path(args.strip())
        php = substitute(snip, {"__DIR_PLACEHOLDER__": php_quote(directory)})
        print("|       Date         |Type|R:W| Size  | Name")
        out = ctx.send(php)
        print(out)
        return None
