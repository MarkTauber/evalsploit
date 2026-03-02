from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote, confirm_dangerous
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("rm", description="Delete file", usage="rm <path>")
class RmModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        path = ctx.resolve_path(args.strip())
        if not confirm_dangerous(ctx, "rm", path):
            return None
        snip = load_snippet(ctx.config.snippet_rm or "rm", "rm")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(path)})
        out = ctx.send(php)
        if out.strip() == "1":
            print("Delete failed (file may still exist)")
        else:
            print("Deleted")
        return None


register("del")(RmModule)
