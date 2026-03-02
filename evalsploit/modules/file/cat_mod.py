from __future__ import annotations

import html
from base64 import b64decode
from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("cat", description="View file contents (style: bcat/cat, set with 'set cat')", usage="cat <path>")
class CatModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        path = ctx.resolve_path(args.strip())
        if not ctx.file_exists(path):
            print("File does not exist")
            return None
        style = ctx.config.cat_style
        snip = load_snippet(style, "cat")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(path)})
        out = ctx.send(php)
        if style == "bcat":
            try:
                print(b64decode(out).decode("utf-8", errors="ignore"))
            except Exception:
                print(out)
        else:
            print(html.unescape(out))
        return None
